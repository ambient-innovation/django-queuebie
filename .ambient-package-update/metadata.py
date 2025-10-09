from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import (
    DEPLOYMENT_STATUS_BETA,
    DEV_DEPENDENCIES,
    LICENSE_MIT,
    SUPPORTED_DJANGO_VERSIONS,
)
from ambient_package_update.metadata.maintainer import PackageMaintainer
from ambient_package_update.metadata.package import PackageMetadata
from ambient_package_update.metadata.readme import ReadmeContent
from ambient_package_update.metadata.ruff_ignored_inspection import RuffIgnoredInspection

METADATA = PackageMetadata(
    package_name="django_queuebie",
    module_name="queuebie",
    github_package_group="ambient-innovation",
    authors=[
        PackageAuthor(
            name="Ambient Digital",
            email="hello@ambient.digital",
        ),
    ],
    maintainer=PackageMaintainer(name="Ambient Digital", url="https://ambient.digital/", email="hello@ambient.digital"),
    licenser="Ambient Innovation: GmbH",
    license=LICENSE_MIT,
    license_year=2025,
    development_status=DEPLOYMENT_STATUS_BETA,
    has_migrations=False,
    main_branch="main",
    claim="A simple and synchronous message queue for commands and events for Django",
    readme_content=ReadmeContent(uses_internationalisation=True),
    dependencies=[
        f"Django>={SUPPORTED_DJANGO_VERSIONS[0]}",
    ],
    supported_django_versions=SUPPORTED_DJANGO_VERSIONS,
    supported_python_versions=[
        "3.10",
        "3.11",
        "3.12",
        "3.13",
    ],
    optional_dependencies={
        "dev": [
            *DEV_DEPENDENCIES,
        ],
    },
    ruff_ignore_list=[
        RuffIgnoredInspection(key="TD002", comment="Missing author in TODO"),
        RuffIgnoredInspection(key="TD003", comment="Missing issue link on the line following this TODO"),
    ],
)
