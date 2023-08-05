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
from ask_smapi_model.v1.skill.asr.annotation_sets.annotation_set_metadata import AnnotationSetMetadata


if typing.TYPE_CHECKING:
    from typing import Dict, List, Optional, Union, Any
    from datetime import datetime


class AnnotationSetItems(AnnotationSetMetadata):
    """

    :param name: Name of the ASR annotation set
    :type name: (optional) str
    :param annotation_count: Number of annotations within an annotation set
    :type annotation_count: (optional) int
    :param last_updated_timestamp: The timestamp for the most recent update of ASR annotation set
    :type last_updated_timestamp: (optional) datetime
    :param eligible_for_evaluation: Indicates if the annotation set is eligible for evaluation. A set is not eligible for evaluation if any annotation within the set has a missing uploadId, filePathInUpload, expectedTranscription, or evaluationWeight.
    :type eligible_for_evaluation: (optional) bool
    :param id: The Annotation set id
    :type id: (optional) str

    """
    deserialized_types = {
        'name': 'str',
        'annotation_count': 'int',
        'last_updated_timestamp': 'datetime',
        'eligible_for_evaluation': 'bool',
        'id': 'str'
    }  # type: Dict

    attribute_map = {
        'name': 'name',
        'annotation_count': 'annotationCount',
        'last_updated_timestamp': 'lastUpdatedTimestamp',
        'eligible_for_evaluation': 'eligibleForEvaluation',
        'id': 'id'
    }  # type: Dict
    supports_multiple_types = False

    def __init__(self, name=None, annotation_count=None, last_updated_timestamp=None, eligible_for_evaluation=None, id=None):
        # type: (Optional[str], Optional[int], Optional[datetime], Optional[bool], Optional[str]) -> None
        """

        :param name: Name of the ASR annotation set
        :type name: (optional) str
        :param annotation_count: Number of annotations within an annotation set
        :type annotation_count: (optional) int
        :param last_updated_timestamp: The timestamp for the most recent update of ASR annotation set
        :type last_updated_timestamp: (optional) datetime
        :param eligible_for_evaluation: Indicates if the annotation set is eligible for evaluation. A set is not eligible for evaluation if any annotation within the set has a missing uploadId, filePathInUpload, expectedTranscription, or evaluationWeight.
        :type eligible_for_evaluation: (optional) bool
        :param id: The Annotation set id
        :type id: (optional) str
        """
        self.__discriminator_value = None  # type: str

        super(AnnotationSetItems, self).__init__(name=name, annotation_count=annotation_count, last_updated_timestamp=last_updated_timestamp, eligible_for_evaluation=eligible_for_evaluation)
        self.id = id

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
        if not isinstance(other, AnnotationSetItems):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        # type: (object) -> bool
        """Returns true if both objects are not equal"""
        return not self == other
