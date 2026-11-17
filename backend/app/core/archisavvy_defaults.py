"""Archi Savvy Studio ERP - what a brand-new user starts with.

New file in this edition (AGPL-3.0-or-later); not part of the original project.

The original application leaves a new user with no company profile, which the
interface reads as "general business". This edition is built for architecture
and design practices, so a new user starts on the ``architecture_practice``
profile instead: construction-pack menus with the practice's business modules
switched on, and the contractor modules switched off. Nothing is removed: every
module can still be turned on from the Modules page, and the user can pick any
other profile there.
"""

from __future__ import annotations

from typing import Any

DEFAULT_COMPANY_TYPE = "architecture_practice"


def default_profile_metadata() -> dict[str, Any]:
    """The ``onboarding`` and ``module_preferences`` entries for a new user."""
    from app.core.onboarding_presets import get_preset, modules_for

    preset = get_preset(DEFAULT_COMPANY_TYPE)
    if preset is None:  # pragma: no cover - guarded by test_archisavvy_defaults
        return {}
    modules = list(preset.enabled_modules)
    return {
        "onboarding": {
            "company_type": DEFAULT_COMPANY_TYPE,
            "company_size": None,
            "enabled_modules": modules,
            "interface_mode": "advanced",
            "completed": True,
        },
        "module_preferences": modules_for(modules, "construction"),
    }


def with_default_profile(metadata: dict[str, Any] | None) -> dict[str, Any]:
    """Return ``metadata`` with the default profile added when it has none.

    A user who already carries an ``onboarding`` record (chosen in a wizard,
    set by a seeder, or restored from a backup) is left exactly as they are.
    """
    current = dict(metadata or {})
    if "onboarding" in current:
        return current
    return {**current, **default_profile_metadata()}
