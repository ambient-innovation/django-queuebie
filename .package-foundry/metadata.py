from package_foundry.metadata.author import PackageAuthor
from package_foundry.metadata.constants import (
    DEPLOYMENT_STATUS_BETA,
    DEV_DEPENDENCIES,
    LICENSE_MIT,
    SUPPORTED_DJANGO_VERSIONS,
    SUPPORTED_PYTHON_VERSIONS,
)
from package_foundry.metadata.maintainer import PackageMaintainer
from package_foundry.metadata.package import PackageMetadata
from package_foundry.metadata.readme import ReadmeContent
from package_foundry.metadata.ruff_ignored_inspection import RuffIgnoredInspection

METADATA = PackageMetadata(
    package_name="django_queuebie",
    module_name="queuebie",
    github_package_group="ambient-innovation",
    authors=[
        PackageAuthor(
            name="Beyonder Deutschland",
            email="hello@beyonder.de",
        ),
    ],
    maintainer=PackageMaintainer(name="Beyonder Deutschland", url="https://beyonder.de/", email="hello@beyonder.de"),
    licenser="Beyonder Deutschland GmbH",
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
    supported_python_versions=SUPPORTED_PYTHON_VERSIONS,
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
