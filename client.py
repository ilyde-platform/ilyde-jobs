# encoding: utf-8
import datetime

import grpc
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Struct

from protos import job_pb2_grpc, job_pb2


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = job_pb2_grpc.ExperimentServicesStub(channel)

    try:
        job = {
  "metadata": {
    "name": "Train Wine Quality Alpha 0.4 l1_ratio 0.3",
    "owner": "7dcab8f2-77b5-400e-bb7b-1b2b6c89f9c0",
    "project": "605b527f12a34dff6b48aa23"
  },
  "spec": {
    "datasets": [
       {
        "id": "605b604aa492cd3d19fab0bd",
        "mount_output": False,
        "version": "1"
      }
    ],
    "entrypoint": "main",
    "environment": "6059daebac046798f30a9efc",
    "hardware": "605c121e3582fedec55fdbc9",
    "params": [
      {
        "name": "alpha",
        "value": "0.4"
      },
      {
        "name": "l1_ratio",
        "value": "0.3"
      }
    ],
    "revision": "605c71d912a34dff6b48aa26"
  }
}
        workspace = stub.Submit(job_pb2.Experiment(**job))
    except grpc.RpcError as e:
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        print(e.details(), e)
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        print(status_code.name)
        # should print `(3, 'invalid argument')`
        print(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
    else:
        print(json_format.MessageToJson(workspace, preserving_proto_field_name=True, including_default_value_fields=True))


if __name__ == '__main__':
    run()
