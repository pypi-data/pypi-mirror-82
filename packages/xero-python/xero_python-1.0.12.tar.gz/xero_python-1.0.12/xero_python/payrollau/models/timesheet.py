# coding: utf-8

"""
    Xero Payroll AU

    This is the Xero Payroll API for orgs in Australia region.  # noqa: E501

    OpenAPI spec version: 2.3.4
    Contact: api@xero.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401

from xero_python.models import BaseModel


class Timesheet(BaseModel):
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
        "employee_id": "str",
        "start_date": "date[ms-format]",
        "end_date": "date[ms-format]",
        "status": "TimesheetStatus",
        "hours": "float",
        "timesheet_id": "str",
        "timesheet_lines": "list[TimesheetLine]",
        "updated_date_utc": "datetime[ms-format]",
        "validation_errors": "list[ValidationError]",
    }

    attribute_map = {
        "employee_id": "EmployeeID",
        "start_date": "StartDate",
        "end_date": "EndDate",
        "status": "Status",
        "hours": "Hours",
        "timesheet_id": "TimesheetID",
        "timesheet_lines": "TimesheetLines",
        "updated_date_utc": "UpdatedDateUTC",
        "validation_errors": "ValidationErrors",
    }

    def __init__(
        self,
        employee_id=None,
        start_date=None,
        end_date=None,
        status=None,
        hours=None,
        timesheet_id=None,
        timesheet_lines=None,
        updated_date_utc=None,
        validation_errors=None,
    ):  # noqa: E501
        """Timesheet - a model defined in OpenAPI"""  # noqa: E501

        self._employee_id = None
        self._start_date = None
        self._end_date = None
        self._status = None
        self._hours = None
        self._timesheet_id = None
        self._timesheet_lines = None
        self._updated_date_utc = None
        self._validation_errors = None
        self.discriminator = None

        self.employee_id = employee_id
        self.start_date = start_date
        self.end_date = end_date
        if status is not None:
            self.status = status
        if hours is not None:
            self.hours = hours
        if timesheet_id is not None:
            self.timesheet_id = timesheet_id
        if timesheet_lines is not None:
            self.timesheet_lines = timesheet_lines
        if updated_date_utc is not None:
            self.updated_date_utc = updated_date_utc
        if validation_errors is not None:
            self.validation_errors = validation_errors

    @property
    def employee_id(self):
        """Gets the employee_id of this Timesheet.  # noqa: E501

        The Xero identifier for an employee  # noqa: E501

        :return: The employee_id of this Timesheet.  # noqa: E501
        :rtype: str
        """
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        """Sets the employee_id of this Timesheet.

        The Xero identifier for an employee  # noqa: E501

        :param employee_id: The employee_id of this Timesheet.  # noqa: E501
        :type: str
        """
        if employee_id is None:
            raise ValueError(
                "Invalid value for `employee_id`, must not be `None`"
            )  # noqa: E501

        self._employee_id = employee_id

    @property
    def start_date(self):
        """Gets the start_date of this Timesheet.  # noqa: E501

        Period start date (YYYY-MM-DD)  # noqa: E501

        :return: The start_date of this Timesheet.  # noqa: E501
        :rtype: date
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this Timesheet.

        Period start date (YYYY-MM-DD)  # noqa: E501

        :param start_date: The start_date of this Timesheet.  # noqa: E501
        :type: date
        """
        if start_date is None:
            raise ValueError(
                "Invalid value for `start_date`, must not be `None`"
            )  # noqa: E501

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this Timesheet.  # noqa: E501

        Period end date (YYYY-MM-DD)  # noqa: E501

        :return: The end_date of this Timesheet.  # noqa: E501
        :rtype: date
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this Timesheet.

        Period end date (YYYY-MM-DD)  # noqa: E501

        :param end_date: The end_date of this Timesheet.  # noqa: E501
        :type: date
        """
        if end_date is None:
            raise ValueError(
                "Invalid value for `end_date`, must not be `None`"
            )  # noqa: E501

        self._end_date = end_date

    @property
    def status(self):
        """Gets the status of this Timesheet.  # noqa: E501


        :return: The status of this Timesheet.  # noqa: E501
        :rtype: TimesheetStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Timesheet.


        :param status: The status of this Timesheet.  # noqa: E501
        :type: TimesheetStatus
        """

        self._status = status

    @property
    def hours(self):
        """Gets the hours of this Timesheet.  # noqa: E501

        Timesheet total hours  # noqa: E501

        :return: The hours of this Timesheet.  # noqa: E501
        :rtype: float
        """
        return self._hours

    @hours.setter
    def hours(self, hours):
        """Sets the hours of this Timesheet.

        Timesheet total hours  # noqa: E501

        :param hours: The hours of this Timesheet.  # noqa: E501
        :type: float
        """

        self._hours = hours

    @property
    def timesheet_id(self):
        """Gets the timesheet_id of this Timesheet.  # noqa: E501

        The Xero identifier for a Payroll Timesheet  # noqa: E501

        :return: The timesheet_id of this Timesheet.  # noqa: E501
        :rtype: str
        """
        return self._timesheet_id

    @timesheet_id.setter
    def timesheet_id(self, timesheet_id):
        """Sets the timesheet_id of this Timesheet.

        The Xero identifier for a Payroll Timesheet  # noqa: E501

        :param timesheet_id: The timesheet_id of this Timesheet.  # noqa: E501
        :type: str
        """

        self._timesheet_id = timesheet_id

    @property
    def timesheet_lines(self):
        """Gets the timesheet_lines of this Timesheet.  # noqa: E501


        :return: The timesheet_lines of this Timesheet.  # noqa: E501
        :rtype: list[TimesheetLine]
        """
        return self._timesheet_lines

    @timesheet_lines.setter
    def timesheet_lines(self, timesheet_lines):
        """Sets the timesheet_lines of this Timesheet.


        :param timesheet_lines: The timesheet_lines of this Timesheet.  # noqa: E501
        :type: list[TimesheetLine]
        """

        self._timesheet_lines = timesheet_lines

    @property
    def updated_date_utc(self):
        """Gets the updated_date_utc of this Timesheet.  # noqa: E501

        Last modified timestamp  # noqa: E501

        :return: The updated_date_utc of this Timesheet.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_date_utc

    @updated_date_utc.setter
    def updated_date_utc(self, updated_date_utc):
        """Sets the updated_date_utc of this Timesheet.

        Last modified timestamp  # noqa: E501

        :param updated_date_utc: The updated_date_utc of this Timesheet.  # noqa: E501
        :type: datetime
        """

        self._updated_date_utc = updated_date_utc

    @property
    def validation_errors(self):
        """Gets the validation_errors of this Timesheet.  # noqa: E501

        Displays array of validation error messages from the API  # noqa: E501

        :return: The validation_errors of this Timesheet.  # noqa: E501
        :rtype: list[ValidationError]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """Sets the validation_errors of this Timesheet.

        Displays array of validation error messages from the API  # noqa: E501

        :param validation_errors: The validation_errors of this Timesheet.  # noqa: E501
        :type: list[ValidationError]
        """

        self._validation_errors = validation_errors
