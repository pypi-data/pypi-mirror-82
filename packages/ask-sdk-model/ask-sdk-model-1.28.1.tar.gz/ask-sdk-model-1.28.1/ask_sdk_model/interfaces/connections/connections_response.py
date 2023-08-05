# coding: utf-8

#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#

import pprint
import re  # noqa: F401
import six
import typing
from enum import Enum
from ask_sdk_model.request import Request


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.interfaces.connections.connections_status import ConnectionsStatus


class ConnectionsResponse(Request):
    """
    This is the request object that a skill will receive as a result of Connections.SendResponse directive from referrer skill.


    :param request_id: Represents the unique identifier for the specific request.
    :type request_id: (optional) str
    :param timestamp: Provides the date and time when Alexa sent the request as an ISO 8601 formatted string. Used to verify the request when hosting your skill as a web service.
    :type timestamp: (optional) datetime
    :param locale: A string indicating the user’s locale. For example: en-US. This value is only provided with certain request types.
    :type locale: (optional) str
    :param status: 
    :type status: (optional) ask_sdk_model.interfaces.connections.connections_status.ConnectionsStatus
    :param name: Name of the action for which response is received.
    :type name: (optional) str
    :param payload: This is an object sent from referrer skill as is.
    :type payload: (optional) dict(str, object)
    :param token: This is the token that the skill originally sent with the ConnectionsSendRequest directive.
    :type token: (optional) str

    """
    deserialized_types = {
        'object_type': 'str',
        'request_id': 'str',
        'timestamp': 'datetime',
        'locale': 'str',
        'status': 'ask_sdk_model.interfaces.connections.connections_status.ConnectionsStatus',
        'name': 'str',
        'payload': 'dict(str, object)',
        'token': 'str'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'request_id': 'requestId',
        'timestamp': 'timestamp',
        'locale': 'locale',
        'status': 'status',
        'name': 'name',
        'payload': 'payload',
        'token': 'token'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, request_id=None, timestamp=None, locale=None, status=None, name=None, payload=None, token=None):
        # type: (Optional[str], Optional[datetime], Optional[str], Optional[ConnectionsStatus], Optional[str], Optional[Dict[str, object]], Optional[str]) -> None
        """This is the request object that a skill will receive as a result of Connections.SendResponse directive from referrer skill.

        :param request_id: Represents the unique identifier for the specific request.
        :type request_id: (optional) str
        :param timestamp: Provides the date and time when Alexa sent the request as an ISO 8601 formatted string. Used to verify the request when hosting your skill as a web service.
        :type timestamp: (optional) datetime
        :param locale: A string indicating the user’s locale. For example: en-US. This value is only provided with certain request types.
        :type locale: (optional) str
        :param status: 
        :type status: (optional) ask_sdk_model.interfaces.connections.connections_status.ConnectionsStatus
        :param name: Name of the action for which response is received.
        :type name: (optional) str
        :param payload: This is an object sent from referrer skill as is.
        :type payload: (optional) dict(str, object)
        :param token: This is the token that the skill originally sent with the ConnectionsSendRequest directive.
        :type token: (optional) str
        """
        self.__discriminator_value = "Connections.Response"  # type: str

        self.object_type = self.__discriminator_value
        super(ConnectionsResponse, self).__init__(object_type=self.__discriminator_value, request_id=request_id, timestamp=timestamp, locale=locale)
        self.status = status
        self.name = name
        self.payload = payload
        self.token = token

    def to_dict(self):
        # type: () -> Dict[str, object]
        """Returns the model properties as a dict"""
        result = {}  # type: Dict

        for attr, _ in six.iteritems(self.deserialized_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else
                    x.value if isinstance(x, Enum) else x,
                    value
                ))
            elif isinstance(value, Enum):
                result[attr] = value.value
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else
                    (item[0], item[1].value)
                    if isinstance(item[1], Enum) else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        # type: () -> str
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        # type: () -> str
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are equal"""
        if not isinstance(other, ConnectionsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
