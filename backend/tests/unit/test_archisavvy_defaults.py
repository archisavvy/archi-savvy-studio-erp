"""ArchiSavvyERP - the default profile a new user starts with."""

from app.core import onboarding_presets as presets
from app.core.archisavvy_defaults import (
    DEFAULT_COMPANY_TYPE,
    default_profile_metadata,
    with_default_profile,
)

CONTRACTOR_ONLY = ("daily_diary", "safety", "payroll", "subcontractors", "equipment", "fieldreports", "ncr")
PRACTICE = ("documents", "transmittals", "rfi", "crm", "sales", "finance", "gl", "tasks", "resources")


def test_default_profile_exists_and_names_only_known_modules() -> None:
    preset = presets.get_preset(DEFAULT_COMPANY_TYPE)
    assert preset is not None
    unknown = [m for m in [*preset.enabled_modules, *preset.optional_modules] if m not in presets._ALL_MODULES]
    assert unknown == []
    assert DEFAULT_COMPANY_TYPE not in presets.BUSINESS_PRESET_KEYS  # construction pack


def test_default_profile_turns_practice_modules_on_and_contractor_modules_off() -> None:
    prefs = default_profile_metadata()["module_preferences"]
    assert all(prefs[key] for key in PRACTICE)
    assert not any(prefs[key] for key in CONTRACTOR_ONLY)
    assert all(prefs[key] for key in ("projects", "contacts", "costs"))  # core stays on


def test_new_user_gets_the_profile_and_skips_the_wizard() -> None:
    onboarding = with_default_profile(None)["onboarding"]
    assert onboarding["company_type"] == DEFAULT_COMPANY_TYPE
    assert onboarding["completed"] is True


def test_existing_choice_is_never_overwritten() -> None:
    chosen = {"onboarding": {"company_type": "it_agency", "completed": True}, "other": 1}
    assert with_default_profile(chosen) == chosen
