"""Solver module schemas"""
# pylint: disable=missing-docstring

import marshmallow as ma

from .task import CELERY_STATUSES_MAPPING, SOLVER_STATUSES_MAPPING


class Schema(ma.Schema):
    class Meta:
        ordered = True


class NodeSchema(Schema):
    id = ma.fields.Tuple(
        (ma.fields.Float, ma.fields.Float),
        required=True,
    )


class LinkSchema(Schema):
    source = ma.fields.Tuple(
        (ma.fields.Float, ma.fields.Float),
        required=True,
    )
    target = ma.fields.Tuple(
        (ma.fields.Float, ma.fields.Float),
        required=True,
    )


class InputProductionTechnologySchema(Schema):
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


class InputProductionNodeSchema(NodeSchema):
    technologies = ma.fields.Dict(
        ma.fields.String(),
        ma.fields.Nested(InputProductionTechnologySchema),
        required=True,
    )


class InputConsumptionNodeSchema(NodeSchema):
    kW = ma.fields.Float(
        required=True
    )
    t_in = ma.fields.Float(
        required=True
    )
    t_out = ma.fields.Float(
        required=True
    )


class InputNodesSchema(Schema):
    production = ma.fields.List(
        ma.fields.Nested(InputProductionNodeSchema),
        required=True
    )
    consumption = ma.fields.List(
        ma.fields.Nested(InputConsumptionNodeSchema),
        required=True
    )


class InputLinkSchema(LinkSchema):
    length = ma.fields.Float(
        required=True
    )


class SolverInputSchema(Schema):
    nodes = ma.fields.Nested(
        InputNodesSchema,
        required=True
    )
    links = ma.fields.List(
        ma.fields.Nested(InputLinkSchema),
        required=True
    )


class OutputProductionTechnologySchema(Schema):
    flow_rate = ma.fields.Float(
        required=True
    )
    power = ma.fields.Float(
        required=True
    )
    t_supply = ma.fields.Float(
        required=True
    )
    t_return = ma.fields.Float(
        required=True
    )


class OutputProductionNodeSchema(NodeSchema):
    technologies = ma.fields.Dict(
        ma.fields.String(),
        ma.fields.Nested(OutputProductionTechnologySchema),
        required=True,
    )
    t_supply = ma.fields.Float(
        required=True
    )
    t_return = ma.fields.Float(
        required=True
    )
    pump_pressure = ma.fields.Float(
        required=True
    )
    flow_rate = ma.fields.Float(
        required=True
    )


class OutputConsumptionNodeSchema(NodeSchema):
    flow_rate_before_exchanger = ma.fields.Float(
        required=True
    )
    flow_rate_after_exchanger = ma.fields.Float(
        required=True
    )
    flow_rate_in_exchanger = ma.fields.Float(
        required=True
    )
    exchanger_power = ma.fields.Float(
        required=True
    )
    exchanger_surface = ma.fields.Float(
        required=True
    )
    exchanger_t_in = ma.fields.Float(
        required=True
    )
    exchanger_t_out = ma.fields.Float(
        required=True
    )
    exchanger_t_supply = ma.fields.Float(
        required=True
    )
    exchanger_t_return = ma.fields.Float(
        required=True
    )
    exchanger_DTLM = ma.fields.Float(
        required=True
    )
    exchanger_delta_t_cold = ma.fields.Float(
        required=True
    )
    exchanger_delta_t_hot = ma.fields.Float(
        required=True
    )


class OutputNodesSchema(Schema):
    production = ma.fields.List(
        ma.fields.Nested(OutputProductionNodeSchema),
        required=True
    )
    consumption = ma.fields.List(
        ma.fields.Nested(OutputConsumptionNodeSchema),
        required=True
    )


class OutputLinkSchema(LinkSchema):
    diameter_int = ma.fields.Float(
        required=True
    )
    diameter_out = ma.fields.Float(
        required=True
    )
    flow_rate = ma.fields.Float(
        required=True
    )
    speed = ma.fields.Float(
        required=True
    )
    t_return_in = ma.fields.Float(
        required=True
    )
    t_return_out = ma.fields.Float(
        required=True
    )
    t_supply_in = ma.fields.Float(
        required=True
    )
    t_supply_out = ma.fields.Float(
        required=True
    )


class OutputGlobalIndicatorsSchema(Schema):
    production_intallation_cost = ma.fields.Float(
        required=True
    )
    exchangers_installation_cost = ma.fields.Float(
        required=True
    )
    network_cost = ma.fields.Float(
        required=True
    )
    trenches_cost = ma.fields.Float(
        required=True
    )
    pipes_cost = ma.fields.Float(
        required=True
    )
    network_length = ma.fields.Float(
        required=True
    )
    heat_production_cost = ma.fields.Float(
        required=True
    )
    pumps_operation_cost = ma.fields.Float(
        required=True
    )


class OutputSolutionSchema(Schema):
    global_indicators = ma.fields.Nested(
        OutputGlobalIndicatorsSchema,
        required=True
    )
    nodes = ma.fields.Nested(
        OutputNodesSchema,
        required=True
    )
    links = ma.fields.List(
        ma.fields.Nested(OutputLinkSchema),
        required=True
    )


class SolverOutputSchema(Schema):
    solution = ma.fields.Nested(OutputSolutionSchema)
    status = ma.fields.String(
        validate=ma.validate.OneOf(SOLVER_STATUSES_MAPPING.values()),
        required=True
    )


class StatusSchema(Schema):
    status = ma.fields.String(
        validate=ma.validate.OneOf(CELERY_STATUSES_MAPPING.values()),
        required=True
    )


class TaskIdSchema(Schema):
    task_id = ma.fields.UUID(
        attribute='id',
        required=True
    )
