#!/bin/bash
# SessionStart hook: readies a cloud session (Claude Code on the web); a no-op on the Mac.
# deterministic + idempotent — safe to re-run.
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0

uv sync --quiet --project "$CLAUDE_PROJECT_DIR/scripts/python" >&2

# The cloud image sets UV_NATIVE_TLS, which uv deprecated: every `uv run` then
# warns on stderr, and the warning corrupts a CLI's JSON captured with 2>&1.
# UV_SYSTEM_CERTS is its replacement. CLAUDE_ENV_FILE is sourced before each
# Bash command.
if [ -n "$CLAUDE_ENV_FILE" ] && [ -n "$UV_NATIVE_TLS" ]; then
  printf 'unset UV_NATIVE_TLS\nexport UV_SYSTEM_CERTS=true\n' >> "$CLAUDE_ENV_FILE"
fi
# settings.json's UV_PROJECT is relative, so `uv run` from inside scripts/python
# looks for scripts/python/scripts/python. Pin it to the clone.
[ -n "$CLAUDE_ENV_FILE" ] && echo "export UV_PROJECT=\"$CLAUDE_PROJECT_DIR/scripts/python\"" >> "$CLAUDE_ENV_FILE"

# Stdout lands in Claude's context: name the secrets this session is missing.
[ -n "$NOTION_TOKEN" ] || echo "Cloud session: NOTION_TOKEN is not set, so every scripts/python CLI will fail. The user adds it in the cloud environment's settings (see CLAUDE.md, Cloud sessions)."
if [ -n "$STATEMENT_PASSWORDS_YAML" ]; then
  bad=$(cd "$CLAUDE_PROJECT_DIR/scripts/python" && uv run --quiet python -c \
    'from lib.statement_secrets import malformed_issuers; print(", ".join(malformed_issuers()))' 2>/dev/null)
  [ -z "$bad" ] || echo "Cloud session: STATEMENT_PASSWORDS_YAML has unusable entries for: $bad (likely a missing quote or brace; see README). Tell the user; never print the value."
fi
[ -n "$STATEMENT_PASSWORDS_YAML" ] || echo "Cloud session: STATEMENT_PASSWORDS_YAML is not set, so encrypted statement PDFs (Krungsri family, ttb, CardX) won't open. The user adds it in the cloud environment's settings (see CLAUDE.md, Cloud sessions)."
exit 0
