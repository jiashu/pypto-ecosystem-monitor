# How to monitor upstream (read-only)

This file documents **personal** ways to stay current with the repositories listed in [`manifest.yaml`](manifest.yaml). None of these steps modify upstream repos.

## GitHub Watch

On each upstream repository page, use **Watch** and choose a level (e.g. **Participating and @mentions** or **All Activity**). That only affects **your** notifications.

## Releases and tags

- Open the upstream repo’s **Releases** page and use your browser or an RSS reader if the project publishes releases.
- For repos that do not use GitHub Releases, follow **commits** on the default branch via Watch or compare occasionally.

## Local mirrors

You may `git clone` or `git fetch` any public repository locally. Do not push to upstream remotes unless you are intentionally contributing under that project’s process (outside the scope of this monitor).

## GitHub Project: link upstream issues (read-only on upstream)

The script [`scripts/sync_upstream_issues_to_project.py`](scripts/sync_upstream_issues_to_project.py) adds **existing** issues from every repo in [`manifest.yaml`](manifest.yaml) as linked items on your user project **[PyPTO upstream monitor](https://github.com/users/jiashu/projects/3)**. That only updates **your** project board; it does **not** create or edit issues on upstream repositories.

Prerequisites: [GitHub CLI](https://cli.github.com/) with `gh auth login` and a token that includes the **project** scope.

From the clone root:

```bash
python3 scripts/sync_upstream_issues_to_project.py
```

Optional environment variables: `PROJECT_NUMBER` (default `3`), `PROJECT_OWNER` (default `jiashu`). Re-running the script is idempotent: already-linked issues are skipped; GitHub’s “Content already exists in this project” response is treated as a no-op.

New issues in upstream repos will not appear on the board until you run the script again (or add them manually in the Project UI).

## Automation in this repository

The workflow [`.github/workflows/refresh-upstream-metadata.yml`](.github/workflows/refresh-upstream-metadata.yml) uses the GitHub API with `GITHUB_TOKEN` to **read** public repository metadata and write **only** into this repository (e.g. [`generated/upstream-snapshot.md`](generated/upstream-snapshot.md)). It does not open issues, PRs, or tags on upstream organizations.

## Policy reminder

**Do not** use this monitor project to open PRs, issues, milestones, wiki edits, or tags on the listed upstream repositories unless you are explicitly acting as a contributor on those repos through their normal channels.
