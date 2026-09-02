# Turbopilot Release Checklist

Use this checklist before moving code into `release-tizi`.

## Preflight

- Confirm the target release branch is `release-tizi`.
- Confirm staging validation branch is `staging-tizi`.
- Confirm the repository is clean except intentional ignored or untracked local work.
- Confirm no secrets, tokens, customer data, or private server URLs are committed.
- Confirm AGNOS is not changed unless the release is explicitly an AGNOS release.

## Code Checks

- Run Python compile checks for changed Python files.
- Run `git diff --check`.
- Search visible UI strings for unwanted comma branding:
  - `Prime`
  - `Firehose`
  - `Pair Device`
  - `connect.comma.ai`
  - `comma.ai support`
  - `Offroad_UnregisteredHardware`
- Confirm license and openpilot attribution remain present.

## Device Checks

- Boot into offroad UI.
- Open settings.
- Open Software page.
- Confirm Turbopilot brand appears on the home page.
- Confirm local data/cloud-disabled state is clear.
- Confirm no comma registration alert appears.
- Confirm Wi-Fi status renders normally.
- Confirm thermal and vehicle status render normally.
- Toggle ignition and verify onroad processes start.
- Verify front camera view appears.
- Verify manual camera toggle still cycles as expected.
- Verify route/log files are created locally.

## OTA Checks

- Push candidate to `staging-tizi`.
- Confirm staging device can fetch from public GitHub.
- Trigger updater check.
- Confirm update downloads into safe staging.
- Reboot and confirm the new commit is active.
- Leave the device running for at least 10 minutes offroad.
- Test an onroad transition after update.

## Release Promotion

Only after all staging checks pass:

```bash
git checkout release-tizi
git merge --ff-only staging-tizi
git push origin release-tizi
git tag turbopilot-vX.Y.Z
git push origin turbopilot-vX.Y.Z
```

## Release Notes

Each release note should include:

- Turbopilot version
- Base openpilot version
- Commit hash
- Hardware target
- User-visible changes
- OTA notes
- Known issues
- Whether the release is recommended for all users

## Stop Conditions

Do not publish if any of these occur:

- Manager repeatedly exits.
- UI crashes or does not render.
- Updater fails to fetch or stage the update.
- Registration alerts reappear.
- Device cannot enter onroad when ignition is present.
- Camera streams are missing.
- Any private credential is found in the diff.
