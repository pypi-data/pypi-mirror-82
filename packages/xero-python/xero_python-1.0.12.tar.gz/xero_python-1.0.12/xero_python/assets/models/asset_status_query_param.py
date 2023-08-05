# coding: utf-8

"""
    Xero Assets API

    This is the Xero Assets API  # noqa: E501

    OpenAPI spec version: 2.3.4
    Contact: api@xero.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401

from enum import Enum


class AssetStatusQueryParam(Enum):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    allowed enum values
    """

    DRAFT = "DRAFT"
    REGISTERED = "REGISTERED"
    DISPOSED = "DISPOSED"
