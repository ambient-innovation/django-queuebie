# Changelog

**0.4.0** (2026-07-03)
  * **Breaking change:** Dropped support for Python 3.10 (nearing end-of-life in October 2026)
  * Added support for Python 3.14
  * Added native uv support to the rendered Read the Docs configuration
  * Replaced the unmaintained "m2r2" documentation dependency with "sphinx-mdinclude"
  * Added a Code of Conduct, issue templates and a pull request template to rendered packages
  * Made the single-version CI and Read the Docs jobs track the newest supported Python version
  * Bumped rendered single-version jobs to Python 3.14
  * Added a cache suffix to the uv setup step to avoid CI cache namespace conflicts
  * Excluded unsupported Python/Django combinations (Python 3.14 with Django 4.2 and 5.2) from the rendered CI matrix
  * Fixed the rendered ruff target-version to track the minimum supported Python (matching requires-python) instead of the newest
  * Removed the stale .md source suffix from the rendered Sphinx config, since sphinx-mdinclude provides only the mdinclude directive (not a Markdown source parser)

**0.3.10** (2026-03-30)
  * Maintenance updates via ambient-package-update

**0.3.9** (2026-03-30)
  * Maintenance updates via ambient-package-update

**0.3.8** (2025-12-11)
  * Maintenance updates via ambient-package-update

**0.3.7** (2025-10-15)
  * Maintenance updates via ambient-package-update

**0.3.6** (2025-10-10)
  * Maintenance updates via ambient-package-update

**0.3.5** (2025-10-09)
  * Maintenance updates via ambient-package-update

**0.3.4** (2025-05-29)
  * Maintenance updates via ambient-package-update

**0.3.3** (2025-04-03)
  * Clarified package tagline

**0.3.2** (2025-04-03)
  * Maintenance updates via ambient-package-update

* *0.3.1* (2025-03-19)
  * Added a paranoid-ish test to check that the import logic isn't breaking any testing functionality

* *0.3.0* (2025-03-19)
  * The whole queue iteration now is wrapped in a transaction atomic

* *0.2.0* (2025-03-17)
  * Extend strict mode to prohibit event (!) handlers to talk to the database

* *0.1.0* (2025-01-29)
  * Project init
