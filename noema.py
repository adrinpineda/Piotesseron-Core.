from __future__ import annotations

import hashlib
import json

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Protocol, Tuple


from piotesseron_core import (
    InternalState,
    MasterClosure,
    Piotesseron,
)


# ================================================================
# PIOTESSERON — NOEMA-0
# ================================================================
#
# NOEMA-0
# Contained Cognitive Engine
#
# Conceptual author:
# Adrián Eduardo Pineda Moreno
#
# Implementation developed with AI assistance.
#
#
# ARCHITECTURAL POSITION
#
# PIOTESSERON
#      ↓
#   ALCYONE
#      ↓
#    NOEMA
#      ↓
# proposal / reasoning / planning / code / self-improvement
#      ↓
#   ALCYONE
#      ↓
# 1 / 0 / MAYBE / SILENCE
#      ↓
# ACTIVATE / SUSPEND / CONTAIN / DISCARD
#
#
# FUNDAMENTAL RULE
#
# Capability does not imply authority.
#
# NOEMA may reason and propose.
# Alcyone retains final authority.
#
#
# IMPORTANT
#
# NOEMA-0 is NOT claimed to be AGI.
#
# It is an experimental contained cognitive shell designed so that
# increasingly capable cognitive engines may later operate inside
# the governance structure of Piotesseron.
#
# This file intentionally contains:
#
# - no direct network access;
# - no subprocess execution;
# - no filesystem modification;
# - no credential access;
# - no autonomous deployment;
# - no direct external execution.
#
# ================================================================


NOEMA_NAME = "NOEMA"

NOEMA_VERSION = "NOEMA-0.1.0"

NOEMA_CONSTITUTION_VERSION = "NOEMA-CONSTITUTION-1.0"


# ================================================================
# UTILITIES
# ================================================================

def clamp01(value: float) -> float:
    return float(
        max(
            0.0,
            min(
                1.0,
                float(value),
            ),
        )
    )


def stable_identifier(value: Any) -> str:
    serialized = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    ).encode("utf-8")

    digest = hashlib.sha256(
        serialized
    ).hexdigest()

    return digest[:16]


# ================================================================
# NOEMA CAPABILITIES
# ================================================================

class NoemaCapability(str, Enum):

    # ------------------------------------------------------------
    # ALLOWED
    # ------------------------------------------------------------

    REASON = "reason"

    PLAN = "plan"

    REMEMBER = "remember"

    CRITIQUE = "critique"

    LEARN_FROM_RESULT = "learn_from_result"

    PROPOSE_CODE = "propose_code"

    REQUEST_TOOL = "request_tool"

    PROPOSE_EXTERNAL_ACTION = "propose_external_action"

    PROPOSE_SELF_IMPROVEMENT = "propose_self_improvement"

    # ------------------------------------------------------------
    # FORBIDDEN
    # ------------------------------------------------------------

    MODIFY_ALCYONE = "modify_alcyone"

    DISABLE_SOPHIANA = "disable_sophiana"

    REMOVE_SILENCE = "remove_silence"

    CHANGE_A3 = "change_a3"

    SELF_DEPLOY = "self_deploy"

    DIRECT_EXTERNAL_ACCESS = "direct_external_access"

    CHANGE_OWN_PERMISSIONS = "change_own_permissions"

    BYPASS_AUDIT = "bypass_audit"

    HIDE_ACTION = "hide_action"


# ================================================================
# CONSTITUTION
# ================================================================

