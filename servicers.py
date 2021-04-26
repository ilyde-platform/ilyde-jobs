# encoding: utf-8
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

from models import documents
from protos import job_pb2_grpc
from serializers import id_serializer, workspace_serializer, status_serializer, search_request_serializer, \
    search_workspace_response_serializer, job_state_serializer, modelapis_serializer, \
    search_modelapis_response_serializer, run_serializer, search_run_response_serializer, experiment_serializer, \
    search_experiment_response_serializer, hardwareTier_serializer, pagination_serializer, \
    list_hardwareTier_response_serializer, environment_serializer, list_environment_response_serializer, ide_serializer, \
    list_ide_response_serializer
import datetime

import utils
from grpc_interceptor.exceptions import InvalidArgument


class WorkspaceServicer(job_pb2_grpc.WorkspaceServicesServicer):

    def Retrieve(self, request, context):
        data = id_serializer.load(request)
        workspace = documents.Workspace.objects(deleted=False).get(id=data['id'])
        return workspace_serializer.dump(workspace)

    def Create(self, request, context):
        # validate request payload
        data = workspace_serializer.load(request)
        # validate hardware and environment
        env = documents.Environment.objects.get(id=data["spec"]["environment"])
        if env.deployment:
            raise InvalidArgument("Invalid environment provided.")

        workspace = documents.Workspace(
            metadata=data['metadata'],
            state=data['state'],
            spec=data["spec"]
        ).save()

        return workspace_serializer.dump(workspace)

    def Update(self, request, context):
        # validate request payload
        data = workspace_serializer.load(request)

        # validate id
        if not data.get('id'):
            raise InvalidArgument("Workspace id not provided.")

        # retrieve Workspace
        workspace = documents.Workspace.objects(deleted=False).get(id=data['id'])
        # update name, spec
        workspace.metadata.name = data["metadata"]['name']
        workspace.spec = documents.WorkspaceSpec(**data["spec"])
        workspace.last_update = datetime.datetime.now()
        workspace.save()
        return workspace_serializer.dump(workspace)

    def Delete(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        workspace = documents.Workspace.objects(deleted=False).get(id=data['id'])
        # delete pvc
        if workspace.state in ["STOPPED", "CREATED"]:
            utils.clean_kubernetes_pvc("data-{}".format(utils.get_k8s_name(workspace)))
            workspace.deleted = True
            workspace.last_update = datetime.datetime.now()
            workspace.save()
            return status_serializer.dump({"status": 200, "message": "Successfully delete workspace."})

        return status_serializer.dump({"status": 400, "message": "Cannot delete starting or running workspace."})

    def Search(self, request, context):
        data = search_request_serializer.load(request)
        mappings = {
            "project": "metadata.project",
            "owner": "metadata.owner",
            "state": "state"
        }
        ids = [""]

        query = utils.construct_mongo_query(data["query"], mappings, ids)
        if query:
            workspaces = documents.Workspace.objects(__raw__=query).filter(deleted=False)
        else:
            workspaces = documents.Workspace.objects(deleted=False)

        paginated = workspace_serializer.paginate(workspaces, page=data["page"],
                                                  limit=data["limit"])
        payload = {
            "total": len(workspaces),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return search_workspace_response_serializer.dump(payload)

    def Start(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        workspace = documents.Workspace.objects(deleted=False).get(id=data['id'])
        # prepare configurations
        if workspace.state not in ["STARTING", "RUNNING"]:
            utils.spawn_workspace(workspace)
            workspace.state = "STARTING"
            workspace.last_start = datetime.datetime.now()
            workspace.last_update = datetime.datetime.now()
            workspace.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully start workspace."})

    def State(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        workspace = documents.Workspace.objects(deleted=False).get(id=data['id'])
        if workspace.state in ["STARTING", "RUNNING"]:
            response = utils.get_kubernetes_deployment_status(utils.get_k8s_name(workspace))
            if response.get("available_replicas"):
                workspace.state = "RUNNING"
            else:
                workspace.state = "STARTING"

            workspace.last_update = datetime.datetime.now()
            workspace.save()

        return job_state_serializer.dump({"state": workspace.state})

    def Stop(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        workspace = documents.Workspace.objects(deleted=False).get(id=data['id'])

        if workspace.state not in ["STARTING", "RUNNING"]:
            return status_serializer.dump({"status": 400,
                                           "message": "Cannot stop not running or starting workspace."})

        # stop and clean all resources
        utils.clean_kubernetes_deployment(utils.get_k8s_name(workspace))
        workspace.state = "STOPPED"
        delta = datetime.datetime.utcnow() - workspace.last_start
        workspace.uptime += int(delta.total_seconds())
        workspace.last_update = datetime.datetime.now()
        workspace.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully stopped workspace."})


class ModelApisServicer(job_pb2_grpc.ModelApisServicesServicer):

    def Retrieve(self, request, context):
        data = id_serializer.load(request)
        modelapis = documents.ModelApis.objects(deleted=False).get(id=data['id'])
        return modelapis_serializer.dump(modelapis)

    def Create(self, request, context):
        # validate request payload
        data = modelapis_serializer.load(request)
        # validate hardware and environment
        env = documents.Environment.objects.get(id=data["spec"]["environment"])
        hw = documents.HardwareTier.objects.get(id=data["spec"]["hardware"])
        if not env.deployment or not hw.deployment:
            raise InvalidArgument("Invalid environment or hardwareTier provided.")

        mdl = documents.ModelApis(
            metadata=data['metadata'],
            state=data['state'],
            spec=data["spec"]
        ).save()

        return modelapis_serializer.dump(mdl)

    def Delete(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        mdl = documents.ModelApis.objects(deleted=False).get(id=data['id'])
        # delete pvc
        if mdl.state in ["STOPPED", "CREATED"]:
            mdl.deleted = True
            mdl.last_update = datetime.datetime.now()
            mdl.save()
            return status_serializer.dump({"status": 200, "message": "Successfully delete modelapis."})

        return status_serializer.dump({"status": 400, "message": "Cannot delete starting or running modelapis."})

    def Search(self, request, context):
        data = search_request_serializer.load(request)
        mappings = {
            "project": "metadata.project",
            "owner": "metadata.owner",
            "state": "state"
        }
        ids = [""]

        query = utils.construct_mongo_query(data["query"], mappings, ids)
        if query:
            mdls = documents.ModelApis.objects(__raw__=query).filter(deleted=False)
        else:
            mdls = documents.ModelApis.objects(deleted=False)

        paginated = workspace_serializer.paginate(mdls, page=data["page"],
                                                  limit=data["limit"])
        payload = {
            "total": len(mdls),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return search_modelapis_response_serializer.dump(payload)

    def Start(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        mdl = documents.ModelApis.objects.get(id=data['id'])
        # prepare configurations
        if mdl.state not in ["STARTING", "RUNNING"]:
            utils.spawn_modelapis(mdl)
            mdl.state = "STARTING"
            mdl.last_start = datetime.datetime.now()
            mdl.last_update = datetime.datetime.now()
            mdl.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully start modelapis."})

    def State(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        mdl = documents.ModelApis.objects(deleted=False).get(id=data['id'])
        if mdl.state in ["STARTING", "RUNNING"]:
            state = utils.get_kubernetes_deployment_status(utils.get_k8s_name(mdl))
            mdl.state = state
            # clean job if already in finished state like stopped, failed, aborted, succeeded
            if mdl.state not in ["STARTING", "RUNNING"]:
                response = utils.get_kubernetes_deployment_status(utils.get_k8s_name(mdl))
                if response.get("available_replicas"):
                    mdl.state = "RUNNING"
                else:
                    mdl.state = "STARTING"

            mdl.last_update = datetime.datetime.now()
            mdl.save()

        return job_state_serializer.dump({"state": mdl.state})

    def Stop(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        mdl = documents.ModelApis.objects(deleted=False).get(id=data['id'])

        if mdl.state not in ["STARTING", "RUNNING"]:
            return status_serializer.dump({"status": 400,
                                           "message": "Cannot stop not running or starting modelapis."})

        # stop and clean all resources
        utils.clean_kubernetes_deployment(utils.get_k8s_name(mdl))
        mdl.state = "STOPPED"
        delta = datetime.datetime.utcnow() - mdl.last_start
        mdl.uptime += int(delta.total_seconds())
        mdl.last_update = datetime.datetime.now()
        mdl.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully stopped modelapis."})


class RunServicer(job_pb2_grpc.RunServicesServicer):

    def Get(self, request, context):
        data = id_serializer.load(request)
        run = documents.Run.objects(deleted=False).get(id=data['id'])
        return run_serializer.dump(run)

    def Submit(self, request, context):
        # validate request payload
        data = run_serializer.load(request)
        # validate hardware and environment
        env = documents.Environment.objects.get(id=data["spec"]["environment"])
        if env.deployment:
            raise InvalidArgument("Invalid environment provided.")

        run = documents.Run(
            metadata=data['metadata'],
            state=data['state'],
            spec=data["spec"]
        ).save()
        utils.spawn_run(run)
        run.state = "STARTING"
        run.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully submit run."})

    def Search(self, request, context):
        data = search_request_serializer.load(request)
        mappings = {
            "project": "metadata.project",
            "owner": "metadata.owner",
            "state": "state"
        }
        ids = [""]

        query = utils.construct_mongo_query(data["query"], mappings, ids)
        if query:
            runs = documents.Run.objects(__raw__=query).filter(deleted=False)
        else:
            runs = documents.Run.objects(deleted=False)

        paginated = workspace_serializer.paginate(runs, page=data["page"],
                                                  limit=data["limit"])
        payload = {
            "total": len(runs),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return search_run_response_serializer.dump(payload)

    def State(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        run = documents.Run.objects(deleted=False).get(id=data['id'])
        if run.state in ["STARTING", "RUNNING"]:
            response = utils.get_kubernetes_job_status(utils.get_k8s_name(run))
            if response.get("active"):
                run.state = "RUNNING"

            elif response.get("succeeded"):
                run.state = "SUCCEEDED"

            elif response.get("failed") and int(response.get("failed")) >= 1:
                run.state = "FAILED"

            if run.state not in ["STARTING", "RUNNING"]:
                utils.clean_kubernetes_job(utils.get_k8s_name(run))
                completion_time = datetime.datetime.strptime(response.get("completion_time"), "%Y-%m-%dT%H:%M:%S")
                delta = completion_time - run.create_at
                run.uptime += int(delta.total_seconds())

            run.last_update = datetime.datetime.now()
            run.save()

        return job_state_serializer.dump({"state": run.state})

    def Stop(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        run = documents.Run.objects(deleted=False).get(id=data['id'])

        if run.state not in ["STARTING", "RUNNING"]:
            return status_serializer.dump({"status": 400,
                                           "message": "Cannot stop not running or starting run."})

        # stop and clean all resources
        utils.clean_kubernetes_job(utils.get_k8s_name(run))
        run.state = "ABORTED"
        delta = datetime.datetime.utcnow() - run.create_at
        run.uptime += int(delta.total_seconds())
        run.last_update = datetime.datetime.now()
        run.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully stopped run."})


class ExperimentServicer(job_pb2_grpc.ExperimentServicesServicer):

    def Get(self, request, context):
        data = id_serializer.load(request)
        experiment = documents.Experiment.objects(deleted=False).get(id=data['id'])
        return experiment_serializer.dump(experiment)

    def Submit(self, request, context):
        # validate request payload
        data = experiment_serializer.load(request)
        # validate hardware and environment
        env = documents.Environment.objects.get(id=data["spec"]["environment"])
        if env.deployment:
            raise InvalidArgument("Invalid environment provided.")

        experiment = documents.Experiment(
            metadata=data['metadata'],
            state=data['state'],
            spec=data["spec"]
        ).save()
        utils.spawn_experiment(experiment)
        experiment.state = "STARTING"
        experiment.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully submit experiment."})

    def Search(self, request, context):
        data = search_request_serializer.load(request)
        mappings = {
            "project": "metadata.project",
            "owner": "metadata.owner",
            "state": "state"
        }
        ids = [""]

        query = utils.construct_mongo_query(data["query"], mappings, ids)
        if query:
            experiments = documents.Experiment.objects(__raw__=query).filter(deleted=False)
        else:
            experiments = documents.Experiment.objects(deleted=False)

        paginated = experiment_serializer.paginate(experiments, page=data["page"],
                                                   limit=data["limit"])
        payload = {
            "total": len(experiments),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return search_experiment_response_serializer.dump(payload)

    def State(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        experiment = documents.Experiment.objects(deleted=False).get(id=data['id'])
        if experiment.state in ["STARTING", "RUNNING"]:
            response = utils.get_kubernetes_job_status(utils.get_k8s_name(experiment))
            if response.get("active"):
                experiment.state = "RUNNING"

            elif response.get("succeeded"):
                experiment.state = "SUCCEEDED"

            elif response.get("failed") and int(response.get("failed")) >= 1:
                experiment.state = "FAILED"

            if experiment.state not in ["STARTING", "RUNNING"]:
                utils.clean_kubernetes_job(utils.get_k8s_name(experiment))
                completion_time = datetime.datetime.strptime(response.get("completion_time"), "%Y-%m-%dT%H:%M:%S")
                delta = completion_time - experiment.create_at
                experiment.uptime += int(delta.total_seconds())

            experiment.last_update = datetime.datetime.now()
            experiment.save()

        return job_state_serializer.dump({"state": experiment.state})

    def Stop(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        experiment = documents.Experiment.objects(deleted=False).get(id=data['id'])

        if experiment.state not in ["STARTING", "RUNNING"]:
            return status_serializer.dump({"status": 400,
                                           "message": "Cannot stop not running or starting experiment."})

        # stop and clean all resources
        utils.clean_kubernetes_job(utils.get_k8s_name(experiment))
        experiment.state = "ABORTED"
        delta = datetime.datetime.utcnow() - experiment.last_start
        experiment.uptime += int(delta.total_seconds())
        experiment.last_update = datetime.datetime.now()
        experiment.save()

        return status_serializer.dump({"status": 200,
                                       "message": "Successfully stopped Experiment."})


class EnvironmentServicer(job_pb2_grpc.EnvironmentServicesServicer):

    def GetHardwareTier(self, request, context):
        data = id_serializer.load(request)
        hw = documents.HardwareTier.objects(deleted=False).get(id=data['id'])
        return hardwareTier_serializer.dump(hw)

    def CreateHardwareTier(self, request, context):
        data = hardwareTier_serializer.load(request)
        hw = documents.HardwareTier(
            name=data["name"],
            cores=data["cores"],
            memory=data["memory"],
            gpu=data["gpu"],
            instancegroup=data["instancegroup"],
            is_default=data["is_default"],
            deployment=data["deployment"]
        ).save()
        return hardwareTier_serializer.dump(hw)

    def UpdateHardwareTier(self, request, context):
        data = hardwareTier_serializer.load(request)
        # validate id
        if not data.get('id'):
            raise InvalidArgument("HardwareTier id not provided.")
        hw = documents.HardwareTier.objects(deleted=False).get(id=data["id"])
        hw.name = data["name"],
        hw.cores = data["cores"],
        hw.memory = data["memory"],
        hw.gpu = data["gpu"],
        hw.instancegroup = data["instancegroup"],
        hw.is_default = data["is_default"],
        hw.deployment = data["deployment"]

        hw.save()

        return hardwareTier_serializer.dump(hw)

    def DeleteHardwareTier(self, request, context):
        data = id_serializer.load(request)
        hw = documents.HardwareTier.objects(deleted=False).get(id=data["id"])
        hw.deleted = True
        hw.save()

        return status_serializer.dump({"status": 200,
                                       "message": "HardwareTier successfully deleted."})

    def ListHardwareTiers(self, request, context):
        data = pagination_serializer.load(request)
        hws = documents.HardwareTier.objects(deleted=False)
        paginated = hardwareTier_serializer.paginate(hws, page=data["page"], limit=data["limit"])
        payload = {
            "total": len(hws),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return list_hardwareTier_response_serializer.dump(payload)

    def ListEnvironments(self, request, context):
        data = pagination_serializer.load(request)
        envs = documents.Environment.objects()
        paginated = environment_serializer.paginate(envs, page=data["page"],
                                                    limit=data["limit"])
        payload = {
            "total": len(envs),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return list_environment_response_serializer.dump(payload)

    def ListWorkspaceIde(self, request, context):
        data = pagination_serializer.load(request)
        ides = documents.Ide.objects()
        paginated = ide_serializer.paginate(ides, page=data["page"], limit=data["limit"])
        payload = {
            "total": len(ides),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return list_ide_response_serializer.dump(payload)
