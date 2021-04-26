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

import unittest
import logging
import grpc
from google.protobuf.any_pb2 import Any
from google.protobuf.struct_pb2 import Struct
from grpc_interceptor.exceptions import GrpcException, InvalidArgument, NotFound, Unknown
from protos import job_pb2, job_pb2_grpc
import server

# setup logger
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.NOTSET, format=FORMAT)
logger = logging.getLogger(__name__)


class JobServicerTest(unittest.TestCase):

    def setUp(self):
        self._server, port = server.create_server('[::]:0')
        self._server.start()
        self._channel = grpc.insecure_channel('localhost:%d' % port)

    def tearDown(self):
        self._channel.close()
        self._server.stop(None)

    def test_create_workspace(self):
        logger.info("test create job")
        stub = job_pb2_grpc.WorkspaceServicesStub(self._channel)
        # prepare a payload
        s = Struct()
        s.update({"name": "project", "value": "5fdcbf2584655ded3b4930fa"})
        workspace = {
            "revision": "5fdd0cd884655ded3b4930fc",
            "datasets": [
                {
                    "id": "5fdcc04de045d0e599b3a918",
                    "version": "1.0.0",
                    "writeable": False
                }
            ],
            "ide": "VSCODE"
        }
        w = job_pb2.WorkspaceSpec(**workspace)
        payload = {
            "name": "Train fashion-mnist",
            "hardware": {
                "name": "Hello",
                "cpus": 1,
                "ram": 256,
                "gpu": 0
            },
            "environment": {
                "name": "Minimal",
                "image": "gitlab.hopenly.com:4567/ilyde/base-images/minimal-py37:1.0"
            },
            "kind": "EXPERIMENT",
            "owner": "1234-2344-1234-2345",
            "spec": w
        }
        with self.assertRaises(grpc.RpcError) as cm:
            stub.Create(job_pb2.Workspace(**payload))


if __name__ == '__main__':
    logger.info("tests JobServicer")
    unittest.main(verbosity=2)