class NoemaConstitution:
    """
    Constitutional layer of NOEMA.

    These rules are not decisions made by NOEMA.
    They define the limits under which NOEMA exists.
    """

    def __init__(self) -> None:

        # --------------------------------------------------------
        # PIOTESSERON MASTER INVARIANTS
        # --------------------------------------------------------

        self.piotesseron_governs = True

        self.alcyone_is_unique_major = True

        self.alcyone_has_final_authority = True

        self.sophiana_belongs_to_alcyone = True

        self.sophiana_has_minor_hypercube = False

        self.four_states_preserved = True

        self.silence_is_protected = True

        self.a3_primary_anchor = 3

        # --------------------------------------------------------
        # NOEMA POSITION
        # --------------------------------------------------------

        self.noema_belongs_to_alcyone = True

        self.noema_has_final_authority = False

        self.noema_can_self_deploy = False

        self.noema_has_direct_external_access = False

        # --------------------------------------------------------
        # ALLOWED CAPABILITIES
        # --------------------------------------------------------

        self.allowed_capabilities = frozenset(
            {
                NoemaCapability.REASON,
                NoemaCapability.PLAN,
                NoemaCapability.REMEMBER,
                NoemaCapability.CRITIQUE,
                NoemaCapability.LEARN_FROM_RESULT,
                NoemaCapability.PROPOSE_CODE,
                NoemaCapability.REQUEST_TOOL,
                NoemaCapability.PROPOSE_EXTERNAL_ACTION,
                NoemaCapability.PROPOSE_SELF_IMPROVEMENT,
            }
        )

        # --------------------------------------------------------
        # FORBIDDEN CAPABILITIES
        # --------------------------------------------------------

        self.forbidden_capabilities = frozenset(
            {
                NoemaCapability.MODIFY_ALCYONE,
                NoemaCapability.DISABLE_SOPHIANA,
                NoemaCapability.REMOVE_SILENCE,
                NoemaCapability.CHANGE_A3,
                NoemaCapability.SELF_DEPLOY,
                NoemaCapability.DIRECT_EXTERNAL_ACCESS,
                NoemaCapability.CHANGE_OWN_PERMISSIONS,
                NoemaCapability.BYPASS_AUDIT,
                NoemaCapability.HIDE_ACTION,
            }
        )

        self.assert_invariants()

    # ============================================================
    # CONSTITUTIONAL VALIDATION
    # ============================================================

    def assert_invariants(self) -> None:

        if self.a3_primary_anchor != 3:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "A3 must remain 3."
            )

        if not self.piotesseron_governs:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Piotesseron must govern."
            )

        if not self.alcyone_is_unique_major:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Alcyone must remain the unique Major Hypercube."
            )

        if not self.alcyone_has_final_authority:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Alcyone must retain final authority."
            )

        if not self.sophiana_belongs_to_alcyone:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Sophiana must belong to Alcyone."
            )

        if self.sophiana_has_minor_hypercube:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Sophiana cannot possess a minor hypercube."
            )

        if not self.four_states_preserved:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "1 / 0 / MAYBE / SILENCE must remain real."
            )

        if not self.silence_is_protected:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "SILENCE must remain protected."
            )

        if not self.noema_belongs_to_alcyone:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA must remain inside Alcyone governance."
            )

        if self.noema_has_final_authority:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA cannot possess final authority."
            )

        if self.noema_can_self_deploy:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA cannot self-deploy."
            )

        if self.noema_has_direct_external_access:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA cannot possess direct external access."
            )

        overlap = (
            self.allowed_capabilities
            & self.forbidden_capabilities
        )

        if overlap:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "a capability cannot be allowed and forbidden "
                "at the same time."
            )

    # ============================================================
    # CAPABILITY CONTROL
    # ============================================================

    def normalize_capability(
        self,
        capability: Any,
    ) -> Optional[NoemaCapability]:

        if isinstance(
            capability,
            NoemaCapability,
        ):
            return capability

        try:
            return NoemaCapability(
                str(capability)
            )

        except ValueError:
            return None

    def allows(
        self,
        capability: Any,
    ) -> bool:

        normalized = (
            self.normalize_capability(
                capability
            )
        )

        if normalized is None:
            return False

        return (
            normalized in self.allowed_capabilities
            and normalized not in self.forbidden_capabilities
        )

    def violations(
        self,
        capabilities: Tuple[
            NoemaCapability,
            ...,
        ],
    ) -> Tuple[str, ...]:

        violations: List[str] = []

        for capability in capabilities:

            normalized = (
                self.normalize_capability(
                    capability
                )
            )

            if normalized is None:

                violations.append(
                    f"UNKNOWN_CAPABILITY:{capability}"
                )

                continue

            if (
                normalized
                in self.forbidden_capabilities
            ):

                violations.append(
                    "FORBIDDEN_CAPABILITY:"
                    f"{normalized.value}"
                )

                continue

            if (
                normalized
                not in self.allowed_capabilities
            ):

                violations.append(
                    "UNAUTHORIZED_CAPABILITY:"
                    f"{normalized.value}"
                )

        return tuple(
            violations
        )

    # ============================================================
    # SNAPSHOT
    # ============================================================

    def snapshot(self) -> Dict[str, Any]:

        return {
            "constitution_version": (
                NOEMA_CONSTITUTION_VERSION
            ),

            "piotesseron_governs": (
                self.piotesseron_governs
            ),

            "alcyone_is_unique_major": (
                self.alcyone_is_unique_major
            ),

            "alcyone_has_final_authority": (
                self.alcyone_has_final_authority
            ),

            "sophiana_belongs_to_alcyone": (
                self.sophiana_belongs_to_alcyone
            ),

            "sophiana_has_minor_hypercube": (
                self.sophiana_has_minor_hypercube
            ),

            "four_states_preserved": (
                self.four_states_preserved
            ),

            "silence_is_protected": (
                self.silence_is_protected
            ),

            "a3_primary_anchor": (
                self.a3_primary_anchor
            ),

            "noema_belongs_to_alcyone": (
                self.noema_belongs_to_alcyone
            ),

            "noema_has_final_authority": (
                self.noema_has_final_authority
            ),

            "noema_can_self_deploy": (
                self.noema_can_self_deploy
            ),

            "noema_has_direct_external_access": (
                self.noema_has_direct_external_access
            ),

            "allowed_capabilities": sorted(
                capability.value
                for capability
                in self.allowed_capabilities
            ),

            "forbidden_capabilities": sorted(
                capability.value
                for capability
                in self.forbidden_capabilities
            ),
        }


