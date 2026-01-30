# Media Plan Open Data Standard (mediaplanschema)

This repository defines a versioned, open, and extensible **JSON-based data standard** for representing media plans. It includes JSON Schema definitions, example media plans, and validation tooling for developers, analysts, and vendors working in the media planning ecosystem.

For developers looking to build applications with this standard, check out our **[mediaplanpy](https://github.com/laurent-colard-l5i/mediaplanpy)** sister repository - an open source Python SDK that provides the foundational tools you need to build, manage, and analyze media plans based on this Open Data Standard.

---

## Repository Structure

```
media-plan-ods/
├── schemas/             # Versioned JSON Schema definitions
│   ├── 1.0/             # Deprecated
│   │   ├── campaign.schema.json
│   │   ├── lineitem.schema.json
│   │   ├── mediaplan.schema.json
│   │   └── documentation/
│   ├── 2.0/             # Supported - Previous version
│   │   ├── campaign.schema.json
│   │   ├── dictionary.schema.json
│   │   ├── lineitem.schema.json
│   │   ├── mediaplan.schema.json
│   │   └── documentation/
│   ├── 3.0/             # Current version
│   │   ├── campaign.schema.json
│   │   ├── dictionary.schema.json
│   │   ├── lineitem.schema.json
│   │   ├── mediaplan.schema.json
│   │   └── documentation/
│   │       └── CHANGELOG_V2_TO_V3.md
│   └── schema_versions.json
├── examples/            # Example media plan files
│   ├── deprecated/
│   │   └── example_mediaplan_v0.0.json
│   ├── example_mediaplan_v1.0.json
│   ├── example_mediaplan_v2.0.json
│   └── example_mediaplan_v3.0.json
├── tests/               # Unit tests for schema validation
│   └── test_examples.py
├── scripts/             # Utility scripts
│   └── generate_schema_doc.py
├── requirements.txt     # Python dependencies
└── README.md
```

---

## JSON Schema Overview

Schemas are versioned under `schemas/<major>.<minor>/`. The main schema file is:

```
schemas/3.0/mediaplan.schema.json
```

This references:
- `campaign.schema.json`
- `lineitem.schema.json`
- `dictionary.schema.json`

Each media plan JSON file must include a `meta.schema_version` field that declares the schema version used (e.g., "2.0" or "3.0").

### Version 3.0 (Current)

Version 3.0 is the current production version. See the [complete changelog](schemas/3.0/documentation/CHANGELOG_V2_TO_V3.md) for detailed migration information.

Key features include:
- Enhanced targeting with `target_audiences` and `target_locations` arrays
- Formula-based metric calculation system with multiple formula types
- 40% more fields (155 vs 116 in v2.0)
- Custom KPIs at campaign level
- 11 new standard metrics
- Enhanced dictionary schema with scoped custom dimensions

### Schema Versioning Strategy

**Major Version (X.0):** Breaking changes including renaming/removing fields, changing data types, changing allowable values, or adding required fields.

**Minor Version (X.Y):** Non-breaking changes including adding optional fields or adding new allowable values to existing fields.

**Preview Versions:** New major versions may be released in preview mode for testing and early adoption before becoming the current version.

Currently available versions:
- **0.0**: Deprecated - No longer supported
- **1.0**: Deprecated - No longer supported
- **2.0**: Supported - Enhanced version with custom field configuration via dictionary schema
- **3.0**: Current - Production version with advanced targeting, formulas, and extensibility (see details below)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/laurent-colard-l5i/mediaplanschema.git
cd mediaplanschema
```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate.bat   # Windows (CMD)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Validation Tests

Run the unit test to validate all media plans in the `examples/` folder:

```bash
pytest tests/test_examples.py
```

Each example is dynamically validated against the appropriate schema version declared in its `meta.schema_version`. The test suite supports all versions including current and supported versions.

---

## Schema Version Details

### Version 1.0 (Deprecated)
- Enhanced campaign and lineitem schemas
- Expanded budget tracking with cost breakdowns
- Support for custom dimensions, metrics, and costs (up to 10 of each)
- Improved targeting and audience definition
- **Note**: This version is deprecated and no longer supported

### Version 2.0 (Supported)
- All features from version 1.0
- **New dictionary schema** for custom field configuration
- Enhanced metadata tracking with separate creator ID and name fields
- Workflow status tracking
- Improved documentation and field descriptions
- Support for currency specification
- Additional standard metrics (engagements, followers, visits, leads, etc.)

#### Dictionary Schema Benefits (v2.0)
The dictionary schema enables:
- **Semantic clarity**: Define what each custom field represents
- **Tool interoperability**: Consistent field meanings across different platforms
- **Data governance**: Centralized configuration of custom field usage
- **User experience**: Human-readable captions for custom fields in applications

Example dictionary configuration:
```json
"dictionary": {
  "custom_dimensions": {
    "dim_custom1": {
      "status": "enabled",
      "caption": "Business Type",
      "description": "Classification of business model (B2B, B2C, B2B2C)"
    }
  }
}
```

### Version 3.0 (Current) - Breaking Changes

Version 3.0 represents a major evolution of the schema with significant breaking changes and new capabilities designed for advanced media planning, forecasting, and optimization workflows.

**Status:** Production - Current version for all new implementations. See the [complete changelog](schemas/3.0/documentation/CHANGELOG_V2_TO_V3.md) for detailed migration information from v2.0.

#### New Features

**Meta-Level Enhancements:**
- **Custom dimensions** (dim_custom1-5): Classify plan versions with custom dimensions
- **Custom properties**: Extensible JSON object for storing arbitrary metadata

**Campaign-Level Enhancements:**
- **BREAKING: target_audiences** (array): Replaces single audience fields with support for multiple audience segments
  - Detailed demographic, interest, intent, and behavioral attributes
  - Audience extension strategies (lookalike modeling)
  - Population size tracking per audience
- **BREAKING: target_locations** (array): Replaces single location fields with flexible geo-targeting
  - Support for multiple location types (Country, State, DMA, County, Postcode, Radius, POI)
  - Inclusion and exclusion lists
  - Population percentage targeting
- **KPI tracking** (kpi_name1-5, kpi_value1-5): Campaign-level KPI targets linked to lineitem metrics
- **Custom dimensions** (dim_custom1-5): Campaign-level classification
- **Custom properties**: Extensible JSON object for campaign settings

**Lineitem-Level Enhancements:**
- **kpi_value**: Target value for the lineitem's primary KPI
- **buy_type & buy_commitment**: Media buying arrangement details (Auction, Programmatic Guaranteed, Upfront, etc.)
- **is_aggregate & aggregation_level**: Support for aggregate line items (channel-level budgets, campaign-level constraints)
- **cost_currency_exchange_rate**: Multi-currency support with exchange rates
- **cost_minimum & cost_maximum**: Budget constraints for optimization
- **New standard metrics**: view_starts, view_completions, reach, units, impression_share, page_views, likes, shares, comments, conversions
- **metric_formulas**: Formula-based metric calculation with coefficients and parameters
  - Supports multiple formula types: cost_per_unit, conversion_rate, constant, power_function
  - Enables forecasting and what-if scenario modeling
- **Custom properties**: Extensible JSON object for targeting settings and metadata

**Dictionary Schema Enhancements:**
- **BREAKING: Scoped custom dimensions**: Separate dictionaries for meta, campaign, and lineitem levels
  - `meta_custom_dimensions` (dim_custom1-5)
  - `campaign_custom_dimensions` (dim_custom1-5)
  - `lineitem_custom_dimensions` (dim_custom1-10, renamed from `custom_dimensions`)
- **standard_metrics**: Formula configuration for standard metrics (metric_impressions, metric_clicks, metric_leads, etc.)
  - Only formula-capable metrics are listed
  - Defines formula_type and base_metric for each
- **Enhanced custom_metrics**: Extended with formula_type and base_metric fields

#### Breaking Changes Summary

**Fields Removed:**
- Campaign: `audience_name`, `audience_age_start`, `audience_age_end`, `audience_gender`, `audience_interests`
- Campaign: `location_type`, `locations`

**Fields Replaced:**
- Campaign: Old audience fields → `target_audiences` (array of audience objects)
- Campaign: Old location fields → `target_locations` (array of location objects)
- Dictionary: `custom_dimensions` → `lineitem_custom_dimensions` (renamed for clarity)

**Migration Path:**
v2.0 media plans can be upgraded to v3.0 by:
1. Converting single audience to `target_audiences` array with one element
2. Converting location fields to `target_locations` array with one element
3. Updating dictionary references from `custom_dimensions` to `lineitem_custom_dimensions`

#### Formula-Based Forecasting (v3.0)

Version 3.0 introduces formula-based metric calculation for forecasting and scenario planning:

```json
"metric_formulas": {
  "metric_leads": {
    "formula_type": "power_function",
    "base_metric": "cost_total",
    "coefficient": 10.5,
    "parameter1": 0.82,
    "comments": "Calibrated using historical data"
  }
}
```

**Supported formula types:**
- `cost_per_unit`: Linear division (e.g., impressions = cost / CPM)
- `conversion_rate`: Linear multiplication (e.g., clicks = impressions × CTR)
- `constant`: Fixed value (e.g., baseline metric)
- `power_function`: Power function for diminishing returns (e.g., leads = coefficient × cost^exponent)

Applications can define additional formula types for specialized use cases (MMM curves, saturation functions, etc.).

---

## Developer Tools

### Python SDK - mediaplanpy

For developers building applications with this standard, we recommend using **[mediaplanpy](https://github.com/planmatic/mediaplanpy)** - our open source Python SDK that provides:

- **Schema validation** - Validate media plans against any schema version
- **Data manipulation** - Create, modify, and analyze media plan data
- **Import/Export** - Convert between different formats and systems
- **Analysis tools** - Built-in functions for media plan analysis and reporting

---

## Contributing

We welcome issues, schema proposals, and example files.

- Ensure you include `schema_version` in any proposed media plan examples
- All PRs are tested for schema validity via unit tests
- Contributions should follow semantic versioning when modifying schemas
- When proposing changes to current versions, consider backward compatibility impact

---

## License

This project is open source under the [MIT License](LICENSE).

---

## Contact

Created and maintained by [Planmatic.io](https://www.planmatic.io).