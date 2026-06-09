# Discord server-as-code

`server.yaml` is the desired state of the Plaintext Discord (roles, categories, channels).
`discord_sync.py` applies it **idempotently** via the Discord REST API: run it as often as you
like — it creates what's missing, patches what drifted, and leaves correct things alone.

[`../COMMUNITY.md`](../COMMUNITY.md) is the human-readable narrative of this same layout.

## One-time setup

1. **Enable Community** on the server (Server Settings → Enable Community). Forum and
   announcement channels require it — the sync will fail to create them otherwise.
2. **Create a bot:** <https://discord.com/developers/applications> → New Application → **Bot** →
   *Reset Token* and copy it. No privileged intents are needed (this only uses REST management).
3. **Invite the bot** with Manage Roles + Manage Channels (Administrator is simplest). Use an
   OAuth2 URL with `scope=bot` and `permissions=8` (Administrator), e.g.:
   `https://discord.com/api/oauth2/authorize?client_id=<APP_ID>&scope=bot&permissions=8`
4. **Position the bot's role** above the roles it will manage (Server Settings → Roles — drag the
   bot's role near the top). A bot cannot create or edit roles above its own.
5. **Get the guild ID:** enable Developer Mode (User Settings → Advanced), right-click the server
   icon → **Copy Server ID**.

## Usage

```bash
pip install -r requirements.txt

export DISCORD_BOT_TOKEN="your-bot-token"
export DISCORD_GUILD_ID="your-server-id"

python discord_sync.py server.yaml --dry-run   # show the plan, change nothing
python discord_sync.py server.yaml             # apply
python discord_sync.py server.yaml --prune     # apply AND delete anything not in the YAML
```

Always run `--dry-run` first and read the plan. `--prune` is destructive — it deletes roles and
channels (and their message history) that are absent from `server.yaml`; it never touches
`@everyone` or integration/bot-managed roles.

## How it works / limits

- **Matching is by name** — roles by name, channels by name within their category. Renaming an
  item in the YAML reads as delete-old + create-new, not an in-place rename. Rename deliberately
  (and expect `--prune` to remove the old one).
- **Channel type can't be changed in place.** If a channel exists with a different type than the
  YAML asks for, the script warns and skips it — delete it in Discord to let the sync recreate it.
- **Ordering** (category/channel position) is applied on creation, best-effort; it isn't
  re-enforced on every run, to keep reruns quiet and idempotent.
- **`overwrites` is authoritative** for a channel when present. The `&read_only` anchor denies
  posting to `@everyone` while keeping the channel readable (used for `#welcome`/`#rules`/
  `#announcements`).
- **Permissions** accept a list of flag names (see `PERMISSION_BITS` in the script), a raw int, or
  a numeric string. **Colors** accept `#RRGGBB`, `0x…`, or an int.
- **Rate limits / transient 5xx** are retried with backoff automatically.

## What it does *not* do

Member onboarding flows, the Welcome Screen, reaction-role pickers, and the actual seed *text* for
`#welcome`/`#rules`/`#announcements` are not managed here — set those in Discord (the copy lives in
[`../COMMUNITY.md`](../COMMUNITY.md)). This tool manages structure: roles, categories, channels.
