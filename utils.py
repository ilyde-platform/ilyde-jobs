# -*- coding: utf-8 -*-
#
# Copyright (c) 2020-2021 Hopenly srl.
#
# This file is part of Ilyde.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import grpc
from bson import ObjectId
from google.protobuf import json_format
from jinja2 import Environment, FileSystemLoader
import config
from models.documents import Workspace, ModelApis, Run, Experiment
from protos import kubespawner_pb2, kubespawner_pb2_grpc

kubeservice = kubespawner_pb2_grpc.KubeSpawnerServicesStub(
    grpc.insecure_channel(config.KUBESPAWNER_SERVICES_ENDPOINT))

TEMPLATE_MAPPING = {
    "RUN": "job.yml",
    "DEPLOYMENT": "deployment.yml",
    "WORKSPACE": "workspace.yml",
    "EXPERIMENT": "job.yml"
}


def construct_mongo_query(data: dict, mappings: dict, ids: list):
    query = {}
    for key, value in data.items():
        if value and key in mappings.keys():
            query[mappings[key]] = value

    for key in query.keys():
        if key in ids:
            query[key] = ObjectId(query[key])
    return query


def load_template(template):
    # Load Jinja2 template
    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True)
    return env.get_template(template)


def get_k8s_name(obj):
    if isinstance(obj, Workspace):
        return "ilyde-workspace-{}".format(obj.id)
    elif isinstance(obj, ModelApis):
        return "ilyde-modelapis-{}".format(obj.id)
    elif isinstance(obj, Run):
        return "ilyde-run-{}".format(obj.id)
    elif isinstance(obj, Experiment):
        return "ilyde-experiment-{}".format(obj.id)

    return ""


def get_envs(obj):
    envs = {
        "JOB_ID": obj.id,
        "AWS_ACCESS_KEY_ID": config.AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": config.AWS_SECRET_ACCESS_KEY,
        "MINIO_HOST": config.MINIO_HOST,
        "MINIO_ENDPOINT": config.MINIO_ENDPOINT,
        "ETCD_HOST": config.ETCD_HOST,
        "DATASETS_SERVICES_ENDPOINT": config.DATASETS_SERVICES_ENDPOINT,
        "PROJECTS_SERVICES_ENDPOINT": config.PROJECTS_SERVICES_ENDPOINT,
        "MLFLOW_TRACKING_URI": config.MLFLOW_TRACKING_URI,
        "MLFLOW_S3_ENDPOINT_URL": config.MINIO_ENDPOINT
    }
    return envs


