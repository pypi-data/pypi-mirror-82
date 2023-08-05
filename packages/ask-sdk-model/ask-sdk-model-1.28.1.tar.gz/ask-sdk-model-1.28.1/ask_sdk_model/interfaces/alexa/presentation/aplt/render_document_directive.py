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
from ask_sdk_model.directive import Directive


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime
    from ask_sdk_model.interfaces.alexa.presentation.aplt.target_profile import TargetProfile


class RenderDocumentDirective(Directive):
    """

    :param token: A unique identifier for the presentation.
    :type token: (optional) str
    :param target_profile: One of supported profiles in character display. Default value is NONE.
    :type target_profile: (optional) ask_sdk_model.interfaces.alexa.presentation.aplt.target_profile.TargetProfile
    :param document: Depending on the document type, it represents either an entire APLT document or a reference Link to the document. In a Link object, the value of the &#39;src&#39; should follow a URI format defined like &#39;doc://alexa/aplt/documents/&lt;document_id&gt;&#39;. The &#39;document_id&#39; is a reference to the APLT document that the developer stores through APL Authoring Tool.
    :type document: (optional) dict(str, object)
    :param datasources: Data sources to bind to the document when rendering.
    :type datasources: (optional) dict(str, object)

    """
    deserialized_types = {
        'object_type': 'str',
        'token': 'str',
        'target_profile': 'ask_sdk_model.interfaces.alexa.presentation.aplt.target_profile.TargetProfile',
        'document': 'dict(str, object)',
        'datasources': 'dict(str, object)'
    }  # type: Dict

    attribute_map = {
        'object_type': 'type',
        'token': 'token',
        'target_profile': 'targetProfile',
        'document': 'document',
        'datasources': 'datasources'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, token=None, target_profile=None, document=None, datasources=None):
        # type: (Optional[str], Optional[TargetProfile], Optional[Dict[str, object]], Optional[Dict[str, object]]) -> None
        """

        :param token: A unique identifier for the presentation.
        :type token: (optional) str
        :param target_profile: One of supported profiles in character display. Default value is NONE.
        :type target_profile: (optional) ask_sdk_model.interfaces.alexa.presentation.aplt.target_profile.TargetProfile
        :param document: Depending on the document type, it represents either an entire APLT document or a reference Link to the document. In a Link object, the value of the &#39;src&#39; should follow a URI format defined like &#39;doc://alexa/aplt/documents/&lt;document_id&gt;&#39;. The &#39;document_id&#39; is a reference to the APLT document that the developer stores through APL Authoring Tool.
        :type document: (optional) dict(str, object)
        :param datasources: Data sources to bind to the document when rendering.
        :type datasources: (optional) dict(str, object)
        """
        self.__discriminator_value = "Alexa.Presentation.APLT.RenderDocument"  # type: str

        self.object_type = self.__discriminator_value
        super(RenderDocumentDirective, self).__init__(object_type=self.__discriminator_value)
        self.token = token
        self.target_profile = target_profile
        self.document = document
        self.datasources = datasources

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
        if not isinstance(other, RenderDocumentDirective):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
