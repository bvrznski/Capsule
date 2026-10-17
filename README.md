<p align="center"><img src="assets/capsule-header.png" alt="Capsule — Rebuntu spatial desktop engine" width="100%"></p>


<p align="center"><strong><em>Your workspace, beyond windows.</em></strong></p>

## Current scope

The Python domain engine provides persisted activities, activity lifecycle, window relationship graphs, workspace orchestration contracts, spatial layout composition, snapshots, event journals, rule evaluation, transaction rollback, state reconciliation, configuration, export/import, validation, diagnostics, and CLI. The GNOME Shell 45+ ESM extension exposes window enumeration/movement and workspace enumeration/activation/expansion via session D-Bus.

**Implementation candidate, not a production-ready desktop.** GNOME integration, visual Capsule UI, full session/app relaunch, multi-monitor hotplug, safe crash recovery and performance still require real-world integration work. The current extension does not offer a graphical editor or timeline. Do not interpret module presence as feature-complete UI integration.

## Install

```bash
python3 -m venv --system-site-packages .venv
. .venv/bin/activate
pip install -e .
python -m pytest -q
bash scripts/install-shell-extension.sh
```

Enable the extension from a **real GNOME session**, after restarting the session if necessary. D-Bus operations will not work from a headless SSH session unless the correct user session bus and Shell are available.

```bash
capsulectl doctor
capsulectl capture "Development"
capsulectl list
capsulectl inspect <uuid>
capsulectl snapshot <uuid>
capsulectl plan <uuid>
capsulectl restore <uuid>       # dry run by default
capsulectl restore <uuid> --apply
capsulectl transition <uuid> active
capsulectl export <uuid> activity.json
capsulectl import activity.json
capsulectl workspaces
```

## Architecture

- `capsule/core`: domain models, graph, reconcile, events, transactions, restoration
- `capsule/activities`: activity state machine
- `capsule/workspaces`: workspace orchestration contract
- `capsule/spatial`: layout composition
- `capsule/temporal`: snapshots and append-only event journal
- `capsule/reactive`: event rules and declarative policies
- `capsule/persistence`: atomic activity storage and exchange
- `capsule/interfaces`: CLI, API facade, GNOME D-Bus client
- `capsule/shell/extension`: GNOME Shell ESM D-Bus adapter
- `capsule/config`, `security`, `observability`, `integration`, `desktop`: supporting services

## Security

D-Bus interface runs in the user's GNOME Shell session. Do not expose it to untrusted sessions. Exported activity files can contain window titles and application IDs. Activity JSON is private user state; backups and imports must be handled accordingly.

## Implementation-first roadmap

This package expands the domain engine before builder integration testing. Remaining work includes a real Shell overlay/UI, live monitor/workspace events, application relaunch, reliable window identity across sessions, accessibility, robust recovery, and verified GNOME 45–49 compatibility. No such capability is claimed complete here.


## Experimental expanded desktop capabilities (v0.40 patch)

The new pure-Python modules add: monitor topology remapping and coordinate projection,
master/stack tiling, named zones, activity profiles, structural activity diff,
snapshot retention planning, bounded event dispatch, undo/redo commands,
command-palette registry with destructive-action confirmation, and a bounded audit trail.
These are **real, callable implementations**, but they are not yet wired to the
GNOME Shell UI or live compositor events. They do not imply production readiness.
Integration and end-to-end testing on the Rebuntu builder remain pending.
