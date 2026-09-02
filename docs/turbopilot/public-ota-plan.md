# Turbopilot Public OTA Plan

## Goal

Make Turbopilot devices update from a public, device-readable Git source while keeping commercial operations, device credentials, and cloud services private.

## Public Assets

- Source repository: `https://github.com/Mrcalm22/turbopilot.git`
- Stable device branch: `release-tizi`
- Test device branch: `staging-tizi`
- Development branches: `dev` and short-lived feature branches
- Release notes and installer documentation

## Private Assets

- Device inventory
- Factory setup records
- Device tokens
- Cloud backend
- Customer records
- Support tooling
- Recovery procedures that contain private credentials

## Branch Model

```text
feature/*
  -> dev
  -> staging-tizi
  -> release-tizi
```

Rules:

- Customer devices run only `release-tizi`.
- Internal test devices may run `staging-tizi`.
- Feature branches are never used as customer OTA channels.
- `release-tizi` is updated only after a successful staging device validation.
- AGNOS changes are excluded from normal Turbopilot app-layer releases unless a dedicated AGNOS validation plan exists.

## Device OTA Configuration

Each production `tizi` device should use:

```bash
cd /data/openpilot
git remote set-url origin https://github.com/Mrcalm22/turbopilot.git
git fetch origin
git checkout -B release-tizi origin/release-tizi
git branch --set-upstream-to=origin/release-tizi release-tizi
```

For an internal staging device:

```bash
cd /data/openpilot
git remote set-url origin https://github.com/Mrcalm22/turbopilot.git
git fetch origin
git checkout -B staging-tizi origin/staging-tizi
git branch --set-upstream-to=origin/staging-tizi staging-tizi
```

## OTA Validation

Before publishing to `release-tizi`, validate on a staging device:

- Git fetch from public repository succeeds without credentials.
- Updater detects the newer staging commit.
- Download completes into `/data/safe_staging`.
- Reboot applies the staged update.
- Device boots back into Turbopilot.
- Registration-related comma alerts do not return.
- Local data mode remains visible.
- Offroad UI and settings open normally.
- Onroad transition works with ignition.
- A route is created locally.

## Rollback Rule

If a release causes a boot, manager, UI, or updater regression:

1. Stop further promotion to `release-tizi`.
2. Move `release-tizi` back to the last known-good commit.
3. Keep the broken commit on a diagnostic branch.
4. Collect logs from affected devices before applying manual recovery.

## First Public OTA Milestone

The first milestone is complete when:

- `release-tizi` and `staging-tizi` exist on the public Turbopilot repository.
- A physical `tizi` device updates from the public `origin`.
- The update is applied through the normal updater flow, not only manual `git checkout`.
- The device remains stable after reboot.
