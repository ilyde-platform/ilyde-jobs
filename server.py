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
import logging
from concurrent import futures
import grpc
from grpc_health.v1 import health, health_pb2_grpc

from interceptors import ExceptionToStatusInterceptor
from protos import job_pb2_grpc

from servicers import WorkspaceServicer, EnvironmentServicer, RunServicer, ExperimentServicer, ModelApisServicer

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def create_server(server_address):
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    job_pb2_grpc.add_WorkspaceServicesServicer_to_server(
        WorkspaceServicer(), server
    )
    job_pb2_grpc.add_ModelApisServicesServicer_to_server(
        ModelApisServicer(), server
    )
    job_pb2_grpc.add_EnvironmentServicesServicer_to_server(
        EnvironmentServicer(), server
    )
    job_pb2_grpc.add_RunServicesServicer_to_server(
        RunServicer(), server
    )
    job_pb2_grpc.add_ExperimentServicesServicer_to_server(
        ExperimentServicer(), server
    )
    # Create a health check servicer. We use the non-blocking implementation
    # to avoid thread starvation.
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=1))
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    port = server.add_insecure_port(server_address)
    return server, port


def serve():
    server, port = create_server('[::]:50051')
    server.start()
    logger.info("server is serving on port {} ............".format(port))
    server.wait_for_termination()
    logger.info("server is stopped............")


if __name__ == '__main__':
    logger.info("server is starting............")
    serve()

