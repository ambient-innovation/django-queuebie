import pytest
from django.contrib.auth.models import User

from queuebie.database_blocker import BlockDatabaseAccess, DatabaseAccessDeniedError


def test_block_database_access_use_db():
    with pytest.raises(DatabaseAccessDeniedError, match=r"Database access is disabled in this context."):
        with BlockDatabaseAccess():
            User.objects.get(pk=1)


def test_block_database_access_dont_use_db():
    with BlockDatabaseAccess():
        user = User(pk=1)

    assert user.id == 1
