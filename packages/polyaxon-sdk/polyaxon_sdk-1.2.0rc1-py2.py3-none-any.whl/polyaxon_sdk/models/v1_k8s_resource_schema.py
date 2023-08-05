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


class V1K8sResourceSchema(object):
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
        'name': 'str',
        'mount_path': 'str',
        'items': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'mount_path': 'mount_path',
        'items': 'items'
    }

    def __init__(self, name=None, mount_path=None, items=None, local_vars_configuration=None):  # noqa: E501
        """V1K8sResourceSchema - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._mount_path = None
        self._items = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if mount_path is not None:
            self.mount_path = mount_path
        if items is not None:
            self.items = items

    @property
    def name(self):
        """Gets the name of this V1K8sResourceSchema.  # noqa: E501


        :return: The name of this V1K8sResourceSchema.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1K8sResourceSchema.


        :param name: The name of this V1K8sResourceSchema.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def mount_path(self):
        """Gets the mount_path of this V1K8sResourceSchema.  # noqa: E501


        :return: The mount_path of this V1K8sResourceSchema.  # noqa: E501
        :rtype: str
        """
        return self._mount_path

    @mount_path.setter
    def mount_path(self, mount_path):
        """Sets the mount_path of this V1K8sResourceSchema.


        :param mount_path: The mount_path of this V1K8sResourceSchema.  # noqa: E501
        :type: str
        """

        self._mount_path = mount_path

    @property
    def items(self):
        """Gets the items of this V1K8sResourceSchema.  # noqa: E501


        :return: The items of this V1K8sResourceSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this V1K8sResourceSchema.


        :param items: The items of this V1K8sResourceSchema.  # noqa: E501
        :type: list[str]
        """

        self._items = items

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
        if not isinstance(other, V1K8sResourceSchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1K8sResourceSchema):
            return True

        return self.to_dict() != other.to_dict()
