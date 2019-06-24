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


class InputProductionTechnologyNode(ma.Schema):
    efficiency = ma.fields.Float(
        required=True,
    )
    t_out_max = ma.fields.Float(
        required=True,
    )
    t_in_min = ma.fields.Float(
        required=True,
    )
    production_unitary_cost = ma.fields.Float(
        required=True,
    )
    energy_unitary_cost = ma.fields.Float(
        required=True,
    )
    energy_cost_inflation_rate = ma.fields.Float(
        required=True,
    )


class InputProductionNode(InputNode):
    """Production node"""
    technologies = ma.fields.Dict(
        ma.fields.String(),
        ma.fields.Nested(InputProductionTechnologyNode),
        required=True,
    )


class InputConsumptionNode(InputNode):
    """Consumption node"""
    kW = ma.fields.Float(
        required=True
    )
    t_in = ma.fields.Float(
        required=True
    )
    t_out = ma.fields.Float(
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
    length = ma.fields.Float(
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
