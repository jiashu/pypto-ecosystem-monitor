#!/usr/bin/env python3
"""
Collect labels, milestones, repo issue/PR-related settings, issue types, and
template paths for repos listed in manifest.yaml. Includes side-by-side
comparison and usage counts (GraphQL search + issues pagination).

Usage:
  python3 scripts/summarize_upstream_github_attributes.py > docs/upstream-issues-prs-attributes.md
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "manifest.yaml")
_REPO_ENTRY = re.compile(r"^\s+-\s+owner:\s*(?P<owner>\S+)\s*$")
_REPO_NAME = re.compile(r"^\s+name:\s*(?P<name>\S+)\s*$")

# Max search aliases per GraphQL request (stay under complexity limits).
SEARCH_BATCH = 18


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


def gh_graphql(query: str, variables: dict | None = None) -> dict | None:
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    if variables:
        for k, v in variables.items():
            if v is None:
                continue
            args.extend(["-f", f"{k}={v}"])
    r = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def gh_api_labels(owner: str, name: str) -> list[dict]:
    r = subprocess.run(
        ["gh", "api", f"repos/{owner}/{name}/labels", "--paginate", "--slurp"],
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
    q = """query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    issueTypes(first: 50) { nodes { name description isEnabled } }
  }
}"""
    data = gh_graphql(q, {"owner": owner, "name": name})
    if not data:
        return None
    repo = (data.get("data") or {}).get("repository")
    if not repo:
        return None
    return ((repo.get("issueTypes") or {}).get("nodes")) or []


def search_issues_rest_total(q: str) -> int:
    enc = quote(q, safe="")
    data = gh_api_json([f"/search/issues?q={enc}"])
    if not data or "total_count" not in data:
        return 0
    return int(data["total_count"])


def graphql_search_batch(
    items: list[tuple[str, str]],
) -> dict[str, int]:
    """items: (alias, search_query_string) -> counts. Uses issueCount on type ISSUE search."""
    out: dict[str, int] = {}
    for i in range(0, len(items), SEARCH_BATCH):
        chunk = items[i : i + SEARCH_BATCH]
        parts = []
        for alias, q in chunk:
            safe_q = q.replace("\\", "\\\\").replace('"', '\\"')
            parts.append(f'{alias}: search(query: "{safe_q}", type: ISSUE, first: 0) {{ issueCount }}')
        query = "query { " + " ".join(parts) + " }"
        data = gh_graphql(query)
        if not data or "data" not in data:
            for alias, _ in chunk:
                out[alias] = 0
            continue
        d = data["data"]
        for alias, _ in chunk:
            node = d.get(alias) if isinstance(d, dict) else None
            out[alias] = int((node or {}).get("issueCount") or 0)
        time.sleep(0.15)
    return out


def label_search_query(repo_full: str, label_name: str, kind: str) -> str:
    """kind: 'issue' or 'pr'."""
    ln = label_name.replace('"', '\\"')
    if " " in label_name or any(c in label_name for c in [":", "&"]):
        lab = f'label:"{ln}"'
    else:
        lab = f"label:{ln}"
    base = f"repo:{repo_full} {lab}"
    return f"{base} is:{kind}"


def safe_alias(prefix: str, key: str) -> str:
    h = abs(hash(key)) % (10**9)
    s = re.sub(r"[^0-9a-zA-Z_]", "_", f"{prefix}_{key}")
    if s and s[0].isdigit():
        s = "_" + s
    return (s[:40] + f"_{h:x}")[:60]


def count_issue_type_usage(owner: str, name: str) -> dict[str, int]:
    """Count issues by GraphQL issueType.name (PRs do not expose issueType)."""
    counts: dict[str, int] = defaultdict(int)
    cursor: str | None = None
    q_tmpl = """query {{
  repository(owner:"{owner}", name:"{name}") {{
    issues(first:100, states:[OPEN, CLOSED]{after}) {{
      pageInfo {{ hasNextPage endCursor }}
      nodes {{ issueType {{ name }} }}
    }}
  }}
}}"""
    while True:
        after_clause = f', after:"{cursor}"' if cursor else ""
        q = q_tmpl.format(owner=owner, name=name, after=after_clause)
        data = gh_graphql(q)
        if not data:
            break
        repo = (data.get("data") or {}).get("repository") or {}
        conn = (repo.get("issues") or {})
        nodes = conn.get("nodes") or []
        for node in nodes:
            it = node.get("issueType") or {}
            nm = it.get("name") if isinstance(it, dict) else None
            key = nm if nm else "(no type set)"
            counts[key] += 1
        pi = conn.get("pageInfo") or {}
        if not pi.get("hasNextPage"):
            break
        cursor = pi.get("endCursor")
        if not cursor:
            break
        time.sleep(0.1)
    return dict(counts)


def list_dot_github(owner: str, name: str) -> tuple[list[str], str | None]:
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


def tri_merge(a: bool | None, b: bool | None, c: bool | None) -> str:
    parts = []
    if a:
        parts.append("merge")
    if b:
        parts.append("squash")
    if c:
        parts.append("rebase")
    return "+".join(parts) if parts else "—"


def main() -> int:
    repos = load_repos(MANIFEST)
    if not repos:
        print("No repos in manifest", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []

    # Collect per-repo snapshots for comparison + detail sections.
    snapshots: list[dict] = []

    for r in repos:
        owner, name = r["owner"], r["name"]
        full = f"{owner}/{name}"
        url = f"https://github.com/{full}"
        snap: dict = {
            "full": full,
            "url": url,
            "owner": owner,
            "name": name,
            "repo": None,
            "labels": [],
            "milestones": [],
            "issue_types": None,
            "templates": [],
            "tpl_err": None,
            "open_issues": 0,
            "closed_issues": 0,
            "open_prs": 0,
            "closed_prs": 0,
            "label_usage": {},
            "milestone_usage": {},
            "issue_type_usage": {},
        }

        repo = gh_api_json([f"repos/{owner}/{name}"])
        snap["repo"] = repo
        if not repo or repo.get("message"):
            snapshots.append(snap)
            continue

        snap["open_issues"] = search_issues_rest_total(f"repo:{full} is:issue is:open")
        snap["closed_issues"] = search_issues_rest_total(f"repo:{full} is:issue is:closed")
        snap["open_prs"] = search_issues_rest_total(f"repo:{full} is:pr is:open")
        snap["closed_prs"] = search_issues_rest_total(f"repo:{full} is:pr is:closed")

        labels = gh_api_labels(owner, name)
        snap["labels"] = labels
        miles = gh_api_json([f"repos/{owner}/{name}/milestones?state=all&per_page=100"])
        snap["milestones"] = miles if isinstance(miles, list) else []

        it = issue_types(owner, name)
        snap["issue_types"] = it

        tpls, err = list_dot_github(owner, name)
        snap["templates"] = tpls
        snap["tpl_err"] = err

        # Label usage: batch GraphQL searches
        batch: list[tuple[str, str]] = []
        label_keys: list[tuple[str, str, str]] = []
        for lb in labels:
            lname = lb.get("name") or ""
            if not lname:
                continue
            for kind in ("issue", "pr"):
                q = label_search_query(full, lname, kind)
                al = safe_alias(f"L_{kind}", f"{full}_{lname}")
                batch.append((al, q))
                label_keys.append((lname, kind, al))
        counts = graphql_search_batch(batch)
        usage: dict[str, dict[str, int]] = {}
        for lname, kind, al in label_keys:
            usage.setdefault(lname, {"issue": 0, "pr": 0})
            usage[lname][kind if kind == "issue" else "pr"] = counts.get(al, 0)
        snap["label_usage"] = usage

        # Milestone usage
        batch_m: list[tuple[str, str]] = []
        ms_keys: list[tuple[str, str, str]] = []
        for m in snap["milestones"]:
            title = m.get("title") or ""
            if not title:
                continue
            mt = title.replace('"', '\\"')
            for kind in ("issue", "pr"):
                q = f'repo:{full} milestone:"{mt}" is:{kind}'
                al = safe_alias(f"M_{kind}", f"{full}_{title}")
                batch_m.append((al, q))
                ms_keys.append((title, kind, al))
        mc = graphql_search_batch(batch_m)
        musage: dict[str, dict[str, int]] = {}
        for title, kind, al in ms_keys:
            musage.setdefault(title, {"issue": 0, "pr": 0})
            musage[title]["issue" if kind == "issue" else "pr"] = mc.get(al, 0)
        snap["milestone_usage"] = musage

        snap["issue_type_usage"] = count_issue_type_usage(owner, name)
        snapshots.append(snap)
        time.sleep(0.2)

    lines.extend(
        [
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
            "| **Label / milestone counts** | From GitHub search (`issueCount` / `total_count`): items with that label or milestone. Split into **issues** vs **PRs**. |",
            "| **Issue type usage** | Count of **issues** (`issueType` on each issue). Pull requests do not support issue types in the API. `(no type set)` = issue has no type. |",
            "| **Open / closed** | Search: `is:issue`/`is:pr` with `is:open` or `is:closed`. |",
            "| **Side-by-side** | Same metrics per repo for quick comparison. |",
            "| **Null merge settings** | REST may return `null` for merge flags (`allow_*_merge`); shown as **—** (org/default may still apply). |",
            "",
            "## Side-by-side comparison",
            "",
        ]
    )

    headers = ["Metric"] + [f"[{s['full']}]({s['url']})" for s in snapshots]

    def row(metric: str, cells: list[str]) -> None:
        lines.append("| " + " | ".join([metric] + cells) + " |")

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    row(
        "`has_issues`",
        [cell((s["repo"] or {}).get("has_issues")) for s in snapshots],
    )
    row(
        "`has_discussions`",
        [cell((s["repo"] or {}).get("has_discussions")) for s in snapshots],
    )
    row(
        "Merge strategies enabled",
        [
            tri_merge(
                (s["repo"] or {}).get("allow_merge_commit"),
                (s["repo"] or {}).get("allow_squash_merge"),
                (s["repo"] or {}).get("allow_rebase_merge"),
            )
            for s in snapshots
        ],
    )
    row(
        "`delete_branch_on_merge`",
        [cell((s["repo"] or {}).get("delete_branch_on_merge")) for s in snapshots],
    )
    row("Open issues (search)", [str(s["open_issues"]) for s in snapshots])
    row("Closed issues (search)", [str(s["closed_issues"]) for s in snapshots])
    row("Open PRs (search)", [str(s["open_prs"]) for s in snapshots])
    row("Closed PRs (search)", [str(s["closed_prs"]) for s in snapshots])
    row(
        "Labels defined (count)",
        [str(len(s["labels"])) if s["repo"] else "—" for s in snapshots],
    )
    row(
        "Milestones defined (count)",
        [str(len(s["milestones"])) if s["repo"] else "—" for s in snapshots],
    )
    row(
        "Issue types configured",
        [
            (
                ", ".join(
                    esc(n.get("name"))
                    for n in (s["issue_types"] or [])
                    if n.get("isEnabled")
                )
                if s["issue_types"]
                else ("—" if s["issue_types"] is None else "*(none)*")
            )
            or "*(none enabled)*"
            for s in snapshots
        ],
    )
    row(
        "Template-related `.github` paths",
        [str(len(s["templates"])) if s["repo"] else "—" for s in snapshots],
    )
    lines.append("")

    # Per-repo detail
    for snap in snapshots:
        full, url = snap["full"], snap["url"]
        lines.append(f"## [{full}]({url})")
        lines.append("")

        repo = snap["repo"]
        if not repo:
            lines.append("*Could not read repository via API (missing, private without auth, or rate limit).*")
            lines.append("")
            continue

        if repo.get("message"):
            lines.append(f"*API: {esc(repo.get('message'))}*")
            lines.append("")
            continue

        lines.append("### Counts (search)")
        lines.append("")
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| Open issues | {snap['open_issues']} |")
        lines.append(f"| Closed issues | {snap['closed_issues']} |")
        lines.append(f"| Open PRs | {snap['open_prs']} |")
        lines.append(f"| Closed PRs | {snap['closed_prs']} |")
        lines.append("")

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

        it = snap["issue_types"]
        lines.append("### Issue types (configuration + issue usage counts)")
        lines.append("")
        usage = snap["issue_type_usage"]
        if it is None:
            lines.append("*GraphQL `issueTypes` unavailable or query failed for this repo.*")
        elif not it:
            lines.append("*No issue types returned (feature may be off or org policy).*")
            if usage:
                lines.append("")
                lines.append("| Tally (all issues, by `issueType`) | Count |")
                lines.append("|-------------------------------------|-------|")
                for k, v in sorted(usage.items(), key=lambda x: (-x[1], x[0])):
                    lines.append(f"| {esc(k)} | {v} |")
        else:
            lines.append("| Name | Enabled | Description | Issues w/ type (count) |")
            lines.append("|------|---------|-------------|------------------------|")
            no_type = usage.get("(no type set)", 0)
            for node in it:
                nm = node.get("name") or ""
                cnt = usage.get(nm, 0)
                lines.append(
                    f"| {esc(nm)} | {cell(node.get('isEnabled'))} | {esc(node.get('description'))} | {cnt} |"
                )
            lines.append(f"| `*(no type set)*` | — | — | {no_type} |")
            lines.append("")
            lines.append(
                "*Issue type counts come from paginating all issues in the repo; PRs do not expose `issueType` in the GraphQL API.*"
            )
        lines.append("")

        labels = snap["labels"]
        lines.append(f"### Labels ({len(labels)} total) with usage")
        lines.append("")
        if not labels:
            lines.append("*No labels or could not list.*")
        else:
            lines.append(
                "| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |"
            )
            lines.append("|------|-------|---------|-------------|-----------------|--------------|-------|")
            lu = snap["label_usage"]
            for lb in sorted(labels, key=lambda x: (x.get("name") or "").lower()):
                lname = lb.get("name") or ""
                u = lu.get(lname, {"issue": 0, "pr": 0})
                ti, tp = u["issue"], u["pr"]
                lines.append(
                    f"| `{esc(lname)}` | `{esc(lb.get('color'))}` | "
                    f"{cell(lb.get('default'))} | {esc(lb.get('description'))} | "
                    f"{ti} | {tp} | {ti + tp} |"
                )
        lines.append("")

        miles = snap["milestones"]
        lines.append("### Milestones with usage")
        lines.append("")
        if not miles:
            lines.append("*None or not accessible.*")
        else:
            lines.append("| Title | State | Description | Due | Issues | PRs | Total |")
            lines.append("|-------|-------|-------------|-----|--------|-----|-------|")
            mu = snap["milestone_usage"]
            for m in sorted(miles, key=lambda x: (x.get("title") or "").lower()):
                title = m.get("title") or ""
                u = mu.get(title, {"issue": 0, "pr": 0})
                ti, tp = u["issue"], u["pr"]
                due = m.get("due_on") or "—"
                lines.append(
                    f"| {esc(title)} | {esc(m.get('state'))} | {esc(m.get('description'))} | "
                    f"{esc(due) if due != '—' else '—'} | {ti} | {tp} | {ti + tp} |"
                )
        lines.append("")

        tpls, err = snap["templates"], snap["tpl_err"]
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
