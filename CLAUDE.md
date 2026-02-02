# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository defines the **Media Plan Open Data Standard** - a versioned, JSON Schema-based data standard for representing media plans. It contains JSON Schema definitions, example media plan files, and validation tooling.

Key concepts:
- **Schema Versioning**: Schemas are organized under `schemas/<major>.<minor>/` directories
- **Version Lifecycle**: Versions can be current (3.0), supported (2.0, 3.0), deprecated (0.0, 1.0), or preview (none currently)
- **Schema Version Registry**: `schemas/schema_versions.json` defines which versions are supported/deprecated
- **Meta-Schema Architecture**: Each version has a main `mediaplan.schema.json` that references component schemas (campaign, lineitem, dictionary)

## Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate.bat     # Windows (CMD)

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Run all validation tests
pytest tests/test_examples.py

# Run tests with verbose output
pytest tests/test_examples.py -v

# Run specific test function
pytest tests/test_examples.py::test_example_is_valid
pytest tests/test_examples.py::test_schema_versions_registry
pytest tests/test_examples.py::test_required_schemas_exist
pytest tests/test_examples.py::test_schema_file_structure
```

### Generate Documentation
```bash
# Generate XLS documentation (defaults to v3.0)
python scripts/generate_schema_doc.py

# To document a different version: edit SCHEMA_VERSION variable at line 16 of generate_schema_doc.py
```

## Architecture

### Schema Version System

The schema version registry (`schemas/schema_versions.json`) is the source of truth for version status:
- `current`: The recommended version for new implementations (currently 3.0)
- `supported`: Versions that are actively maintained and validated (2.0, 3.0)
- `deprecated`: Versions no longer supported (0.0, 1.0)
- `preview`: Beta versions for early adoption (empty currently)

### Schema Reference Resolution

Each version uses JSON Schema `$ref` to reference component schemas. The test suite uses `jsonschema.RefResolver` with a preloaded schema store to resolve these references during validation.

**Example schema structure for v3.0:**
```
schemas/3.0/
├── mediaplan.schema.json    # Main schema with $ref to others
├── campaign.schema.json      # Referenced by mediaplan
├── lineitem.schema.json      # Referenced by mediaplan
└── dictionary.schema.json    # Referenced by mediaplan
```

When validating, all schemas for a version are loaded into a resolver store to handle cross-references.

### Test Suite Design

The test suite (`tests/test_examples.py`) dynamically validates examples against their declared schema version:

1. **Dynamic Version Detection**: Each example declares its schema version via `meta.schema_version`
2. **Version Validation**: Only supported/preview versions are validated (deprecated examples are skipped)
3. **Dynamic Schema Loading**: Schemas are loaded from the appropriate version directory
4. **Cross-Reference Validation**: A custom resolver validates all `$ref` references across schema files

### Breaking vs Non-Breaking Changes

**Major versions (X.0)** involve breaking changes:
- Removing fields (e.g., v2.0 → v3.0 removed `audience_name`)
- Renaming fields (e.g., v2.0 `custom_dimensions` → v3.0 `lineitem_custom_dimensions`)
- Changing data types
- Adding required fields
- Changing enum allowable values

**Minor versions (X.Y)** are non-breaking:
- Adding optional fields
- Adding new enum values to existing fields

### Version 3.0 Key Features

v3.0 introduces significant enhancements over v2.0:

1. **Array-Based Targeting**: Single audience/location fields replaced with arrays of objects
   - `target_audiences`: Array of audience segments with demographic, interest, intent, and behavioral attributes
   - `target_locations`: Array of location objects supporting multiple geo-types and exclusions

2. **Formula-Based Forecasting**: `metric_formulas` object enables predictive modeling
   - Supported formula types: `cost_per_unit`, `conversion_rate`, `constant`, `power_function`
   - Each formula references a `base_metric` and includes coefficients/parameters
   - Applications can define custom formula types for specialized use cases

3. **Scoped Custom Dimensions**: Dictionary schema now has separate custom dimension configs for meta, campaign, and lineitem levels

4. **Extensibility**: `custom_properties` objects at meta/campaign/lineitem levels for arbitrary JSON data

See `schemas/3.0/documentation/CHANGELOG_V2_TO_V3.md` for complete field-by-field comparison.

## Working with Schemas

### Adding a New Schema Version

When creating a new major version:

1. Create new directory: `schemas/X.0/`
2. Copy and modify schemas from previous version
3. Update `schemas/schema_versions.json` to add version to `preview` array
4. Create example file: `examples/example_mediaplan_vX.0.json`
5. Add documentation: `schemas/X.0/documentation/CHANGELOG_VY_TO_VX.md`
6. Run tests to ensure validation works

### Modifying Existing Schemas

**For current/supported versions:**
- Minor changes only (adding optional fields, new enum values)
- Test all existing examples still validate after changes
- Update schema version number in `mediaplan.schema.json` if needed

**For major changes:**
- Create a new major version (see above)
- Never modify deprecated versions

### Creating Example Files

All example media plans must:
- Include `meta.schema_version` field matching a supported/preview version
- Validate against their declared schema version
- Be placed in `examples/` directory with naming pattern `example_mediaplan_vX.Y.json`

## File Locations

- **Schema definitions**: `schemas/<version>/*.schema.json`
- **Schema version registry**: `schemas/schema_versions.json`
- **Example media plans**: `examples/example_mediaplan_v*.json`
- **Deprecated examples**: `examples/deprecated/`
- **Tests**: `tests/test_examples.py`
- **Documentation generation**: `scripts/generate_schema_doc.py`
- **Version-specific docs**: `schemas/<version>/documentation/`

## Related Projects

- **[mediaplanpy](https://github.com/planmatic/mediaplanpy)**: Python SDK for working with media plans
  - SDK v2.0.7 supports schema v2.0 only
  - SDK v3.0.x supports schema v3.0 only
  - SDK v3.0.x includes migration utility for v2.0 → v3.0 workspace upgrades
