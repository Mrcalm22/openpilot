#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import secrets
from dataclasses import dataclass
from pathlib import Path

IDENTITY_PATH = Path(os.getenv("TURBOPILOT_IDENTITY_PATH", "/data/turbopilot/identity.json"))


@dataclass(frozen=True)
class TurbopilotIdentity:
  device_id: str
  device_secret: str
  seed: str


def _normalize_hardware_serial(serial: str | None) -> str:
  if not serial:
    return "unknown"
  return serial.strip().lower()


def _format_device_id(digest: str) -> str:
  return f"tp-{digest[:4]}-{digest[4:8]}-{digest[8:12]}-{digest[12:16]}"


def generate_device_id(hardware_serial: str, seed: str) -> str:
  digest = hashlib.sha256(f"turbopilot-device-id:v1:{hardware_serial}:{seed}".encode("utf-8")).hexdigest()
  return _format_device_id(digest)


def _read_identity(path: Path) -> dict[str, str]:
  try:
    with path.open() as f:
      data = json.load(f)
    if isinstance(data, dict):
      return {str(k): str(v) for k, v in data.items()}
  except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
    pass
  return {}


def _write_identity(path: Path, data: dict[str, str]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  tmp_path = path.with_suffix(".tmp")
  with tmp_path.open("w") as f:
    json.dump(data, f, indent=2, sort_keys=True)
    f.write("\n")
  os.chmod(tmp_path, 0o600)
  os.replace(tmp_path, path)
  os.chmod(path, 0o600)


def ensure_turbopilot_identity(*, reset: bool = False, path: Path = IDENTITY_PATH,
                               hardware_serial: str | None = None) -> TurbopilotIdentity:
  if reset:
    path.unlink(missing_ok=True)

  data = _read_identity(path)

  seed = data.get("seed")
  if seed is None:
    seed = secrets.token_hex(16)

  device_id = data.get("device_id")
  if device_id is None:
    if hardware_serial is None:
      from openpilot.system.hardware import HARDWARE
      hardware_serial = HARDWARE.get_serial()
    hardware_serial = _normalize_hardware_serial(hardware_serial)
    device_id = generate_device_id(hardware_serial, seed)

  device_secret = data.get("device_secret")
  if device_secret is None:
    device_secret = f"tps_{secrets.token_urlsafe(32)}"

  identity = TurbopilotIdentity(device_id=device_id, device_secret=device_secret, seed=seed)
  _write_identity(path, {
    "device_id": identity.device_id,
    "device_secret": identity.device_secret,
    "seed": identity.seed,
  })
  return identity


def main() -> None:
  parser = argparse.ArgumentParser(description="Manage Turbopilot device identity")
  parser.add_argument("--reset", action="store_true", help="generate a new Turbopilot device identity")
  parser.add_argument("--show-secret", action="store_true", help="print the device secret")
  args = parser.parse_args()

  identity = ensure_turbopilot_identity(reset=args.reset)
  print(f"TurbopilotDeviceId={identity.device_id}")
  if args.show_secret:
    print(f"TurbopilotDeviceSecret={identity.device_secret}")


if __name__ == "__main__":
  main()
