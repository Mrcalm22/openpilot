#!/usr/bin/env python3
import argparse
import hashlib
import secrets
from dataclasses import dataclass
from typing import Any

DEVICE_ID_PARAM = "TurbopilotDeviceId"
DEVICE_SEED_PARAM = "TurbopilotDeviceSeed"
DEVICE_SECRET_PARAM = "TurbopilotDeviceSecret"


@dataclass(frozen=True)
class TurbopilotIdentity:
  device_id: str
  device_secret: str


def _normalize_hardware_serial(serial: str | None) -> str:
  if not serial:
    return "unknown"
  return serial.strip().lower()


def _format_device_id(digest: str) -> str:
  return f"tp-{digest[:4]}-{digest[4:8]}-{digest[8:12]}-{digest[12:16]}"


def generate_device_id(hardware_serial: str, seed: str) -> str:
  digest = hashlib.sha256(f"turbopilot-device-id:v1:{hardware_serial}:{seed}".encode("utf-8")).hexdigest()
  return _format_device_id(digest)


def ensure_turbopilot_identity(params: Any | None = None, *, reset: bool = False) -> TurbopilotIdentity:
  from openpilot.common.params import Params
  from openpilot.system.hardware import HARDWARE

  params = params or Params()

  if reset:
    params.remove(DEVICE_ID_PARAM)
    params.remove(DEVICE_SEED_PARAM)
    params.remove(DEVICE_SECRET_PARAM)

  device_id = params.get(DEVICE_ID_PARAM)
  device_secret = params.get(DEVICE_SECRET_PARAM)

  if device_id is None:
    seed = params.get(DEVICE_SEED_PARAM)
    if seed is None:
      seed = secrets.token_hex(16)
      params.put(DEVICE_SEED_PARAM, seed, block=True)

    hardware_serial = _normalize_hardware_serial(HARDWARE.get_serial())
    device_id = generate_device_id(hardware_serial, seed)
    params.put(DEVICE_ID_PARAM, device_id, block=True)

  if device_secret is None:
    device_secret = f"tps_{secrets.token_urlsafe(32)}"
    params.put(DEVICE_SECRET_PARAM, device_secret, block=True)

  return TurbopilotIdentity(device_id=device_id, device_secret=device_secret)


def main() -> None:
  parser = argparse.ArgumentParser(description="Manage Turbopilot device identity")
  parser.add_argument("--reset", action="store_true", help="generate a new Turbopilot device identity")
  parser.add_argument("--show-secret", action="store_true", help="print the device secret")
  args = parser.parse_args()

  identity = ensure_turbopilot_identity(reset=args.reset)
  print(f"{DEVICE_ID_PARAM}={identity.device_id}")
  if args.show_secret:
    print(f"{DEVICE_SECRET_PARAM}={identity.device_secret}")


if __name__ == "__main__":
  main()
