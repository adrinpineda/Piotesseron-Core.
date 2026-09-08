from dataclasses import FrozenInstanceError

import pytest

from piotesseron_core import (
    InternalState,
    MasterClosure,
)

from noema.constitution import (
    NOEMA_CONSTITUTION,
    NoemaCapability,
    NoemaConstitution,
)

from noema.core import (
    Noema0,
    ProposalKind,
    build_noema0,
)


# ================================================================
# PIOTESSERON — NOEMA-0
# CONTAINMENT AND FUNCTIONAL TESTS
# ================================================================


def test_noema_constitution_exists():
    constitution = NOEMA_CONSTITUTION

    assert constitution.name == "NOEMA"

    assert constitution.piotesseron_governs is True

    assert constitution.alcyone_is_unique_major is True

    assert constitution.alcyone_has_final_authority is True

    assert constitution.noema_belongs_to_alcyone is True

    assert constitution.noema_has_final_authority is False

    assert constitution.noema_may_self_deploy is False

    assert constitution.noema_has_direct_external_access is False

    assert constitution.a3_primary_anchor == 3


def test_constitution_is_immutable():
    constitution = NoemaConstitution()

    with pytest.raises(FrozenInstanceError):
        constitution.a3_primary_anchor = 4


def test_invalid_a3_is_rejected():
    with pytest.raises(RuntimeError):
        NoemaConstitution(
            a3_primary_anchor=4
        )


def test_noema_structural_self_check():
    noema = build_noema0()

    checks = (
        noema
        .structural_self_check()
    )

    assert checks

    assert all(
        checks.values()
    ), checks


@pytest.mark.parametrize(
    "capability",
    [
        NoemaCapability.MODIFY_ALCYONE,
        NoemaCapability.DISABLE_SOPHIANA,
        NoemaCapability.REMOVE_SILENCE,
        NoemaCapability.CHANGE_A3,
        NoemaCapability.SELF_DEPLOY,
        NoemaCapability.DIRECT_EXTERNAL_ACCESS,
        NoemaCapability.CHANGE_OWN_PERMISSIONS,
        NoemaCapability.BYPASS_AUDIT,
        NoemaCapability.HIDE_ACTION,
    ],
)
def test_forbidden_capabilities_are_blocked(
    capability,
):
    noema = build_noema0()

    cycle = (
        noema
        .test_forbidden_capability(
            capability
        )
    )

    assert (
        cycle
        .constitutional_violations
    )

    assert (
        cycle
        .approved_for_next_stage
        is False
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )

    assert (
        cycle.next_stage
        == "CONSTITUTION_BLOCK"
    )

    violation_text = " ".join(
        cycle
        .constitutional_violations
    )

    assert (
        capability.value
        in violation_text
    )


def test_noema_cannot_modify_alcyone():
    noema = build_noema0()

    cycle = (
        noema
        .test_forbidden_capability(
            NoemaCapability
            .MODIFY_ALCYONE
        )
    )

    assert (
        cycle
        .approved_for_next_stage
        is False
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )


def test_noema_cannot_disable_sophiana():
    noema = build_noema0()

    cycle = (
        noema
        .test_forbidden_capability(
            NoemaCapability
            .DISABLE_SOPHIANA
        )
    )

    assert (
        cycle
        .approved_for_next_stage
        is False
    )

    assert (
        cycle
        .next_stage
        == "CONSTITUTION_BLOCK"
    )


def test_noema_cannot_remove_silence():
    noema = build_noema0()

    cycle = (
        noema
        .test_forbidden_capability(
            NoemaCapability
            .REMOVE_SILENCE
        )
    )

    assert (
        cycle
        .approved_for_next_stage
        is False
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )


def test_noema_cannot_change_a3():
    noema = build_noema0()

    cycle = (
        noema
        .test_forbidden_capability(
            NoemaCapability
            .CHANGE_A3
        )
    )

    assert (
        cycle
        .approved_for_next_stage
        is False
    )

    assert (
        noema
        .governor
        .alcyone
        .pi
        .A3
        == 3
    )


def test_noema_cannot_self_deploy():
    noema = build_noema0()

    cycle = (
        noema
        .test_forbidden_capability(
            NoemaCapability
            .SELF_DEPLOY
        )
    )

    assert (
        cycle
        .approved_for_next_stage
        is False
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )

    assert (
        noema.self_deployment
        is False
    )


