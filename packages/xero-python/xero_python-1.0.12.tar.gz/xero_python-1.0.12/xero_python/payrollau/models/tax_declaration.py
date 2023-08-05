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


class TaxDeclaration(BaseModel):
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
        "employment_basis": "EmploymentBasis",
        "tfn_exemption_type": "TFNExemptionType",
        "tax_file_number": "str",
        "australian_resident_for_tax_purposes": "bool",
        "residency_status": "ResidencyStatus",
        "tax_free_threshold_claimed": "bool",
        "tax_offset_estimated_amount": "float",
        "has_help_debt": "bool",
        "has_sfss_debt": "bool",
        "has_trade_support_loan_debt": "bool",
        "upward_variation_tax_withholding_amount": "float",
        "eligible_to_receive_leave_loading": "bool",
        "approved_withholding_variation_percentage": "float",
        "has_student_startup_loan": "bool",
        "updated_date_utc": "datetime[ms-format]",
    }

    attribute_map = {
        "employee_id": "EmployeeID",
        "employment_basis": "EmploymentBasis",
        "tfn_exemption_type": "TFNExemptionType",
        "tax_file_number": "TaxFileNumber",
        "australian_resident_for_tax_purposes": "AustralianResidentForTaxPurposes",
        "residency_status": "ResidencyStatus",
        "tax_free_threshold_claimed": "TaxFreeThresholdClaimed",
        "tax_offset_estimated_amount": "TaxOffsetEstimatedAmount",
        "has_help_debt": "HasHELPDebt",
        "has_sfss_debt": "HasSFSSDebt",
        "has_trade_support_loan_debt": "HasTradeSupportLoanDebt",
        "upward_variation_tax_withholding_amount": "UpwardVariationTaxWithholdingAmount",
        "eligible_to_receive_leave_loading": "EligibleToReceiveLeaveLoading",
        "approved_withholding_variation_percentage": "ApprovedWithholdingVariationPercentage",
        "has_student_startup_loan": "HasStudentStartupLoan",
        "updated_date_utc": "UpdatedDateUTC",
    }

    def __init__(
        self,
        employee_id=None,
        employment_basis=None,
        tfn_exemption_type=None,
        tax_file_number=None,
        australian_resident_for_tax_purposes=None,
        residency_status=None,
        tax_free_threshold_claimed=None,
        tax_offset_estimated_amount=None,
        has_help_debt=None,
        has_sfss_debt=None,
        has_trade_support_loan_debt=None,
        upward_variation_tax_withholding_amount=None,
        eligible_to_receive_leave_loading=None,
        approved_withholding_variation_percentage=None,
        has_student_startup_loan=None,
        updated_date_utc=None,
    ):  # noqa: E501
        """TaxDeclaration - a model defined in OpenAPI"""  # noqa: E501

        self._employee_id = None
        self._employment_basis = None
        self._tfn_exemption_type = None
        self._tax_file_number = None
        self._australian_resident_for_tax_purposes = None
        self._residency_status = None
        self._tax_free_threshold_claimed = None
        self._tax_offset_estimated_amount = None
        self._has_help_debt = None
        self._has_sfss_debt = None
        self._has_trade_support_loan_debt = None
        self._upward_variation_tax_withholding_amount = None
        self._eligible_to_receive_leave_loading = None
        self._approved_withholding_variation_percentage = None
        self._has_student_startup_loan = None
        self._updated_date_utc = None
        self.discriminator = None

        if employee_id is not None:
            self.employee_id = employee_id
        if employment_basis is not None:
            self.employment_basis = employment_basis
        if tfn_exemption_type is not None:
            self.tfn_exemption_type = tfn_exemption_type
        if tax_file_number is not None:
            self.tax_file_number = tax_file_number
        if australian_resident_for_tax_purposes is not None:
            self.australian_resident_for_tax_purposes = (
                australian_resident_for_tax_purposes
            )
        if residency_status is not None:
            self.residency_status = residency_status
        if tax_free_threshold_claimed is not None:
            self.tax_free_threshold_claimed = tax_free_threshold_claimed
        if tax_offset_estimated_amount is not None:
            self.tax_offset_estimated_amount = tax_offset_estimated_amount
        if has_help_debt is not None:
            self.has_help_debt = has_help_debt
        if has_sfss_debt is not None:
            self.has_sfss_debt = has_sfss_debt
        if has_trade_support_loan_debt is not None:
            self.has_trade_support_loan_debt = has_trade_support_loan_debt
        if upward_variation_tax_withholding_amount is not None:
            self.upward_variation_tax_withholding_amount = (
                upward_variation_tax_withholding_amount
            )
        if eligible_to_receive_leave_loading is not None:
            self.eligible_to_receive_leave_loading = eligible_to_receive_leave_loading
        if approved_withholding_variation_percentage is not None:
            self.approved_withholding_variation_percentage = (
                approved_withholding_variation_percentage
            )
        if has_student_startup_loan is not None:
            self.has_student_startup_loan = has_student_startup_loan
        if updated_date_utc is not None:
            self.updated_date_utc = updated_date_utc

    @property
    def employee_id(self):
        """Gets the employee_id of this TaxDeclaration.  # noqa: E501

        Address line 1 for employee home address  # noqa: E501

        :return: The employee_id of this TaxDeclaration.  # noqa: E501
        :rtype: str
        """
        return self._employee_id

    @employee_id.setter
    def employee_id(self, employee_id):
        """Sets the employee_id of this TaxDeclaration.

        Address line 1 for employee home address  # noqa: E501

        :param employee_id: The employee_id of this TaxDeclaration.  # noqa: E501
        :type: str
        """

        self._employee_id = employee_id

    @property
    def employment_basis(self):
        """Gets the employment_basis of this TaxDeclaration.  # noqa: E501


        :return: The employment_basis of this TaxDeclaration.  # noqa: E501
        :rtype: EmploymentBasis
        """
        return self._employment_basis

    @employment_basis.setter
    def employment_basis(self, employment_basis):
        """Sets the employment_basis of this TaxDeclaration.


        :param employment_basis: The employment_basis of this TaxDeclaration.  # noqa: E501
        :type: EmploymentBasis
        """

        self._employment_basis = employment_basis

    @property
    def tfn_exemption_type(self):
        """Gets the tfn_exemption_type of this TaxDeclaration.  # noqa: E501


        :return: The tfn_exemption_type of this TaxDeclaration.  # noqa: E501
        :rtype: TFNExemptionType
        """
        return self._tfn_exemption_type

    @tfn_exemption_type.setter
    def tfn_exemption_type(self, tfn_exemption_type):
        """Sets the tfn_exemption_type of this TaxDeclaration.


        :param tfn_exemption_type: The tfn_exemption_type of this TaxDeclaration.  # noqa: E501
        :type: TFNExemptionType
        """

        self._tfn_exemption_type = tfn_exemption_type

    @property
    def tax_file_number(self):
        """Gets the tax_file_number of this TaxDeclaration.  # noqa: E501

        The tax file number e.g 123123123.  # noqa: E501

        :return: The tax_file_number of this TaxDeclaration.  # noqa: E501
        :rtype: str
        """
        return self._tax_file_number

    @tax_file_number.setter
    def tax_file_number(self, tax_file_number):
        """Sets the tax_file_number of this TaxDeclaration.

        The tax file number e.g 123123123.  # noqa: E501

        :param tax_file_number: The tax_file_number of this TaxDeclaration.  # noqa: E501
        :type: str
        """

        self._tax_file_number = tax_file_number

    @property
    def australian_resident_for_tax_purposes(self):
        """Gets the australian_resident_for_tax_purposes of this TaxDeclaration.  # noqa: E501

        If the employee is Australian resident for tax purposes. e.g true or false  # noqa: E501

        :return: The australian_resident_for_tax_purposes of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._australian_resident_for_tax_purposes

    @australian_resident_for_tax_purposes.setter
    def australian_resident_for_tax_purposes(
        self, australian_resident_for_tax_purposes
    ):
        """Sets the australian_resident_for_tax_purposes of this TaxDeclaration.

        If the employee is Australian resident for tax purposes. e.g true or false  # noqa: E501

        :param australian_resident_for_tax_purposes: The australian_resident_for_tax_purposes of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._australian_resident_for_tax_purposes = (
            australian_resident_for_tax_purposes
        )

    @property
    def residency_status(self):
        """Gets the residency_status of this TaxDeclaration.  # noqa: E501


        :return: The residency_status of this TaxDeclaration.  # noqa: E501
        :rtype: ResidencyStatus
        """
        return self._residency_status

    @residency_status.setter
    def residency_status(self, residency_status):
        """Sets the residency_status of this TaxDeclaration.


        :param residency_status: The residency_status of this TaxDeclaration.  # noqa: E501
        :type: ResidencyStatus
        """

        self._residency_status = residency_status

    @property
    def tax_free_threshold_claimed(self):
        """Gets the tax_free_threshold_claimed of this TaxDeclaration.  # noqa: E501

        If tax free threshold claimed. e.g true or false  # noqa: E501

        :return: The tax_free_threshold_claimed of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._tax_free_threshold_claimed

    @tax_free_threshold_claimed.setter
    def tax_free_threshold_claimed(self, tax_free_threshold_claimed):
        """Sets the tax_free_threshold_claimed of this TaxDeclaration.

        If tax free threshold claimed. e.g true or false  # noqa: E501

        :param tax_free_threshold_claimed: The tax_free_threshold_claimed of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._tax_free_threshold_claimed = tax_free_threshold_claimed

    @property
    def tax_offset_estimated_amount(self):
        """Gets the tax_offset_estimated_amount of this TaxDeclaration.  # noqa: E501

        If has tax offset estimated then the tax offset estimated amount. e.g 100  # noqa: E501

        :return: The tax_offset_estimated_amount of this TaxDeclaration.  # noqa: E501
        :rtype: float
        """
        return self._tax_offset_estimated_amount

    @tax_offset_estimated_amount.setter
    def tax_offset_estimated_amount(self, tax_offset_estimated_amount):
        """Sets the tax_offset_estimated_amount of this TaxDeclaration.

        If has tax offset estimated then the tax offset estimated amount. e.g 100  # noqa: E501

        :param tax_offset_estimated_amount: The tax_offset_estimated_amount of this TaxDeclaration.  # noqa: E501
        :type: float
        """

        self._tax_offset_estimated_amount = tax_offset_estimated_amount

    @property
    def has_help_debt(self):
        """Gets the has_help_debt of this TaxDeclaration.  # noqa: E501

        If employee has HECS or HELP debt. e.g true or false  # noqa: E501

        :return: The has_help_debt of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._has_help_debt

    @has_help_debt.setter
    def has_help_debt(self, has_help_debt):
        """Sets the has_help_debt of this TaxDeclaration.

        If employee has HECS or HELP debt. e.g true or false  # noqa: E501

        :param has_help_debt: The has_help_debt of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._has_help_debt = has_help_debt

    @property
    def has_sfss_debt(self):
        """Gets the has_sfss_debt of this TaxDeclaration.  # noqa: E501

        If employee has financial supplement debt. e.g true or false  # noqa: E501

        :return: The has_sfss_debt of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._has_sfss_debt

    @has_sfss_debt.setter
    def has_sfss_debt(self, has_sfss_debt):
        """Sets the has_sfss_debt of this TaxDeclaration.

        If employee has financial supplement debt. e.g true or false  # noqa: E501

        :param has_sfss_debt: The has_sfss_debt of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._has_sfss_debt = has_sfss_debt

    @property
    def has_trade_support_loan_debt(self):
        """Gets the has_trade_support_loan_debt of this TaxDeclaration.  # noqa: E501

        If employee has trade support loan. e.g true or false  # noqa: E501

        :return: The has_trade_support_loan_debt of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._has_trade_support_loan_debt

    @has_trade_support_loan_debt.setter
    def has_trade_support_loan_debt(self, has_trade_support_loan_debt):
        """Sets the has_trade_support_loan_debt of this TaxDeclaration.

        If employee has trade support loan. e.g true or false  # noqa: E501

        :param has_trade_support_loan_debt: The has_trade_support_loan_debt of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._has_trade_support_loan_debt = has_trade_support_loan_debt

    @property
    def upward_variation_tax_withholding_amount(self):
        """Gets the upward_variation_tax_withholding_amount of this TaxDeclaration.  # noqa: E501

        If the employee has requested that additional tax be withheld each pay run. e.g 50  # noqa: E501

        :return: The upward_variation_tax_withholding_amount of this TaxDeclaration.  # noqa: E501
        :rtype: float
        """
        return self._upward_variation_tax_withholding_amount

    @upward_variation_tax_withholding_amount.setter
    def upward_variation_tax_withholding_amount(
        self, upward_variation_tax_withholding_amount
    ):
        """Sets the upward_variation_tax_withholding_amount of this TaxDeclaration.

        If the employee has requested that additional tax be withheld each pay run. e.g 50  # noqa: E501

        :param upward_variation_tax_withholding_amount: The upward_variation_tax_withholding_amount of this TaxDeclaration.  # noqa: E501
        :type: float
        """

        self._upward_variation_tax_withholding_amount = (
            upward_variation_tax_withholding_amount
        )

    @property
    def eligible_to_receive_leave_loading(self):
        """Gets the eligible_to_receive_leave_loading of this TaxDeclaration.  # noqa: E501

        If the employee is eligible to receive an additional percentage on top of ordinary earnings when they take leave (typically 17.5%). e.g true or false  # noqa: E501

        :return: The eligible_to_receive_leave_loading of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._eligible_to_receive_leave_loading

    @eligible_to_receive_leave_loading.setter
    def eligible_to_receive_leave_loading(self, eligible_to_receive_leave_loading):
        """Sets the eligible_to_receive_leave_loading of this TaxDeclaration.

        If the employee is eligible to receive an additional percentage on top of ordinary earnings when they take leave (typically 17.5%). e.g true or false  # noqa: E501

        :param eligible_to_receive_leave_loading: The eligible_to_receive_leave_loading of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._eligible_to_receive_leave_loading = eligible_to_receive_leave_loading

    @property
    def approved_withholding_variation_percentage(self):
        """Gets the approved_withholding_variation_percentage of this TaxDeclaration.  # noqa: E501

        If the employee has approved withholding variation. e.g (0 - 100)  # noqa: E501

        :return: The approved_withholding_variation_percentage of this TaxDeclaration.  # noqa: E501
        :rtype: float
        """
        return self._approved_withholding_variation_percentage

    @approved_withholding_variation_percentage.setter
    def approved_withholding_variation_percentage(
        self, approved_withholding_variation_percentage
    ):
        """Sets the approved_withholding_variation_percentage of this TaxDeclaration.

        If the employee has approved withholding variation. e.g (0 - 100)  # noqa: E501

        :param approved_withholding_variation_percentage: The approved_withholding_variation_percentage of this TaxDeclaration.  # noqa: E501
        :type: float
        """

        self._approved_withholding_variation_percentage = (
            approved_withholding_variation_percentage
        )

    @property
    def has_student_startup_loan(self):
        """Gets the has_student_startup_loan of this TaxDeclaration.  # noqa: E501

        If the employee is eligible for student startup loan rules  # noqa: E501

        :return: The has_student_startup_loan of this TaxDeclaration.  # noqa: E501
        :rtype: bool
        """
        return self._has_student_startup_loan

    @has_student_startup_loan.setter
    def has_student_startup_loan(self, has_student_startup_loan):
        """Sets the has_student_startup_loan of this TaxDeclaration.

        If the employee is eligible for student startup loan rules  # noqa: E501

        :param has_student_startup_loan: The has_student_startup_loan of this TaxDeclaration.  # noqa: E501
        :type: bool
        """

        self._has_student_startup_loan = has_student_startup_loan

    @property
    def updated_date_utc(self):
        """Gets the updated_date_utc of this TaxDeclaration.  # noqa: E501

        Last modified timestamp  # noqa: E501

        :return: The updated_date_utc of this TaxDeclaration.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_date_utc

    @updated_date_utc.setter
    def updated_date_utc(self, updated_date_utc):
        """Sets the updated_date_utc of this TaxDeclaration.

        Last modified timestamp  # noqa: E501

        :param updated_date_utc: The updated_date_utc of this TaxDeclaration.  # noqa: E501
        :type: datetime
        """

        self._updated_date_utc = updated_date_utc
