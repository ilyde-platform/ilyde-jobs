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

from marshmallow import Schema, fields, pre_load, post_dump
from google.protobuf import json_format

from protos.job_pb2 import ID, Status, JobState, Ide, Environment, HardwareTier, Workspace, ModelApis, Run, Experiment, \
    Pagination, SearchWorkspaceResponse, SearchRunResponse, SearchExperimentResponse, SearchModelApisResponse, \
    ListHardwareTierResponse, ListEnvironmentResponse, ListIdeResponse


class BaseSchema(Schema):
    # Custom options
    __proto_class__ = None
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    def parse_proto_message(self, message):
        return json_format.MessageToDict(message, **self.__decode_options__)

    @staticmethod
    def paginate(data, page: int, limit: int):
        begin = (page - 1) * limit
        end = begin + limit
        return page, limit, data[begin:end]

    @pre_load(pass_many=True)
    def decode(self, data, many, **kwargs):
        if many:
            return [self.parse_proto_message(message) for message in data]
        return self.parse_proto_message(data)

    @post_dump(pass_many=True)
    def encode(self, data, many, **kwargs):
        if many:
            return [self.__proto_class__(**message) for message in data]
        return self.__proto_class__(**data)


class IDSerializer(BaseSchema):
    __proto_class__ = ID

    id = fields.Str(required=True)


class StatusSerializer(BaseSchema):
    __proto_class__ = Status

    status = fields.Integer()
    message = fields.Str()


class JobStateSerializer(BaseSchema):
    __proto_class__ = JobState

    state = fields.Str()


class ParamSerializer(Schema):
    name = fields.Str(required=True)
    value = fields.Str(required=True)


class IdeSerializer(BaseSchema):
    __proto_class__ = Ide

    id = fields.Str()
    name = fields.Str()
    title = fields.Str()


class ModelSerializer(Schema):
    model = fields.Str(required=True)
    version = fields.Int(required=True)
    stage = fields.Str()
    hardware = fields.Str(required=True)
    environment = fields.Str(required=True)


class DatasetSpecSerializer(Schema):
    id = fields.Str(required=True)
    version = fields.Str(required=True)
    mount_output = fields.Bool(default=False, missing=False)


class ExperimentSpecSerializer(Schema):
    revision = fields.Str(required=True)
    datasets = fields.List(fields.Nested(DatasetSpecSerializer), default=[], missing=[])
    entrypoint = fields.Str(required=True)
    params = fields.List(fields.Nested(ParamSerializer), default=[], missing=[])
    hardware = fields.Str(required=True)
    environment = fields.Str(required=True)


class WorkspaceSpecSerializer(Schema):
    ide = fields.Str(required=True)
    datasets = fields.List(fields.Nested(DatasetSpecSerializer), default=[], missing=[])
    revision = fields.Str(required=True)
    hardware = fields.Str(required=True)
    environment = fields.Str(required=True)


class RunSpecSerializer(Schema):
    command = fields.Str(required=True)
    datasets = fields.List(fields.Nested(DatasetSpecSerializer), default=[], missing=[])
    revision = fields.Str(required=True)
    schedule_time = fields.Str()
    hardware = fields.Str(required=True)
    environment = fields.Str(required=True)


class EnvironmentSerializer(BaseSchema):
    __proto_class__ = Environment

    id = fields.Str()
    name = fields.Str()
    image = fields.Str()
    deployment = fields.Bool()


class HardwareTierSerializer(BaseSchema):
    __proto_class__ = HardwareTier

    id = fields.Str()
    name = fields.Str(required=True)
    cores = fields.Int(required=True)
    memory = fields.Int(required=True)
    gpu = fields.Int(default=0, missing=0)
    instancegroup = fields.Str(required=True)
    is_default = fields.Bool(missing=False)
    deployment = fields.Bool(missing=False)


class MetadataSerializer(Schema):
    name = fields.Str(required=True)
    project = fields.Str(required=True)
    owner = fields.Str(required=True)
    link = fields.Str(missing="")


