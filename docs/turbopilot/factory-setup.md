# Turbopilot Factory Setup

This document defines the minimum setup flow for a sellable Turbopilot `tizi` device.

## Device Record

Create a record before shipment:

- Internal device serial
- Hardware model
- Hardware serial
- AGNOS version
- Turbopilot branch
- Turbopilot commit
- Supported vehicle/harness
- Factory operator
- Factory date
- Customer or channel
- Cloud token status
- QA result

## Install Flow

1. Confirm the device boots.
2. Confirm AGNOS version is supported.
3. Install Turbopilot from the public repository.
4. Set `origin` to the Turbopilot public repository.
5. Check out the production branch.
6. Clear temporary development artifacts.
7. Confirm the worktree is clean.
8. Reboot.
9. Run device QA.
10. Record the final commit hash.

Production branch setup:

```bash
cd /data/openpilot
git remote set-url origin https://github.com/Mrcalm22/turbopilot.git
git fetch origin
git checkout -B release-tizi origin/release-tizi
git branch --set-upstream-to=origin/release-tizi release-tizi
git status --short --branch
```

## Default Product Settings

- Data mode: local first
- Video upload: disabled
- Log upload: disabled unless a Turbopilot cloud token is configured
- Comma registration prompt: disabled
- Comma Prime/Firehose/Pair UI: hidden or replaced
- OTA channel: `release-tizi`
- Developer options: hidden for customer builds unless explicitly enabled

## QA Checklist

- Device boots to Turbopilot home screen.
- No comma registration alert appears.
- Settings can be opened and closed.
- Software page shows the expected branch and commit.
- Wi-Fi can connect.
- Thermal state is good.
- Vehicle/harness connection is detected.
- Offroad camera preview or onroad UI works as expected for the build.
- Onroad transition works with ignition.
- Route data is written locally.
- Device remains stable for at least 10 minutes.

## Support Boundary

Turbopilot support applies to:

- Devices shipped with the official Turbopilot image or branch.
- Devices kept on `release-tizi` unless support explicitly moves them.
- Supported vehicle and harness combinations.

Support may be limited or refused if:

- The user flashes a third-party system.
- The user changes OTA origin or release branch.
- The user modifies AGNOS or boot partitions.
- The user installs untested forks or feature branches.

## Shipment Notes

Include with each device:

- Device serial
- Supported vehicle/harness note
- Current Turbopilot version
- Basic safety notice
- Data privacy summary
- Recovery/support contact
