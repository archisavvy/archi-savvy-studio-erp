# Taking updates from the original project

Branches:

- `upstream-main`: an untouched copy of the original project's `main`. Never commit to it.
- `upstream-branded`: `upstream-main` after `tools/rebrand/rebrand.py` has run. Machine-made, never edited by hand.
- `main`: `upstream-branded` plus everything that is ours (logo, brand settings, fork notice, practice modules).

Because the rebrand is a deterministic script, the difference between two
versions of `upstream-branded` is exactly what the original project changed,
already carrying our name. Merging it into `main` therefore conflicts only
where our own edits touch the same lines.

## Steps for a new upstream release

```bash
git remote add upstream https://github.com/datadrivenconstruction/OpenBusinessERP.git   # once
git fetch upstream --no-tags
git branch -f upstream-main upstream/main

git checkout upstream-branded
git merge --no-commit -X theirs upstream-main      # take upstream as it is
git checkout main -- tools/rebrand                   # use our current script
python3 -I tools/rebrand/rebrand.py
git add -A && git commit -m "Rebrand upstream <version>"

git checkout main
git merge upstream-branded                           # resolve our few hand edits
python3 -I tools/rebrand/rebrand.py --check          # must report 0 files
python3 -I tools/rebrand/make_icons.py               # restore our icons if upstream changed theirs
```

Then push `main` and let the Windows build run before installing anything.

## Rules that keep this cheap

1. Do not push upstream version tags (`v18.5.0` and so on) to this repository. A `v*` tag starts the full release workflow.
2. Put our features in new folders (`backend/app/modules/<our_module>/`, `frontend/src/features/<our-feature>/`). New files never conflict.
3. Change module defaults through configuration, not by editing module code.
4. Keep hand edits to upstream files small, and list them in `MODIFICATIONS.md`.
5. Never edit `LICENSE`, `NOTICE`, `COPYRIGHT`, `CONTRIBUTORS.md`, `AUTHORS.md` or copyright header lines.

## Files we edit by hand in upstream code (the likely conflict points)

- `frontend/src/shared/ui/Logo.tsx`
- `frontend/public/splash.html`
- `frontend/src/app/layout/Header.tsx`, `AppLayout.tsx`, `Sidebar.tsx`
- `frontend/src/features/dashboard/DashboardPage.tsx`
- `frontend/src/features/about/AboutPage.tsx`
- `frontend/src/shared/ui/ReviewPromptCard.test.tsx`
