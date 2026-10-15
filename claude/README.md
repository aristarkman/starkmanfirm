# Setting up automatic blog publishing

**Read this once, do the three steps, and the blog publishes itself from then on.**

## Why this exists

The biweekly post used to be written by a scheduled Claude task running in a sandbox.
That sandbox could *download* this repo but could not *upload* to it — its git proxy only
hands over a credential for repositories attached to the session, and a Project-attached
scheduled task has no place to attach one. Five runs in a row ended the same way:

```
remote: access denied by the git proxy: aristarkman/starkmanfirm is not in this
session's authorized repository set
fatal: The requested URL returned error: 403
```

Every post then had to be hand-delivered as a zip and dragged into GitHub. That worked
when it was remembered. The Oct 1 2026 post sat unpublished for two weeks when it wasn't.

A GitHub Action runs **inside GitHub**, where pushing is native. No proxy, no permission
list, nothing that can quietly go empty.

## What happens once it's on

On the 1st and 15th at 13:17 UTC, the workflow:

1. Checks out the site and installs Python + Playwright.
2. Runs Claude Code with `claude/blog-playbook.md` as its instructions.
3. Picks the top unused topic from the playbook's queue.
4. Researches it and verifies every statute, figure and deadline against a primary source.
5. Builds the English and Spanish pages, both index cards and the sitemap entries.
6. Runs all five checks in `claude/scripts/verify_site.py`.
7. **Opens a pull request** — it never merges. If a check fails it opens an issue instead.

You review and merge. Netlify deploys on the merge.

---

## Step 1 — Install the Claude GitHub App

Go to **https://github.com/apps/claude** → **Install** (or **Configure**) →
**Only select repositories** → pick **starkmanfirm** → save.

The Action needs three of its permissions: Contents (read/write), Issues (read/write) and
Pull requests (read/write).

## Step 2 — Add one secret

In this repo: **Settings → Secrets and variables → Actions → New repository secret**.

Pick whichever is easier:

| Secret name | Where it comes from | Billing |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | run `claude setup-token` in a terminal on your Mac (needs the Claude Code CLI) | your Claude subscription |
| `ANTHROPIC_API_KEY` | create a key at https://platform.claude.com | separate API billing — set a spend limit |

The workflow is set up for `CLAUDE_CODE_OAUTH_TOKEN`. If you use the API key instead, open
`.github/workflows/biweekly-blog-post.yml` and swap these two lines:

```yaml
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          # anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

to:

```yaml
          # claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Step 3 — Test it before trusting the schedule

Go to **Actions → Biweekly blog post → Run workflow**. You can type a topic in the box to
force one, or leave it blank to take the top of the queue.

Watch the run. If it finishes with a pull request, you're done. If it fails, the log says
where — most first-run failures are the secret being missing or misnamed.

**Do this once manually.** Do not wait until the 1st to find out.

---

## Things worth knowing

- **Turn off the old scheduled task** once a run has succeeded, or you'll get two posts a
  cycle. It's in the Claude app under Scheduled tasks → "Starkman Firm — biweekly blog
  post" → toggle Active off.
- **Public repos disable cron after 60 days of no activity.** Merging a post every two
  weeks is activity, so this should never trigger — but if the blog goes quiet for two
  months, GitHub silently stops the schedule and you re-enable it in the Actions tab.
- **Scheduled runs are attributed to whoever last edited the cron line.** That'll be you,
  which is what the Action wants. If a bot ever edits it, the run is rejected until that
  bot is listed in `allowed_bots`.
- **Cost control.** `--max-turns 120` and `timeout-minutes: 60` cap a runaway run. Lower
  them if runs come in cheap; raise them if posts come out truncated.
- **The model** is whatever Claude Code defaults to. To pin one, add
  `--model <name>` to the `claude_args` block.

## If you'd rather it just pushed to main

Change step 5 of the prompt in the workflow to commit directly to `main` instead of
opening a PR. I'd argue against it. These posts assert statutes, dollar figures and filing
deadlines under Morris's bar license, and the review gate costs you one tap on a phone.

## Files in here

| Path | What it is |
|---|---|
| `blog-playbook.md` | Firm details, voice, topic queue, what's published, verified facts and the fact-check traps. **The instructions the job actually follows.** |
| `site-build-notes.md` | The exact recipe for adding a page to this codebase. |
| `scripts/build_post.py` | Builds both pages, both index cards and the sitemap entries from a copy module. Generic — needs no editing between cycles. |
| `scripts/verify_site.py` | The five pre-ship checks. Exit 0 means safe to ship. |
| `scripts/copy_<date>.py` | One post's copy. Saved per cycle so any post can be rebuilt. |
| `posts/<date>-<slug>.md` | The Markdown draft and its dated source table. |
