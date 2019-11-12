"""Solver module schemas"""
# pylint: disable=missing-docstring

import marshmallow as ma

from .task import CELERY_STATUSES_MAPPING, SOLVER_STATUSES_MAPPING


class Schema(ma.Schema):
    class Meta:
        ordered = True


class NodeSchema(Schema):
    id = ma.fields.List(
        ma.fields.Float,
        validate=ma.validate.Length(min=2, max=2),
        required=True,
    )


class LinkSchema(Schema):
    source = ma.fields.List(
        ma.fields.Float,
        validate=ma.validate.Length(min=2, max=2),
        required=True,
    )
    target = ma.fields.List(
        ma.fields.Float,
        validate=ma.validate.Length(min=2, max=2),
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
    coverage_rate = ma.fields.Float(
        validate=ma.validate.Range(min=0, max=1),
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


class InputParametersSchema(Schema):
    speed_min = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    speed_max = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    diameter_int_min = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    diameter_int_max = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    operation_time = ma.fields.Float(
        validate=ma.validate.Range(min=0, max=365*24),
    )
    depreciation_period = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    discout_rate = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    trench_unit_cost = ma.fields.Float(
        validate=ma.validate.Range(min=0),
    )
    pipe_diameter_unit_cost_slope = ma.fields.Float()
    pipe_diameter_unit_cost_y_intercept = ma.fields.Float()
    exchanger_power_cost_slope = ma.fields.Float()
    exchanger_power_cost_y_intercept = ma.fields.Float()
    pump_energy_ratio_cost = ma.fields.Float(
        validate=ma.validate.Range(min=0, max=1),
    )
    simultaneity_ratio = ma.fields.Float(
        validate=ma.validate.Range(min=0, max=1),
    )


class SolverInputSchema(Schema):

    @ma.validates_schema
    def validate_links_coordinates(self, data, **kwargs):
        # pylint: disable=unused-argument,no-self-use
        """Check all links link to nodes"""
        node_coords = (
            set(tuple(p['id']) for p in data['nodes']['production']) |
            set(tuple(c['id']) for c in data['nodes']['consumption'])
        )
        link_coords = (
            set(tuple(l['source']) for l in data['links']) |
            set(tuple(l['target']) for l in data['links'])
        )
        if link_coords - node_coords:
            raise ma.ValidationError("Network contains links with no node")

    nodes = ma.fields.Nested(
        InputNodesSchema,
        required=True
    )
    links = ma.fields.List(
        ma.fields.Nested(InputLinkSchema),
        required=True
    )
    parameters = ma.fields.Nested(InputParametersSchema)


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
