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


class RepeatingInvoices(BaseModel):
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
    openapi_types = {"repeating_invoices": "list[RepeatingInvoice]"}

    attribute_map = {"repeating_invoices": "RepeatingInvoices"}

    def __init__(self, repeating_invoices=None):  # noqa: E501
        """RepeatingInvoices - a model defined in OpenAPI"""  # noqa: E501

        self._repeating_invoices = None
        self.discriminator = None

        if repeating_invoices is not None:
            self.repeating_invoices = repeating_invoices

    @property
    def repeating_invoices(self):
        """Gets the repeating_invoices of this RepeatingInvoices.  # noqa: E501


        :return: The repeating_invoices of this RepeatingInvoices.  # noqa: E501
        :rtype: list[RepeatingInvoice]
        """
        return self._repeating_invoices

    @repeating_invoices.setter
    def repeating_invoices(self, repeating_invoices):
        """Sets the repeating_invoices of this RepeatingInvoices.


        :param repeating_invoices: The repeating_invoices of this RepeatingInvoices.  # noqa: E501
        :type: list[RepeatingInvoice]
        """

        self._repeating_invoices = repeating_invoices
