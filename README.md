<p align="center">
  <img src="assets/capsule-header.png" alt="Capsule — Rebuntu Dynamic Desktop Engine" width="100%">
</p>

<p align="center"><strong>Your workspace, beyond windows.</strong></p>

# Capsule 0.9 implementation candidate

Rebuntu-only deterministic desktop state engine. Includes v0.1 baseline and incremental features through 0.9.

## CLI

`python -m pip install -e .` then `capsulectl list`, `capsulectl capture Work`, `capsulectl inspect UUID`, `capsulectl snapshot UUID`, `capsulectl restore UUID` (dry run), `capsulectl restore UUID --apply`.

## GNOME integration

The bundled `extension.js` uses GNOME Shell **42–44 legacy imports**. Install it in `~/.local/share/gnome-shell/extensions/capsule@rebuntu/` and enable through `gnome-extensions enable capsule@rebuntu` after a compatible shell restart/reload. GNOME Shell 45+ requires an ESM rewrite: the metadata is not a compatibility guarantee. This integration has not been tested in a live GNOME session.

## Limitations

Window restoration matches running windows by WM_CLASS and title; it does not relaunch closed applications. Session-local window tokens are not stable across logins. Monitor remapping, workspace creation, authorization policy, crash recovery, and UI overlays need further implementation and live integration tests. The D-Bus method is session-local and should not be exposed outside the user's desktop session. Treat `--apply` as experimental.
