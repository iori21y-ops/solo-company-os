#!/bin/bash
# Hand the long-lived Claude Code token (made with `claude setup-token`) to every launchd job of this user, so unattended
# `claude -p` calls do not stop when the browser sign-in expires. launchd com.solo.claude-token runs this at login and
# whenever the token file changes. The token stays in the file; nothing here prints it.
# Renew: run `claude setup-token` again and save it to the same file (steps: _meta/scripts/README.md).
F="$HOME/.cadam-secrets/claude_oauth_token"
if [ -s "$F" ]; then
  launchctl setenv CLAUDE_CODE_OAUTH_TOKEN "$(tr -d '[:space:]' < "$F")"
  echo "$(date '+%F %T') token set for launchd jobs ($(wc -c < "$F" | tr -d ' ') chars)"
else
  launchctl unsetenv CLAUDE_CODE_OAUTH_TOKEN
  echo "$(date '+%F %T') token file missing or empty — unset (jobs fall back to the browser sign-in)"
fi
