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
    Type = ma.fields.Str(
        validate=ma.validate.OneOf(('Source',))
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
    nodes = ma.fields.List(
        ma.fields.Nested(InputNode),
        required=True
    )
    links = ma.fields.List(
        ma.fields.Nested(InputLink),
        required=True
    )
