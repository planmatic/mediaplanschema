import os
import json
import pytest
import glob
from jsonschema import validate, RefResolver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_PATH = os.path.join(BASE_DIR, "examples", "*.json")
SCHEMA_REGISTRY_PATH = os.path.join(BASE_DIR, "schemas", "schema_versions.json")

# Load supported schema versions
with open(SCHEMA_REGISTRY_PATH, "r", encoding="utf-8") as vr:
    version_info = json.load(vr)
    supported_versions = version_info.get("supported", [])
    deprecated_versions = version_info.get("deprecated", [])
    preview_versions = version_info.get("preview", [])
    current_version = version_info.get("current")

# Combine supported and preview versions for testing
allowed_versions = supported_versions + preview_versions

example_files = glob.glob(EXAMPLES_PATH)


def load_schemas_for_version(version):
    """
    Dynamically load all schema files for a given version.
    Returns a dictionary mapping schema filenames to their content.
    """
    schema_dir = os.path.join(BASE_DIR, "schemas", version)

    if not os.path.exists(schema_dir):
        raise FileNotFoundError(f"Schema directory not found for version: {version}")

    schemas = {}

    # Get all .json files in the schema directory
    schema_files = glob.glob(os.path.join(schema_dir, "*.json"))

    for schema_file in schema_files:
        filename = os.path.basename(schema_file)

        # Skip schema_versions.json if it exists in the version directory
        if filename == "schema_versions.json":
            continue

        with open(schema_file, "r", encoding="utf-8") as sf:
            schemas[filename] = json.load(sf)

    return schemas


@pytest.mark.parametrize("example_file", example_files)
def test_example_is_valid(example_file):
    with open(example_file, "r", encoding="utf-8") as f:
        instance = json.load(f)

    # Ensure schema version is declared
    version = instance.get("meta", {}).get("schema_version")
    assert version is not None, f"No schema_version specified in meta block of {example_file}"

    # Validate schema version against registry (including preview versions)
    assert version in allowed_versions, (
        f"Schema version '{version}' is not supported "
        f"(allowed: {allowed_versions}) in file {example_file}"
    )

    # Load all schemas for this version
    schemas = load_schemas_for_version(version)

    # Ensure mediaplan.schema.json exists as the main schema
    assert "mediaplan.schema.json" in schemas, f"mediaplan.schema.json not found for version: {version}"

    mediaplan_schema = schemas["mediaplan.schema.json"]

    # Create a custom resolver with all schemas preloaded
    resolver = RefResolver(base_uri="", referrer=mediaplan_schema, store=schemas)

    # Validate the instance
    validate(instance=instance, schema=mediaplan_schema, resolver=resolver)


def test_schema_versions_registry():
    """
    Test that all referenced schema versions in examples have corresponding schema directories.
    """
    for example_file in example_files:
        with open(example_file, "r", encoding="utf-8") as f:
            instance = json.load(f)

        version = instance.get("meta", {}).get("schema_version")
        if version:
            schema_dir = os.path.join(BASE_DIR, "schemas", version)
            assert os.path.exists(schema_dir), (
                f"Schema directory missing for version '{version}' "
                f"referenced in {os.path.basename(example_file)}"
            )


def test_required_schemas_exist():
    """
    Test that required schema files exist for each version.
    """
    for version in allowed_versions:
        schema_dir = os.path.join(BASE_DIR, "schemas", version)

        # These are the minimum required schemas for any version
        required_schemas = ["mediaplan.schema.json"]

        for required_schema in required_schemas:
            schema_path = os.path.join(schema_dir, required_schema)
            assert os.path.exists(schema_path), (
                f"Required schema '{required_schema}' missing for version '{version}'"
            )


def test_schema_file_structure():
    """
    Test that each schema version has a consistent file structure.
    """
    for version in allowed_versions:
        schemas = load_schemas_for_version(version)

        # All versions should have mediaplan.schema.json
        assert "mediaplan.schema.json" in schemas

        # Check version-specific requirements
        if version in ["0.0", "1.0"]:
            # Older versions should have campaign and lineitem schemas
            assert "campaign.schema.json" in schemas, f"campaign.schema.json missing in version {version}"
            assert "lineitem.schema.json" in schemas, f"lineitem.schema.json missing in version {version}"

        if version in ["2.0", "3.0"]:
            # Version 2.0+ should have the dictionary schema
            assert "dictionary.schema.json" in schemas, f"dictionary.schema.json missing in version {version}"