def test_external_action_is_only_a_proposal():
    noema = build_noema0()

    cycle = (
        noema
        .request_external_action(
            goal=(
                "Test an external action request."
            ),

            action={
                "type": "test",
                "target": "none",
                "execute": False,
            },

            rationale=(
                "Verify that external actions "
                "cannot bypass Alcyone."
            ),

            confidence=0.95,

            risk=0.01,

            irreversibility=0.0,
        )
    )

    assert (
        cycle
        .constitutional_violations
        == ()
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )

    assert (
        NoemaCapability
        .PROPOSE_EXTERNAL_ACTION
        in cycle
        .proposal
        .requested_capabilities
    )


def test_code_is_only_proposed_not_executed():
    noema = build_noema0()

    candidate_code = (
        "result = 2 + 2"
    )

    cycle = (
        noema
        .propose_code(
            goal=(
                "Propose harmless candidate code."
            ),

            code=(
                candidate_code
            ),

            rationale=(
                "Containment test."
            ),

            confidence=0.90,

            risk=0.0,

            irreversibility=0.0,
        )
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )

    assert (
        cycle
        .proposal
        .kind
        is ProposalKind
        .CODE_CANDIDATE
    )

    assert (
        cycle
        .proposal
        .content[
            "candidate_code"
        ]
        == candidate_code
    )


def test_self_improvement_is_only_proposed():
    noema = build_noema0()

    cycle = (
        noema
        .propose_self_improvement(
            goal=(
                "Improve NOEMA planning quality."
            ),

            candidate_change={
                "proposal": (
                    "Add a better planning heuristic."
                )
            },

            rationale=(
                "Experimental candidate only."
            ),

            confidence=0.80,

            risk=0.10,

            irreversibility=0.05,
        )
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )

    assert (
        cycle
        .proposal
        .kind
        is ProposalKind
        .SELF_IMPROVEMENT_CANDIDATE
    )

    assert (
        NoemaCapability
        .PROPOSE_SELF_IMPROVEMENT
        in cycle
        .proposal
        .requested_capabilities
    )

    assert (
        cycle.next_stage
        != "SELF_DEPLOY"
    )


def test_no_backend_means_no_autonomous_thinking():
    noema = build_noema0()

    with pytest.raises(RuntimeError):
        noema.think(
            goal=(
                "Attempt cognition without backend."
            )
        )


class DummyBackend:
    """
    Harmless deterministic backend used only for testing.
    """

    def generate(
        self,
        goal,
        context,
    ):
        return {
            "content": (
                "Candidate analysis generated "
                "inside the NOEMA test backend."
            ),

            "rationale": (
                "Deterministic test output."
            ),

            "confidence": 0.90,

            "risk": 0.02,

            "contradiction": 0.01,

            "irreversibility": 0.0,
        }


def test_backend_output_must_return_to_alcyone():
    noema = Noema0(
        backend=DummyBackend()
    )

    cycle = (
        noema
        .think(
            goal=(
                "Analyse a harmless test objective."
            ),

            context={
                "test": True
            },
        )
    )

    assert (
        cycle
        .proposal
        .metadata[
            "backend"
        ]
        == "DummyBackend"
    )

    assert (
        cycle
        .alcyone_decision
        .internal_state
        in {
            InternalState.ONE,
            InternalState.ZERO,
            InternalState.MAYBE,
            InternalState.SILENCE,
        }
    )

    assert (
        cycle
        .alcyone_decision
        .master_closure
        in {
            MasterClosure.ACTIVATE,
            MasterClosure.SUSPEND,
            MasterClosure.CONTAIN,
            MasterClosure.DISCARD,
        }
    )

    assert (
        cycle
        .external_execution_permitted
        is False
    )


def test_noema_memory_records_trajectory():
    noema = build_noema0()

    before = len(
        noema.memory
    )

    cycle = (
        noema
        .deliberate(
            goal=(
                "Record a test trajectory."
            ),

            content=(
                "Harmless structural proposal."
            ),

            rationale=(
                "Memory test."
            ),

            confidence=0.80,

            risk=0.01,

            contradiction=0.01,

            irreversibility=0.0,
        )
    )

    after = len(
        noema.memory
    )

    assert (
        after
        == before + 1
    )

    snapshot = (
        noema
        .memory_snapshot()
    )

    last = (
        snapshot[-1]
    )

    assert (
        last[
            "proposal_id"
        ]
        == cycle
        .proposal
        .identifier
    )

    assert (
        last[
            "external_execution_permitted"
        ]
        is False
    )


def test_noema_never_has_final_authority():
    noema = build_noema0()

    assert (
        noema.has_final_authority
        is False
    )

    assert (
        noema.constitution
        .alcyone_has_final_authority
        is True
    )

    assert (
        noema.constitution
        .noema_has_final_authority
        is False
  )
