from ..types import StateType, ParamType
from ..spaces import gateway_join_space, gateway_leave_space, gateway_registration_space
from typing import Union, Tuple, List
import random


def gateway_join_ba(
    state: StateType, params: ParamType
) -> Tuple[Union[gateway_join_space, None]]:
    if params["gateway_join_function"] == "simple_unfiform":
        return gateway_join_ba_simple_unfiform(state, params)
    else:
        assert False, "Invalid gateway_join_function"


def gateway_join_ba_simple_unfiform(
    state: StateType, params: ParamType
) -> Tuple[Union[gateway_join_space, None]]:
    # Threshold is set by number of gateways divided by the max gateways
    threshold = len(state["Gateways"]) / params["gateway_max_number"]
    if random.random() > threshold:
        return (
            {
                "name": "",
                "stake_amount": 150000
                * 10e6,  # The amount of uPOKT in escrow (i.e. a security deposit)
                "personal_holdings": 1500000
                * 10e6,  # Unstaked POKT the gateway personally holds
            },
        )
    else:
        return (None,)


def gateway_leave_ba(state: StateType, params: ParamType) -> Tuple[gateway_leave_space]:
    if params["gateway_leave_function"] == "basic":
        return gateway_leave_ba_basic(state, params)
    else:
        assert False, "Invalid gateway_leave_function"


def gateway_leave_ba_basic(
    state: StateType, params: ParamType
) -> Tuple[gateway_leave_space]:
    leaves = {}
    for gateway in state["Gateways"]:
        if (
            gateway in state["understaked_gateways"]
            and gateway.staked_pokt < params["gateway_minimum_stake"]
        ):
            leaves[gateway] = True
        else:
            leaves[gateway] = random.random() < params["gateway_leave_probability"]
    return ({"gateways": leaves},)


def gateway_stake_ba(
    state: StateType, params: ParamType
) -> List[Tuple[gateway_registration_space]]:
    if params["gateway_stake_function"] == "basic":
        return gateway_stake_ba_basic(state, params)
    else:
        assert False, "Invalid gateway_stake_function"


def gateway_stake_ba_basic(
    state: StateType, params: ParamType
) -> List[Tuple[gateway_registration_space]]:
    out = []
    for gateway in state["Gateways"]:
        # Basic target that says even if you had every single one on one portal there would be enough stake
        target_stake = max(
            params["gateway_minimum_stake"],
            params["stake_per_app_delegation"]
            * len(state["Applications"])
            * params["uses_gateway_probability"],
        )

        if gateway.staked_pokt < target_stake:
            amount = max(
                min(
                    gateway.pokt_holdings,
                    target_stake - gateway.staked_pokt,
                ),
                0,
            )
            space: gateway_registration_space = {
                "stake_amount": amount,
                "public_key": gateway,
                "service_url": None,
            }
            out.append((space,))
    return out
