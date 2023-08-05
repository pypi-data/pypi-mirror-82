#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

    Polyaxon SDKs and REST API specification.  # noqa: E501

    The version of the OpenAPI document: 1.2.0-rc1
    Contact: contact@polyaxon.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from polyaxon_sdk.configuration import Configuration


class V1RunSettings(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'namespace': 'str',
        'agent': 'V1RunSettingsCatalog',
        'queue': 'V1RunSettingsCatalog',
        'artifacts_store': 'V1RunSettingsCatalog',
        'connections': 'list[V1RunSettingsCatalog]',
        'concurrency': 'int',
        'meta_info': 'object'
    }

    attribute_map = {
        'namespace': 'namespace',
        'agent': 'agent',
        'queue': 'queue',
        'artifacts_store': 'artifacts_store',
        'connections': 'connections',
        'concurrency': 'concurrency',
        'meta_info': 'meta_info'
    }

    def __init__(self, namespace=None, agent=None, queue=None, artifacts_store=None, connections=None, concurrency=None, meta_info=None, local_vars_configuration=None):  # noqa: E501
        """V1RunSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._namespace = None
        self._agent = None
        self._queue = None
        self._artifacts_store = None
        self._connections = None
        self._concurrency = None
        self._meta_info = None
        self.discriminator = None

        if namespace is not None:
            self.namespace = namespace
        if agent is not None:
            self.agent = agent
        if queue is not None:
            self.queue = queue
        if artifacts_store is not None:
            self.artifacts_store = artifacts_store
        if connections is not None:
            self.connections = connections
        if concurrency is not None:
            self.concurrency = concurrency
        if meta_info is not None:
            self.meta_info = meta_info

    @property
    def namespace(self):
        """Gets the namespace of this V1RunSettings.  # noqa: E501


        :return: The namespace of this V1RunSettings.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this V1RunSettings.


        :param namespace: The namespace of this V1RunSettings.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def agent(self):
        """Gets the agent of this V1RunSettings.  # noqa: E501


        :return: The agent of this V1RunSettings.  # noqa: E501
        :rtype: V1RunSettingsCatalog
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this V1RunSettings.


        :param agent: The agent of this V1RunSettings.  # noqa: E501
        :type: V1RunSettingsCatalog
        """

        self._agent = agent

    @property
    def queue(self):
        """Gets the queue of this V1RunSettings.  # noqa: E501


        :return: The queue of this V1RunSettings.  # noqa: E501
        :rtype: V1RunSettingsCatalog
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this V1RunSettings.


        :param queue: The queue of this V1RunSettings.  # noqa: E501
        :type: V1RunSettingsCatalog
        """

        self._queue = queue

    @property
    def artifacts_store(self):
        """Gets the artifacts_store of this V1RunSettings.  # noqa: E501


        :return: The artifacts_store of this V1RunSettings.  # noqa: E501
        :rtype: V1RunSettingsCatalog
        """
        return self._artifacts_store

    @artifacts_store.setter
    def artifacts_store(self, artifacts_store):
        """Sets the artifacts_store of this V1RunSettings.


        :param artifacts_store: The artifacts_store of this V1RunSettings.  # noqa: E501
        :type: V1RunSettingsCatalog
        """

        self._artifacts_store = artifacts_store

    @property
    def connections(self):
        """Gets the connections of this V1RunSettings.  # noqa: E501


        :return: The connections of this V1RunSettings.  # noqa: E501
        :rtype: list[V1RunSettingsCatalog]
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """Sets the connections of this V1RunSettings.


        :param connections: The connections of this V1RunSettings.  # noqa: E501
        :type: list[V1RunSettingsCatalog]
        """

        self._connections = connections

    @property
    def concurrency(self):
        """Gets the concurrency of this V1RunSettings.  # noqa: E501


        :return: The concurrency of this V1RunSettings.  # noqa: E501
        :rtype: int
        """
        return self._concurrency

    @concurrency.setter
    def concurrency(self, concurrency):
        """Sets the concurrency of this V1RunSettings.


        :param concurrency: The concurrency of this V1RunSettings.  # noqa: E501
        :type: int
        """

        self._concurrency = concurrency

    @property
    def meta_info(self):
        """Gets the meta_info of this V1RunSettings.  # noqa: E501


        :return: The meta_info of this V1RunSettings.  # noqa: E501
        :rtype: object
        """
        return self._meta_info

    @meta_info.setter
    def meta_info(self, meta_info):
        """Sets the meta_info of this V1RunSettings.


        :param meta_info: The meta_info of this V1RunSettings.  # noqa: E501
        :type: object
        """

        self._meta_info = meta_info

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1RunSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1RunSettings):
            return True

        return self.to_dict() != other.to_dict()
