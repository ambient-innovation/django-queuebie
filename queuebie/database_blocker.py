from unittest.mock import patch

from django.db import connections


class DatabaseAccessDeniedError(RuntimeError):
    def __init__(self):
        super().__init__("Database access is disabled in this context.")


class BlockDatabaseAccess:
    def __enter__(self):
        # Patcht alle aktiven DB-Verbindungen, sodass jede Query fehlschlägt
        self.patches = [
            patch.object(connections[alias], "cursor", side_effect=self._raise_error) for alias in connections
        ]
        for p in self.patches:
            p.start()

    def __exit__(self, exc_type, exc_value, traceback):
        for p in self.patches:
            p.stop()

    def _raise_error(self, *args, **kwargs):
        raise DatabaseAccessDeniedError()
