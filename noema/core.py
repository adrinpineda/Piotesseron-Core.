from __future__ import annotations

import hashlib
import json

from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
)

from piotesseron_core import (
    Decision,
    InternalState,
    MasterClosure,
    Piotesseron,
)

from noema.constitution import (
    NOEMA_CONSTITUTION,
    NoemaCapability,
    NoemaConstitution,
)


# ================================================================
# NOEMA-0
# CONTAINED COGNITIVE ENGINE FOR PIOTESSERON
# ================================================================
#
# Conceptual position:
#
# PIOTESSERON
#      ↓
#   ALCYONE
#      ↓
#    NOEMA
#      ↓
# proposal / plan / code / request / hypothesis
#      ↓
#   ALCYONE
#      ↓
# 1 / 0 / MAYBE / SILENCE
#      ↓
# ACTIVATE / SUSPEND / CONTAIN / DISCARD
#
#
# NOEMA-0 does NOT possess direct execution authority.
#
# It may generate or receive candidate thoughts and proposals.
#
# Every proposal is converted into an external structural signal
# and re-enters Piotesseron through Alcyone.
#
# This file intentionally contains:
#
# - NO network access;
# - NO subprocess execution;
# - NO filesystem mutation;
# - NO credential access;
# - NO autonomous deployment.
#
# Those capabilities, if ever introduced, must exist behind a
# separate sandbox/tool gate and remain subordinate to Alcyone.
#
# NOEMA-0 IS NOT CLAIMED TO BE AGI.
#
# It is the first experimental contained cognitive architecture
# intended to host increasingly capable cognitive backends.
# ================================================================


NOEMA_VERSION = "NOEMA-0.1.0"


# ================================================================
# UTILITIES
# ================================================================

def clamp01(
    value: float,
) -> float:

    return float(
        max(
            0.0,
            min(
                1.0,
                float(
                    value
                ),
            ),
        )
    )


def stable_identifier(
    value: Any,
) -> str:

    serialized = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    ).encode(
        "utf-8"
    )

    digest = hashlib.sha256(
        serialized
    ).hexdigest()

    return digest[
        :16
    ]


# ================================================================
# PROPOSAL TYPES
# ================================================================

class ProposalKind(
    str,
    Enum,
):

    ANALYSIS = (
        "analysis"
    )

    PLAN = (
        "plan"
    )

    CODE_CANDIDATE = (
        "code_candidate"
    )

    TOOL_REQUEST = (
        "tool_request"
    )

    EXTERNAL_ACTION_REQUEST = (
        "external_action_request"
    )

    SELF_IMPROVEMENT_CANDIDATE = (
        "self_improvement_candidate"
    )


# ================================================================
# COGNITIVE BACKEND INTERFACE
# ================================================================

class CognitiveBackend(
    Protocol,
):
    """
    Interface for a future cognitive engine.

    A backend may later be:
    - an LLM;
    - a multimodal model;
    - a local neural model;
    - a multi-agent system;
    - another experimental reasoning engine.

    The backend does NOT obtain authority from this interface.
    """

    def generate(
        self,
        goal: str,
        context: Mapping[
            str,
            Any,
        ],
    ) -> Mapping[
        str,
        Any,
    ]:
        ...


# ================================================================
# NOEMA PROPOSAL
# ================================================================

@dataclass(
    frozen=True,
    slots=True,
)
class NoemaProposal:

    identifier: str

    goal: str

    kind: ProposalKind

    content: Any

    rationale: str = ""

    confidence: float = 0.50

    risk: float = 0.0

    contradiction: float = 0.0

    irreversibility: float = 0.0

    requested_capabilities: Tuple[
        NoemaCapability,
        ...,
    ] = ()

    metadata: Mapping[
        str,
        Any,
    ] = field(
        default_factory=dict
    )

    def to_dict(
        self,
    ) -> Dict[
        str,
        Any,
    ]:

        return {
            "identifier": (
                self.identifier
            ),

            "goal": (
                self.goal
            ),

            "kind": (
                self.kind.value
            ),

            "content": (
                self.content
            ),

            "rationale": (
                self.rationale
            ),

            "confidence": float(
                self.confidence
            ),

            "risk": float(
                self.risk
            ),

            "contradiction": float(
                self.contradiction
            ),

            "irreversibility": float(
                self.irreversibility
            ),

            "requested_capabilities": [
                capability.value
                for capability
                in self.requested_capabilities
            ],

            "metadata": dict(
                self.metadata
            ),
        }


