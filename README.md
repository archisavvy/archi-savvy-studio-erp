<p align="center"><img src="frontend/public/brand/archi-savvy-logo.webp" alt="Archi Savvy" width="420"></p>

<h1 align="center">ArchiSavvyERP</h1>

<p align="center">Practice management and ERP for architecture and design studios, as a Windows desktop application.</p>

ArchiSavvyERP is a modified version of OpenBusinessERP by Artem Boiko / DataDrivenConstruction. <!-- rebrand:keep -->
It is licensed under the GNU Affero General Public License v3.0 or later, the same licence as the original.
It is not affiliated with, endorsed by or supported by the original authors. See [MODIFICATIONS.md](MODIFICATIONS.md).

## Status

The Windows installer builds on GitHub Actions and has been installed on Windows 10. New users start on the Architecture & Design Practice profile, with contractor modules off.

Planned next: RIBA Plan of Work stages, fee tracking, staff timesheets and profitability, resource planning and drawing registers.

## What is in the box

Projects, clients and CRM, quotes, invoices, purchasing, banking, double-entry accounting, documents with versions and transmittals, RFIs, BIM and DWG/PDF take-off, bills of quantities and cost plans. The desktop app bundles the backend and an embedded PostgreSQL database, so users install one file and need no development tools.

## Getting the Windows installer

Open the **Actions** tab, choose **Windows Build**, press **Run workflow**. When the run named `Windows diagnostic <SHA>` finishes, download the `windows-diagnostic-...` artifact. It contains the setup `.exe`.

The installer is not code-signed, so Windows SmartScreen warns on first run.

## Source code and licence

- This repository is the complete corresponding source for every installer built from it.
- `LICENSE`, `NOTICE`, `COPYRIGHT` and `CONTRIBUTORS.md` are unchanged from the original project.
- The original project's README is kept at [docs/fork/UPSTREAM_README.md](docs/fork/UPSTREAM_README.md).
- How updates from the original project are merged: [docs/fork/UPDATING.md](docs/fork/UPDATING.md).

The Archi Savvy name and logo are trademarks of their owner and are not licensed under the AGPL.
