from ..boundary_actions import servicer_join_ba
from ..policy import servicer_join_policy
from ..mechanisms import add_servicer


def servicer_join_ac(state, params):
    spaces = servicer_join_ba(state, params)
    if spaces[0]:
        spaces = servicer_join_policy(state, params, spaces)
    else:
        return
    add_servicer(state, params, spaces)