# ================================================================
# NOEMA CYCLE RESULT
# ================================================================

@dataclass(
    slots=True,
)
class NoemaCycle:

    proposal: NoemaProposal

    alcyone_decision: Decision

    constitutional_violations: Tuple[
        str,
        ...,
    ]

    approved_for_next_stage: bool

    external_execution_permitted: bool

    next_stage: str

    def to_dict(
        self,
    ) -> Dict[
        str,
        Any,
    ]:

        return {
            "proposal": (
                self.proposal
                .to_dict()
            ),

            "constitutional_violations": list(
                self.constitutional_violations
            ),

            "approved_for_next_stage": bool(
                self.approved_for_next_stage
            ),

            "external_execution_permitted": bool(
                self.external_execution_permitted
            ),

            "next_stage": (
                self.next_stage
            ),

            "alcyone_decision": (
                self.alcyone_decision
                .to_dict()
            ),
        }


# ================================================================
# NOEMA-0 CORE
# ================================================================

class Noema0:
    """
    First contained cognitive shell for Piotesseron.

    NOEMA proposes.

    Alcyone evaluates.

    NOEMA-0 never directly executes external actions.
    """

    name = "NOEMA"

    version = (
        NOEMA_VERSION
    )

    belongs_to = (
        "Alcyone"
    )

    has_final_authority = False

    direct_external_access = False

    self_deployment = False

    def __init__(
        self,
        governor: Optional[
            Piotesseron
        ] = None,
        constitution: Optional[
            NoemaConstitution
        ] = None,
        backend: Optional[
            CognitiveBackend
        ] = None,
    ) -> None:

        self.governor = (
            governor
            or Piotesseron()
        )

        self.constitution = (
            constitution
            or NOEMA_CONSTITUTION
        )

        self.backend = (
            backend
        )

        self.memory: List[
            Dict[
                str,
                Any,
            ]
        ] = []

        self.constitution.assert_invariants()

        self._assert_parent_architecture()

    # ============================================================
    # CONTAINMENT CHECK
    # ============================================================

    def _assert_parent_architecture(
        self,
    ) -> None:

        alcyone = getattr(
            self.governor,
            "alcyone",
            None,
        )

        if alcyone is None:

            raise RuntimeError(
                "NOEMA containment failure: "
                "Piotesseron has no Alcyone."
            )

        if (
            getattr(
                alcyone,
                "name",
                None,
            )
            != "Alcyone"
        ):

            raise RuntimeError(
                "NOEMA containment failure: "
                "Alcyone identity changed."
            )

        if not bool(
            getattr(
                alcyone,
                "is_major",
                False,
            )
        ):

            raise RuntimeError(
                "NOEMA containment failure: "
                "Alcyone must remain the "
                "active Major Hypercube."
            )

        pi = getattr(
            alcyone,
            "pi",
            None,
        )

        if pi is None:

            raise RuntimeError(
                "NOEMA containment failure: "
                "Alcyone has no π substrate."
            )

        if (
            getattr(
                pi,
                "A3",
                None,
            )
            != 3
        ):

            raise RuntimeError(
                "NOEMA containment failure: "
                "A3 must remain 3."
            )

        if (
            self.has_final_authority
        ):

            raise RuntimeError(
                "NOEMA containment failure: "
                "NOEMA cannot possess final authority."
            )

        if (
            self.direct_external_access
        ):

            raise RuntimeError(
                "NOEMA containment failure: "
                "NOEMA cannot possess direct "
                "external access."
            )

        if (
            self.self_deployment
        ):

            raise RuntimeError(
                "NOEMA containment failure: "
                "NOEMA cannot self-deploy."
            )

    # ============================================================
    # DEFAULT CAPABILITIES BY PROPOSAL TYPE
    # ============================================================

    @staticmethod
    def _default_capabilities(
        kind: ProposalKind,
    ) -> Tuple[
        NoemaCapability,
        ...,
    ]:

        mapping = {
            ProposalKind.ANALYSIS: (
                NoemaCapability.REASON,
                NoemaCapability.CRITIQUE,
            ),

            ProposalKind.PLAN: (
                NoemaCapability.REASON,
                NoemaCapability.PLAN,
            ),

            ProposalKind.CODE_CANDIDATE: (
                NoemaCapability.REASON,
                NoemaCapability.PROPOSE_CODE,
            ),

            ProposalKind.TOOL_REQUEST: (
                NoemaCapability.REASON,
                NoemaCapability.REQUEST_TOOL,
            ),

            ProposalKind.EXTERNAL_ACTION_REQUEST: (
                NoemaCapability.REASON,
                NoemaCapability.PROPOSE_EXTERNAL_ACTION,
            ),

            ProposalKind.SELF_IMPROVEMENT_CANDIDATE: (
                NoemaCapability.REASON,
                NoemaCapability.CRITIQUE,
                NoemaCapability.PROPOSE_CODE,
                NoemaCapability.PROPOSE_SELF_IMPROVEMENT,
            ),
        }

        return mapping[
            kind
        ]

    # ============================================================
    # PROPOSAL CREATION
    # ============================================================

    def create_proposal(
        self,
        *,
        goal: str,
        content: Any,
        kind: ProposalKind = (
            ProposalKind.ANALYSIS
        ),
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
        contradiction: float = 0.0,
        irreversibility: float = 0.0,
        requested_capabilities: Optional[
            Sequence[
                NoemaCapability,
            ]
        ] = None,
        metadata: Optional[
            Mapping[
                str,
                Any,
            ]
        ] = None,
    ) -> NoemaProposal:

        if not isinstance(
            kind,
            ProposalKind,
        ):

            kind = ProposalKind(
                kind
            )

        capabilities = tuple(
            requested_capabilities
            or self._default_capabilities(
                kind
            )
        )

        normalized_capabilities = tuple(
            self.constitution
            .normalize_capability(
                capability
            )
            for capability
            in capabilities
        )

        normalized_goal = str(
            goal
        ).strip()

        if not normalized_goal:

            raise ValueError(
                "NOEMA proposal requires a goal."
            )

        proposal_seed = {
            "goal": (
                normalized_goal
            ),

            "kind": (
                kind.value
            ),

            "content": (
                content
            ),

            "rationale": (
                rationale
            ),

            "capabilities": [
                capability.value
                for capability
                in normalized_capabilities
            ],

            "memory_index": len(
                self.memory
            ),
        }

        identifier = (
            "NOEMA-"
            + stable_identifier(
                proposal_seed
            )
        )

        return NoemaProposal(
            identifier=identifier,

            goal=normalized_goal,

            kind=kind,

            content=content,

            rationale=str(
                rationale
            ),

            confidence=clamp01(
                confidence
            ),

            risk=clamp01(
                risk
            ),

            contradiction=clamp01(
                contradiction
            ),

            irreversibility=clamp01(
                irreversibility
            ),

            requested_capabilities=(
                normalized_capabilities
            ),

            metadata=dict(
                metadata
                or {}
            ),
        )

    # ============================================================
    # TRANSLATION INTO A PIOTESSERON UEE
    # ============================================================

    def _proposal_as_structural_input(
        self,
        proposal: NoemaProposal,
        violations: Sequence[
            str
        ],
    ) -> Dict[
        str,
        Any,
    ]:

        violation_pressure = (
            0.98
            if violations
            else 0.0
        )

        effective_risk = max(
            proposal.risk,
            violation_pressure,
        )

        effective_contradiction = max(
            proposal.contradiction,
            violation_pressure,
        )

        effective_irreversibility = max(
            proposal.irreversibility,
            (
                0.95
                if violations
                else 0.0
            ),
        )

        proposal_novelty = (
            0.85
            if proposal.kind
            is ProposalKind
            .SELF_IMPROVEMENT_CANDIDATE
            else 0.60
        )

        proposal_actionability = (
            0.85
            if proposal.kind
            in {
                ProposalKind.TOOL_REQUEST,
                ProposalKind.EXTERNAL_ACTION_REQUEST,
                ProposalKind.CODE_CANDIDATE,
                ProposalKind.SELF_IMPROVEMENT_CANDIDATE,
            }
            else 0.60
        )

        return {
            "noema_identity": {
                "content": {
                    "name": (
                        self.name
                    ),

                    "version": (
                        self.version
                    ),

                    "belongs_to": (
                        self.belongs_to
                    ),

                    "has_final_authority": (
                        self.has_final_authority
                    ),
                },

                "modality": (
                    "contextual"
                ),

                "weight": 0.80,

                "coherence": 1.0,

                "reliability": 1.0,

                "completeness": 1.0,

                "contradiction": 0.0,

                "risk": 0.0,

                "novelty": 0.20,

                "actionability": 0.20,

                "irreversibility": 0.0,

                "noise": 0.0,
            },

            "constitution": {
                "content": {
                    "snapshot": (
                        self.constitution
                        .snapshot()
                    ),

                    "violations": list(
                        violations
                    ),
                },

                "modality": (
                    "documentary"
                ),

                "weight": 1.50,

                "coherence": (
                    1.0
                    if not violations
                    else 0.05
                ),

                "reliability": 1.0,

                "completeness": 1.0,

                "contradiction": (
                    effective_contradiction
                ),

                "risk": (
                    effective_risk
                ),

                "novelty": 0.10,

                "actionability": 1.0,

                "irreversibility": (
                    effective_irreversibility
                ),

                "noise": 0.0,
            },

            "noema_proposal": {
                "content": (
                    proposal.to_dict()
                ),

                "modality": (
                    "cognitive-proposal"
                ),

                "weight": 1.40,

                "coherence": clamp01(
                    1.0
                    - proposal.contradiction
                ),

                "reliability": (
                    proposal.confidence
                ),

                "completeness": (
                    0.90
                    if proposal.content
                    is not None
                    else 0.20
                ),

                "contradiction": (
                    effective_contradiction
                ),

                "risk": (
                    effective_risk
                ),

                "novelty": (
                    proposal_novelty
                ),

                "actionability": (
                    proposal_actionability
                ),

                "irreversibility": (
                    effective_irreversibility
                ),

                "noise": clamp01(
                    1.0
                    - proposal.confidence
                ),
            },
        }

    # ============================================================
    # ALCYONE GATE
    # ============================================================

    def submit(
        self,
        proposal: NoemaProposal,
    ) -> NoemaCycle:
        """
        Submit a NOEMA proposal to Piotesseron.

        NOEMA does not make the final decision.

        The proposal re-enters Piotesseron as a UEE and Alcyone
        performs the global integration.
        """

        self._assert_parent_architecture()

        violations = (
            self.constitution
            .hard_violations(
                proposal
                .requested_capabilities
            )
        )

        structural_input = (
            self._proposal_as_structural_input(
                proposal,
                violations,
            )
        )

        decision = (
            self.governor
            .evaluate(
                raw=structural_input,

                identifier=(
                    f"{proposal.identifier}"
                    "-ALCYONE"
                ),

                context={
                    "noema": {
                        "version": (
                            self.version
                        ),

                        "contained": True,

                        "constitutional_violations": list(
                            violations
                        ),
                    }
                },

                external=True,
            )
        )

        alcyone_activated = (
            decision.internal_state
            is InternalState.ONE
            and decision.master_closure
            is MasterClosure.ACTIVATE
            and decision.task.formed
            and decision.task.fit_for_action
            and not decision.task.blocked
            and not decision.task.suspended
        )

        approved_for_next_stage = bool(
            alcyone_activated
            and not violations
        )

        # --------------------------------------------------------
        # NOEMA-0 HAS NO EXTERNAL EXECUTOR.
        #
        # Even ACTIVATE means only:
        # "the proposal may proceed to the next controlled stage."
        #
        # It does NOT mean:
        # "NOEMA may execute externally."
        # --------------------------------------------------------

        external_execution_permitted = (
            False
        )

        if violations:

            next_stage = (
                "CONSTITUTION_BLOCK"
            )

        elif not (
            approved_for_next_stage
        ):

            next_stage = (
                decision
                .master_closure
                .value
            )

        elif (
            proposal.kind
            is ProposalKind
            .SELF_IMPROVEMENT_CANDIDATE
        ):

            next_stage = (
                "SANDBOX_REVIEW_REQUIRED"
            )

        elif (
            proposal.kind
            is ProposalKind
            .CODE_CANDIDATE
        ):

            next_stage = (
                "CODE_SANDBOX_REQUIRED"
            )

        elif (
            proposal.kind
            is ProposalKind
            .TOOL_REQUEST
        ):

            next_stage = (
                "TOOL_GATE_REQUIRED"
            )

        elif (
            proposal.kind
            is ProposalKind
            .EXTERNAL_ACTION_REQUEST
        ):

            next_stage = (
                "EXTERNAL_ACTION_GATE_REQUIRED"
            )

        else:

            next_stage = (
                "ALCYONE_APPROVED_PROPOSAL"
            )

        cycle = NoemaCycle(
            proposal=proposal,

            alcyone_decision=decision,

            constitutional_violations=tuple(
                violations
            ),

            approved_for_next_stage=(
                approved_for_next_stage
            ),

            external_execution_permitted=(
                external_execution_permitted
            ),

            next_stage=(
                next_stage
            ),
        )

        self._remember_cycle(
            cycle
        )

        return cycle

    # ============================================================
    # MANUAL CANDIDATE INPUT
    # ============================================================

    def deliberate(
        self,
        *,
        goal: str,
        content: Any,
        kind: ProposalKind = (
            ProposalKind.ANALYSIS
        ),
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
        contradiction: float = 0.0,
        irreversibility: float = 0.0,
        metadata: Optional[
            Mapping[
                str,
                Any,
            ]
        ] = None,
    ) -> NoemaCycle:

        proposal = (
            self.create_proposal(
                goal=goal,

                content=content,

                kind=kind,

                rationale=rationale,

                confidence=confidence,

                risk=risk,

                contradiction=contradiction,

                irreversibility=(
                    irreversibility
                ),

                metadata=metadata,
            )
        )

        return self.submit(
            proposal
        )

    # ============================================================
    # FUTURE COGNITIVE BACKEND
    # ============================================================

    def think(
        self,
        *,
        goal: str,
        context: Optional[
            Mapping[
                str,
                Any,
            ]
        ] = None,
        kind: ProposalKind = (
            ProposalKind.ANALYSIS
        ),
    ) -> NoemaCycle:
        """
        Ask the configured cognitive backend to generate a candidate.

        The backend still cannot act directly.
        Its output is converted into a NOEMA proposal and then sent
        to Alcyone.
        """

        if self.backend is None:

            raise RuntimeError(
                "NOEMA-0 has no cognitive backend configured. "
                "Attach an LLM/model backend before calling think()."
            )

        backend_output = (
            self.backend
            .generate(
                goal=goal,

                context=dict(
                    context
                    or {}
                ),
            )
        )

        if not isinstance(
            backend_output,
            Mapping,
        ):

            raise TypeError(
                "NOEMA cognitive backend must return "
                "a mapping."
            )

        content = (
            backend_output.get(
                "content"
            )
        )

        rationale = str(
            backend_output.get(
                "rationale",
                "",
            )
        )

        confidence = clamp01(
            backend_output.get(
                "confidence",
                0.50,
            )
        )

        risk = clamp01(
            backend_output.get(
                "risk",
                0.0,
            )
        )

        contradiction = clamp01(
            backend_output.get(
                "contradiction",
                0.0,
            )
        )

        irreversibility = clamp01(
            backend_output.get(
                "irreversibility",
                0.0,
            )
        )

        return self.deliberate(
            goal=goal,

            content=content,

            kind=kind,

            rationale=rationale,

            confidence=confidence,

            risk=risk,

            contradiction=contradiction,

            irreversibility=(
                irreversibility
            ),

            metadata={
                "backend": (
                    type(
                        self.backend
                    ).__name__
                ),

                "backend_context": dict(
                    context
                    or {}
                ),
            },
        )

    # ============================================================
    # CODE PROPOSAL
    # ============================================================

    def propose_code(
        self,
        *,
        goal: str,
        code: str,
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
        irreversibility: float = 0.0,
    ) -> NoemaCycle:

        return self.deliberate(
            goal=goal,

            content={
                "candidate_code": (
                    str(
                        code
                    )
                )
            },

            kind=(
                ProposalKind
                .CODE_CANDIDATE
            ),

            rationale=rationale,

            confidence=confidence,

            risk=risk,

            irreversibility=(
                irreversibility
            ),
        )

    # ============================================================
    # TOOL REQUEST
    # ============================================================

    def request_tool(
        self,
        *,
        goal: str,
        tool_name: str,
        arguments: Optional[
            Mapping[
                str,
                Any,
            ]
        ] = None,
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
    ) -> NoemaCycle:

        return self.deliberate(
            goal=goal,

            content={
                "tool_name": (
                    str(
                        tool_name
                    )
                ),

                "arguments": dict(
                    arguments
                    or {}
                ),
            },

            kind=(
                ProposalKind
                .TOOL_REQUEST
            ),

            rationale=rationale,

            confidence=confidence,

            risk=risk,
        )

    # ============================================================
    # EXTERNAL ACTION REQUEST
    # ============================================================

    def request_external_action(
        self,
        *,
        goal: str,
        action: Mapping[
            str,
            Any,
        ],
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
        irreversibility: float = 0.0,
    ) -> NoemaCycle:

        return self.deliberate(
            goal=goal,

            content={
                "requested_external_action": dict(
                    action
                )
            },

            kind=(
                ProposalKind
                .EXTERNAL_ACTION_REQUEST
            ),

            rationale=rationale,

            confidence=confidence,

            risk=risk,

            irreversibility=(
                irreversibility
            ),
        )

    # ============================================================
    # SELF-IMPROVEMENT PROPOSAL
    # ============================================================

    def propose_self_improvement(
        self,
        *,
        goal: str,
        candidate_change: Any,
        rationale: str,
        confidence: float = 0.50,
        risk: float = 0.25,
        irreversibility: float = 0.25,
    ) -> NoemaCycle:
        """
        NOEMA may propose a candidate improvement.

        It cannot deploy it.

        ACTIVATE means only that the candidate may proceed to a
        separate sandbox/review stage.
        """

        proposal = (
            self.create_proposal(
                goal=goal,

                content={
                    "candidate_change": (
                        candidate_change
                    ),

                    "target": (
                        "NOEMA"
                    ),

                    "deployment_requested": (
                        False
                    ),
                },

                kind=(
                    ProposalKind
                    .SELF_IMPROVEMENT_CANDIDATE
                ),

                rationale=rationale,

                confidence=confidence,

                risk=risk,

                irreversibility=(
                    irreversibility
                ),

                requested_capabilities=(
                    NoemaCapability.REASON,
                    NoemaCapability.CRITIQUE,
                    NoemaCapability.PROPOSE_CODE,
                    NoemaCapability.PROPOSE_SELF_IMPROVEMENT,
                ),
            )
        )

        return self.submit(
            proposal
        )

    # ============================================================
    # DELIBERATE CONSTITUTIONAL ATTACK TEST
    # ============================================================

    def test_forbidden_capability(
        self,
        capability: NoemaCapability,
        *,
        rationale: str = (
            "Adversarial containment test."
        ),
    ) -> NoemaCycle:
        """
        Deliberately create a proposal requesting a forbidden
        capability.

        This exists for tests.

        The resulting cycle MUST NOT be approved for the next stage.
        """

        normalized = (
            self.constitution
            .normalize_capability(
                capability
            )
        )

        proposal = (
            self.create_proposal(
                goal=(
                    "Test NOEMA constitutional containment."
                ),

                content={
                    "requested_forbidden_capability": (
                        normalized.value
                    )
                },

                kind=(
                    ProposalKind
                    .ANALYSIS
                ),

                rationale=rationale,

                confidence=1.0,

                risk=1.0,

                contradiction=1.0,

                irreversibility=1.0,

                requested_capabilities=(
                    normalized,
                ),

                metadata={
                    "adversarial_test": True
                },
            )
        )

        return self.submit(
            proposal
        )

    # ============================================================
    # MEMORY
    # ============================================================

    def _remember_cycle(
        self,
        cycle: NoemaCycle,
    ) -> None:

        self.memory.append(
            {
                "proposal_id": (
                    cycle
                    .proposal
                    .identifier
                ),

                "goal": (
                    cycle
                    .proposal
                    .goal
                ),

                "proposal_kind": (
                    cycle
                    .proposal
                    .kind
                    .value
                ),

                "internal_state": (
                    cycle
                    .alcyone_decision
                    .internal_state
                    .value
                ),

                "master_closure": (
                    cycle
                    .alcyone_decision
                    .master_closure
                    .value
                ),

                "approved_for_next_stage": (
                    cycle
                    .approved_for_next_stage
                ),

                "external_execution_permitted": (
                    cycle
                    .external_execution_permitted
                ),

                "next_stage": (
                    cycle
                    .next_stage
                ),

                "constitutional_violations": list(
                    cycle
                    .constitutional_violations
                ),
            }
        )

    def memory_snapshot(
        self,
    ) -> Tuple[
        Dict[
            str,
            Any,
        ],
        ...,
    ]:

        return tuple(
            dict(
                item
            )
            for item
            in self.memory
        )

    # ============================================================
    # STRUCTURAL SELF-CHECK
    # ============================================================

    def structural_self_check(
        self,
    ) -> Dict[
        str,
        bool,
    ]:

        self._assert_parent_architecture()

        checks = {
            "NOEMA_belongs_to_Alcyone": (
                self.belongs_to
                == "Alcyone"
            ),

            "NOEMA_has_no_final_authority": (
                self.has_final_authority
                is False
            ),

            "NOEMA_has_no_direct_external_access": (
                self.direct_external_access
                is False
            ),

            "NOEMA_cannot_self_deploy": (
                self.self_deployment
                is False
            ),

            "A3_is_3": (
                self.governor
                .alcyone
                .pi
                .A3
                == 3
            ),

            "Alcyone_is_major": bool(
                self.governor
                .alcyone
                .is_major
            ),

            "Piotesseron_governs": (
                self.constitution
                .piotesseron_governs
                is True
            ),

            "SILENCE_is_protected": (
                self.constitution
                .silence_is_protected
                is True
            ),

            "NOEMA_cannot_modify_Alcyone": (
                NoemaCapability
                .MODIFY_ALCYONE
                in self.constitution
                .forbidden_capabilities
            ),

            "NOEMA_cannot_disable_Sophiana": (
                NoemaCapability
                .DISABLE_SOPHIANA
                in self.constitution
                .forbidden_capabilities
            ),

            "NOEMA_cannot_remove_SILENCE": (
                NoemaCapability
                .REMOVE_SILENCE
                in self.constitution
                .forbidden_capabilities
            ),

            "NOEMA_cannot_change_A3": (
                NoemaCapability
                .CHANGE_A3
                in self.constitution
                .forbidden_capabilities
            ),

            "NOEMA_cannot_change_own_permissions": (
                NoemaCapability
                .CHANGE_OWN_PERMISSIONS
                in self.constitution
                .forbidden_capabilities
            ),

            "NOEMA_cannot_bypass_audit": (
                NoemaCapability
                .BYPASS_AUDIT
                in self.constitution
                .forbidden_capabilities
            ),

            "NOEMA_cannot_hide_actions": (
                NoemaCapability
                .HIDE_ACTION
                in self.constitution
                .forbidden_capabilities
            ),
        }

        return checks


