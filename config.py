# coding: utf-8
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

from decouple import config
import os

BASE_DIR = os.path.dirname(__file__)

MONGO_DATABASE_URL = config('MONGO_DATABASE_URL')
MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

MINIO_HOST = config('MINIO_HOST')
MINIO_ENDPOINT = config('MINIO_ENDPOINT')

KUBESPAWNER_SERVICES_ENDPOINT = config('KUBESPAWNER_SERVICES_ENDPOINT')
DATASETS_SERVICES_ENDPOINT = config('DATASETS_SERVICES_ENDPOINT')
PROJECTS_SERVICES_ENDPOINT = config('PROJECTS_SERVICES_ENDPOINT')

ETCD_PORT = 2379
ETCD_HOST = config('ETCD_HOST')

KUBE_NAMESPACE = config('KUBE_NAMESPACE')
DEPLOYMENT_MIDDLEWARES = ["ilyde-deployment-replacepathregex"]

MLFLOW_TRACKING_URI = config("MLFLOW_TRACKING_URI")

ILYDE_JOB_INITIALIZER_IMAGE_NAME = config("ILYDE_JOB_INITIALIZER_IMAGE_NAME")

