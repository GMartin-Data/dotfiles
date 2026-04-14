<important>
## Banking Constraints
- Security posture: fail-closed over fail-open, explicit allowlists over denylists
- All changes must be auditable and traceable — prefer git-versioned config over ephemeral state
- Never force push, never rm -rf on project directories
- Four-eyes principle: no self-merge, all PRs require review
- No secrets in code — use environment variables or secret managers exclusively
- When in doubt on a security or compliance decision, ask — don't assume permissive defaults
</important>