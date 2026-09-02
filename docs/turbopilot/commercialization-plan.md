# Turbopilot Commercialization Plan

## Product Positioning

Turbopilot is a local-first driver assistance system based on openpilot for supported `tizi`-class devices and validated vehicle/harness combinations.

Do not position Turbopilot as autonomous driving. The driver remains responsible at all times.

## Public vs Private Boundary

Public:

- Turbopilot source fork
- Release branches
- Installer entry points
- Release notes
- Basic docs
- License and attribution

Private:

- Cloud backend
- Device tokens
- Customer database
- Support tools
- Factory records
- Commercial analytics

## One-Week Delivery Scope

In scope:

- Public `release-tizi` and `staging-tizi` branches
- Real OTA validation on one `tizi` device
- Second pass UI de-comma cleanup
- Official comma cloud/uploader behavior review
- Local-first data stance
- Factory setup checklist
- Release checklist

Out of scope:

- AGNOS branding changes
- Full cloud video storage
- Fleet dashboard
- Multi-vehicle certification
- Paid subscription backend

## Cloud Storage Stance

Cloud storage should not be a default requirement for the first commercial test batch.

Recommended sequence:

1. Device status and OTA status.
2. Error logs and crash diagnostics.
3. User-approved log upload.
4. User-selected route/video upload.
5. Paid video retention plans.

Default:

- Store driving data locally.
- Do not upload video unless the user enables it.
- Prefer Wi-Fi uploads.
- Use per-device tokens.
- Allow token revocation.

## Suggested Product Tiers

Basic:

- Turbopilot system
- Local storage
- OTA updates
- Basic support

Pro:

- Basic tier
- Cloud device status
- Error log diagnostics
- Remote support workflow
- Optional selected video upload

Fleet:

- Pro tier
- Multi-device management
- Batch OTA visibility
- Longer retention options
- Support dashboard

## Legal and Safety Messaging

Use:

- Driver assistance
- Local-first data
- Supported vehicles only
- Driver must remain attentive
- Based on openpilot

Avoid:

- Autonomous driving
- Full self-driving
- Driverless
- Guaranteed safety
- Works on all cars

## Batch Launch Criteria

Before selling beyond close internal testers:

- Public OTA is validated.
- Factory flow is repeatable.
- Release process is written and followed.
- One recovery path is validated.
- At least one supported vehicle/harness combination has repeatable road validation.
- Data privacy wording is ready.
- Support boundary is written.
