# Changelog

**0.6.0** (2026-09-08)
  * Auto-discovery now walks the whole subtree of every local Django app, so `handlers/commands` and `handlers/events`
    directories may live in sub-packages instead of only at the app root
  * Added the setting `QUEUEBIE_EXCLUDED_DIRECTORIES` (default `{"tests", "migrations"}`) to keep handler-shaped
    directories out of the auto-discovery. It replaces the default rather than extending it
  * Auto-discovery descends only into directories holding an `__init__.py`, so asset directories, virtualenvs and
    `__pycache__` stay out of the walk without being named. A `handlers/commands` directory relying on an implicit
    namespace package is therefore no longer found - queuebie logs a warning naming the directory when it sees one
  * **Breaking change:** Strict mode compares the package owning the `handlers/` or `messages/` directory instead of
    the Django app. Nested layouts get the boundary enforced they always described, and two cases which used to pass
    the check unconditionally are now validated:
    * handlers and commands living outside any installed Django app
    * commands living inside an app but outside a `messages/` directory - a command in, say,
      `my_app/domain/orders/commands.py` has no owning `messages/` directory, so its scope is its full module path,
      which no handler can share. Registering a handler for it raises `RegisterOutOfScopeCommandError` at import
      time. Move such commands into a `messages/` directory or turn strict mode off
  * **Breaking change:** Replaced `queuebie.utils.is_part_of_app()` with `queuebie.utils.is_same_scope()` and
    `queuebie.utils.message_scope()`
  * **Breaking change:** `RegisterOutOfScopeCommandError` now names both scopes instead of only the command and the
    handler, so a mismatch between two sub-packages of the same app can be read off the message
  * Handlers are now registered in a deterministic order - the handler package first, then its modules sorted by
    name. Where a message has more than one handler, and since the bus is synchronous, that order is observable and
    may differ from the one the file system happened to yield before

**0.5.0** (2026-08-27)
  * Added support for Django 6.1
  * **Breaking change:** Dropped support for Django 4.2, whose extended support ended in April 2026
  * Updated the linting and CI setup to the current ambient-package-update template

**0.4.1** (2026-07-03)
  * Updated company and maintainer information to "Beyonder Deutschland"

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
