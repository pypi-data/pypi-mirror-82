# coding: utf-8

"""
    Accounting API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: 2.3.4
    Contact: api@xero.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401

from xero_python.models import BaseModel


class TaxComponent(BaseModel):
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
        "name": "str",
        "rate": "float",
        "is_compound": "bool",
        "is_non_recoverable": "bool",
    }

    attribute_map = {
        "name": "Name",
        "rate": "Rate",
        "is_compound": "IsCompound",
        "is_non_recoverable": "IsNonRecoverable",
    }

    def __init__(
        self, name=None, rate=None, is_compound=None, is_non_recoverable=None
    ):  # noqa: E501
        """TaxComponent - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self._rate = None
        self._is_compound = None
        self._is_non_recoverable = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if rate is not None:
            self.rate = rate
        if is_compound is not None:
            self.is_compound = is_compound
        if is_non_recoverable is not None:
            self.is_non_recoverable = is_non_recoverable

    @property
    def name(self):
        """Gets the name of this TaxComponent.  # noqa: E501

        Name of Tax Component  # noqa: E501

        :return: The name of this TaxComponent.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaxComponent.

        Name of Tax Component  # noqa: E501

        :param name: The name of this TaxComponent.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def rate(self):
        """Gets the rate of this TaxComponent.  # noqa: E501

        Tax Rate (up to 4dp)  # noqa: E501

        :return: The rate of this TaxComponent.  # noqa: E501
        :rtype: float
        """
        return self._rate

    @rate.setter
    def rate(self, rate):
        """Sets the rate of this TaxComponent.

        Tax Rate (up to 4dp)  # noqa: E501

        :param rate: The rate of this TaxComponent.  # noqa: E501
        :type: float
        """

        self._rate = rate

    @property
    def is_compound(self):
        """Gets the is_compound of this TaxComponent.  # noqa: E501

        Boolean to describe if Tax rate is compounded.  # noqa: E501

        :return: The is_compound of this TaxComponent.  # noqa: E501
        :rtype: bool
        """
        return self._is_compound

    @is_compound.setter
    def is_compound(self, is_compound):
        """Sets the is_compound of this TaxComponent.

        Boolean to describe if Tax rate is compounded.  # noqa: E501

        :param is_compound: The is_compound of this TaxComponent.  # noqa: E501
        :type: bool
        """

        self._is_compound = is_compound

    @property
    def is_non_recoverable(self):
        """Gets the is_non_recoverable of this TaxComponent.  # noqa: E501

        Boolean to describe if tax rate is non-recoverable. Non-recoverable rates are only applicable to Canadian organisations  # noqa: E501

        :return: The is_non_recoverable of this TaxComponent.  # noqa: E501
        :rtype: bool
        """
        return self._is_non_recoverable

    @is_non_recoverable.setter
    def is_non_recoverable(self, is_non_recoverable):
        """Sets the is_non_recoverable of this TaxComponent.

        Boolean to describe if tax rate is non-recoverable. Non-recoverable rates are only applicable to Canadian organisations  # noqa: E501

        :param is_non_recoverable: The is_non_recoverable of this TaxComponent.  # noqa: E501
        :type: bool
        """

        self._is_non_recoverable = is_non_recoverable
