#!/usr/bin/env python3
"""
Link every GitHub issue from repos in manifest.yaml into the user Project.

Uses `gh` (same auth as `gh auth login`). Adding items to your project does not
open or edit issues on upstream repositories.

Usage (from repo root):
  python3 scripts/sync_upstream_issues_to_project.py
  PROJECT_NUMBER=3 PROJECT_OWNER=jiashu python3 scripts/sync_upstream_issues_to_project.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "manifest.yaml")
PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER", "3").strip()
PROJECT_OWNER = os.environ.get("PROJECT_OWNER", "jiashu").strip()

# Minimal parser for manifest.yaml `repos:` list (owner / name only).
_REPO_ENTRY = re.compile(r"^\s+-\s+owner:\s*(?P<owner>\S+)\s*$")
_REPO_NAME = re.compile(r"^\s+name:\s*(?P<name>\S+)\s*$")


def load_repos_from_manifest(path: str) -> list[dict[str, str]]:
    repos: list[dict[str, str]] = []
    current_owner: str | None = None
    with open(path, encoding="utf-8") as f:
        in_repos = False
        for line in f:
            if line.strip() == "repos:":
                in_repos = True
                continue
            if not in_repos:
                continue
            m = _REPO_ENTRY.match(line)
            if m:
                current_owner = m.group("owner")
                continue
            m = _REPO_NAME.match(line)
            if m and current_owner is not None:
                repos.append({"owner": current_owner, "name": m.group("name")})
                current_owner = None
    return repos


def run_gh(args: list[str], *, check: bool = True) -> str:
    r = subprocess.run(
        ["gh", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if check and r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        raise subprocess.CalledProcessError(r.returncode, args, r.stdout, r.stderr)
    return r.stdout


def main() -> int:
    repos = load_repos_from_manifest(MANIFEST)
    if not repos:
        print(f"No repos parsed from {MANIFEST}", file=sys.stderr)
        return 1

    issue_urls: list[str] = []
    for r in repos:
        full = f'{r["owner"]}/{r["name"]}'
        out = run_gh(
            [
                "issue",
                "list",
                "-R",
                full,
                "--state",
                "all",
                "--limit",
                "5000",
                "--json",
                "url",
            ]
        )
        for row in json.loads(out or "[]"):
            u = row.get("url")
            if u:
                issue_urls.append(u)

    # stable unique
    seen: set[str] = set()
    unique: list[str] = []
    for u in issue_urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)

    listed = run_gh(
        [
            "project",
            "item-list",
            PROJECT_NUMBER,
            "--owner",
            PROJECT_OWNER,
            "--format",
            "json",
            "-L",
            "2000",
        ]
    )
    payload = json.loads(listed or '{"items":[]}')
    items = payload.get("items") or []
    already: set[str] = set()
    for it in items:
        c = it.get("content") or {}
        if c.get("type") == "Issue" and c.get("url"):
            already.add(c["url"])

    added = 0
    skipped = 0
    errors = 0
    for u in unique:
        if u in already:
            skipped += 1
            continue
        r = subprocess.run(
            [
                "gh",
                "project",
                "item-add",
                PROJECT_NUMBER,
                "--owner",
                PROJECT_OWNER,
                "--url",
                u,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            err = (r.stderr or "") + (r.stdout or "")
            if "Content already exists in this project" in err:
                already.add(u)
                skipped += 1
                continue
            errors += 1
            print(f"FAIL {u}\n{r.stderr}", file=sys.stderr)
            continue
        already.add(u)
        added += 1

    print(
        f"Done. Repos: {len(repos)} | Issues fetched: {len(issue_urls)} | "
        f"Unique: {len(unique)} | Already on project: {skipped} | Added: {added} | Errors: {errors}"
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
