from copy import deepcopy
from ..types import (
    ParamType,
    SystemParamsType,
    BehaviorParamsType,
    FunctionalParamsType,
)
from typing import Dict
from itertools import product

# A map of simulation configurations to the three components (system, behaviors, and functional parameterization)
config_option_map = {
    "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"},
    "Base": {"System": "Base", "Behaviors": "Base", "Functional": "Base"},
}


def build_params(config_option: str, singles: bool = False) -> ParamType:
    # Find the mapping of configuration option to the system, behaviors, and functional parameterization selections
    if config_option in config_option_map:
        config_option = config_option_map[config_option]
        # Pull the relevant parameterizations
        a = system_param_config[config_option["System"]]
        b = behavior_param_config[config_option["Behaviors"]]
        c = functional_param_config[config_option["Functional"]]

        # Combine parameterizations
        params = {**a, **b, **c}
    else:
        params = config_option_map_sweep[config_option]

    # Add a check which makes it only single dimension lists
    assert all(
        [len(x) == 1 for x in params.values()]
    ), "All the lengths must be 1 for this set of cadCAD simulations"

    # Deepcopy to avoid changing source
    params = deepcopy(params)

    if singles:
        for x in params:
            params[x] = params[x][0]

    return params


def create_sweep(prefix, sweep, config_option_map_sweep):
    i = 1

    cartesian_product = list(product(*sweep.values()))
    for i in range(len(cartesian_product)):
        vals = cartesian_product[i]
        config_option_map_sweep["{}{}".format(prefix, i + 1)] = {}
        for k, x in zip(sweep.keys(), vals):
            config_option_map_sweep["{}{}".format(prefix, i + 1)][k] = [x]


system_param_config: Dict[str, SystemParamsType] = {
    "Test": {
        "minimum_stake_servicer": [15000 * 10e6],
        "minimum_stake_period_servicer": [10],
        "minimum_pause_time": [10],
        "max_chains_servicer": [15],
        # "salary_block_frequency": [None],
        # "minimum_test_score_threshold": [None],
        # "minimum_report_card_threshold": [None],
        # "servicer_unbounding_period": [None],
        "relays_to_tokens_multiplier": [161.29],
        "slash_fraction_downtime": [0.000001000000000000],
        # "replay_attack_burn_multiplier": [3],
        # "max_jailed_blocks": [37960],
        "downtime_jail_duration": [3600000000000],  # In nanoseconds
        "minimum_servicers_per_session": [1],
        "maximum_servicers_per_session": [5],
        # "application_unstaking_time": [None],
        "application_fee_per_relay": [27.42],
        "minimum_application_stake": [15000 * 10e6],
        "app_burn_per_session": [0],
        "app_burn_per_relay": [0],
        "block_proposer_allocation": [0.05],
        "dao_allocation": [0.1],
        "servicer_allocation": [0.85],
        "stake_per_app_delegation": [15000 * 10e6],
        "gateway_fee_per_relay": [27.42],
        "gateway_minimum_stake": [150000 * 10e6],
        # "gateway_unstaking_time": [None],
        # "session_block_frequency": [None],
        "session_token_bucket_coefficient": [100],
        "dao_fee_percentage": [0.1],
        "validator_fee_percentage": [0.9],
        # "maturity_relay_cost": [None],
        # "maturity_relay_charge": [None],
        # "min_bootstrap_gateway_fee_per_relay": [None],
        # "max_bootstrap_servicer_cost_per_relay": [None],
        # "servicer_bootstrap_unwind_start": [None],
        # "servicer_bootstrap_end": [None],
        # "gateway_bootstrap_unwind_start": [None],
        # "gateway_bootstrap_unwind_end": [None],
        "transaction_fee": [0.01],
        # "supported_services": [None],
    },
    "Base": {
        "minimum_stake_servicer": [15000 * 10e6],
        "minimum_stake_period_servicer": [10],
        "minimum_pause_time": [10],
        "max_chains_servicer": [15],
        "relays_to_tokens_multiplier": [161.29],
        "slash_fraction_downtime": [0.000001000000000000],
        "downtime_jail_duration": [3600000000000],  # In nanoseconds
        "minimum_servicers_per_session": [1],
        "maximum_servicers_per_session": [5],
        "application_fee_per_relay": [27.42],
        "minimum_application_stake": [15000 * 10e6],
        "app_burn_per_session": [0],
        "app_burn_per_relay": [0],
        "block_proposer_allocation": [0.05],
        "dao_allocation": [0.1],
        "servicer_allocation": [0.85],
        "stake_per_app_delegation": [15000 * 10e6],
        "gateway_fee_per_relay": [27.42],
        "gateway_minimum_stake": [150000 * 10e6],
        "session_token_bucket_coefficient": [100],
        "dao_fee_percentage": [0.1],
        "validator_fee_percentage": [0.9],
        "transaction_fee": [0.01],
    },
}


