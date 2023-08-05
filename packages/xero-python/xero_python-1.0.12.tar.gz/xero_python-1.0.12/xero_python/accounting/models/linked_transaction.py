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


class LinkedTransaction(BaseModel):
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
        "source_transaction_id": "str",
        "source_line_item_id": "str",
        "contact_id": "str",
        "target_transaction_id": "str",
        "target_line_item_id": "str",
        "linked_transaction_id": "str",
        "status": "str",
        "type": "str",
        "updated_date_utc": "datetime[ms-format]",
        "source_transaction_type_code": "str",
        "validation_errors": "list[ValidationError]",
    }

    attribute_map = {
        "source_transaction_id": "SourceTransactionID",
        "source_line_item_id": "SourceLineItemID",
        "contact_id": "ContactID",
        "target_transaction_id": "TargetTransactionID",
        "target_line_item_id": "TargetLineItemID",
        "linked_transaction_id": "LinkedTransactionID",
        "status": "Status",
        "type": "Type",
        "updated_date_utc": "UpdatedDateUTC",
        "source_transaction_type_code": "SourceTransactionTypeCode",
        "validation_errors": "ValidationErrors",
    }

    def __init__(
        self,
        source_transaction_id=None,
        source_line_item_id=None,
        contact_id=None,
        target_transaction_id=None,
        target_line_item_id=None,
        linked_transaction_id=None,
        status=None,
        type=None,
        updated_date_utc=None,
        source_transaction_type_code=None,
        validation_errors=None,
    ):  # noqa: E501
        """LinkedTransaction - a model defined in OpenAPI"""  # noqa: E501

        self._source_transaction_id = None
        self._source_line_item_id = None
        self._contact_id = None
        self._target_transaction_id = None
        self._target_line_item_id = None
        self._linked_transaction_id = None
        self._status = None
        self._type = None
        self._updated_date_utc = None
        self._source_transaction_type_code = None
        self._validation_errors = None
        self.discriminator = None

        if source_transaction_id is not None:
            self.source_transaction_id = source_transaction_id
        if source_line_item_id is not None:
            self.source_line_item_id = source_line_item_id
        if contact_id is not None:
            self.contact_id = contact_id
        if target_transaction_id is not None:
            self.target_transaction_id = target_transaction_id
        if target_line_item_id is not None:
            self.target_line_item_id = target_line_item_id
        if linked_transaction_id is not None:
            self.linked_transaction_id = linked_transaction_id
        if status is not None:
            self.status = status
        if type is not None:
            self.type = type
        if updated_date_utc is not None:
            self.updated_date_utc = updated_date_utc
        if source_transaction_type_code is not None:
            self.source_transaction_type_code = source_transaction_type_code
        if validation_errors is not None:
            self.validation_errors = validation_errors

    @property
    def source_transaction_id(self):
        """Gets the source_transaction_id of this LinkedTransaction.  # noqa: E501

        Filter by the SourceTransactionID. Get all the linked transactions created from a particular ACCPAY invoice  # noqa: E501

        :return: The source_transaction_id of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._source_transaction_id

    @source_transaction_id.setter
    def source_transaction_id(self, source_transaction_id):
        """Sets the source_transaction_id of this LinkedTransaction.

        Filter by the SourceTransactionID. Get all the linked transactions created from a particular ACCPAY invoice  # noqa: E501

        :param source_transaction_id: The source_transaction_id of this LinkedTransaction.  # noqa: E501
        :type: str
        """

        self._source_transaction_id = source_transaction_id

    @property
    def source_line_item_id(self):
        """Gets the source_line_item_id of this LinkedTransaction.  # noqa: E501

        The line item identifier from the source transaction.  # noqa: E501

        :return: The source_line_item_id of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._source_line_item_id

    @source_line_item_id.setter
    def source_line_item_id(self, source_line_item_id):
        """Sets the source_line_item_id of this LinkedTransaction.

        The line item identifier from the source transaction.  # noqa: E501

        :param source_line_item_id: The source_line_item_id of this LinkedTransaction.  # noqa: E501
        :type: str
        """

        self._source_line_item_id = source_line_item_id

    @property
    def contact_id(self):
        """Gets the contact_id of this LinkedTransaction.  # noqa: E501

        Filter by the combination of ContactID and Status. Get all the linked transactions that have been assigned to a particular customer and have a particular status e.g. GET /LinkedTransactions?ContactID=4bb34b03-3378-4bb2-a0ed-6345abf3224e&Status=APPROVED.  # noqa: E501

        :return: The contact_id of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._contact_id

    @contact_id.setter
    def contact_id(self, contact_id):
        """Sets the contact_id of this LinkedTransaction.

        Filter by the combination of ContactID and Status. Get all the linked transactions that have been assigned to a particular customer and have a particular status e.g. GET /LinkedTransactions?ContactID=4bb34b03-3378-4bb2-a0ed-6345abf3224e&Status=APPROVED.  # noqa: E501

        :param contact_id: The contact_id of this LinkedTransaction.  # noqa: E501
        :type: str
        """

        self._contact_id = contact_id

    @property
    def target_transaction_id(self):
        """Gets the target_transaction_id of this LinkedTransaction.  # noqa: E501

        Filter by the TargetTransactionID. Get all the linked transactions  allocated to a particular ACCREC invoice  # noqa: E501

        :return: The target_transaction_id of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._target_transaction_id

    @target_transaction_id.setter
    def target_transaction_id(self, target_transaction_id):
        """Sets the target_transaction_id of this LinkedTransaction.

        Filter by the TargetTransactionID. Get all the linked transactions  allocated to a particular ACCREC invoice  # noqa: E501

        :param target_transaction_id: The target_transaction_id of this LinkedTransaction.  # noqa: E501
        :type: str
        """

        self._target_transaction_id = target_transaction_id

    @property
    def target_line_item_id(self):
        """Gets the target_line_item_id of this LinkedTransaction.  # noqa: E501

        The line item identifier from the target transaction. It is possible  to link multiple billable expenses to the same TargetLineItemID.  # noqa: E501

        :return: The target_line_item_id of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._target_line_item_id

    @target_line_item_id.setter
    def target_line_item_id(self, target_line_item_id):
        """Sets the target_line_item_id of this LinkedTransaction.

        The line item identifier from the target transaction. It is possible  to link multiple billable expenses to the same TargetLineItemID.  # noqa: E501

        :param target_line_item_id: The target_line_item_id of this LinkedTransaction.  # noqa: E501
        :type: str
        """

        self._target_line_item_id = target_line_item_id

    @property
    def linked_transaction_id(self):
        """Gets the linked_transaction_id of this LinkedTransaction.  # noqa: E501

        The Xero identifier for an Linked Transaction e.g./LinkedTransactions/297c2dc5-cc47-4afd-8ec8-74990b8761e9  # noqa: E501

        :return: The linked_transaction_id of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._linked_transaction_id

    @linked_transaction_id.setter
    def linked_transaction_id(self, linked_transaction_id):
        """Sets the linked_transaction_id of this LinkedTransaction.

        The Xero identifier for an Linked Transaction e.g./LinkedTransactions/297c2dc5-cc47-4afd-8ec8-74990b8761e9  # noqa: E501

        :param linked_transaction_id: The linked_transaction_id of this LinkedTransaction.  # noqa: E501
        :type: str
        """

        self._linked_transaction_id = linked_transaction_id

    @property
    def status(self):
        """Gets the status of this LinkedTransaction.  # noqa: E501

        Filter by the combination of ContactID and Status. Get all the linked transactions that have been assigned to a particular customer and have a particular status e.g. GET /LinkedTransactions?ContactID=4bb34b03-3378-4bb2-a0ed-6345abf3224e&Status=APPROVED.  # noqa: E501

        :return: The status of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this LinkedTransaction.

        Filter by the combination of ContactID and Status. Get all the linked transactions that have been assigned to a particular customer and have a particular status e.g. GET /LinkedTransactions?ContactID=4bb34b03-3378-4bb2-a0ed-6345abf3224e&Status=APPROVED.  # noqa: E501

        :param status: The status of this LinkedTransaction.  # noqa: E501
        :type: str
        """
        allowed_values = [
            "APPROVED",
            "DRAFT",
            "ONDRAFT",
            "BILLED",
            "VOIDED",
            "None",
        ]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}".format(  # noqa: E501
                    status, allowed_values
                )
            )

        self._status = status

    @property
    def type(self):
        """Gets the type of this LinkedTransaction.  # noqa: E501

        This will always be BILLABLEEXPENSE. More types may be added in future.  # noqa: E501

        :return: The type of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this LinkedTransaction.

        This will always be BILLABLEEXPENSE. More types may be added in future.  # noqa: E501

        :param type: The type of this LinkedTransaction.  # noqa: E501
        :type: str
        """
        allowed_values = ["BILLABLEEXPENSE", "None"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}".format(  # noqa: E501
                    type, allowed_values
                )
            )

        self._type = type

    @property
    def updated_date_utc(self):
        """Gets the updated_date_utc of this LinkedTransaction.  # noqa: E501

        The last modified date in UTC format  # noqa: E501

        :return: The updated_date_utc of this LinkedTransaction.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_date_utc

    @updated_date_utc.setter
    def updated_date_utc(self, updated_date_utc):
        """Sets the updated_date_utc of this LinkedTransaction.

        The last modified date in UTC format  # noqa: E501

        :param updated_date_utc: The updated_date_utc of this LinkedTransaction.  # noqa: E501
        :type: datetime
        """

        self._updated_date_utc = updated_date_utc

    @property
    def source_transaction_type_code(self):
        """Gets the source_transaction_type_code of this LinkedTransaction.  # noqa: E501

        The Type of the source tranasction. This will be ACCPAY if the linked transaction was created from an invoice and SPEND if it was created from a bank transaction.  # noqa: E501

        :return: The source_transaction_type_code of this LinkedTransaction.  # noqa: E501
        :rtype: str
        """
        return self._source_transaction_type_code

    @source_transaction_type_code.setter
    def source_transaction_type_code(self, source_transaction_type_code):
        """Sets the source_transaction_type_code of this LinkedTransaction.

        The Type of the source tranasction. This will be ACCPAY if the linked transaction was created from an invoice and SPEND if it was created from a bank transaction.  # noqa: E501

        :param source_transaction_type_code: The source_transaction_type_code of this LinkedTransaction.  # noqa: E501
        :type: str
        """
        allowed_values = ["ACCPAY", "SPEND", "None"]  # noqa: E501
        if source_transaction_type_code not in allowed_values:
            raise ValueError(
                "Invalid value for `source_transaction_type_code` ({0}), must be one of {1}".format(  # noqa: E501
                    source_transaction_type_code, allowed_values
                )
            )

        self._source_transaction_type_code = source_transaction_type_code

    @property
    def validation_errors(self):
        """Gets the validation_errors of this LinkedTransaction.  # noqa: E501

        Displays array of validation error messages from the API  # noqa: E501

        :return: The validation_errors of this LinkedTransaction.  # noqa: E501
        :rtype: list[ValidationError]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """Sets the validation_errors of this LinkedTransaction.

        Displays array of validation error messages from the API  # noqa: E501

        :param validation_errors: The validation_errors of this LinkedTransaction.  # noqa: E501
        :type: list[ValidationError]
        """

        self._validation_errors = validation_errors
