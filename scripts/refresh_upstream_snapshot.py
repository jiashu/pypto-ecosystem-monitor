#!/usr/bin/env python3
"""Read manifest.yaml and write generated/upstream-snapshot.md from GitHub API (read-only)."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "manifest.yaml")
OUT = os.path.join(ROOT, "generated", "upstream-snapshot.md")


def api_get(path: str, token: str) -> dict:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pypto-ecosystem-monitor-snapshot",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1

    with open(MANIFEST, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    repos = data.get("repos") or []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Upstream snapshot",
        "",
        f"_Generated at **{now}** by `scripts/refresh_upstream_snapshot.py` (read-only API)._",
        "",
        "| Repository | Stars | Open issues | Default branch | Pushed at (default branch activity) | Description |",
        "| ---------- | ----- | ----------- | -------------- | ------------------------------------ | ----------- |",
    ]

    for r in repos:
        owner = r["owner"]
        name = r["name"]
        path = f"/repos/{owner}/{name}"
        try:
            j = api_get(path, token)
        except urllib.error.HTTPError as e:
            lines.append(
                f"| [{owner}/{name}](https://github.com/{owner}/{name}) | — | — | — | **error {e.code}** | |"
            )
            continue
        desc = (j.get("description") or "").replace("|", "\\|").replace("\n", " ")
        pushed = j.get("pushed_at") or "—"
        lines.append(
            f"| [{owner}/{name}]({j.get('html_url', f'https://github.com/{owner}/{name}')}) "
            f"| {j.get('stargazers_count', '—')} "
            f"| {j.get('open_issues_count', '—')} "
            f"| `{j.get('default_branch', '—')}` "
            f"| {pushed} "
            f"| {desc} |"
        )

    lines.append("")
    lines.append(
        "This file is committed only to **this** repository. "
        "No issues, PRs, or tags are created on upstream repos by this job."
    )
    lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
