from openpilot.system.turbopilot.identity import generate_device_id


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
