from ..types import StateType, ParamType, ApplicationEntityType
from ..spaces import (
    application_join_space,
    application_delegate_to_gateway_space,
    submit_relay_request_space,
    application_leave_space,
    application_undelegation_space,
    application_stake_space,
)
from typing import Union, Tuple, List
import random
import numpy as np


def application_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[application_join_space, None]]:
    if params["application_join_function"] == "simple_unfiform":
        return application_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid application_join_function"


def application_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[application_join_space, None]]:
    # Threshold is set by number of applicatons divided by the max applications
    threshold = len(state["Applications"]) / params["application_max_number"]
    if random.random() > threshold:
        return (
            {
                "name": "",
                "stake_amount": 15000,  # The amount of uPOKT in escrow (i.e. a security deposit)
                "geo_zone": "ABC",  # The physical geo-location identifier this Servicer registered in
                "number_servicers": 1,  # The number of Servicers requested per session
                "personal_holdings": 100,  # Unstaked POKT the application personally holds
            },
        )
    else:
        return (None,)


def gateway_delegation_ba(
    state: StateType, params: ParamType, application: ApplicationEntityType
) -> Tuple[Union[application_delegate_to_gateway_space, None]]:
    if params["gateway_delegation_function"] == "test":
        return gateway_delegation_ba_test(state, params, application)
    else:
        assert False, "Invalid gateway_delegation_function"


def gateway_delegation_ba_test(
    state: StateType, params: ParamType, application: ApplicationEntityType
) -> Tuple[Union[application_delegate_to_gateway_space, None]]:
    if (
        not application.delegate
        and application.id_number % 2 == 1
        and len(state["Gateways"]) > 0
    ):
        gateway = random.choice(state["Gateways"])
        return ({"application_public_key": application, "gateway_public_key": gateway},)
    else:
        return (None,)


def gateway_undelegation_ba(
    state: StateType, params: ParamType, application: ApplicationEntityType
) -> Tuple[Union[application_undelegation_space, None]]:
    if params["gateway_undelegation_function"] == "basic":
        return gateway_delegation_ba_basic(state, params, application)
    else:
        assert False, "Invalid gateway_undelegation_function"


def gateway_delegation_ba_basic(
    state: StateType, params: ParamType, application: ApplicationEntityType
) -> Tuple[Union[application_undelegation_space, None]]:
    if application.delegate:
        if random.random() < params["gateway_undelegation_probability"]:
            space: application_undelegation_space = {
                "application_public_key": application,
                "gateway_public_key": application.delegate,
            }
            return (space,)
        else:
            return (None,)
    else:
        return (None,)


def submit_relay_requests_ba(
    state: StateType,
    params: ParamType,
) -> Tuple[submit_relay_request_space]:
    if params["submit_relay_requests_function"] == "test":
        return submit_relay_requests_ba_test(state, params)
    if params["submit_relay_requests_function"] == "basic_gamma":
        return submit_relay_requests_ba_gamma(state, params)
    else:
        assert False, "Invalid submit_relay_requests_function"


def submit_relay_requests_ba_test(
    state: StateType,
    params: ParamType,
) -> Tuple[submit_relay_request_space]:
    application = random.choice(state["Applications"])
    number_of_requests = 10

    return (
        {"application_address": application, "number_of_requests": number_of_requests},
    )


def submit_relay_requests_ba_gamma(
    state: StateType,
    params: ParamType,
) -> Tuple[submit_relay_request_space]:
    application = random.choice(state["Applications"])
    number_of_requests = int(
        np.random.gamma(
            params["relays_per_session_gamma_distribution_shape"],
            params["relays_per_session_gamma_distribution_scale"],
        )
    )

    return (
        {"application_address": application, "number_of_requests": number_of_requests},
    )


def application_leave_ba(
    state: StateType, params: ParamType
) -> Tuple[application_leave_space]:
    if params["application_leave_function"] == "basic":
        return application_leave_ba_basic(state, params)
    else:
        assert False, "Invalid application_leave_function"


def application_leave_ba_basic(
    state: StateType, params: ParamType
) -> Tuple[application_leave_space]:
    leaves = {}
    for application in state["Applications"]:
        leaves[application] = random.random() < params["application_leave_probability"]
    return ({"applications": leaves},)


def application_stake_ba(
    state: StateType, params: ParamType
) -> List[Tuple[application_stake_space]]:
    if params["application_stake_function"] == "basic":
        return application_stake_ba_basic(state, params)
    else:
        assert False, "Invalid application_stake_function"


def application_stake_ba_basic(
    state: StateType, params: ParamType
) -> List[Tuple[application_stake_space]]:
    out = []
    for application in state["Applications"]:
        buffer = 1.2
        average_relays = (
            params["relays_per_session_gamma_distribution_shape"]
            * params["relays_per_session_gamma_distribution_scale"]
        )
        target_stake = (
            buffer
            * average_relays
            * params["average_session_per_application"]
            * params["relays_to_tokens_multiplier"]
        )
        if application.staked_pokt < target_stake:
            amount = max(
                min(
                    application.pokt_holdings,
                    target_stake - application.staked_pokt,
                ),
                0,
            )
            space: application_stake_space = {
                "geo_zone": application.geo_zone,
                "number_servicers": application.number_of_services,
                "public_key": application,
                "services": application.services,
                "stake_amount": amount,
            }
            out.append((space,))
    return out
