"""Turbopilot product version helpers."""

TURBOPILOT_VERSION = "0.1.0"
TURBOPILOT_DISPLAY_NAME = "Turbopilot"


def get_turbopilot_version() -> str:
  return TURBOPILOT_VERSION


def format_turbopilot_version(base_description: str | None = None) -> str:
  prefix = f"{TURBOPILOT_DISPLAY_NAME} {TURBOPILOT_VERSION}"
  if base_description:
    return f"{prefix} / {base_description}"
  return prefix
