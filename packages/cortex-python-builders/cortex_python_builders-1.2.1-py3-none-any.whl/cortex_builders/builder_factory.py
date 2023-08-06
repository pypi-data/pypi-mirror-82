"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re

from cortex.pipeline import Pipeline
from cortex.dataset import DatasetsClient
from cortex.catalog import CatalogClient
from cortex.action import ActionClient
from cortex.connection import ConnectionClient

from .action_builder import ActionBuilder
from .connection_builder import ConnectionBuilder
from .dataset_builder import DatasetBuilder, LocalDatasetBuilder
from .schema_builder import SchemaBuilder
from .skill_builder import SkillBuilder


class BuilderFactory:
    """
    Builds component builders.
    """
    def __init__(self, client):
        self.client = client

    def dataset(self, name: str, camel_version='1.0.0') -> DatasetBuilder:
        """
        Creates a DatasetBuilder with the given name.

        **Example**

        >>> builder = cortex.builder()
        >>> train_df = pd.read_csv(' <path to data as csv file>')
        >>> train_ds = builder.dataset('<cortex name space>/<dataset name>').from_df(train_df).build()

        :param name: name of the dataset builder. The name must provide at least one cortex namespace identifier and a resource name.
        """
        validate_resource_name(name)

        ds_client = DatasetsClient(self.client, version=3)
        return DatasetBuilder(name, ds_client, camel_version)

    def connection(self, name: str, camel_version='1.0.0') -> ConnectionBuilder:
        """
        Creates a connection with the given name.

        :param name: name of the connection builder. The name must provide at least one cortex namespace identifier and a resource name.
        """
        validate_resource_name(name)

        connection_client = ConnectionClient(self.client, version=2)
        return ConnectionBuilder(name, connection_client, camel_version)

    def skill(self, name: str, camel_version='1.0.0') -> SkillBuilder:
        """
        Creates a SkillBuilder with the given name.

        :param name: name of the skill builder. The name must provide at least one cortex namespace identifier and a resource name.
        """
        validate_resource_name(name)

        catalog_client = CatalogClient(self.client, version=3)
        return SkillBuilder(name, catalog_client, camel_version)

    def action(self, name: str, camel_version='1.0.0'):
        """
        Creates an ActionBuilder with the given name.

        :param name: name of the action builder. The name must provide at least one cortex namespace identifier and a resource name.
        """
        validate_resource_name(name)

        action_client = ActionClient(self.client, version=3)
        return ActionBuilder(name, action_client, camel_version)

    def schema(self, name: str, camel_version='1.0.0'):
        """
        Creates a SchemaBuilder with the given name.

        :param name: name of the schema builder
        """
        validate_resource_name(name)

        catalog_client = CatalogClient(self.client, version=3)
        return SchemaBuilder(name, catalog_client, camel_version)

    def pipeline(self, name: str):
        """
        Creates a pipeline with the given name.

        :param name: name of the pipeline
        """
        return Pipeline(name)


class LocalBuilderFactory:
    """
    Builds local component builders.
    """
    def __init__(self, basedir=None):
        self._basedir = basedir

    def dataset(self, name: str, camel_version='1.0.0') -> DatasetBuilder:
        """
        Creates a LocalDatasetBuilder with the given name.

        **Example**

        >>> builder = cortex.builder()
        >>> train_df = pd.read_csv(' <path to data as csv file>')
        >>> train_ds = builder.dataset(' <data set name> ')\
                .from_df(train_df).build()

        :param name: name of the local dataset builder
        """
        return LocalDatasetBuilder(name, camel_version, self._basedir)

    def pipeline(self, name: str):
        """
        Creates a local pipeline with the given name.

        :param name: name of the local dataset builder pipeline
        """
        return Pipeline(name)

def validate_resource_name(name: str):
    """
    A function to ensure that a name has at least one cortex namespace identifier.

    :param name: name of the Cortex resource. The name must provide a Cortex namespace identifier and a resource name.
    """
    if (re.compile('.+\/.+').match(name) is None): # enforce namespace validation
            raise ValueError('ERROR: {name} must provide a namespace path element'.format(name=name))
