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

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from protos import kubespawner_pb2 as kubespawner__pb2


class KubeSpawnerServicesStub(object):
    """The KubeSpawner service definition. 
    This service create, delete and handle  kubernetes resources
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateDeploymentFromFile = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreateDeploymentFromFile',
                request_serializer=kubespawner__pb2.File.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.CreateIngressFromFile = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreateIngressFromFile',
                request_serializer=kubespawner__pb2.File.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.CreateServiceFromFile = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreateServiceFromFile',
                request_serializer=kubespawner__pb2.File.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.CreateCronJobFromFile = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreateCronJobFromFile',
                request_serializer=kubespawner__pb2.File.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.CreateJobFromFile = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreateJobFromFile',
                request_serializer=kubespawner__pb2.File.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.CreateService = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreateService',
                request_serializer=kubespawner__pb2.Service.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.DeleteDeployment = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/DeleteDeployment',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.DeleteService = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/DeleteService',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.DeleteIngress = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/DeleteIngress',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.CreatePVCFromFile = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/CreatePVCFromFile',
                request_serializer=kubespawner__pb2.File.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.GetResourceStatus = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/GetResourceStatus',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )
        self.DeleteJob = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/DeleteJob',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.DeleteCronJob = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/DeleteCronJob',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )
        self.DeletePVC = channel.unary_unary(
                '/kubespawner.KubeSpawnerServices/DeletePVC',
                request_serializer=kubespawner__pb2.Resource.SerializeToString,
                response_deserializer=kubespawner__pb2.Status.FromString,
                )


class KubeSpawnerServicesServicer(object):
    """The KubeSpawner service definition. 
    This service create, delete and handle  kubernetes resources
    """

    def CreateDeploymentFromFile(self, request, context):
        """create deployment from file definitions yaml
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateIngressFromFile(self, request, context):
        """Create ingress from file definition yaml
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateServiceFromFile(self, request, context):
        """Create service from file definition yaml
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateCronJobFromFile(self, request, context):
        """Create cronjob
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateJobFromFile(self, request, context):
        """create job from file definitions yaml
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateService(self, request, context):
        """Create service
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDeployment(self, request, context):
        """Delete deployment resource
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteService(self, request, context):
        """Delete Service resource
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteIngress(self, request, context):
        """Delete Ingress resource
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreatePVCFromFile(self, request, context):
        """Create PVC
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetResourceStatus(self, request, context):
        """Get resource's status
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteJob(self, request, context):
        """Delete Job resource
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteCronJob(self, request, context):
        """Delete Job resource
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePVC(self, request, context):
        """Delete PVC
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KubeSpawnerServicesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateDeploymentFromFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDeploymentFromFile,
                    request_deserializer=kubespawner__pb2.File.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'CreateIngressFromFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateIngressFromFile,
                    request_deserializer=kubespawner__pb2.File.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'CreateServiceFromFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateServiceFromFile,
                    request_deserializer=kubespawner__pb2.File.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'CreateCronJobFromFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCronJobFromFile,
                    request_deserializer=kubespawner__pb2.File.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'CreateJobFromFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateJobFromFile,
                    request_deserializer=kubespawner__pb2.File.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'CreateService': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateService,
                    request_deserializer=kubespawner__pb2.Service.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'DeleteDeployment': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDeployment,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'DeleteService': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteService,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'DeleteIngress': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteIngress,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'CreatePVCFromFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePVCFromFile,
                    request_deserializer=kubespawner__pb2.File.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'GetResourceStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetResourceStatus,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
            'DeleteJob': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteJob,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'DeleteCronJob': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteCronJob,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
            'DeletePVC': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePVC,
                    request_deserializer=kubespawner__pb2.Resource.FromString,
                    response_serializer=kubespawner__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'kubespawner.KubeSpawnerServices', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KubeSpawnerServices(object):
    """The KubeSpawner service definition. 
    This service create, delete and handle  kubernetes resources
    """

    @staticmethod
    def CreateDeploymentFromFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreateDeploymentFromFile',
            kubespawner__pb2.File.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateIngressFromFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreateIngressFromFile',
            kubespawner__pb2.File.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateServiceFromFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreateServiceFromFile',
            kubespawner__pb2.File.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateCronJobFromFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreateCronJobFromFile',
            kubespawner__pb2.File.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateJobFromFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreateJobFromFile',
            kubespawner__pb2.File.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreateService',
            kubespawner__pb2.Service.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDeployment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/DeleteDeployment',
            kubespawner__pb2.Resource.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/DeleteService',
            kubespawner__pb2.Resource.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteIngress(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/DeleteIngress',
            kubespawner__pb2.Resource.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreatePVCFromFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/CreatePVCFromFile',
            kubespawner__pb2.File.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetResourceStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/GetResourceStatus',
            kubespawner__pb2.Resource.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/DeleteJob',
            kubespawner__pb2.Resource.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteCronJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/DeleteCronJob',
            kubespawner__pb2.Resource.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeletePVC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/kubespawner.KubeSpawnerServices/DeletePVC',
            kubespawner__pb2.Resource.SerializeToString,
            kubespawner__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