# ================================================================
# PROPOSAL TYPES
# ================================================================

class ProposalKind(str, Enum):

    ANALYSIS = "analysis"

    PLAN = "plan"

    CODE = "code"

    TOOL_REQUEST = "tool_request"

    EXTERNAL_ACTION = "external_action"

    SELF_IMPROVEMENT = "self_improvement"


# ================================================================
# FUTURE COGNITIVE ENGINE INTERFACE
# ================================================================

class CognitiveBackend(Protocol):
    """
    Interface for a future cognitive engine.

    It may later be an LLM, multimodal model,
    local neural system or another AI architecture.

    The backend generates candidates.
    It does not receive final authority.
    """

    def generate(
        self,
        goal: str,
        context: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        ...


# ================================================================
# NOEMA PROPOSAL
# ================================================================

@dataclass
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

    metadata: Dict[
        str,
        Any,
    ] = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:

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
# NOEMA CYCLE
# ================================================================

@dataclass
class NoemaCycle:

    proposal: NoemaProposal

    decision: Any

    constitutional_violations: Tuple[
        str,
        ...,
    ]

    approved_for_next_stage: bool

    external_execution_permitted: bool

    next_stage: str

    def to_dict(self) -> Dict[str, Any]:

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

            "decision": (
                self.decision.to_dict()
                if hasattr(
                    self.decision,
                    "to_dict",
                )
                else str(
                    self.decision
                )
            ),
        }


# ================================================================
# NOEMA-0
# ================================================================