def spawn_workspace(workspace):
    # check job kind
    name = get_k8s_name(workspace)
    # resources
    cpus_limit = "{}m".format(workspace.spec.hardware.cores)
    ram_limit = "{}Mi".format(workspace.spec.hardware.memory)
    cpus_request = "{}m".format(workspace.spec.hardware.cores)
    ram_request = "{}Mi".format(workspace.spec.hardware.memory)
    port = 8888
    websocket_port = 6789
    path_prefix = "/workspacesession/{}".format(workspace.id)
    middlewares = workspace.spec.ide.middlewares
    enable_websocket = True
    websocket_prefix = "/wssession/{}".format(workspace.id)
    relative_path = path_prefix if workspace.spec.ide.has_relative_path else "/"
    startup_probe_endpoint = "http://localhost:{}{}".format(port, relative_path)

    args = ["job", "--kind", "WORKSPACE", "--user-id", workspace.metadata.owner]
    # add project id
    args += ["--project-id", workspace.metadata.project]

    # add revision
    args += ["--project-revision-id", workspace.spec.revision]
    # add datasets
    if workspace.spec.datasets:
        for dataset in workspace.spec.datasets:
            args += ["--dataset", dataset.id, dataset.version, dataset.mount_output]

    # compose command
    args += ["--command", workspace.spec.ide.start]

    # create persistence volume claim
    pvc_name = "data-{}".format(name)
    if not workspace.last_start:
        template = load_template("pvc.yml").render(
            name=pvc_name,
        )
        kubeservice.CreatePVCFromFile(
            kubespawner_pb2.File(
                namespace=config.KUBE_NAMESPACE,
                content=template
            ))
    # deploy in kubernetes
    envs = get_envs(workspace)
    template = load_template(TEMPLATE_MAPPING["WORKSPACE"]).render(
        name=name,
        environment=workspace.spec.environment.image,
        args=args,
        port=port,
        websocket_port=websocket_port,
        startup_probe_endpoint=startup_probe_endpoint,
        cpus_limit=cpus_limit,
        ram_limit=ram_limit,
        cpus_request=cpus_request,
        ram_request=ram_request,
        claim_name=pvc_name,
        instancegroup=workspace.spec.hardware.instancegroup,
        **envs
    )

    kubeservice.CreateDeploymentFromFile(
        kubespawner_pb2.File(
            namespace=config.KUBE_NAMESPACE,
            content=template))
    # create ingress and service
    template = load_template("service.yml").render(
        name=name,
        service_port=port,
        enable_websocket=enable_websocket,
        websocket_port=websocket_port,
        app_selector_name=name,
    )
    kubeservice.CreateServiceFromFile(
        kubespawner_pb2.File(
            namespace=config.KUBE_NAMESPACE,
            content=template
        ))

    template = load_template("ingress.yml").render(
        name=name,
        path_prefix=path_prefix,
        service_name=name,
        service_port=port,
        middlewares=middlewares,
        enable_websocket=enable_websocket,
        websocket_prefix=websocket_prefix,
        websocket_port=websocket_port
    )
    kubeservice.CreateIngressFromFile(
        kubespawner_pb2.File(
            namespace=config.KUBE_NAMESPACE,
            content=template
        ))


def spawn_modelapis(mdl):
    # check job kind
    name = get_k8s_name(mdl)
    # resources
    cpus_limit = "{}m".format(mdl.spec.hardware.cores)
    ram_limit = "{}Mi".format(mdl.spec.hardware.memory)
    cpus_request = "{}m".format(mdl.spec.hardware.cores)
    ram_request = "{}Mi".format(mdl.spec.hardware.memory)
    model_uri = "models:/{}/{}".format(mdl.spec.model, mdl.spec.version)
    port = 5000
    startup_probe_endpoint = "http://localhost:{}/invocations".format(port)
    envs = get_envs(mdl)
    template = load_template(TEMPLATE_MAPPING["DEPLOYMENT"]).render(
        name=name,
        model_uri=model_uri,
        port=port,
        startup_probe_endpoint=startup_probe_endpoint,
        environment=mdl.spec.environment.image,
        cpus_limit=cpus_limit,
        ram_limit=ram_limit,
        cpus_request=cpus_request,
        ram_request=ram_request,
        instancegroup=mdl.spec.hardware.instancegroup,
        **envs
    )
    # deploy in kubernetes
    kubeservice.CreateDeploymentFromFile(kubespawner_pb2.File(namespace=config.KUBE_NAMESPACE, content=template))
    # create ingress
    middlewares = config.DEPLOYMENT_MIDDLEWARES
    path_prefix = "/modelapis/{}".format(mdl.id)
    enable_websocket = False
    websocket_prefix = ""
    websocket_port = ""

    template = load_template("ingress.yml").render(
        name=name,
        path_prefix=path_prefix,
        service_name=name,
        service_port=port,
        middlewares=middlewares,
        enable_websocket=enable_websocket,
        websocket_prefix=websocket_prefix,
        websocket_port=websocket_port
    )
    kubeservice.CreateIngressFromFile(
        kubespawner_pb2.File(
            namespace=config.KUBE_NAMESPACE,
            content=template
        ))

    template = load_template("service.yml").render(
        name=name,
        service_port=port,
        enable_websocket=enable_websocket,
        websocket_port=websocket_port,
        app_selector_name=name,
    )
    kubeservice.CreateServiceFromFile(
        kubespawner_pb2.File(
            namespace=config.KUBE_NAMESPACE,
            content=template
        ))


