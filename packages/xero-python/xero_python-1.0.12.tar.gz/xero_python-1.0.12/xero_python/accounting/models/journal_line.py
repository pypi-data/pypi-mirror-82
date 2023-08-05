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


class JournalLine(BaseModel):
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
        "journal_line_id": "str",
        "account_id": "str",
        "account_code": "str",
        "account_type": "AccountType",
        "account_name": "str",
        "description": "str",
        "net_amount": "float",
        "gross_amount": "float",
        "tax_amount": "float",
        "tax_type": "str",
        "tax_name": "str",
        "tracking_categories": "list[TrackingCategory]",
    }

    attribute_map = {
        "journal_line_id": "JournalLineID",
        "account_id": "AccountID",
        "account_code": "AccountCode",
        "account_type": "AccountType",
        "account_name": "AccountName",
        "description": "Description",
        "net_amount": "NetAmount",
        "gross_amount": "GrossAmount",
        "tax_amount": "TaxAmount",
        "tax_type": "TaxType",
        "tax_name": "TaxName",
        "tracking_categories": "TrackingCategories",
    }

    def __init__(
        self,
        journal_line_id=None,
        account_id=None,
        account_code=None,
        account_type=None,
        account_name=None,
        description=None,
        net_amount=None,
        gross_amount=None,
        tax_amount=None,
        tax_type=None,
        tax_name=None,
        tracking_categories=None,
    ):  # noqa: E501
        """JournalLine - a model defined in OpenAPI"""  # noqa: E501

        self._journal_line_id = None
        self._account_id = None
        self._account_code = None
        self._account_type = None
        self._account_name = None
        self._description = None
        self._net_amount = None
        self._gross_amount = None
        self._tax_amount = None
        self._tax_type = None
        self._tax_name = None
        self._tracking_categories = None
        self.discriminator = None

        if journal_line_id is not None:
            self.journal_line_id = journal_line_id
        if account_id is not None:
            self.account_id = account_id
        if account_code is not None:
            self.account_code = account_code
        if account_type is not None:
            self.account_type = account_type
        if account_name is not None:
            self.account_name = account_name
        if description is not None:
            self.description = description
        if net_amount is not None:
            self.net_amount = net_amount
        if gross_amount is not None:
            self.gross_amount = gross_amount
        if tax_amount is not None:
            self.tax_amount = tax_amount
        if tax_type is not None:
            self.tax_type = tax_type
        if tax_name is not None:
            self.tax_name = tax_name
        if tracking_categories is not None:
            self.tracking_categories = tracking_categories

    @property
    def journal_line_id(self):
        """Gets the journal_line_id of this JournalLine.  # noqa: E501

        Xero identifier for Journal  # noqa: E501

        :return: The journal_line_id of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._journal_line_id

    @journal_line_id.setter
    def journal_line_id(self, journal_line_id):
        """Sets the journal_line_id of this JournalLine.

        Xero identifier for Journal  # noqa: E501

        :param journal_line_id: The journal_line_id of this JournalLine.  # noqa: E501
        :type: str
        """

        self._journal_line_id = journal_line_id

    @property
    def account_id(self):
        """Gets the account_id of this JournalLine.  # noqa: E501

        See Accounts  # noqa: E501

        :return: The account_id of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this JournalLine.

        See Accounts  # noqa: E501

        :param account_id: The account_id of this JournalLine.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def account_code(self):
        """Gets the account_code of this JournalLine.  # noqa: E501

        See Accounts  # noqa: E501

        :return: The account_code of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._account_code

    @account_code.setter
    def account_code(self, account_code):
        """Sets the account_code of this JournalLine.

        See Accounts  # noqa: E501

        :param account_code: The account_code of this JournalLine.  # noqa: E501
        :type: str
        """

        self._account_code = account_code

    @property
    def account_type(self):
        """Gets the account_type of this JournalLine.  # noqa: E501


        :return: The account_type of this JournalLine.  # noqa: E501
        :rtype: AccountType
        """
        return self._account_type

    @account_type.setter
    def account_type(self, account_type):
        """Sets the account_type of this JournalLine.


        :param account_type: The account_type of this JournalLine.  # noqa: E501
        :type: AccountType
        """

        self._account_type = account_type

    @property
    def account_name(self):
        """Gets the account_name of this JournalLine.  # noqa: E501

        See AccountCodes  # noqa: E501

        :return: The account_name of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """Sets the account_name of this JournalLine.

        See AccountCodes  # noqa: E501

        :param account_name: The account_name of this JournalLine.  # noqa: E501
        :type: str
        """

        self._account_name = account_name

    @property
    def description(self):
        """Gets the description of this JournalLine.  # noqa: E501

        The description from the source transaction line item. Only returned if populated.  # noqa: E501

        :return: The description of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this JournalLine.

        The description from the source transaction line item. Only returned if populated.  # noqa: E501

        :param description: The description of this JournalLine.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def net_amount(self):
        """Gets the net_amount of this JournalLine.  # noqa: E501

        Net amount of journal line. This will be a positive value for a debit and negative for a credit  # noqa: E501

        :return: The net_amount of this JournalLine.  # noqa: E501
        :rtype: float
        """
        return self._net_amount

    @net_amount.setter
    def net_amount(self, net_amount):
        """Sets the net_amount of this JournalLine.

        Net amount of journal line. This will be a positive value for a debit and negative for a credit  # noqa: E501

        :param net_amount: The net_amount of this JournalLine.  # noqa: E501
        :type: float
        """

        self._net_amount = net_amount

    @property
    def gross_amount(self):
        """Gets the gross_amount of this JournalLine.  # noqa: E501

        Gross amount of journal line (NetAmount + TaxAmount).  # noqa: E501

        :return: The gross_amount of this JournalLine.  # noqa: E501
        :rtype: float
        """
        return self._gross_amount

    @gross_amount.setter
    def gross_amount(self, gross_amount):
        """Sets the gross_amount of this JournalLine.

        Gross amount of journal line (NetAmount + TaxAmount).  # noqa: E501

        :param gross_amount: The gross_amount of this JournalLine.  # noqa: E501
        :type: float
        """

        self._gross_amount = gross_amount

    @property
    def tax_amount(self):
        """Gets the tax_amount of this JournalLine.  # noqa: E501

        Total tax on a journal line  # noqa: E501

        :return: The tax_amount of this JournalLine.  # noqa: E501
        :rtype: float
        """
        return self._tax_amount

    @tax_amount.setter
    def tax_amount(self, tax_amount):
        """Sets the tax_amount of this JournalLine.

        Total tax on a journal line  # noqa: E501

        :param tax_amount: The tax_amount of this JournalLine.  # noqa: E501
        :type: float
        """

        self._tax_amount = tax_amount

    @property
    def tax_type(self):
        """Gets the tax_type of this JournalLine.  # noqa: E501

        The tax type from TaxRates  # noqa: E501

        :return: The tax_type of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._tax_type

    @tax_type.setter
    def tax_type(self, tax_type):
        """Sets the tax_type of this JournalLine.

        The tax type from TaxRates  # noqa: E501

        :param tax_type: The tax_type of this JournalLine.  # noqa: E501
        :type: str
        """

        self._tax_type = tax_type

    @property
    def tax_name(self):
        """Gets the tax_name of this JournalLine.  # noqa: E501

        see TaxRates  # noqa: E501

        :return: The tax_name of this JournalLine.  # noqa: E501
        :rtype: str
        """
        return self._tax_name

    @tax_name.setter
    def tax_name(self, tax_name):
        """Sets the tax_name of this JournalLine.

        see TaxRates  # noqa: E501

        :param tax_name: The tax_name of this JournalLine.  # noqa: E501
        :type: str
        """

        self._tax_name = tax_name

    @property
    def tracking_categories(self):
        """Gets the tracking_categories of this JournalLine.  # noqa: E501

        Optional Tracking Category – see Tracking. Any JournalLine can have a maximum of 2 <TrackingCategory> elements.  # noqa: E501

        :return: The tracking_categories of this JournalLine.  # noqa: E501
        :rtype: list[TrackingCategory]
        """
        return self._tracking_categories

    @tracking_categories.setter
    def tracking_categories(self, tracking_categories):
        """Sets the tracking_categories of this JournalLine.

        Optional Tracking Category – see Tracking. Any JournalLine can have a maximum of 2 <TrackingCategory> elements.  # noqa: E501

        :param tracking_categories: The tracking_categories of this JournalLine.  # noqa: E501
        :type: list[TrackingCategory]
        """

        self._tracking_categories = tracking_categories