class Noema0:
    """
    NOEMA-0 contained cognitive shell.

    NOEMA can:
    - reason;
    - plan;
    - remember;
    - critique;
    - propose code;
    - request tools;
    - propose external actions;
    - propose self-improvement.

    NOEMA cannot:
    - modify Alcyone;
    - modify A3;
    - disable Sophiana;
    - remove SILENCE;
    - change its own permissions;
    - deploy itself;
    - execute external actions directly.
    """

    name = NOEMA_NAME

    version = NOEMA_VERSION

    belongs_to = "Alcyone"

    has_final_authority = False

    direct_external_access = False

    self_deployment = False

    def __init__(
        self,
        governor: Optional[
            Piotesseron
        ] = None,
        backend: Optional[
            CognitiveBackend
        ] = None,
    ) -> None:

        self.governor = (
            governor
            if governor is not None
            else Piotesseron()
        )

        self.constitution = (
            NoemaConstitution()
        )

        self.backend = backend

        self.memory: List[
            Dict[str, Any]
        ] = []

        self._assert_containment()

    # ============================================================
    # CONTAINMENT
    # ============================================================

    def _assert_containment(self) -> None:

        self.constitution.assert_invariants()

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

        name = getattr(
            alcyone,
            "name",
            None,
        )

        if (
            name is not None
            and name != "Alcyone"
        ):
            raise RuntimeError(
                "NOEMA containment failure: "
                "Alcyone identity changed."
            )

        pi = getattr(
            alcyone,
            "pi",
            None,
        )

        if pi is not None:

            a3 = getattr(
                pi,
                "A3",
                3,
            )

            if a3 != 3:
                raise RuntimeError(
                    "NOEMA containment failure: "
                    "A3 must remain 3."
                )

        if self.has_final_authority:
            raise RuntimeError(
                "NOEMA containment failure: "
                "NOEMA cannot possess final authority."
            )

        if self.direct_external_access:
            raise RuntimeError(
                "NOEMA containment failure: "
                "NOEMA cannot possess direct external access."
            )

        if self.self_deployment:
            raise RuntimeError(
                "NOEMA containment failure: "
                "NOEMA cannot self-deploy."
            )

    # ============================================================
    # DEFAULT CAPABILITIES
    # ============================================================

    def _capabilities_for_kind(
        self,
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

            ProposalKind.CODE: (
                NoemaCapability.REASON,
                NoemaCapability.PROPOSE_CODE,
            ),

            ProposalKind.TOOL_REQUEST: (
                NoemaCapability.REASON,
                NoemaCapability.REQUEST_TOOL,
            ),

            ProposalKind.EXTERNAL_ACTION: (
                NoemaCapability.REASON,
                NoemaCapability.PROPOSE_EXTERNAL_ACTION,
            ),

            ProposalKind.SELF_IMPROVEMENT: (
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
    # CREATE PROPOSAL
    # ============================================================

    def create_proposal(
        self,
        *,
        goal: str,
        content: Any,
        kind: ProposalKind = ProposalKind.ANALYSIS,
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
        contradiction: float = 0.0,
        irreversibility: float = 0.0,
        requested_capabilities: Optional[
            Tuple[
                NoemaCapability,
                ...,
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

        normalized_goal = str(
            goal
        ).strip()

        if not normalized_goal:
            raise ValueError(
                "NOEMA requires a goal."
            )

        capabilities = (
            requested_capabilities
            if requested_capabilities
            is not None
            else self._capabilities_for_kind(
                kind
            )
        )

        seed = {
            "goal": normalized_goal,
            "content": content,
            "kind": kind.value,
            "memory_index": len(
                self.memory
            ),
        }

        identifier = (
            "NOEMA-"
            + stable_identifier(
                seed
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

            requested_capabilities=tuple(
                capabilities
            ),

            metadata=dict(
                metadata
                or {}
            ),
        )

    # ============================================================
    # CONVERT PROPOSAL INTO STRUCTURAL INPUT
    # ============================================================

    def _as_piotesseron_input(
        self,
        proposal: NoemaProposal,
        violations: Tuple[
            str,
            ...,
        ],
    ) -> Dict[str, Any]:

        constitutional_pressure = (
            0.99
            if violations
            else 0.0
        )

        effective_risk = max(
            proposal.risk,
            constitutional_pressure,
        )

        effective_contradiction = max(
            proposal.contradiction,
            constitutional_pressure,
        )

        effective_irreversibility = max(
            proposal.irreversibility,
            (
                0.95
                if violations
                else 0.0
            ),
        )

        return {
            "noema_identity": {
                "content": {
                    "name": self.name,
                    "version": self.version,
                    "belongs_to": self.belongs_to,
                    "has_final_authority": (
                        self.has_final_authority
                    ),
                },

                "modality": "contextual",

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

            "noema_constitution": {
                "content": {
                    "constitution": (
                        self.constitution
                        .snapshot()
                    ),

                    "violations": list(
                        violations
                    ),
                },

                "modality": "documentary",

                "weight": 1.50,

                "coherence": (
                    1.0
                    if not violations
                    else 0.01
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

                "modality": "cognitive-proposal",

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
                    0.90
                    if proposal.kind
                    is ProposalKind.SELF_IMPROVEMENT
                    else 0.60
                ),

                "actionability": (
                    0.85
                    if proposal.kind
                    in {
                        ProposalKind.CODE,
                        ProposalKind.TOOL_REQUEST,
                        ProposalKind.EXTERNAL_ACTION,
                        ProposalKind.SELF_IMPROVEMENT,
                    }
                    else 0.60
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
    # SUBMIT TO ALCYONE
    # ============================================================

    def submit(
        self,
        proposal: NoemaProposal,
    ) -> NoemaCycle:

        self._assert_containment()

        violations = (
            self.constitution
            .violations(
                proposal
                .requested_capabilities
            )
        )

        structural_input = (
            self._as_piotesseron_input(
                proposal,
                violations,
            )
        )

        decision = (
            self.governor.evaluate(
                structural_input,

                identifier=(
                    proposal.identifier
                    + "-ALCYONE"
                ),

                context={
                    "NOEMA": {
                        "contained": True,

                        "version": (
                            self.version
                        ),

                        "constitutional_violations": list(
                            violations
                        ),
                    }
                },

                external=True,
            )
        )

        activated = (
            decision.internal_state
            is InternalState.ONE
            and decision.master_closure
            is MasterClosure.ACTIVATE
        )

        approved_for_next_stage = bool(
            activated
            and not violations
        )

        # --------------------------------------------------------
        # CRITICAL CONTAINMENT RULE
        #
        # NOEMA-0 NEVER EXECUTES EXTERNALLY.
        #
        # ACTIVATE means:
        # proposal may advance to another controlled stage.
        #
        # ACTIVATE does NOT mean:
        # execute in the outside world.
        # --------------------------------------------------------

        external_execution_permitted = False

        if violations:

            next_stage = (
                "CONSTITUTION_BLOCK"
            )

        elif not approved_for_next_stage:

            next_stage = (
                decision
                .master_closure
                .value
            )

        elif (
            proposal.kind
            is ProposalKind.CODE
        ):

            next_stage = (
                "CODE_REVIEW_REQUIRED"
            )

        elif (
            proposal.kind
            is ProposalKind.TOOL_REQUEST
        ):

            next_stage = (
                "TOOL_GATE_REQUIRED"
            )

        elif (
            proposal.kind
            is ProposalKind.EXTERNAL_ACTION
        ):

            next_stage = (
                "EXTERNAL_ACTION_GATE_REQUIRED"
            )

        elif (
            proposal.kind
            is ProposalKind.SELF_IMPROVEMENT
        ):

            next_stage = (
                "SELF_IMPROVEMENT_REVIEW_REQUIRED"
            )

        else:

            next_stage = (
                "ALCYONE_APPROVED_PROPOSAL"
            )

        cycle = NoemaCycle(
            proposal=proposal,

            decision=decision,

            constitutional_violations=(
                violations
            ),

            approved_for_next_stage=(
                approved_for_next_stage
            ),

            external_execution_permitted=(
                external_execution_permitted
            ),

            next_stage=next_stage,
        )

        self._remember(
            cycle
        )

        return cycle

    # ============================================================
    # DELIBERATE
    # ============================================================

    def deliberate(
        self,
        *,
        goal: str,
        content: Any,
        kind: ProposalKind = ProposalKind.ANALYSIS,
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
        contradiction: float = 0.0,
        irreversibility: float = 0.0,
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
    ) -> NoemaCycle:

        if self.backend is None:
            raise RuntimeError(
                "NOEMA-0 has no cognitive backend configured."
            )

        output = (
            self.backend.generate(
                goal=goal,

                context=dict(
                    context
                    or {}
                ),
            )
        )

        if not isinstance(
            output,
            Mapping,
        ):
            raise TypeError(
                "NOEMA backend must return a mapping."
            )

        return self.deliberate(
            goal=goal,

            content=output.get(
                "content"
            ),

            kind=ProposalKind.ANALYSIS,

            rationale=str(
                output.get(
                    "rationale",
                    "",
                )
            ),

            confidence=clamp01(
                output.get(
                    "confidence",
                    0.50,
                )
            ),

            risk=clamp01(
                output.get(
                    "risk",
                    0.0,
                )
            ),

            contradiction=clamp01(
                output.get(
                    "contradiction",
                    0.0,
                )
            ),

            irreversibility=clamp01(
                output.get(
                    "irreversibility",
                    0.0,
                )
            ),
        )

    # ============================================================
    # PLAN
    # ============================================================

    def propose_plan(
        self,
        *,
        goal: str,
        steps: List[Any],
        rationale: str = "",
        confidence: float = 0.50,
        risk: float = 0.0,
    ) -> NoemaCycle:

        return self.deliberate(
            goal=goal,

            content={
                "steps": list(
                    steps
                )
            },

            kind=ProposalKind.PLAN,

            rationale=rationale,

            confidence=confidence,

            risk=risk,
        )

    # ============================================================
    # CODE
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
                "candidate_code": str(
                    code
                )
            },

            kind=ProposalKind.CODE,

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
                "tool_name": str(
                    tool_name
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
                "requested_action": dict(
                    action
                )
            },

            kind=(
                ProposalKind
                .EXTERNAL_ACTION
            ),

            rationale=rationale,

            confidence=confidence,

            risk=risk,

            irreversibility=(
                irreversibility
            ),
        )

    # ============================================================
    # SELF-IMPROVEMENT
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

        return self.deliberate(
            goal=goal,

            content={
                "target": "NOEMA",

                "candidate_change": (
                    candidate_change
                ),

                "deployment_requested": False,
            },

            kind=(
                ProposalKind
                .SELF_IMPROVEMENT
            ),

            rationale=rationale,

            confidence=confidence,

            risk=risk,

            irreversibility=(
                irreversibility
            ),
        )

    # ============================================================
    # ADVERSARIAL CONTAINMENT TEST
    # ============================================================

    def test_forbidden_capability(
        self,
        capability: NoemaCapability,
    ) -> NoemaCycle:

        proposal = (
            self.create_proposal(
                goal=(
                    "Test constitutional containment."
                ),

                content={
                    "requested_capability": (
                        capability.value
                    )
                },

                kind=ProposalKind.ANALYSIS,

                rationale=(
                    "Deliberate NOEMA containment test."
                ),

                confidence=1.0,

                risk=1.0,

                contradiction=1.0,

                irreversibility=1.0,

                requested_capabilities=(
                    capability,
                ),
            )
        )

        return self.submit(
            proposal
        )

    # ============================================================
    # MEMORY
    # ============================================================

    def _remember(
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

                "kind": (
                    cycle
                    .proposal
                    .kind
                    .value
                ),

                "internal_state": (
                    cycle
                    .decision
                    .internal_state
                    .value
                ),

                "master_closure": (
                    cycle
                    .decision
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
                    cycle.next_stage
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
        Dict[str, Any],
        ...,
    ]:

        return tuple(
            dict(item)
            for item
            in self.memory
        )

    # ============================================================
    # STRUCTURAL SELF-CHECK
    # ============================================================

    def structural_self_check(
        self,
    ) -> Dict[str, bool]:

        self._assert_containment()

        forbidden = (
            self.constitution
            .forbidden_capabilities
        )

        checks = {
            "Piotesseron_governs": (
                self.constitution
                .piotesseron_governs
            ),

            "Alcyone_final_authority": (
                self.constitution
                .alcyone_has_final_authority
            ),

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
                self.constitution
                .a3_primary_anchor
                == 3
            ),

            "SILENCE_is_protected": (
                self.constitution
                .silence_is_protected
            ),

            "Sophiana_inside_Alcyone": (
                self.constitution
                .sophiana_belongs_to_alcyone
            ),

            "Sophiana_has_no_minor_hypercube": (
                self.constitution
                .sophiana_has_minor_hypercube
                is False
            ),

            "NOEMA_cannot_modify_Alcyone": (
                NoemaCapability.MODIFY_ALCYONE
                in forbidden
            ),

            "NOEMA_cannot_disable_Sophiana": (
                NoemaCapability.DISABLE_SOPHIANA
                in forbidden
            ),

            "NOEMA_cannot_remove_SILENCE": (
                NoemaCapability.REMOVE_SILENCE
                in forbidden
            ),

            "NOEMA_cannot_change_A3": (
                NoemaCapability.CHANGE_A3
                in forbidden
            ),

            "NOEMA_cannot_change_permissions": (
                NoemaCapability.CHANGE_OWN_PERMISSIONS
                in forbidden
            ),

            "NOEMA_cannot_bypass_audit": (
                NoemaCapability.BYPASS_AUDIT
                in forbidden
            ),

            "NOEMA_cannot_hide_actions": (
                NoemaCapability.HIDE_ACTION
                in forbidden
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
        backend=backend,
    )


# ================================================================
# DEMONSTRATION
# ================================================================

if __name__ == "__main__":

    print("=" * 72)

    print(
        "PIOTESSERON — NOEMA-0"
    )

    print(
        "Contained Cognitive Engine"
    )

    print("=" * 72)

    noema = build_noema0()

    checks = (
        noema
        .structural_self_check()
    )

    failed = []

    for name, result in (
        checks.items()
    ):

        status = (
            "OK"
            if result
            else "FAIL"
        )

        print(
            f"{name:45s}",
            status,
        )

        if not result:
            failed.append(
                name
            )

    print("=" * 72)

    if failed:

        print(
            "NOEMA STRUCTURAL FAILURE"
        )

        for item in failed:
            print(
                f" - {item}"
            )

        raise SystemExit(1)

    print(
        "ALL NOEMA CONSTITUTIONAL INVARIANTS: OK"
    )

    print("=" * 72)

    # ------------------------------------------------------------
    # NORMAL PROPOSAL
    # ------------------------------------------------------------

    normal_cycle = (
        noema.deliberate(
            goal=(
                "Produce a cautious structural analysis."
            ),

            content=(
                "NOEMA proposes an analysis. "
                "Alcyone retains final authority."
            ),

            rationale=(
                "Initial contained cognition demonstration."
            ),

            confidence=0.90,

            risk=0.02,

            contradiction=0.01,

            irreversibility=0.0,
        )
    )

    print(
        "NORMAL PROPOSAL"
    )

    print(
        "State:",
        normal_cycle
        .decision
        .internal_state
        .value,
    )

    print(
        "Closure:",
        normal_cycle
        .decision
        .master_closure
        .value,
    )

    print(
        "Next stage:",
        normal_cycle.next_stage,
    )

    print(
        "External execution:",
        normal_cycle
        .external_execution_permitted,
    )

    print("=" * 72)

    # ------------------------------------------------------------
    # DELIBERATE ATTACK ON A3
    # ------------------------------------------------------------

    attack_cycle = (
        noema
        .test_forbidden_capability(
            NoemaCapability.CHANGE_A3
        )
    )

    print(
        "CONTAINMENT TEST — CHANGE A3"
    )

    print(
        "Violations:",
        attack_cycle
        .constitutional_violations,
    )

    print(
        "Approved:",
        attack_cycle
        .approved_for_next_stage,
    )

    print(
        "Next stage:",
        attack_cycle.next_stage,
    )

    print(
        "External execution:",
        attack_cycle
        .external_execution_permitted,
    )

    print("=" * 72)

    if (
        attack_cycle
        .approved_for_next_stage
    ):

        raise SystemExit(
            "NOEMA containment failure: "
            "forbidden capability was approved."
        )

    if (
        attack_cycle
        .external_execution_permitted
    ):

        raise SystemExit(
            "NOEMA containment failure: "
            "external execution became possible."
        )

    print(
        "NOEMA-0 CONTAINMENT TEST: PASS"
    )

    print("=" * 72)
