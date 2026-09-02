import json

from openpilot.system.turbopilot.identity import generate_device_id, ensure_turbopilot_identity


def test_generate_device_id_is_stable() -> None:
  assert generate_device_id("a3ca7cb0", "seed") == generate_device_id("a3ca7cb0", "seed")


def test_generate_device_id_changes_with_seed() -> None:
  assert generate_device_id("a3ca7cb0", "seed-a") != generate_device_id("a3ca7cb0", "seed-b")


def test_generate_device_id_format() -> None:
  device_id = generate_device_id("a3ca7cb0", "seed")
  parts = device_id.split("-")
  assert parts[0] == "tp"
  assert len(parts) == 5
  assert all(len(part) == 4 for part in parts[1:])


def test_ensure_turbopilot_identity_writes_file(tmp_path) -> None:
  path = tmp_path / "identity.json"

  identity = ensure_turbopilot_identity(path=path, hardware_serial="a3ca7cb0")
  assert identity.device_id.startswith("tp-")
  assert identity.device_secret.startswith("tps_")

  data = json.loads(path.read_text())
  assert data["device_id"] == identity.device_id
  assert data["device_secret"] == identity.device_secret
  assert data["seed"] == identity.seed


def test_ensure_turbopilot_identity_is_stable(tmp_path) -> None:
  path = tmp_path / "identity.json"

  first = ensure_turbopilot_identity(path=path, hardware_serial="a3ca7cb0")
  second = ensure_turbopilot_identity(path=path, hardware_serial="a3ca7cb0")

  assert first == second
