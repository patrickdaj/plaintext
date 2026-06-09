# Plaintext Discord — setup runbook

A top-to-bottom checklist to stand up the community server and wire it to the repo. Work the phases
in order; each builds on the last. Companion files:

- [`COMMUNITY.md`](../COMMUNITY.md) — the layout + the seed text (welcome/rules/etc.) to paste in.
- [`server.yaml`](server.yaml) — the structure as code (roles, categories, channels).
- [`discord_sync.py`](discord_sync.py) / [`README.md`](README.md) — the sync tool and its reference.
- [`.github/workflows/discord-sync.yml`](../.github/workflows/discord-sync.yml) — the CI that applies it.

> **Security rule that runs through all of this:** the bot token is a password for your server.
> Never paste it into chat, commits, screenshots, or issues. In CI it lives only as an
> **environment** secret (Phase 4). If it ever leaks, reset it in the Developer Portal immediately.

---

## Phase 1 — Create & configure the server

- [ ] **Create the server.** Discord → **+** (Add a Server) → **Create My Own** → name it `Plaintext`.
- [ ] **Enable Community.** Server Settings → **Enable Community** → follow the wizard.
      *Required* — forum channels and the announcements channel won't create without it.
- [ ] **Set a permanent invite.** The current link (`discord.gg/sZjQYqVvG`) may be a temporary invite.
      Server Settings → Invites (or right-click the server → Invite People → **Edit invite link** →
      set **Expire after: Never**, **Max number of uses: No limit**). If the server reaches Boost
      Level 3, set a **Vanity URL** (e.g. `discord.gg/plaintext`) under Server Settings → Vanity URL.
- [ ] **Note the final invite link** — you'll wire it into the site in Phase 6.

## Phase 2 — Create the bot

- [ ] Go to <https://discord.com/developers/applications> → **New Application** → name it
      `plaintext-sync`.
- [ ] **Bot** tab → **Reset Token** → copy it somewhere safe (a password manager). This is the
      `DISCORD_BOT_TOKEN`.
- [ ] No **Privileged Gateway Intents** are needed — this tool only uses REST management. Leave them off.
- [ ] **Invite the bot** to the server with management permissions. On the **OAuth2 → URL Generator**
      pick scope `bot` and permission **Administrator** (simplest), or build the URL directly:
      ```
      https://discord.com/api/oauth2/authorize?client_id=<APPLICATION_ID>&scope=bot&permissions=8
      ```
      Open it, choose your server, authorize.
- [ ] **Raise the bot's role.** Server Settings → Roles → drag the `plaintext-sync` role **near the
      top**, above every role it will manage. A bot can't create or edit roles above its own.

## Phase 3 — Apply the structure

You can apply locally first to see it work, then let CI own it (Phase 4). To apply locally:

- [ ] **Get the guild (server) ID.** User Settings → Advanced → enable **Developer Mode**. Then
      right-click the server icon → **Copy Server ID**. This is `DISCORD_GUILD_ID`.
- [ ] **Run a dry-run, then apply:**
      ```bash
      cd community
      pip install -r requirements.txt
      export DISCORD_BOT_TOKEN="…"      # from Phase 2
      export DISCORD_GUILD_ID="…"       # from above
      python discord_sync.py server.yaml --dry-run   # read the plan
      python discord_sync.py server.yaml             # apply it
      ```
- [ ] Confirm in Discord: 5 categories, the 14 HELP forums, voice rooms, and the roles all appear.
      Re-running should report everything as `= ok` (idempotent).

> Skip this phase and let CI do the first apply if you prefer — but running once locally is the
> fastest way to confirm the bot's token and permissions are right.

## Phase 4 — Secure the CI (so the file stays the source of truth)

The workflow validates on PRs (no secrets) and applies on push to `main` — but only after you set
up the protected environment and secrets. Do this **once**:

- [ ] **Create the environment.** Repo → **Settings → Environments → New environment** → name it
      exactly **`discord`**.
- [ ] In that environment: add yourself (and/or a maintainer) as a **Required reviewer**, and under
      **Deployment branches** restrict to **`main`**. Now every live apply pauses for a human click.
- [ ] **Add the secrets to the `discord` environment** (NOT as repo-wide secrets):
      - `DISCORD_BOT_TOKEN` — the bot token from Phase 2
      - `DISCORD_GUILD_ID` — the server ID from Phase 3
      Environment-scoped secrets can't be read by the PR `validate` job — that's the safety boundary.
- [ ] *(Recommended)* Pin the `actions/checkout` and `actions/setup-python` steps in the workflow to
      full commit SHAs instead of `@v4`/`@v5` for supply-chain hardening.
- [ ] **Test it.** Open a PR that tweaks `community/server.yaml` → the `validate` check runs. Merge to
      `main` → the `apply` job starts and waits on your environment approval → approve → it syncs.
      Or trigger **Actions → Discord sync → Run workflow** manually (`mode: apply`).

> Never run `--prune` in CI (the workflow doesn't). Prune deletes channels/roles — and their message
> history — that aren't in the YAML. Only do that deliberately, locally, after a `--dry-run`.

## Phase 5 — The manual bits (the script doesn't manage these)

`discord_sync.py` manages **structure** (roles, categories, channels). These need a human in the
Discord UI; the copy to paste lives in [`COMMUNITY.md`](../COMMUNITY.md):

- [ ] **Welcome Screen** (Server Settings → Welcome Screen): short description + 2–3 channel cards
      (`#rules`, `#introduce-yourself`, `#00-foundations-help`).
- [ ] **Rules screening** (Server Settings → Membership Screening / Onboarding): require new members
      to agree before posting; point at `#rules`.
- [ ] **Track self-assign roles.** Either **Onboarding** ("Which track are you on?" → multi-select,
      mapped to the `@Foundations`…`@AI-Ops` roles) **or** a reaction-role bot (Carl-bot / Mee6) in a
      `#pick-your-tracks` post. The roles already exist after Phase 3.
- [ ] **Seed text.** Paste the blocks from `COMMUNITY.md` into `#welcome`, `#rules`, and
      `#announcements`; pin the intro template in `#introduce-yourself`; pin the forum guidelines in
      each `*-help` forum.
- [ ] **Read-only check.** `#welcome`/`#rules`/`#announcements` should already be read-only for
      `@everyone` (set by the YAML overwrites) — confirm a normal member can't post there.
- [ ] *(Optional hardening)* Set a **Verification Level** (Medium+), enable **AutoMod** spam/keyword
      rules, and require 2FA for moderation actions.

## Phase 6 — Wire the final invite into the site

If the permanent/vanity invite from Phase 1 differs from the current `discord.gg/sZjQYqVvG`, update
it in **all four** places (ask me and I'll do it in one commit):

- [ ] `README.md` — the Discord badge **and** the Community section link
- [ ] `overrides/home.html` — the hero button **and** the bottom-CTA link
- [ ] `mkdocs.yml` — `extra.social` Discord entry
- [ ] `COMMUNITY.md` — the "Join the Discord" line

Then run `mkdocs build --strict` (or just push to `main` and watch the Pages deploy go green).

---

## Quick verification checklist

- [ ] Invite link is permanent and resolves.
- [ ] Server has Community enabled; all categories/channels/roles from `server.yaml` exist.
- [ ] `python discord_sync.py server.yaml --dry-run` reports everything as already in sync.
- [ ] A PR touching `community/**` runs `validate`; merging to `main` runs `apply` and waits for approval.
- [ ] Read-only channels reject posts from a normal member; track roles are self-assignable.
- [ ] The site badge, hero buttons, and footer icon all point at the final invite.
