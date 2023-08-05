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


class PayRun(BaseModel):
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
        "payroll_calendar_id": "str",
        "pay_run_id": "str",
        "pay_run_period_start_date": "date[ms-format]",
        "pay_run_period_end_date": "date[ms-format]",
        "pay_run_status": "PayRunStatus",
        "payment_date": "date[ms-format]",
        "payslip_message": "str",
        "updated_date_utc": "datetime[ms-format]",
        "payslips": "list[PayslipSummary]",
        "wages": "float",
        "deductions": "float",
        "tax": "float",
        "super": "float",
        "reimbursement": "float",
        "net_pay": "float",
        "validation_errors": "list[ValidationError]",
    }

    attribute_map = {
        "payroll_calendar_id": "PayrollCalendarID",
        "pay_run_id": "PayRunID",
        "pay_run_period_start_date": "PayRunPeriodStartDate",
        "pay_run_period_end_date": "PayRunPeriodEndDate",
        "pay_run_status": "PayRunStatus",
        "payment_date": "PaymentDate",
        "payslip_message": "PayslipMessage",
        "updated_date_utc": "UpdatedDateUTC",
        "payslips": "Payslips",
        "wages": "Wages",
        "deductions": "Deductions",
        "tax": "Tax",
        "super": "Super",
        "reimbursement": "Reimbursement",
        "net_pay": "NetPay",
        "validation_errors": "ValidationErrors",
    }

    def __init__(
        self,
        payroll_calendar_id=None,
        pay_run_id=None,
        pay_run_period_start_date=None,
        pay_run_period_end_date=None,
        pay_run_status=None,
        payment_date=None,
        payslip_message=None,
        updated_date_utc=None,
        payslips=None,
        wages=None,
        deductions=None,
        tax=None,
        super=None,
        reimbursement=None,
        net_pay=None,
        validation_errors=None,
    ):  # noqa: E501
        """PayRun - a model defined in OpenAPI"""  # noqa: E501

        self._payroll_calendar_id = None
        self._pay_run_id = None
        self._pay_run_period_start_date = None
        self._pay_run_period_end_date = None
        self._pay_run_status = None
        self._payment_date = None
        self._payslip_message = None
        self._updated_date_utc = None
        self._payslips = None
        self._wages = None
        self._deductions = None
        self._tax = None
        self._super = None
        self._reimbursement = None
        self._net_pay = None
        self._validation_errors = None
        self.discriminator = None

        self.payroll_calendar_id = payroll_calendar_id
        if pay_run_id is not None:
            self.pay_run_id = pay_run_id
        if pay_run_period_start_date is not None:
            self.pay_run_period_start_date = pay_run_period_start_date
        if pay_run_period_end_date is not None:
            self.pay_run_period_end_date = pay_run_period_end_date
        if pay_run_status is not None:
            self.pay_run_status = pay_run_status
        if payment_date is not None:
            self.payment_date = payment_date
        if payslip_message is not None:
            self.payslip_message = payslip_message
        if updated_date_utc is not None:
            self.updated_date_utc = updated_date_utc
        if payslips is not None:
            self.payslips = payslips
        if wages is not None:
            self.wages = wages
        if deductions is not None:
            self.deductions = deductions
        if tax is not None:
            self.tax = tax
        if super is not None:
            self.super = super
        if reimbursement is not None:
            self.reimbursement = reimbursement
        if net_pay is not None:
            self.net_pay = net_pay
        if validation_errors is not None:
            self.validation_errors = validation_errors

    @property
    def payroll_calendar_id(self):
        """Gets the payroll_calendar_id of this PayRun.  # noqa: E501

        Xero identifier for pay run  # noqa: E501

        :return: The payroll_calendar_id of this PayRun.  # noqa: E501
        :rtype: str
        """
        return self._payroll_calendar_id

    @payroll_calendar_id.setter
    def payroll_calendar_id(self, payroll_calendar_id):
        """Sets the payroll_calendar_id of this PayRun.

        Xero identifier for pay run  # noqa: E501

        :param payroll_calendar_id: The payroll_calendar_id of this PayRun.  # noqa: E501
        :type: str
        """
        if payroll_calendar_id is None:
            raise ValueError(
                "Invalid value for `payroll_calendar_id`, must not be `None`"
            )  # noqa: E501

        self._payroll_calendar_id = payroll_calendar_id

    @property
    def pay_run_id(self):
        """Gets the pay_run_id of this PayRun.  # noqa: E501

        Xero identifier for pay run  # noqa: E501

        :return: The pay_run_id of this PayRun.  # noqa: E501
        :rtype: str
        """
        return self._pay_run_id

    @pay_run_id.setter
    def pay_run_id(self, pay_run_id):
        """Sets the pay_run_id of this PayRun.

        Xero identifier for pay run  # noqa: E501

        :param pay_run_id: The pay_run_id of this PayRun.  # noqa: E501
        :type: str
        """

        self._pay_run_id = pay_run_id

    @property
    def pay_run_period_start_date(self):
        """Gets the pay_run_period_start_date of this PayRun.  # noqa: E501

        Period Start Date for the PayRun (YYYY-MM-DD)  # noqa: E501

        :return: The pay_run_period_start_date of this PayRun.  # noqa: E501
        :rtype: date
        """
        return self._pay_run_period_start_date

    @pay_run_period_start_date.setter
    def pay_run_period_start_date(self, pay_run_period_start_date):
        """Sets the pay_run_period_start_date of this PayRun.

        Period Start Date for the PayRun (YYYY-MM-DD)  # noqa: E501

        :param pay_run_period_start_date: The pay_run_period_start_date of this PayRun.  # noqa: E501
        :type: date
        """

        self._pay_run_period_start_date = pay_run_period_start_date

    @property
    def pay_run_period_end_date(self):
        """Gets the pay_run_period_end_date of this PayRun.  # noqa: E501

        Period End Date for the PayRun (YYYY-MM-DD)  # noqa: E501

        :return: The pay_run_period_end_date of this PayRun.  # noqa: E501
        :rtype: date
        """
        return self._pay_run_period_end_date

    @pay_run_period_end_date.setter
    def pay_run_period_end_date(self, pay_run_period_end_date):
        """Sets the pay_run_period_end_date of this PayRun.

        Period End Date for the PayRun (YYYY-MM-DD)  # noqa: E501

        :param pay_run_period_end_date: The pay_run_period_end_date of this PayRun.  # noqa: E501
        :type: date
        """

        self._pay_run_period_end_date = pay_run_period_end_date

    @property
    def pay_run_status(self):
        """Gets the pay_run_status of this PayRun.  # noqa: E501


        :return: The pay_run_status of this PayRun.  # noqa: E501
        :rtype: PayRunStatus
        """
        return self._pay_run_status

    @pay_run_status.setter
    def pay_run_status(self, pay_run_status):
        """Sets the pay_run_status of this PayRun.


        :param pay_run_status: The pay_run_status of this PayRun.  # noqa: E501
        :type: PayRunStatus
        """

        self._pay_run_status = pay_run_status

    @property
    def payment_date(self):
        """Gets the payment_date of this PayRun.  # noqa: E501

        Payment Date for the PayRun (YYYY-MM-DD)  # noqa: E501

        :return: The payment_date of this PayRun.  # noqa: E501
        :rtype: date
        """
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        """Sets the payment_date of this PayRun.

        Payment Date for the PayRun (YYYY-MM-DD)  # noqa: E501

        :param payment_date: The payment_date of this PayRun.  # noqa: E501
        :type: date
        """

        self._payment_date = payment_date

    @property
    def payslip_message(self):
        """Gets the payslip_message of this PayRun.  # noqa: E501

        Payslip message for the PayRun  # noqa: E501

        :return: The payslip_message of this PayRun.  # noqa: E501
        :rtype: str
        """
        return self._payslip_message

    @payslip_message.setter
    def payslip_message(self, payslip_message):
        """Sets the payslip_message of this PayRun.

        Payslip message for the PayRun  # noqa: E501

        :param payslip_message: The payslip_message of this PayRun.  # noqa: E501
        :type: str
        """

        self._payslip_message = payslip_message

    @property
    def updated_date_utc(self):
        """Gets the updated_date_utc of this PayRun.  # noqa: E501

        Last modified timestamp  # noqa: E501

        :return: The updated_date_utc of this PayRun.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_date_utc

    @updated_date_utc.setter
    def updated_date_utc(self, updated_date_utc):
        """Sets the updated_date_utc of this PayRun.

        Last modified timestamp  # noqa: E501

        :param updated_date_utc: The updated_date_utc of this PayRun.  # noqa: E501
        :type: datetime
        """

        self._updated_date_utc = updated_date_utc

    @property
    def payslips(self):
        """Gets the payslips of this PayRun.  # noqa: E501

        The payslips in the payrun  # noqa: E501

        :return: The payslips of this PayRun.  # noqa: E501
        :rtype: list[PayslipSummary]
        """
        return self._payslips

    @payslips.setter
    def payslips(self, payslips):
        """Sets the payslips of this PayRun.

        The payslips in the payrun  # noqa: E501

        :param payslips: The payslips of this PayRun.  # noqa: E501
        :type: list[PayslipSummary]
        """

        self._payslips = payslips

    @property
    def wages(self):
        """Gets the wages of this PayRun.  # noqa: E501

        The total Wages for the Payrun  # noqa: E501

        :return: The wages of this PayRun.  # noqa: E501
        :rtype: float
        """
        return self._wages

    @wages.setter
    def wages(self, wages):
        """Sets the wages of this PayRun.

        The total Wages for the Payrun  # noqa: E501

        :param wages: The wages of this PayRun.  # noqa: E501
        :type: float
        """

        self._wages = wages

    @property
    def deductions(self):
        """Gets the deductions of this PayRun.  # noqa: E501

        The total Deductions for the Payrun  # noqa: E501

        :return: The deductions of this PayRun.  # noqa: E501
        :rtype: float
        """
        return self._deductions

    @deductions.setter
    def deductions(self, deductions):
        """Sets the deductions of this PayRun.

        The total Deductions for the Payrun  # noqa: E501

        :param deductions: The deductions of this PayRun.  # noqa: E501
        :type: float
        """

        self._deductions = deductions

    @property
    def tax(self):
        """Gets the tax of this PayRun.  # noqa: E501

        The total Tax for the Payrun  # noqa: E501

        :return: The tax of this PayRun.  # noqa: E501
        :rtype: float
        """
        return self._tax

    @tax.setter
    def tax(self, tax):
        """Sets the tax of this PayRun.

        The total Tax for the Payrun  # noqa: E501

        :param tax: The tax of this PayRun.  # noqa: E501
        :type: float
        """

        self._tax = tax

    @property
    def super(self):
        """Gets the super of this PayRun.  # noqa: E501

        The total Super for the Payrun  # noqa: E501

        :return: The super of this PayRun.  # noqa: E501
        :rtype: float
        """
        return self._super

    @super.setter
    def super(self, super):
        """Sets the super of this PayRun.

        The total Super for the Payrun  # noqa: E501

        :param super: The super of this PayRun.  # noqa: E501
        :type: float
        """

        self._super = super

    @property
    def reimbursement(self):
        """Gets the reimbursement of this PayRun.  # noqa: E501

        The total Reimbursements for the Payrun  # noqa: E501

        :return: The reimbursement of this PayRun.  # noqa: E501
        :rtype: float
        """
        return self._reimbursement

    @reimbursement.setter
    def reimbursement(self, reimbursement):
        """Sets the reimbursement of this PayRun.

        The total Reimbursements for the Payrun  # noqa: E501

        :param reimbursement: The reimbursement of this PayRun.  # noqa: E501
        :type: float
        """

        self._reimbursement = reimbursement

    @property
    def net_pay(self):
        """Gets the net_pay of this PayRun.  # noqa: E501

        The total NetPay for the Payrun  # noqa: E501

        :return: The net_pay of this PayRun.  # noqa: E501
        :rtype: float
        """
        return self._net_pay

    @net_pay.setter
    def net_pay(self, net_pay):
        """Sets the net_pay of this PayRun.

        The total NetPay for the Payrun  # noqa: E501

        :param net_pay: The net_pay of this PayRun.  # noqa: E501
        :type: float
        """

        self._net_pay = net_pay

    @property
    def validation_errors(self):
        """Gets the validation_errors of this PayRun.  # noqa: E501

        Displays array of validation error messages from the API  # noqa: E501

        :return: The validation_errors of this PayRun.  # noqa: E501
        :rtype: list[ValidationError]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """Sets the validation_errors of this PayRun.

        Displays array of validation error messages from the API  # noqa: E501

        :param validation_errors: The validation_errors of this PayRun.  # noqa: E501
        :type: list[ValidationError]
        """

        self._validation_errors = validation_errors