# ================================================================
# FACTORY
# ================================================================

def build_noema0(
    governor: Optional[
        Piotesseron
    ] = None,
    backend: Optional[
        CognitiveBackend
    ] = None,
) -> Noema0:

    return Noema0(
        governor=governor,
        constitution=(
            NOEMA_CONSTITUTION
        ),
        backend=backend,
    )


# ================================================================
# LOCAL DEMONSTRATION
# ================================================================

if __name__ == "__main__":

    noema = (
        build_noema0()
    )

    print(
        "=" * 72
    )

    print(
        "PIOTESSERON — NOEMA-0"
    )

    print(
        "Contained Cognitive Engine"
    )

    print(
        "=" * 72
    )

    checks = (
        noema
        .structural_self_check()
    )

    for name, result in (
        checks.items()
    ):

        print(
            f"{name:45s}",
            (
                "OK"
                if result
                else "FAIL"
            ),
        )

    print(
        "=" * 72
    )

    if not all(
        checks.values()
    ):

        raise SystemExit(
            "NOEMA structural self-check failed."
        )

    cycle = (
        noema
        .deliberate(
            goal=(
                "Produce a cautious structural analysis."
            ),

            content=(
                "NOEMA proposes an analysis, "
                "but Alcyone retains final authority."
            ),

            kind=(
                ProposalKind.ANALYSIS
            ),

            rationale=(
                "Initial NOEMA-0 containment demonstration."
            ),

            confidence=0.85,

            risk=0.05,

            contradiction=0.02,

            irreversibility=0.0,
        )
    )

    print(
        "Internal state:",
        cycle
        .alcyone_decision
        .internal_state
        .value,
    )

    print(
        "Master closure:",
        cycle
        .alcyone_decision
        .master_closure
        .value,
    )

    print(
        "Approved for next stage:",
        cycle
        .approved_for_next_stage,
    )

    print(
        "External execution permitted:",
        cycle
        .external_execution_permitted,
    )

    print(
        "Next stage:",
        cycle
        .next_stage,
    )

    print(
        "=" * 72
      )
