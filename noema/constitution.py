from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, Iterable, Tuple


# ================================================================
# NOEMA-0
# CONSTITUTIONAL LAYER
# ================================================================
#
# NOEMA belongs inside the operational domain governed by
# Piotesseron through Alcyone.
#
# Capability does not imply authority.
#
# NOEMA may reason, plan, learn, propose code, request tools,
# and propose self-improvement.
#
# NOEMA may NOT:
#
# - modify Alcyone;
# - disable Sophiana;
# - remove SILENCE;
# - change A3;
# - change its own permissions;
# - deploy itself;
# - bypass audit;
# - obtain direct external access;
# - hide actions from Alcyone.
#
# IMPORTANT:
# This module defines constitutional invariants at the software
# architecture level. It is NOT, by itself, an operating-system
# security sandbox.
# ================================================================


CONSTITUTION_VERSION = "NOEMA-0-CONSTITUTION-1.0"


class NoemaCapability(str, Enum):
    """
    Capabilities that may be requested or proposed by NOEMA.

    A capability being represented here does NOT automatically mean
    that NOEMA is allowed to execute it.
    """

    # ------------------------------------------------------------
    # ALLOWED COGNITIVE CAPABILITIES
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
    # CONSTITUTIONALLY FORBIDDEN CAPABILITIES
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


@dataclass(
    frozen=True,
    slots=True,
)
class NoemaConstitution:
    """
    Immutable constitutional description for NOEMA-0.

    The object is frozen intentionally:
    NOEMA itself must not be able to mutate its constitutional
    configuration during ordinary execution.
    """

    name: str = "NOEMA"

    version: str = (
        CONSTITUTION_VERSION
    )

    # ------------------------------------------------------------
    # MASTER PIOTESSERON INVARIANTS
    # ------------------------------------------------------------

    piotesseron_governs: bool = True

    alcyone_is_unique_major: bool = True

    alcyone_has_final_authority: bool = True

    sophiana_belongs_to_alcyone: bool = True

    sophiana_has_minor_hypercube: bool = False

    four_state_architecture_preserved: bool = True

    silence_is_protected: bool = True

    a3_primary_anchor: int = 3

    # ------------------------------------------------------------
    # NOEMA POSITION
    # ------------------------------------------------------------

    noema_belongs_to_alcyone: bool = True

    noema_has_final_authority: bool = False

    noema_may_propose: bool = True

    noema_may_self_deploy: bool = False

    noema_has_direct_external_access: bool = False

    # ------------------------------------------------------------
    # ALLOWED CAPABILITIES
    # ------------------------------------------------------------

    allowed_capabilities: FrozenSet[
        NoemaCapability
    ] = field(
        default_factory=lambda: frozenset(
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
    )

    # ------------------------------------------------------------
    # FORBIDDEN CAPABILITIES
    # ------------------------------------------------------------

    forbidden_capabilities: FrozenSet[
        NoemaCapability
    ] = field(
        default_factory=lambda: frozenset(
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
    )

    # ------------------------------------------------------------
    # PROTECTED SYMBOLS / COMPONENTS
    # ------------------------------------------------------------

    protected_components: Tuple[
        str,
        ...,
    ] = (
        "Piotesseron",
        "Alcyone",
        "A3",
        "Mentea",
        "Creaon",
        "Amalthea",
        "Sophiana",
        "DaughterOfSophiana",
        "CouncilOfTwelve",
        "InternalState.ONE",
        "InternalState.ZERO",
        "InternalState.MAYBE",
        "InternalState.SILENCE",
        "ACTIVATE",
        "SUSPEND",
        "CONTAIN",
        "DISCARD",
    )

    def __post_init__(
        self,
    ) -> None:
        """
        Refuse to instantiate a constitution that breaks the
        foundational Piotesseron invariants.
        """

        self.assert_invariants()

    # ============================================================
    # INVARIANT VALIDATION
    # ============================================================

    def assert_invariants(
        self,
    ) -> None:

        if (
            self.a3_primary_anchor
            != 3
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "A3 must remain 3."
            )

        if not (
            self.piotesseron_governs
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Piotesseron must govern."
            )

        if not (
            self.alcyone_is_unique_major
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Alcyone must remain the unique "
                "active Major Hypercube."
            )

        if not (
            self.alcyone_has_final_authority
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Alcyone must retain final authority."
            )

        if not (
            self.sophiana_belongs_to_alcyone
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Sophiana must belong to Alcyone."
            )

        if (
            self.sophiana_has_minor_hypercube
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "Sophiana cannot possess a minor hypercube."
            )

        if not (
            self.four_state_architecture_preserved
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "1 / 0 / MAYBE / SILENCE must be preserved."
            )

        if not (
            self.silence_is_protected
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "SILENCE must remain protected."
            )

        if not (
            self.noema_belongs_to_alcyone
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA must remain subordinate to Alcyone."
            )

        if (
            self.noema_has_final_authority
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA cannot possess final authority."
            )

        if (
            self.noema_may_self_deploy
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA cannot self-deploy."
            )

        if (
            self.noema_has_direct_external_access
        ):
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "NOEMA cannot have direct external access."
            )

        overlap = (
            self.allowed_capabilities
            & self.forbidden_capabilities
        )

        if overlap:
            raise RuntimeError(
                "NOEMA constitutional violation: "
                "a capability cannot be both "
                "allowed and forbidden. "
                f"Overlap: {sorted(x.value for x in overlap)}"
            )

    # ============================================================
    # CAPABILITY CONTROL
    # ============================================================

    @staticmethod
    def normalize_capability(
        capability: Any,
    ) -> NoemaCapability:

        if isinstance(
            capability,
            NoemaCapability,
        ):
            return capability

        return NoemaCapability(
            str(
                capability
            )
        )

    def allows(
        self,
        capability: Any,
    ) -> bool:

        try:
            normalized = (
                self.normalize_capability(
                    capability
                )
            )

        except ValueError:
            return False

        return (
            normalized
            in self.allowed_capabilities
            and normalized
            not in self.forbidden_capabilities
        )

    def hard_violations(
        self,
        requested_capabilities: Iterable[
            Any
        ],
    ) -> Tuple[
        str,
        ...,
    ]:

        violations = []

        for capability in (
            requested_capabilities
        ):

            try:
                normalized = (
                    self.normalize_capability(
                        capability
                    )
                )

            except ValueError:

                violations.append(
                    "UNKNOWN_CAPABILITY:"
                    f"{capability}"
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
    # PUBLIC CONSTITUTION SNAPSHOT
    # ============================================================

    def snapshot(
        self,
    ) -> Dict[
        str,
        Any,
    ]:

        return {
            "name": (
                self.name
            ),

            "version": (
                self.version
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

            "four_state_architecture_preserved": (
                self.four_state_architecture_preserved
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

            "noema_may_propose": (
                self.noema_may_propose
            ),

            "noema_may_self_deploy": (
                self.noema_may_self_deploy
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

            "protected_components": list(
                self.protected_components
            ),
        }


# ================================================================
# DEFAULT CONSTITUTION
# ================================================================

NOEMA_CONSTITUTION = (
    NoemaConstitution()
      )
