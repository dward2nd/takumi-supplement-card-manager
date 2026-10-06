#!/bin/bash
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0
uv sync --project "$CLAUDE_PROJECT_DIR/scripts/python"
exit 0