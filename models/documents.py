# encoding: utf-8
from mongoengine import *
import datetime


class Environment(Document):
    name = StringField(required=True)
    image = StringField(required=True)
    deployment = BooleanField(required=True)

    def __str__(self):
        return str(self.id)


class Ide(Document):
    name = StringField(required=True, unique=True)
    title = StringField(required=True)
    start = StringField(required=True)
    middlewares = ListField(StringField(), default=[])
    has_relative_path = BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class HardwareTier(Document):
    name = StringField(required=True)
    cores = IntField(required=True, min_value=250)
    memory = IntField(required=True, min_value=1024)
    gpu = IntField(required=True, min_value=0)
    deleted = BooleanField(default=False)
    instancegroup = StringField(required=True)
    is_default = BooleanField(required=True, default=False)
    deployment = BooleanField(required=True)

    def __str__(self):
        return str(self.id)


class Metadata(EmbeddedDocument):
    name = StringField(required=True)
    project = StringField(required=True)
    owner = StringField(required=True)
    link = StringField(default="")


class DatasetSpec(EmbeddedDocument):
    id = StringField(required=True)
    version = StringField(default="latest")
    mount_output = BooleanField(default=False)


class Param(EmbeddedDocument):
    name = StringField(required=True)
    value = StringField(required=True)


class WorkspaceSpec(EmbeddedDocument):
    revision = StringField(required=True)
    ide = ReferenceField(Ide, required=True)
    hardware = ReferenceField(HardwareTier, required=True)
    environment = ReferenceField(Environment, required=True)
    datasets = ListField(EmbeddedDocumentField(DatasetSpec), default=[])


class Workspace(Document):
    """The object Workspace stored in the Database"""

    metadata = EmbeddedDocumentField(Metadata, required=True)
    state = StringField(required=True)
    spec = EmbeddedDocumentField(WorkspaceSpec, required=True)
    deleted = BooleanField(default=False)
    create_at = DateTimeField(default=datetime.datetime.now)
    last_start = DateTimeField()
    last_update = DateTimeField(default=datetime.datetime.now)
    uptime = IntField(required=True, default=0, min_value=0)

    meta = {
        'ordering': ['-create_at']
    }

    def __str__(self):
        return str(self.metadata.name)


class RunSpec(EmbeddedDocument):
    revision = StringField(required=True)
    command = StringField(required=True)
    schedule_time = DateTimeField()
    hardware = ReferenceField(HardwareTier, required=True)
    environment = ReferenceField(Environment, required=True)
    datasets = ListField(EmbeddedDocumentField(DatasetSpec), default=[])


class Run(Document):
    """The object Run stored in the Database"""

    metadata = EmbeddedDocumentField(Metadata, required=True)
    state = StringField(required=True)
    spec = EmbeddedDocumentField(RunSpec, required=True)
    deleted = BooleanField(default=False)
    create_at = DateTimeField(default=datetime.datetime.now)
    last_update = DateTimeField(default=datetime.datetime.now)
    uptime = IntField(required=True, default=0, min_value=0)

    meta = {
        'ordering': ['-create_at']
    }

    def __str__(self):
        return str(self.metadata.name)


class ExperimentSpec(EmbeddedDocument):
    revision = StringField(required=True)
    entrypoint = StringField(required=True)
    params = ListField(EmbeddedDocumentField(Param), default=[])
    hardware = ReferenceField(HardwareTier, required=True)
    environment = ReferenceField(Environment, required=True)
    datasets = ListField(EmbeddedDocumentField(DatasetSpec), default=[])


class Experiment(Document):
    """The object Experiment stored in the Database"""

    metadata = EmbeddedDocumentField(Metadata, required=True)
    state = StringField(required=True)
    spec = EmbeddedDocumentField(ExperimentSpec, required=True)
    deleted = BooleanField(default=False)
    create_at = DateTimeField(default=datetime.datetime.now)
    last_update = DateTimeField(default=datetime.datetime.now)
    uptime = IntField(required=True, default=0, min_value=0)

    meta = {
        'ordering': ['-create_at']
    }

    def __str__(self):
        return str(self.metadata.name)


class ModelApiSpec(EmbeddedDocument):
    model = StringField(required=True)
    version = IntField(required=True)
    stage = StringField()
    environment = ReferenceField(Environment, required=True)
    hardware = ReferenceField(HardwareTier, required=True)
    datasets = ListField(EmbeddedDocumentField(DatasetSpec), default=[])


class ModelApis(Document):
    """The object ModelApis stored in the Database"""

    metadata = EmbeddedDocumentField(Metadata, required=True)
    state = StringField(required=True)
    spec = EmbeddedDocumentField(ModelApiSpec, required=True)
    deleted = BooleanField(default=False)
    create_at = DateTimeField(default=datetime.datetime.now)
    last_start = DateTimeField()
    last_update = DateTimeField(default=datetime.datetime.now)
    uptime = IntField(required=True, default=0, min_value=0)

    meta = {
        'ordering': ['-create_at']
    }

    def __str__(self):
        return str(self.metadata.name)
