#!/usr/bin/env python3
"""Idempotently apply a Discord server layout (roles, categories, channels) from YAML.

The YAML file is the desired state. Running this repeatedly converges the guild to
that state: missing roles/channels are created, drifted properties are patched, and
already-correct items are left alone. With ``--prune`` it also deletes roles and
channels that exist on the server but are absent from the YAML.

Usage:
    export DISCORD_BOT_TOKEN=...        # bot token (Bot ... — no "Bot " prefix needed here)
    export DISCORD_GUILD_ID=...         # the server (guild) ID
    python discord_sync.py server.yaml --dry-run    # show the plan, change nothing
    python discord_sync.py server.yaml              # apply
    python discord_sync.py server.yaml --prune      # apply AND delete extras

Matching is by NAME (roles by role name, channels by name within their category).
Renaming an item in the YAML therefore reads as "delete old + create new" rather than
an in-place rename — change names deliberately.

Requires the bot to have Manage Roles + Manage Channels (Administrator is simplest),
and its highest role must sit ABOVE any role it creates/edits. Forum and announcement
channels require the server's Community feature to be enabled.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Any

import requests
import yaml

API = "https://discord.com/api/v10"

CHANNEL_TYPES = {
    "text": 0,
    "voice": 2,
    "category": 4,
    "announcement": 5,
    "stage": 13,
    "forum": 15,
}
TYPE_NAMES = {v: k for k, v in CHANNEL_TYPES.items()}

# Discord permission flags (subset covering server management + common channel perms).
PERMISSION_BITS = {
    "create_instant_invite": 1 << 0,
    "kick_members": 1 << 1,
    "ban_members": 1 << 2,
    "administrator": 1 << 3,
    "manage_channels": 1 << 4,
    "manage_guild": 1 << 5,
    "add_reactions": 1 << 6,
    "view_audit_log": 1 << 7,
    "priority_speaker": 1 << 8,
    "stream": 1 << 9,
    "view_channel": 1 << 10,
    "send_messages": 1 << 11,
    "send_tts_messages": 1 << 12,
    "manage_messages": 1 << 13,
    "embed_links": 1 << 14,
    "attach_files": 1 << 15,
    "read_message_history": 1 << 16,
    "mention_everyone": 1 << 17,
    "use_external_emojis": 1 << 18,
    "view_guild_insights": 1 << 19,
    "connect": 1 << 20,
    "speak": 1 << 21,
    "mute_members": 1 << 22,
    "deafen_members": 1 << 23,
    "move_members": 1 << 24,
    "use_vad": 1 << 25,
    "change_nickname": 1 << 26,
    "manage_nicknames": 1 << 27,
    "manage_roles": 1 << 28,
    "manage_webhooks": 1 << 29,
    "manage_guild_expressions": 1 << 30,
    "use_application_commands": 1 << 31,
    "request_to_speak": 1 << 32,
    "manage_events": 1 << 33,
    "manage_threads": 1 << 34,
    "create_public_threads": 1 << 35,
    "create_private_threads": 1 << 36,
    "use_external_stickers": 1 << 37,
    "send_messages_in_threads": 1 << 38,
    "use_embedded_activities": 1 << 39,
    "moderate_members": 1 << 40,
}


def perms_to_int(value: Any) -> int:
    """Accept an int, a numeric string, or a list of permission names -> bitfield int."""
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    total = 0
    for name in value:
        key = str(name).strip().lower()
        if key not in PERMISSION_BITS:
            raise ValueError(f"unknown permission: {name!r}")
        total |= PERMISSION_BITS[key]
    return total


def color_to_int(value: Any) -> int:
    """Accept '#RRGGBB', '0x..', an int, or None -> Discord color int (0 = default)."""
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    s = str(value).strip().lstrip("#")
    return int(s, 16)


class Discord:
    """Thin Discord REST client with rate-limit handling."""

    def __init__(self, token: str, guild_id: str, dry_run: bool = False):
        self.guild_id = str(guild_id)
        self.dry_run = dry_run
        self.s = requests.Session()
        self.s.headers.update(
            {
                "Authorization": f"Bot {token}",
                "User-Agent": "plaintext-discord-sync (https://github.com/plaintext-security/plaintext, 1.0)",
                "Content-Type": "application/json",
            }
        )

    def _request(self, method: str, path: str, **kw) -> Any:
        url = f"{API}{path}"
        for attempt in range(8):
            resp = self.s.request(method, url, timeout=30, **kw)
            if resp.status_code == 429:  # rate limited
                retry = resp.json().get("retry_after", 1.0)
                time.sleep(float(retry) + 0.25)
                continue
            if resp.status_code >= 500:  # transient server error
                time.sleep(2 ** attempt)
                continue
            if resp.status_code >= 400:
                raise RuntimeError(
                    f"{method} {path} -> {resp.status_code}: {resp.text}"
                )
            if resp.status_code == 204 or not resp.content:
                return None
            return resp.json()
        raise RuntimeError(f"{method} {path}: gave up after retries")

    # --- reads (always run, even in dry-run) ---
    def get_roles(self) -> list[dict]:
        return self._request("GET", f"/guilds/{self.guild_id}/roles")

    def get_channels(self) -> list[dict]:
        return self._request("GET", f"/guilds/{self.guild_id}/channels")

    # --- writes (no-ops in dry-run, returning a fake stub) ---
    def create_role(self, payload: dict) -> dict:
        if self.dry_run:
            return {"id": f"<new:{payload.get('name')}>", **payload}
        return self._request("POST", f"/guilds/{self.guild_id}/roles", json=payload)

    def modify_role(self, role_id: str, payload: dict) -> dict:
        if self.dry_run:
            return {"id": role_id, **payload}
        return self._request(
            "PATCH", f"/guilds/{self.guild_id}/roles/{role_id}", json=payload
        )

    def delete_role(self, role_id: str) -> None:
        if self.dry_run:
            return
        self._request("DELETE", f"/guilds/{self.guild_id}/roles/{role_id}")

    def create_channel(self, payload: dict) -> dict:
        if self.dry_run:
            return {"id": f"<new:{payload.get('name')}>", **payload}
        return self._request("POST", f"/guilds/{self.guild_id}/channels", json=payload)

    def modify_channel(self, channel_id: str, payload: dict) -> dict:
        if self.dry_run:
            return {"id": channel_id, **payload}
        return self._request("PATCH", f"/channels/{channel_id}", json=payload)

    def delete_channel(self, channel_id: str) -> None:
        if self.dry_run:
            return
        self._request("DELETE", f"/channels/{channel_id}")


# Console logging -------------------------------------------------------------
def log(action: str, kind: str, name: str, detail: str = "") -> None:
    tag = {
        "create": "+ create",
        "update": "~ update",
        "skip": "= ok    ",
        "delete": "- delete",
        "warn": "! warn  ",
    }[action]
    line = f"  {tag}  {kind:9} {name}"
    if detail:
        line += f"   ({detail})"
    print(line)


# Reconcilers -----------------------------------------------------------------
def overwrites_payload(ch: dict, role_ids: dict[str, str], guild_id: str) -> list[dict] | None:
    """Build a permission_overwrites array from a channel's ``overwrites`` block.

    When ``overwrites`` is set it is authoritative for that channel. ``@everyone``
    resolves to the guild id; other names resolve via ``role_ids``.
    """
    if "overwrites" not in ch:
        return None
    out = []
    for ov in ch["overwrites"]:
        role_name = ov["role"]
        rid = guild_id if role_name == "@everyone" else role_ids.get(role_name)
        if rid is None:
            raise ValueError(f"overwrite references unknown role {role_name!r}")
        out.append(
            {
                "id": str(rid),
                "type": 0,  # 0 = role
                "allow": str(perms_to_int(ov.get("allow"))),
                "deny": str(perms_to_int(ov.get("deny"))),
            }
        )
    return out


def overwrites_equal(existing: list[dict], desired: list[dict]) -> bool:
    def norm(lst):
        return {
            o["id"]: (int(o.get("allow", 0)), int(o.get("deny", 0))) for o in lst
        }
    e, d = norm(existing), norm(desired)
    # Only compare the ids we manage; ignore unmanaged overwrites already present.
    return all(e.get(k) == v for k, v in d.items())


def sync_roles(dc: Discord, spec: list[dict], prune: bool) -> tuple[dict[str, str], set[str]]:
    existing = dc.get_roles()
    by_name = {r["name"]: r for r in existing}
    role_ids: dict[str, str] = {r["name"]: r["id"] for r in existing}
    seen: set[str] = set()

    print("Roles:")
    for r in spec:
        name = r["name"]
        desired = {
            "name": name,
            "color": color_to_int(r.get("color")),
            "hoist": bool(r.get("hoist", False)),
            "mentionable": bool(r.get("mentionable", False)),
            "permissions": str(perms_to_int(r.get("permissions"))),
        }
        cur = by_name.get(name)
        if cur is None:
            created = dc.create_role(desired)
            role_ids[name] = created["id"]
            seen.add(created["id"])
            log("create", "role", name)
            continue
        seen.add(cur["id"])
        diff = {
            k: v
            for k, v in desired.items()
            if str(cur.get(k)) != str(v) and k != "name"
        }
        if diff:
            dc.modify_role(cur["id"], desired)
            log("update", "role", name, ", ".join(sorted(diff)))
        else:
            log("skip", "role", name)

    if prune:
        for r in existing:
            if r["id"] in seen:
                continue
            if r.get("managed") or r["name"] == "@everyone":
                continue  # never touch integration/bot roles or @everyone
            dc.delete_role(r["id"])
            log("delete", "role", r["name"])
    return role_ids, seen


def sync_channels(dc: Discord, spec: dict, role_ids: dict[str, str], prune: bool) -> None:
    existing = dc.get_channels()
    categories = {c["name"]: c for c in existing if c["type"] == CHANNEL_TYPES["category"]}
    # (parent_id, name) -> channel  ; parent_id None means top-level
    children: dict[tuple[str | None, str], dict] = {
        (c.get("parent_id"), c["name"]): c
        for c in existing
        if c["type"] != CHANNEL_TYPES["category"]
    }
    seen: set[str] = set()

    def ensure_category(name: str, position: int) -> dict:
        cur = categories.get(name)
        if cur is None:
            cur = dc.create_channel(
                {"name": name, "type": CHANNEL_TYPES["category"], "position": position}
            )
            categories[name] = cur
            log("create", "category", name)
        else:
            log("skip", "category", name)
        seen.add(cur["id"])
        return cur

    def ensure_channel(ch: dict, parent_id: str | None, position: int) -> None:
        name = ch["name"]
        ctype = CHANNEL_TYPES[ch.get("type", "text")]
        key = (parent_id, name)
        cur = children.get(key)
        ov = overwrites_payload(ch, role_ids, dc.guild_id)
        tags = [{"name": t} for t in ch.get("tags", [])] if ch.get("type") == "forum" else None

        if cur is None:
            payload: dict[str, Any] = {"name": name, "type": ctype, "position": position}
            if parent_id:
                payload["parent_id"] = parent_id
            if ch.get("topic"):
                payload["topic"] = ch["topic"]
            if ov is not None:
                payload["permission_overwrites"] = ov
            if tags:
                payload["available_tags"] = tags
            created = dc.create_channel(payload)
            children[key] = created
            seen.add(created["id"])
            log("create", ch.get("type", "text"), name)
            return

        seen.add(cur["id"])
        if cur["type"] != ctype:
            log("warn", TYPE_NAMES.get(cur["type"], "?"), name,
                f"type differs (have {TYPE_NAMES.get(cur['type'])}, want {ch.get('type','text')}); "
                "Discord can't convert in place — delete it to recreate")
            return

        patch: dict[str, Any] = {}
        changed: list[str] = []
        if ch.get("topic") and cur.get("topic") != ch["topic"]:
            patch["topic"] = ch["topic"]
            changed.append("topic")
        if ov is not None and not overwrites_equal(cur.get("permission_overwrites", []), ov):
            patch["permission_overwrites"] = ov
            changed.append("overwrites")
        if tags:
            have = {t["name"] for t in cur.get("available_tags", [])}
            want = {t["name"] for t in tags}
            if not want.issubset(have):
                merged = cur.get("available_tags", []) + [
                    {"name": n} for n in want - have
                ]
                patch["available_tags"] = merged
                changed.append("tags")
        if patch:
            dc.modify_channel(cur["id"], patch)
            log("update", ch.get("type", "text"), name, ", ".join(changed))
        else:
            log("skip", ch.get("type", "text"), name)

    print("Categories & channels:")
    pos = 0
    for cat in spec.get("categories", []):
        cat_obj = ensure_category(cat["name"], pos)
        pos += 1
        for i, ch in enumerate(cat.get("channels", [])):
            ensure_channel(ch, cat_obj["id"], i)
    for i, ch in enumerate(spec.get("channels", [])):  # top-level (no category)
        ensure_channel(ch, None, i)

    if prune:
        # delete unseen non-category channels first, then unseen categories
        for c in existing:
            if c["id"] in seen or c["type"] == CHANNEL_TYPES["category"]:
                continue
            dc.delete_channel(c["id"])
            log("delete", TYPE_NAMES.get(c["type"], "channel"), c["name"])
        for c in existing:
            if c["id"] in seen or c["type"] != CHANNEL_TYPES["category"]:
                continue
            dc.delete_channel(c["id"])
            log("delete", "category", c["name"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="path to the desired-state YAML (e.g. server.yaml)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan without making any changes")
    ap.add_argument("--prune", action="store_true",
                    help="delete roles/channels on the server that are absent from the YAML")
    args = ap.parse_args()

    token = os.environ.get("DISCORD_BOT_TOKEN")
    guild = os.environ.get("DISCORD_GUILD_ID")
    if not token or not guild:
        print("error: set DISCORD_BOT_TOKEN and DISCORD_GUILD_ID in the environment",
              file=sys.stderr)
        return 2

    with open(args.spec, encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)

    dc = Discord(token, guild, dry_run=args.dry_run)
    mode = " (dry-run — no changes)" if args.dry_run else ""
    prune = " +prune" if args.prune else ""
    print(f"Syncing guild {guild} from {args.spec}{mode}{prune}\n")

    role_ids, _ = sync_roles(dc, spec.get("roles", []), args.prune)
    print()
    sync_channels(dc, spec, role_ids, args.prune)
    print("\nDone." + (" (nothing was changed — dry run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