def spawn_run(run):
    # check job kind
    name = get_k8s_name(run)
    # resources
    cpus_limit = "{}m".format(run.spec.hardware.cores)
    ram_limit = "{}Mi".format(run.spec.hardware.memory)
    cpus_request = "{}m".format(run.spec.hardware.cores)
    ram_request = "{}Mi".format(run.spec.hardware.memory)
    args = ["job", "--kind", "RUN", "--user-id", run.metadata.owner]
    # add project id
    args += ["--project-id", run.metadata.project]

    # add revision
    args += ["--project-revision-id", run.spec.revision]
    # add datasets
    if run.spec.datasets:
        for dataset in run.spec.datasets:
            args += ["--dataset", dataset.id, dataset.version, dataset.mount_output]

    # compose command
    args += ["--command", run.spec.command]
    envs = get_envs(run)
    template = load_template(TEMPLATE_MAPPING["RUN"]).render(
        name=name,
        environment=run.spec.environment.image,
        args=args,
        cpus_limit=cpus_limit,
        ram_limit=ram_limit,
        cpus_request=cpus_request,
        ram_request=ram_request,
        instancegroup=run.spec.hardware.instancegroup,
        **envs
    )
    kubeservice.CreateJobFromFile(kubespawner_pb2.File(
        namespace=config.KUBE_NAMESPACE,
        content=template
    ))


def spawn_experiment(experiment):
    # check job kind
    name = get_k8s_name(experiment)
    # resources
    cpus_limit = "{}m".format(experiment.spec.hardware.cores)
    ram_limit = "{}Mi".format(experiment.spec.hardware.memory)
    cpus_request = "{}m".format(experiment.spec.hardware.cores)
    ram_request = "{}Mi".format(experiment.spec.hardware.memory)
    args = ["job", "--kind", "EXPERIMENT", "--user-id", experiment.metadata.owner]
    # add project id
    args += ["--project-id", experiment.metadata.project]

    # add revision
    args += ["--project-revision-id", experiment.spec.revision]
    # add datasets
    if experiment.spec.datasets:
        for dataset in experiment.spec.datasets:
            args += ["--dataset", dataset.id, dataset.version, dataset.mount_output]

    # compose command
    parameters = ["--params {} {}".format(param['name'], param['value']) for param in experiment.spec.params]
    cmd = ["python", "-m", "experiment", "--entrypoint", experiment.spec.entrypoint]
    cmd += parameters
    args += ["--command", " ".join(cmd)]

    envs = get_envs(experiment)
    template = load_template(TEMPLATE_MAPPING["EXPERIMENT"]).render(
        name=name,
        environment=experiment.spec.environment.image,
        args=args,
        cpus_limit=cpus_limit,
        ram_limit=ram_limit,
        cpus_request=cpus_request,
        ram_request=ram_request,
        instancegroup=experiment.spec.hardware.instancegroup,
        **envs
    )
    kubeservice.CreateJobFromFile(kubespawner_pb2.File(
        namespace=config.KUBE_NAMESPACE,
        content=template
    ))


def clean_kubernetes_job(name):
    kubeservice.DeleteJob(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="JOB"))


def clean_kubernetes_deployment(name):
    kubeservice.DeleteDeployment(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="DEPLOYMENT"))
    kubeservice.DeleteService(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="SERVICE"))
    kubeservice.DeleteIngress(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="INGRESS"))


def clean_kubernetes_pvc(name):
    kubeservice.DeletePVC(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="PVC"))


def get_kubernetes_deployment_status(name):

    response = kubeservice.GetResourceStatus(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="DEPLOYMENT"))

    return json_format.MessageToDict(response, preserving_proto_field_name=True)


def get_kubernetes_job_status(name):

    response = kubeservice.GetResourceStatus(
        kubespawner_pb2.Resource(
            namespace=config.KUBE_NAMESPACE,
            name=name,
            type="JOB"))
    return json_format.MessageToDict(response, preserving_proto_field_name=True)