behavior_param_config: Dict[str, BehaviorParamsType] = {
    "Test": {
        "application_max_number": [20],
        "servicer_max_number": [20],
        "service_max_number": [10],
        "gateway_max_number": [25],
        "service_max_number_link": [8],
        "application_leave_probability": [0.01],
        "gateway_leave_probability": [0.01],
        "service_leave_probability": [0.0025],
        "servicer_leave_probability": [0.01],
        "service_unlinking_probability": [0.01],
        "gateway_undelegation_probability": [0.01],
        "relays_per_session_gamma_distribution_shape": [500],
        "relays_per_session_gamma_distribution_scale": [50],
        "average_session_per_application": [24],
        "servicer_jailing_probability": [0.001],
        "uses_gateway_probability": [0.5],
        "applications_use_min_servicers": [1],
        "applications_use_max_servicers": [3],
        "lambda_ewm_revenue_expectation": [0.9],
        "service_linking_probability_normal": [0.01],
        "service_linking_probability_just_joined": [0.5],
        "kick_bottom_probability": [0.5],
    },
    "Base": {
        "application_max_number": [20],
        "servicer_max_number": [20],
        "service_max_number": [10],
        "gateway_max_number": [25],
        "service_max_number_link": [15],
        "application_leave_probability": [0.01],
        "gateway_leave_probability": [0.01],
        "service_leave_probability": [0.0025],
        "servicer_leave_probability": [0.01],
        "service_unlinking_probability": [0.01],
        "gateway_undelegation_probability": [0.01],
        "relays_per_session_gamma_distribution_shape": [5],
        "relays_per_session_gamma_distribution_scale": [300000],
        "average_session_per_application": [24],
        "servicer_jailing_probability": [0.001],
        "uses_gateway_probability": [0.5],
        "applications_use_min_servicers": [1],
        "applications_use_max_servicers": [3],
        "lambda_ewm_revenue_expectation": [0.9],
        "service_linking_probability_normal": [0.01],
        "service_linking_probability_just_joined": [0.5],
        "kick_bottom_probability": [0.5],
    },
}


functional_param_config: Dict[str, FunctionalParamsType] = {
    "Test": {
        "application_join_function": ["simple_unfiform"],
        "servicer_join_function": ["simple_unfiform"],
        "service_join_function": ["simple_unfiform"],
        "gateway_join_function": ["simple_unfiform"],
        "service_linking_function": ["basic"],
        "gateway_delegation_function": ["basic"],
        "relay_requests_function": ["test"],
        "submit_relay_requests_function": ["basic_gamma"],
        "submit_relay_requests_policy_function": ["V1"],
        "application_leave_function": ["basic"],
        "service_leave_function": ["basic"],
        "servicer_leave_function": ["basic"],
        "gateway_leave_function": ["basic"],
        "service_unlinking_function": ["basic"],
        "gateway_undelegation_function": ["basic"],
        "servicer_stake_function": ["basic"],
        "application_stake_function": ["basic"],
        "jailing_function": ["basic"],
        "gateway_stake_function": ["basic"],
    },
    "Base": {
        "application_join_function": ["simple_unfiform"],
        "servicer_join_function": ["simple_unfiform"],
        "service_join_function": ["simple_unfiform"],
        "gateway_join_function": ["simple_unfiform"],
        "service_linking_function": ["basic"],
        "gateway_delegation_function": ["basic"],
        "relay_requests_function": ["test"],
        "submit_relay_requests_function": ["basic_gamma"],
        "submit_relay_requests_policy_function": ["V1"],
        "application_leave_function": ["basic"],
        "service_leave_function": ["basic"],
        "servicer_leave_function": ["basic"],
        "gateway_leave_function": ["basic"],
        "service_unlinking_function": ["basic"],
        "gateway_undelegation_function": ["basic"],
        "servicer_stake_function": ["basic"],
        "application_stake_function": ["basic"],
        "jailing_function": ["basic"],
        "gateway_stake_function": ["basic"],
    },
}
config_option_map_sweep = {}

test_sweep = build_params("Base")
test_sweep["application_max_number"] = [20, 30, 40]
test_sweep["servicer_max_number"] = [20, 30, 40]
test_sweep["relays_per_session_gamma_distribution_scale"] = [200000, 300000, 400000]

create_sweep("Test", test_sweep, config_option_map_sweep)

gateway_viability_sweep_ag1_ = build_params("Base")
gateway_viability_sweep_ag1_["relays_to_tokens_multiplier"] = [25, 400]
gateway_viability_sweep_ag1_["gateway_fee_per_relay"] = [20, 30]
gateway_viability_sweep_ag1_["application_fee_per_relay"] = [20, 30]
gateway_viability_sweep_ag1_["gateway_minimum_stake"] = [100000 * 10e6, 200000 * 10e6]
gateway_viability_sweep_ag1_["application_minimum_stake"] = [
    100000 * 10e6,
    200000 * 10e6,
]
gateway_viability_sweep_ag1_["application_max_number"] = [5, 20, 100]
gateway_viability_sweep_ag1_["relays_per_session_gamma_distribution_scale"] = [
    100000,
    300000,
    900000,
]

create_sweep(
    "gateway_viability_sweep_ag1_",
    gateway_viability_sweep_ag1_,
    config_option_map_sweep,
)
