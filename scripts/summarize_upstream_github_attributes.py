#!/usr/bin/env python3
"""
Collect labels, milestones, repo issue/PR-related settings, issue types, and
template paths for repos listed in manifest.yaml. Writes Markdown to stdout.

Usage:
  python3 scripts/summarize_upstream_github_attributes.py > docs/upstream-issues-prs-attributes.md
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "manifest.yaml")
_REPO_ENTRY = re.compile(r"^\s+-\s+owner:\s*(?P<owner>\S+)\s*$")
_REPO_NAME = re.compile(r"^\s+name:\s*(?P<name>\S+)\s*$")


def load_repos(path: str) -> list[dict[str, str]]:
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


def gh_api_json(args: list[str]) -> object | None:
    r = subprocess.run(
        ["gh", "api", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if r.returncode != 0:
        return None
    if not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def gh_api_labels(owner: str, name: str) -> list[dict]:
    r = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{owner}/{name}/labels",
            "--paginate",
            "--slurp",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if r.returncode != 0:
        return []
    try:
        pages = json.loads(r.stdout)
    except json.JSONDecodeError:
        return []
    if not isinstance(pages, list):
        return []
    out: list[dict] = []
    for page in pages:
        if isinstance(page, list):
            out.extend(page)
    return out


def issue_types(owner: str, name: str) -> list[dict] | None:
    q = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    issueTypes(first: 50) {
      nodes { name description isEnabled }
    }
  }
}
"""
    r = subprocess.run(
        ["gh", "api", "graphql", "-f", f"query={q}", "-f", f"owner={owner}", "-f", f"name={name}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if r.returncode != 0:
        return None
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None
    repo = (data.get("data") or {}).get("repository")
    if not repo:
        return None
    nodes = ((repo.get("issueTypes") or {}).get("nodes")) or []
    return nodes


def list_dot_github(owner: str, name: str) -> tuple[list[str], str | None]:
    """Return (relevant paths under .github/, error note)."""
    raw = gh_api_json([f"repos/{owner}/{name}/contents/.github"])
    if raw is None:
        return [], "`.github` not present or not accessible"
    if not isinstance(raw, list):
        return [], "unexpected `.github` response"
    names: list[str] = []
    for item in raw:
        n = item.get("name") or ""
        t = item.get("type") or ""
        if not (
            "ISSUE" in n.upper()
            or "PULL_REQUEST" in n.upper()
            or n.lower() == "issue_template"
        ):
            continue
        if t == "dir":
            names.append(f"{n}/")
            sub = gh_api_json([f"repos/{owner}/{name}/contents/.github/{n}"])
            if isinstance(sub, list):
                for ch in sub:
                    cn = ch.get("name") or ""
                    names.append(f"{n}/{cn}")
        else:
            names.append(n)
    return sorted(set(names)), None


def esc(s: str | None) -> str:
    if s is None:
        return ""
    return str(s).replace("|", "\\|").replace("\n", " ")


def cell(v: object) -> str:
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "true" if v else "false"
    return esc(str(v))


def main() -> int:
    repos = load_repos(MANIFEST)
    if not repos:
        print("No repos in manifest", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Upstream repos: issues, PRs, labels, and related GitHub settings",
        "",
        f"_Generated **{now}** by `scripts/summarize_upstream_github_attributes.py` using `gh api` (read-only)._",
        "",
        "Repositories are those listed in [`manifest.yaml`](../manifest.yaml). **Issues and pull requests share the same label namespace** on each repository (GitHub does not maintain separate label sets).",
        "",
        "## Legend",
        "",
        "| Concept | Meaning |",
        "|---------|---------|",
        "| **Labels** | Repo-wide; apply to issues and PRs |",
        "| **Milestones** | Grouping for issues and PRs |",
        "| **Issue types** | Repository issue types (GraphQL `issueTypes`), when enabled |",
        "| **PR merge** | Repository settings for allowed merge strategies |",
        "| **Templates** | Files under `.github/` related to issues or PRs (names only) |",
        "",
    ]

    for r in repos:
        owner, name = r["owner"], r["name"]
        full = f"{owner}/{name}"
        url = f"https://github.com/{full}"
        lines.append(f"## [{full}]({url})")
        lines.append("")

        repo = gh_api_json([f"repos/{owner}/{name}"])
        if not repo:
            lines.append("*Could not read repository via API (missing, private without auth, or rate limit).*")
            lines.append("")
            continue

        if repo.get("message"):
            lines.append(f"*API: {esc(repo.get('message'))}*")
            lines.append("")
            continue

        lines.append("### Repository flags (issues / PRs / collaboration)")
        lines.append("")
        lines.append("| Attribute | Value |")
        lines.append("|-----------|-------|")
        flags = [
            ("`has_issues`", repo.get("has_issues")),
            ("`has_projects`", repo.get("has_projects")),
            ("`has_wiki`", repo.get("has_wiki")),
            ("`has_discussions`", repo.get("has_discussions")),
            ("`archived`", repo.get("archived")),
            ("`disabled`", repo.get("disabled")),
            ("`default_branch`", f"`{repo.get('default_branch')}`" if repo.get("default_branch") else "—"),
            ("`visibility`", repo.get("visibility")),
        ]
        for k, v in flags:
            lines.append(f"| {k} | {cell(v)} |")
        lines.append("")

        lines.append("### Pull request merge settings")
        lines.append("")
        lines.append("| Setting | Value |")
        lines.append("|---------|-------|")
        pr_settings = [
            ("`allow_merge_commit`", repo.get("allow_merge_commit")),
            ("`allow_squash_merge`", repo.get("allow_squash_merge")),
            ("`allow_rebase_merge`", repo.get("allow_rebase_merge")),
            ("`allow_auto_merge`", repo.get("allow_auto_merge")),
            ("`allow_update_branch`", repo.get("allow_update_branch")),
            ("`delete_branch_on_merge`", repo.get("delete_branch_on_merge")),
            ("`squash_merge_commit_title`", esc(str(repo.get("squash_merge_commit_title") or "—"))),
            ("`squash_merge_commit_message`", esc(str(repo.get("squash_merge_commit_message") or "—"))),
            ("`merge_commit_title`", esc(str(repo.get("merge_commit_title") or "—"))),
            ("`merge_commit_message`", esc(str(repo.get("merge_commit_message") or "—"))),
        ]
        for k, v in pr_settings:
            lines.append(f"| {k} | {cell(v)} |")
        lines.append("")

        it = issue_types(owner, name)
        lines.append("### Issue types (if configured)")
        lines.append("")
        if it is None:
            lines.append("*GraphQL `issueTypes` unavailable or query failed for this repo.*")
        elif not it:
            lines.append("*No issue types returned (feature may be off or org policy).*")
        else:
            lines.append("| Name | Enabled | Description |")
            lines.append("|------|---------|-------------|")
            for node in it:
                lines.append(
                    f"| {esc(node.get('name'))} | {cell(node.get('isEnabled'))} | {esc(node.get('description'))} |"
                )
        lines.append("")

        labels = gh_api_labels(owner, name)
        lines.append(f"### Labels ({len(labels)} total)")
        lines.append("")
        if not labels:
            lines.append("*No labels or could not list.*")
        else:
            lines.append("| Name | Color | Default | Description |")
            lines.append("|------|-------|---------|-------------|")
            for lb in sorted(labels, key=lambda x: (x.get("name") or "").lower()):
                lines.append(
                    f"| `{esc(lb.get('name'))}` | `{esc(lb.get('color'))}` | "
                    f"{cell(lb.get('default'))} | {esc(lb.get('description'))} |"
                )
        lines.append("")

        miles = gh_api_json([f"repos/{owner}/{name}/milestones?state=all&per_page=100"])
        lines.append("### Milestones")
        lines.append("")
        if not miles or not isinstance(miles, list):
            lines.append("*None or not accessible.*")
        else:
            lines.append("| Title | State | Description | Due |")
            lines.append("|-------|-------|-------------|-----|")
            for m in sorted(miles, key=lambda x: (x.get("title") or "").lower()):
                due = m.get("due_on") or "—"
                lines.append(
                    f"| {esc(m.get('title'))} | {esc(m.get('state'))} | {esc(m.get('description'))} | {esc(due) if due != '—' else '—'} |"
                )
        lines.append("")

        tpls, err = list_dot_github(owner, name)
        lines.append("### `.github` issue / PR template paths (top-level names)")
        lines.append("")
        if err:
            lines.append(f"*{err}*")
        elif not tpls:
            lines.append("*No matching template entries found at `.github/` root (or only nested paths).*")
        else:
            for t in tpls:
                lines.append(f"- `{t}`")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "GitHub **Projects** custom fields are defined per **Project**, not per repository; "
        "they are not included here. For your monitor board, see the project UI or "
        "`gh project field-list` for [PyPTO upstream monitor](https://github.com/users/jiashu/projects/3)."
    )
    lines.append("")

    sys.stdout.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
