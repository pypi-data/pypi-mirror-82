import glob
import os
import subprocess

import pkg_resources.extern.packaging.version
import pytest
from pytest_postgresql import factories

from swh.core.utils import numfile_sortkey as sortkey
from swh.storage.tests import SQL_DIR as STORAGE_SQL_DIR
from swh.vault import get_vault
from swh.vault.tests import SQL_DIR

os.environ["LC_ALL"] = "C.UTF-8"

pytest_v = pkg_resources.get_distribution("pytest").parsed_version
if pytest_v < pkg_resources.extern.packaging.version.parse("3.9"):

    @pytest.fixture
    def tmp_path(request):
        import pathlib
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            yield pathlib.Path(tmpdir)


def db_url(name, postgresql_proc):
    return "postgresql://{user}@{host}:{port}/{dbname}".format(
        host=postgresql_proc.host,
        port=postgresql_proc.port,
        user="postgres",
        dbname=name,
    )


postgresql2 = factories.postgresql("postgresql_proc", "tests2")


@pytest.fixture
def swh_vault(request, postgresql_proc, postgresql, postgresql2, tmp_path):

    for sql_dir, pg in ((SQL_DIR, postgresql), (STORAGE_SQL_DIR, postgresql2)):
        dump_files = os.path.join(sql_dir, "*.sql")
        all_dump_files = sorted(glob.glob(dump_files), key=sortkey)

        for fname in all_dump_files:
            subprocess.check_call(
                [
                    "psql",
                    "--quiet",
                    "--no-psqlrc",
                    "-v",
                    "ON_ERROR_STOP=1",
                    "-d",
                    pg.dsn,
                    "-f",
                    fname,
                ]
            )

    vault_config = {
        "db": db_url("tests", postgresql_proc),
        "storage": {
            "cls": "local",
            "db": db_url("tests2", postgresql_proc),
            "objstorage": {
                "cls": "pathslicing",
                "args": {"root": str(tmp_path), "slicing": "0:1/1:5",},
            },
        },
        "cache": {
            "cls": "pathslicing",
            "args": {
                "root": str(tmp_path),
                "slicing": "0:1/1:5",
                "allow_delete": True,
            },
        },
        "scheduler": {"cls": "remote", "url": "http://swh-scheduler:5008",},
    }

    return get_vault("local", vault_config)


@pytest.fixture
def swh_storage(swh_vault):
    return swh_vault.storage
