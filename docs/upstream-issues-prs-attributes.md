# Upstream repos: issues, PRs, labels, and related GitHub settings

_Generated **2026-03-24 03:09 UTC** by `scripts/summarize_upstream_github_attributes.py` using `gh api` (read-only)._

Repositories are those listed in [`manifest.yaml`](../manifest.yaml). **Issues and pull requests share the same label namespace** on each repository (GitHub does not maintain separate label sets).

## Legend

| Concept | Meaning |
|---------|---------|
| **Label / milestone counts** | From GitHub search (`issueCount` / `total_count`): items with that label or milestone. Split into **issues** vs **PRs**. |
| **Issue type usage** | Count of **issues** (`issueType` on each issue). Pull requests do not support issue types in the API. `(no type set)` = issue has no type. |
| **Open / closed** | Search: `is:issue`/`is:pr` with `is:open` or `is:closed`. |
| **Side-by-side** | Same metrics per repo for quick comparison. |
| **Null merge settings** | REST may return `null` for merge flags (`allow_*_merge`); shown as **—** (org/default may still apply). |

## Side-by-side comparison

| Metric | [hengliao1972/pypto_top_level_design_documents](https://github.com/hengliao1972/pypto_top_level_design_documents) | [hw-native-sys/pypto](https://github.com/hw-native-sys/pypto) | [hw-native-sys/simpler](https://github.com/hw-native-sys/simpler) | [hengliao1972/pypto_runtime_distributed](https://github.com/hengliao1972/pypto_runtime_distributed) | [zhangstevenunity/PTOAS](https://github.com/zhangstevenunity/PTOAS) | [PTO-ISA/pto-isa](https://github.com/PTO-ISA/pto-isa) | [hw-native-sys/pypto-lib](https://github.com/hw-native-sys/pypto-lib) | [hengliao1972/pypto-serving](https://github.com/hengliao1972/pypto-serving) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `has_issues` | true | true | true | true | true | true | true | true |
| `has_discussions` | false | true | false | false | true | false | false | false |
| Merge strategies enabled | — | — | — | — | — | — | — | — |
| `delete_branch_on_merge` | — | — | — | — | — | — | — | — |
| Open issues (search) | 0 | 37 | 3 | 0 | 17 | 0 | 2 | 0 |
| Closed issues (search) | 0 | 125 | 9 | 0 | 60 | 6 | 0 | 0 |
| Open PRs (search) | 0 | 5 | 13 | 0 | 12 | 1 | 3 | 0 |
| Closed PRs (search) | 0 | 521 | 324 | 1 | 248 | 13 | 33 | 0 |
| Labels defined (count) | 9 | 11 | 9 | 9 | 10 | 9 | 9 | 9 |
| Milestones defined (count) | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Issue types configured | *(none)* | Task, Bug, Feature | Task, Bug, Feature | *(none)* | *(none)* | Task, Bug, Feature | Task, Bug, Feature | *(none)* |
| Template-related `.github` paths | 0 | 9 | 7 | 0 | 8 | 0 | 5 | 0 |

## [hengliao1972/pypto_top_level_design_documents](https://github.com/hengliao1972/pypto_top_level_design_documents)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 0 |
| Closed issues | 0 |
| Open PRs | 0 |
| Closed PRs | 0 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | true |
| `has_discussions` | false |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

*No issue types returned (feature may be off or org policy).*

### Labels (9 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 0 | 0 | 0 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 0 | 0 | 0 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 0 | 0 | 0 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

*`.github` not present or not accessible*

## [hw-native-sys/pypto](https://github.com/hw-native-sys/pypto)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 37 |
| Closed issues | 125 |
| Open PRs | 5 |
| Closed PRs | 521 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | false |
| `has_wiki` | false |
| `has_discussions` | true |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

| Name | Enabled | Description | Issues w/ type (count) |
|------|---------|-------------|------------------------|
| Task | true | A specific piece of work | 0 |
| Bug | true | An unexpected problem or behavior | 0 |
| Feature | true | A request, idea, or new functionality | 0 |
| `*(no type set)*` | — | — | 162 |

*Issue type counts come from paginating all issues in the repo; PRs do not expose `issueType` in the GraphQL API.*

### Labels (11 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 55 | 0 | 55 |
| `code health` | `c5def5` | false | Technical debt, robustness concerns, code quality improvements | 20 | 0 | 20 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 2 | 0 | 2 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 55 | 0 | 55 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `Tracking` | `ce357b` | false | Tracking the roadmap or other process | 3 | 0 | 3 |
| `wontfix` | `ffffff` | true | This will not be worked on | 1 | 0 | 1 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

- `ISSUE_TEMPLATE/`
- `ISSUE_TEMPLATE/bug_report.yml`
- `ISSUE_TEMPLATE/code_health.yml`
- `ISSUE_TEMPLATE/config.yml`
- `ISSUE_TEMPLATE/documentation.yml`
- `ISSUE_TEMPLATE/feature_request.yml`
- `ISSUE_TEMPLATE/new_operation.yml`
- `ISSUE_TEMPLATE/pass_bug.yml`
- `ISSUE_TEMPLATE/performance_issue.yml`

## [hw-native-sys/simpler](https://github.com/hw-native-sys/simpler)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 3 |
| Closed issues | 9 |
| Open PRs | 13 |
| Closed PRs | 324 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | true |
| `has_discussions` | false |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

| Name | Enabled | Description | Issues w/ type (count) |
|------|---------|-------------|------------------------|
| Task | true | A specific piece of work | 0 |
| Bug | true | An unexpected problem or behavior | 0 |
| Feature | true | A request, idea, or new functionality | 0 |
| `*(no type set)*` | — | — | 12 |

*Issue type counts come from paginating all issues in the repo; PRs do not expose `issueType` in the GraphQL API.*

### Labels (9 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 0 | 0 | 0 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 0 | 0 | 0 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 0 | 0 | 0 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

| Title | State | Description | Due | Issues | PRs | Total |
|-------|-------|-------------|-----|--------|-----|-------|
| 126 | open |  | — | 0 | 0 | 0 |

### `.github` issue / PR template paths (top-level names)

- `ISSUE_TEMPLATE/`
- `ISSUE_TEMPLATE/bug_report.yml`
- `ISSUE_TEMPLATE/code_health.yml`
- `ISSUE_TEMPLATE/config.yml`
- `ISSUE_TEMPLATE/documentation.yml`
- `ISSUE_TEMPLATE/feature_request.yml`
- `ISSUE_TEMPLATE/performance_issue.yml`

## [hengliao1972/pypto_runtime_distributed](https://github.com/hengliao1972/pypto_runtime_distributed)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 0 |
| Closed issues | 0 |
| Open PRs | 0 |
| Closed PRs | 1 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | true |
| `has_discussions` | false |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

*No issue types returned (feature may be off or org policy).*

### Labels (9 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 0 | 0 | 0 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 0 | 0 | 0 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 0 | 0 | 0 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

*`.github` not present or not accessible*

## [zhangstevenunity/PTOAS](https://github.com/zhangstevenunity/PTOAS)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 17 |
| Closed issues | 60 |
| Open PRs | 12 |
| Closed PRs | 248 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | true |
| `has_discussions` | true |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

*No issue types returned (feature may be off or org policy).*

| Tally (all issues, by `issueType`) | Count |
|-------------------------------------|-------|
| (no type set) | 77 |

### Labels (10 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 13 | 0 | 13 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 3 | 0 | 3 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 8 | 0 | 8 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `pypto` | `c434b7` | false |  | 4 | 0 | 4 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

- `ISSUE_TEMPLATE/`
- `ISSUE_TEMPLATE/bug_report.yml`
- `ISSUE_TEMPLATE/config.yml`
- `ISSUE_TEMPLATE/documentation.yml`
- `ISSUE_TEMPLATE/feature_request.yml`
- `ISSUE_TEMPLATE/new_operation.yml`
- `ISSUE_TEMPLATE/pass_bug.yml`
- `ISSUE_TEMPLATE/performance_issue.yml`

## [PTO-ISA/pto-isa](https://github.com/PTO-ISA/pto-isa)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 0 |
| Closed issues | 6 |
| Open PRs | 1 |
| Closed PRs | 13 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | true |
| `has_discussions` | false |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

| Name | Enabled | Description | Issues w/ type (count) |
|------|---------|-------------|------------------------|
| Task | true | A specific piece of work | 0 |
| Bug | true | An unexpected problem or behavior | 0 |
| Feature | true | A request, idea, or new functionality | 0 |
| `*(no type set)*` | — | — | 6 |

*Issue type counts come from paginating all issues in the repo; PRs do not expose `issueType` in the GraphQL API.*

### Labels (9 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 0 | 0 | 0 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 0 | 0 | 0 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 0 | 0 | 0 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

*No matching template entries found at `.github/` root (or only nested paths).*

## [hw-native-sys/pypto-lib](https://github.com/hw-native-sys/pypto-lib)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 2 |
| Closed issues | 0 |
| Open PRs | 3 |
| Closed PRs | 33 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | false |
| `has_discussions` | false |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

| Name | Enabled | Description | Issues w/ type (count) |
|------|---------|-------------|------------------------|
| Task | true | A specific piece of work | 0 |
| Bug | true | An unexpected problem or behavior | 0 |
| Feature | true | A request, idea, or new functionality | 0 |
| `*(no type set)*` | — | — | 2 |

*Issue type counts come from paginating all issues in the repo; PRs do not expose `issueType` in the GraphQL API.*

### Labels (9 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 0 | 0 | 0 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 0 | 0 | 0 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 1 | 0 | 1 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

- `ISSUE_TEMPLATE/`
- `ISSUE_TEMPLATE/bug_report.yml`
- `ISSUE_TEMPLATE/config.yml`
- `ISSUE_TEMPLATE/documentation.yml`
- `ISSUE_TEMPLATE/feature_request.yml`

## [hengliao1972/pypto-serving](https://github.com/hengliao1972/pypto-serving)

### Counts (search)

| Metric | Count |
|--------|-------|
| Open issues | 0 |
| Closed issues | 0 |
| Open PRs | 0 |
| Closed PRs | 0 |

### Repository flags (issues / PRs / collaboration)

| Attribute | Value |
|-----------|-------|
| `has_issues` | true |
| `has_projects` | true |
| `has_wiki` | true |
| `has_discussions` | false |
| `archived` | false |
| `disabled` | false |
| `default_branch` | `main` |
| `visibility` | public |

### Pull request merge settings

| Setting | Value |
|---------|-------|
| `allow_merge_commit` | — |
| `allow_squash_merge` | — |
| `allow_rebase_merge` | — |
| `allow_auto_merge` | — |
| `allow_update_branch` | — |
| `delete_branch_on_merge` | — |
| `squash_merge_commit_title` | — |
| `squash_merge_commit_message` | — |
| `merge_commit_title` | — |
| `merge_commit_message` | — |

### Issue types (configuration + issue usage counts)

*No issue types returned (feature may be off or org policy).*

### Labels (9 total) with usage

| Name | Color | Default | Description | Issues w/ label | PRs w/ label | Total |
|------|-------|---------|-------------|-----------------|--------------|-------|
| `bug` | `d73a4a` | true | Something isn't working | 0 | 0 | 0 |
| `documentation` | `0075ca` | true | Improvements or additions to documentation | 0 | 0 | 0 |
| `duplicate` | `cfd3d7` | true | This issue or pull request already exists | 0 | 0 | 0 |
| `enhancement` | `a2eeef` | true | New feature or request | 0 | 0 | 0 |
| `good first issue` | `7057ff` | true | Good for newcomers | 0 | 0 | 0 |
| `help wanted` | `008672` | true | Extra attention is needed | 0 | 0 | 0 |
| `invalid` | `e4e669` | true | This doesn't seem right | 0 | 0 | 0 |
| `question` | `d876e3` | true | Further information is requested | 0 | 0 | 0 |
| `wontfix` | `ffffff` | true | This will not be worked on | 0 | 0 | 0 |

### Milestones with usage

*None or not accessible.*

### `.github` issue / PR template paths (top-level names)

*`.github` not present or not accessible*

---

GitHub **Projects** custom fields are defined per **Project**, not per repository; they are not included here. For your monitor board, see the project UI or `gh project field-list` for [PyPTO upstream monitor](https://github.com/users/jiashu/projects/3).
