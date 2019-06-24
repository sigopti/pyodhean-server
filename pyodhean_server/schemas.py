"""PyODHeaN server application schemas

This module defines schema used to deserialize and validate API inputs
"""
# pylint: disable=missing-docstring

import marshmallow as ma


class InputNode(ma.Schema):
    id = ma.fields.Tuple(
        (ma.fields.Float, ma.fields.Float),
        required=True,
    )
    kWh = ma.fields.Float(
        required=True
    )
    tot_kWh = ma.fields.Float(
        required=True
    )


class InputProductionNode(InputNode):
    """Production node"""


class InputConsumptionNode(InputNode):
    """Consumption node"""
    kW = ma.fields.Float(
        required=True
    )
    Tin = ma.fields.Float(
        required=True
    )
    Tout = ma.fields.Float(
        required=True
    )


class InputNodes(ma.Schema):
    production = ma.fields.List(
        ma.fields.Nested(InputProductionNode),
        required=True
    )
    consumption = ma.fields.List(
        ma.fields.Nested(InputConsumptionNode),
        required=True
    )


class InputLink(ma.Schema):
    Length = ma.fields.Float(
        required=True
    )
    source = ma.fields.Tuple(
        (ma.fields.Float, ma.fields.Float),
        required=True,
    )
    target = ma.fields.Tuple(
        (ma.fields.Float, ma.fields.Float),
        required=True,
    )


class InputSchema(ma.Schema):
    nodes = ma.fields.Nested(
        InputNodes,
        required=True
    )
    links = ma.fields.List(
        ma.fields.Nested(InputLink),
        required=True
    )
