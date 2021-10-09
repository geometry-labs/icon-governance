from icon_governance.utils.rpc import (
    convert_hex_int,
    getDelegation,
    getPReps,
    getStake,
    post_rpc_json,
)

SKIMPY_ADDRESS = "hxf5a52d659df00ef0517921647516daaf7502a728"
ADDRESS = "hx28c08b299995a88756af64374e13db2240bc3142"


def test_post_rpc_json():
    delegation = post_rpc_json(getDelegation(ADDRESS))  # Parrot9
    stake = post_rpc_json(getStake(ADDRESS))["stake"]  # Foundation
    stake = int(stake, 16) / 1e18
    assert delegation
    assert stake >= 0


def test_convert_hex_int():
    delegated = convert_hex_int("0x21e19e0c9bab2400000")
    assert delegated == 10000000000000000000000


def test_get_delegation():
    delegation = post_rpc_json(getDelegation(ADDRESS))

    total_delegation = 0
    for d in delegation["delegations"]:
        total_delegation += convert_hex_int(d["value"])

    totalDelegated = convert_hex_int(delegation["totalDelegated"])
    assert totalDelegated == total_delegation
