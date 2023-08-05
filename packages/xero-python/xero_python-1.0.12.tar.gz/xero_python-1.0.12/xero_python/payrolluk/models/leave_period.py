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


class LeavePeriod(BaseModel):
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
        "period_start_date": "date",
        "period_end_date": "date",
        "number_of_units": "float",
        "period_status": "str",
    }

    attribute_map = {
        "period_start_date": "periodStartDate",
        "period_end_date": "periodEndDate",
        "number_of_units": "numberOfUnits",
        "period_status": "periodStatus",
    }

    def __init__(
        self,
        period_start_date=None,
        period_end_date=None,
        number_of_units=None,
        period_status=None,
    ):  # noqa: E501
        """LeavePeriod - a model defined in OpenAPI"""  # noqa: E501

        self._period_start_date = None
        self._period_end_date = None
        self._number_of_units = None
        self._period_status = None
        self.discriminator = None

        if period_start_date is not None:
            self.period_start_date = period_start_date
        if period_end_date is not None:
            self.period_end_date = period_end_date
        if number_of_units is not None:
            self.number_of_units = number_of_units
        if period_status is not None:
            self.period_status = period_status

    @property
    def period_start_date(self):
        """Gets the period_start_date of this LeavePeriod.  # noqa: E501

        The Pay Period Start Date (YYYY-MM-DD)  # noqa: E501

        :return: The period_start_date of this LeavePeriod.  # noqa: E501
        :rtype: date
        """
        return self._period_start_date

    @period_start_date.setter
    def period_start_date(self, period_start_date):
        """Sets the period_start_date of this LeavePeriod.

        The Pay Period Start Date (YYYY-MM-DD)  # noqa: E501

        :param period_start_date: The period_start_date of this LeavePeriod.  # noqa: E501
        :type: date
        """

        self._period_start_date = period_start_date

    @property
    def period_end_date(self):
        """Gets the period_end_date of this LeavePeriod.  # noqa: E501

        The Pay Period End Date (YYYY-MM-DD)  # noqa: E501

        :return: The period_end_date of this LeavePeriod.  # noqa: E501
        :rtype: date
        """
        return self._period_end_date

    @period_end_date.setter
    def period_end_date(self, period_end_date):
        """Sets the period_end_date of this LeavePeriod.

        The Pay Period End Date (YYYY-MM-DD)  # noqa: E501

        :param period_end_date: The period_end_date of this LeavePeriod.  # noqa: E501
        :type: date
        """

        self._period_end_date = period_end_date

    @property
    def number_of_units(self):
        """Gets the number_of_units of this LeavePeriod.  # noqa: E501

        The Number of Units for the leave  # noqa: E501

        :return: The number_of_units of this LeavePeriod.  # noqa: E501
        :rtype: float
        """
        return self._number_of_units

    @number_of_units.setter
    def number_of_units(self, number_of_units):
        """Sets the number_of_units of this LeavePeriod.

        The Number of Units for the leave  # noqa: E501

        :param number_of_units: The number_of_units of this LeavePeriod.  # noqa: E501
        :type: float
        """

        self._number_of_units = number_of_units

    @property
    def period_status(self):
        """Gets the period_status of this LeavePeriod.  # noqa: E501

        Period Status  # noqa: E501

        :return: The period_status of this LeavePeriod.  # noqa: E501
        :rtype: str
        """
        return self._period_status

    @period_status.setter
    def period_status(self, period_status):
        """Sets the period_status of this LeavePeriod.

        Period Status  # noqa: E501

        :param period_status: The period_status of this LeavePeriod.  # noqa: E501
        :type: str
        """
        allowed_values = ["Approved", "Completed", "None"]  # noqa: E501
        if period_status not in allowed_values:
            raise ValueError(
                "Invalid value for `period_status` ({0}), must be one of {1}".format(  # noqa: E501
                    period_status, allowed_values
                )
            )

        self._period_status = period_status
