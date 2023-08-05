# coding: utf-8

"""
    Xero Payroll UK

    This is the Xero Payroll API for orgs in the UK region.  # noqa: E501

    OpenAPI spec version: 2.3.4
    Contact: api@xero.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401

from xero_python.models import BaseModel


class EmploymentObject(BaseModel):
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
        "pagination": "Pagination",
        "problem": "Problem",
        "employment": "Employment",
    }

    attribute_map = {
        "pagination": "pagination",
        "problem": "problem",
        "employment": "employment",
    }

    def __init__(self, pagination=None, problem=None, employment=None):  # noqa: E501
        """EmploymentObject - a model defined in OpenAPI"""  # noqa: E501

        self._pagination = None
        self._problem = None
        self._employment = None
        self.discriminator = None

        if pagination is not None:
            self.pagination = pagination
        if problem is not None:
            self.problem = problem
        if employment is not None:
            self.employment = employment

    @property
    def pagination(self):
        """Gets the pagination of this EmploymentObject.  # noqa: E501


        :return: The pagination of this EmploymentObject.  # noqa: E501
        :rtype: Pagination
        """
        return self._pagination

    @pagination.setter
    def pagination(self, pagination):
        """Sets the pagination of this EmploymentObject.


        :param pagination: The pagination of this EmploymentObject.  # noqa: E501
        :type: Pagination
        """

        self._pagination = pagination

    @property
    def problem(self):
        """Gets the problem of this EmploymentObject.  # noqa: E501


        :return: The problem of this EmploymentObject.  # noqa: E501
        :rtype: Problem
        """
        return self._problem

    @problem.setter
    def problem(self, problem):
        """Sets the problem of this EmploymentObject.


        :param problem: The problem of this EmploymentObject.  # noqa: E501
        :type: Problem
        """

        self._problem = problem

    @property
    def employment(self):
        """Gets the employment of this EmploymentObject.  # noqa: E501


        :return: The employment of this EmploymentObject.  # noqa: E501
        :rtype: Employment
        """
        return self._employment

    @employment.setter
    def employment(self, employment):
        """Sets the employment of this EmploymentObject.


        :param employment: The employment of this EmploymentObject.  # noqa: E501
        :type: Employment
        """

        self._employment = employment
