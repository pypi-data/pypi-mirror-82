# coding: utf-8

"""
    Xero Assets API

    This is the Xero Assets API  # noqa: E501

    OpenAPI spec version: 2.3.4
    Contact: api@xero.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401

from xero_python.models import BaseModel


class FieldValidationErrorsElement(BaseModel):
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
        "field_name": "str",
        "value_provided": "str",
        "localised_message": "str",
        "type": "str",
        "title": "str",
        "detail": "str",
    }

    attribute_map = {
        "field_name": "fieldName",
        "value_provided": "valueProvided",
        "localised_message": "localisedMessage",
        "type": "type",
        "title": "title",
        "detail": "detail",
    }

    def __init__(
        self,
        field_name=None,
        value_provided=None,
        localised_message=None,
        type=None,
        title=None,
        detail=None,
    ):  # noqa: E501
        """FieldValidationErrorsElement - a model defined in OpenAPI"""  # noqa: E501

        self._field_name = None
        self._value_provided = None
        self._localised_message = None
        self._type = None
        self._title = None
        self._detail = None
        self.discriminator = None

        if field_name is not None:
            self.field_name = field_name
        if value_provided is not None:
            self.value_provided = value_provided
        if localised_message is not None:
            self.localised_message = localised_message
        if type is not None:
            self.type = type
        if title is not None:
            self.title = title
        if detail is not None:
            self.detail = detail

    @property
    def field_name(self):
        """Gets the field_name of this FieldValidationErrorsElement.  # noqa: E501

        The field name of the erroneous field  # noqa: E501

        :return: The field_name of this FieldValidationErrorsElement.  # noqa: E501
        :rtype: str
        """
        return self._field_name

    @field_name.setter
    def field_name(self, field_name):
        """Sets the field_name of this FieldValidationErrorsElement.

        The field name of the erroneous field  # noqa: E501

        :param field_name: The field_name of this FieldValidationErrorsElement.  # noqa: E501
        :type: str
        """

        self._field_name = field_name

    @property
    def value_provided(self):
        """Gets the value_provided of this FieldValidationErrorsElement.  # noqa: E501

        The provided value  # noqa: E501

        :return: The value_provided of this FieldValidationErrorsElement.  # noqa: E501
        :rtype: str
        """
        return self._value_provided

    @value_provided.setter
    def value_provided(self, value_provided):
        """Sets the value_provided of this FieldValidationErrorsElement.

        The provided value  # noqa: E501

        :param value_provided: The value_provided of this FieldValidationErrorsElement.  # noqa: E501
        :type: str
        """

        self._value_provided = value_provided

    @property
    def localised_message(self):
        """Gets the localised_message of this FieldValidationErrorsElement.  # noqa: E501

        Explaination of the field validation error  # noqa: E501

        :return: The localised_message of this FieldValidationErrorsElement.  # noqa: E501
        :rtype: str
        """
        return self._localised_message

    @localised_message.setter
    def localised_message(self, localised_message):
        """Sets the localised_message of this FieldValidationErrorsElement.

        Explaination of the field validation error  # noqa: E501

        :param localised_message: The localised_message of this FieldValidationErrorsElement.  # noqa: E501
        :type: str
        """

        self._localised_message = localised_message

    @property
    def type(self):
        """Gets the type of this FieldValidationErrorsElement.  # noqa: E501

        Internal type of the field validation error message  # noqa: E501

        :return: The type of this FieldValidationErrorsElement.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this FieldValidationErrorsElement.

        Internal type of the field validation error message  # noqa: E501

        :param type: The type of this FieldValidationErrorsElement.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def title(self):
        """Gets the title of this FieldValidationErrorsElement.  # noqa: E501

        Title of the field validation error  # noqa: E501

        :return: The title of this FieldValidationErrorsElement.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this FieldValidationErrorsElement.

        Title of the field validation error  # noqa: E501

        :param title: The title of this FieldValidationErrorsElement.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def detail(self):
        """Gets the detail of this FieldValidationErrorsElement.  # noqa: E501

        Detail of the field validation error  # noqa: E501

        :return: The detail of this FieldValidationErrorsElement.  # noqa: E501
        :rtype: str
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this FieldValidationErrorsElement.

        Detail of the field validation error  # noqa: E501

        :param detail: The detail of this FieldValidationErrorsElement.  # noqa: E501
        :type: str
        """

        self._detail = detail
