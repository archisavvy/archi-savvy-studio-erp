# Modifications

Archi Savvy Studio ERP is a modified version of OpenBusinessERP.

- Original work: OpenBusinessERP, Copyright (C) 2024-2026 Artem Boiko / DataDrivenConstruction.io and OpenBusinessERP Contributors, https://github.com/datadrivenconstruction/OpenBusinessERP
- Licence: GNU Affero General Public License v3.0 or later. See `LICENSE`, `NOTICE` and `COPYRIGHT`, which are unchanged.
- Base version: upstream v18.5.0, commit 996b1fc27b40417d8739fdd4abca19400e680006.
- Modified by: Archi Savvy Studio, starting 15 November 2026.
- This version is not affiliated with, endorsed by or supported by the original authors. "OpenBusinessERP" and "DataDrivenConstruction" are their trademarks and are used here only to state what this software is based on.

## What was changed

| Date | Change |
|---|---|
| 2026-11-15 | Product renamed to Archi Savvy Studio ERP across the interface, installer, desktop shell and documentation (`tools/rebrand/rebrand.py`). Copyright, licence and provenance lines were left as they were. |
| 2026-11-15 | New logo, application icon and installer artwork (`tools/rebrand/make_icons.py`). |
| 2026-11-15 | Application identifier, sidecar binary name and data folder changed so this version can be installed next to the original without sharing data. |
| 2026-11-15 | The original project's own promotion (donations, newsletter, review requests, consulting, founder profile, book) switched off through `frontend/src/shared/lib/brand.ts`. The code is still present. |
| 2026-11-15 | About page: added a notice naming this edition, its source code and the original work. |
| 2026-11-15 | Upstream CI, publishing and docs workflows moved to `.github/workflows-disabled/`. The desktop build, desktop check, release signing and SBOM workflows stay. Added `windows-build.yml`. |
| 2026-11-15 | Dependabot configuration moved to `.github/workflows-disabled/` so the new repository is not flooded with automated update requests. |

The full, line-by-line record is the git history of this repository.
