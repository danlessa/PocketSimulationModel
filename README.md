# Pocket Network Simulation Model

## Summary

The enclosed repository serves as a simulation model for testing economic scenarios related to the Pocket Network. It is built off cadCAD under the hood.

## Model Background

This model is the next step in the evolution from the [Pocket Math Spec](https://github.com/BlockScience/PocketMathSpec) which served as a foundational architecture document prior to development.

## Current Development

The current development updates are:

1. Majority of the core development for action chains are completed but there is still refinement needed in terms of constraints and non-basic behaviors.
2. Parameters are being filled in over time as all their relationships are filled in (sourced from the math spec for easily knowing where parameters need to be invoked).
3. Basic scenario creation tools implemented which allow for testing iteratively during development.
4. Lots of work in progress, all tracked through github issues and tagged for easier triage.

## Structure of the Model Repository

1. Exploratory Folder: All jupytyer notebooks being used to test and build the system
2. Model Folder
    A. Action Chains: The code that pieces together the boundary actions, policies, and mechanisms
    B. Boundary Actions, Policies, Mechanisms: All code which implements modular logic
    C. Classes: The class definitions for entities used in the model
    D. Spaces, Types: The annotations used for functions to make it more readable
    E. PSUBs: The partial state update blocks that mostly are used as pass throughs to action chains
    F. Config: The utility functions for setting up configurations as well as options for starting state + parameter sets

## Partial State Update Blocks

The following are the partial state update blocks which as a whole represent one timestep in the system. The current timestep is one day. Hence T = 365 in the scenario running would mean 365 days. 

1. Meta Update Block: Updates the time in the system
2. Join Block: All logic around servicers, services, portals, and applications joining.
3. Stake Block: Any logic for staking that happens in the system.
4. Delegation and Service Linking Block: Block which takes care of applications delegating to portals and servicers linking to services.
5. Relay Request Block: All logic around requests being created and relayed.
6. Jailing & Slashing Block: Block for servicers or portals being slashed or jailed.
7. Block & Fee Rewards Block: The logic for both the block rewards as well as the fee rewards.
8. Undelegation & Unservice Block: The block which handles any portals undelegating or any services being unlinked from.
9. Leave Block: All logic around servicers, services, portals, and applications leaving.

## Running Simulations

### run_experiments

To run pre-packaged simulations, import run_experiments and then pass a list of experiment keys like so:

    from model import run_experiments
    df = run_experiments(["test1"])

### auto_run_sets

This option allows for running sets in chunks, saving down the results as CSV files, and picking up where last started off. The chunk size determines how many simulations to run at a time

    from model import run_experiments
    df = auto_run_sets(["test1"], "Data", 10)

### Creating Simulation Configuration

Within model/config/experiment, the experimental_configs dictionary can be modified to add in different experiments. The structure of it is like so:

    experimental_setups = {
        "test1": {
            "config_option_state": "Test",
            "config_option_params": "Test",
            "monte_carlo_n": 1,
            "T": 365,
        }
    }

Where each key represents a set, the config_option_state refers to a specific starting state, config_option_params does the same for parameters, monte_carlo_n defines the number of monte carlo runs, and T defines the number of timesteps for the experiment.

Within model/config/params, the config_option_map is set up to handle the different options for creating parameter sweeps. More detail in the parameters section on specifics.

    config_option_map = {
        "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"}
    }

Likewise, within model/config/state, there is a config_option_map for the specific types of starting state assumptions to implement.

    config_option_map = {
        "Test": {
            "Geozones": "Test",
            "Applications": "Test",
            "DAO": "Test",
            "Portals": "Test",
            "Services": "Test",
            "Servicers": "Test",
            "Validators": "Test",
        }
    }


## Parameters

Parameters are made from combining three subsets of parameters:

1. System Parameters: All parameters that would be present in the actual implementation
2. Behavior Parameters: All parameters used for assumptions in the model
3. Function Parameters: All parameters which decide functions for either:
    A. Behaviors in which case the functional parameters allow for experimenting with different classes of behavior (i.e. pulling from a random distribution or feeding in a specific signal that is meant to represent the randomness)
    B. Policies: This allows for A/B testing of different implementations of policies, i.e. if one wanted to test out different schemes of reward disbursement based on quality of service or other factors.

## State

The state can be seeded with different starting state representations so that for example one might test the impacts of starting with few servicers versus many.