class WorkspaceSerializer(BaseSchema):
    __proto_class__ = Workspace

    id = fields.Str()
    metadata = fields.Nested(MetadataSerializer, required=True)
    state = fields.Str(missing="CREATED")
    spec = fields.Nested(WorkspaceSpecSerializer, required=True)
    create_at = fields.Str()
    last_start = fields.Str()
    last_update = fields.Str()
    uptime = fields.Int()


class ModelApisSerializer(BaseSchema):
    __proto_class__ = ModelApis

    id = fields.Str()
    metadata = fields.Nested(MetadataSerializer, required=True)
    state = fields.Str(missing="CREATED")
    spec = fields.Nested(ModelSerializer, required=True)
    create_at = fields.Str()
    last_start = fields.Str()
    last_update = fields.Str()
    uptime = fields.Int()


class RunSerializer(BaseSchema):
    __proto_class__ = Run

    id = fields.Str()
    metadata = fields.Nested(MetadataSerializer, required=True)
    state = fields.Str(missing="CREATED")
    spec = fields.Nested(RunSpecSerializer, required=True)
    create_at = fields.Str()
    last_update = fields.Str()
    uptime = fields.Int()


class ExperimentSerializer(BaseSchema):
    __proto_class__ = Experiment

    id = fields.Str()
    metadata = fields.Nested(MetadataSerializer, required=True)
    state = fields.Str(missing="CREATED")
    spec = fields.Nested(ExperimentSpecSerializer, required=True)
    create_at = fields.Str()
    last_update = fields.Str()
    uptime = fields.Int()


class PaginationSerializer(BaseSchema):
    __proto_class__ = Pagination
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}
    page = fields.Int(missing=1)
    limit = fields.Int(missing=25)


class SearchFilterSerializer(Schema):
    project = fields.Str()
    owner = fields.Str()
    state = fields.Str()


class SearchRequestSerializer(BaseSchema):
    __proto_class__ = Pagination
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}
    query = fields.Nested(SearchFilterSerializer, missing={})
    page = fields.Int(missing=1)
    limit = fields.Int(missing=25)


class SearchWorkspaceResponseSerializer(BaseSchema):
    __proto_class__ = SearchWorkspaceResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(WorkspaceSerializer))


class SearchRunResponseSerializer(BaseSchema):
    __proto_class__ = SearchRunResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(RunSerializer))


class SearchExperimentResponseSerializer(BaseSchema):
    __proto_class__ = SearchExperimentResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(ExperimentSerializer))


class SearchModelApisResponseSerializer(BaseSchema):
    __proto_class__ = SearchModelApisResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(ModelApisSerializer))


class ListHardwareTierResponseSerializer(BaseSchema):
    __proto_class__ = ListHardwareTierResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(HardwareTierSerializer))


class ListEnvironmentResponseSerializer(BaseSchema):
    __proto_class__ = ListEnvironmentResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(EnvironmentSerializer))


class ListIdeResponseSerializer(BaseSchema):
    __proto_class__ = ListIdeResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(IdeSerializer))


workspace_serializer = WorkspaceSerializer()
run_serializer = RunSerializer()
experiment_serializer = ExperimentSerializer()
modelapis_serializer = ModelApisSerializer()
hardwareTier_serializer = HardwareTierSerializer()
environment_serializer = EnvironmentSerializer()
ide_serializer = IdeSerializer()
list_hardwareTier_response_serializer = ListHardwareTierResponseSerializer()
list_environment_response_serializer = ListEnvironmentResponseSerializer()
list_ide_response_serializer = ListIdeResponseSerializer()
id_serializer = IDSerializer()
status_serializer = StatusSerializer()
job_state_serializer = JobStateSerializer()
search_request_serializer = SearchRequestSerializer()
pagination_serializer = PaginationSerializer()
search_workspace_response_serializer = SearchWorkspaceResponseSerializer()
search_experiment_response_serializer = SearchExperimentResponseSerializer()
search_modelapis_response_serializer = SearchModelApisResponseSerializer()
search_run_response_serializer = SearchRunResponseSerializer()
