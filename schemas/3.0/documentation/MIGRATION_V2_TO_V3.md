# Migration Guide: v2.0 to v3.0

This guide is for **developers** who need to understand how to migrate media plan JSON documents from schema v2.0 to v3.0. Whether you're manually updating documents, building migration tools, or integrating with systems that use v3.0, this document provides the systematic rules needed to perform accurate migrations.

## Audience

This guide is intended for:
- **Developers** building migration utilities or converters
- **System integrators** working with v3.0 media plans
- **Tool builders** implementing v2.0 → v3.0 upgrade functionality
- **Data engineers** performing manual document migrations

## Automated Migration

If you're using the **MediaPlanPy SDK v3.0.x**, automatic migration is available via the CLI command:
```bash
mediaplanpy workspace upgrade
```

This guide documents the underlying migration logic for those who need to implement their own migration tools or understand the transformation process.

---

## Overview of Required Changes

Version 3.0 has **4 required changes** that must be implemented for compatibility:

1. **Update schema version number** (`meta.schema_version`)
2. **Migrate campaign audience fields** to array structure (`target_audiences`)
3. **Migrate campaign location fields** to array structure (`target_locations`)
4. **Rename dictionary key** (`custom_dimensions` → `lineitem_custom_dimensions`)

These are **breaking changes** - v3.0 documents that don't implement these changes will fail validation.

All other v3.0 features (KPIs, formulas, custom properties, new metrics, etc.) are **optional additions** that can be added incrementally after the core migration.

---

## Migration Steps

Each step below provides the field changes, migration logic, and systematic rules needed to implement the transformation.

### Step 1: Update Schema Version

**Location**: `meta.schema_version`

**Change**:
```json
// v2.0
"schema_version": "2.0"

// v3.0
"schema_version": "3.0"
```

---

### Step 2: Migrate Campaign Audience Fields

**Location**: `campaign` object

#### Fields to Remove:
- `audience_name` (string)
- `audience_age_start` (integer)
- `audience_age_end` (integer)
- `audience_gender` (string)
- `audience_interests` (array of strings)

#### Field to Add:
- `target_audiences` (array of audience objects)

#### Migration Logic:

**v2.0 Format:**
```json
{
  "campaign": {
    "audience_name": "Tech Executives",
    "audience_age_start": 35,
    "audience_age_end": 55,
    "audience_gender": "Any",
    "audience_interests": ["Enterprise software", "Cloud computing", "AI/ML"]
  }
}
```

**v3.0 Format:**
```json
{
  "campaign": {
    "target_audiences": [
      {
        "name": "Tech Executives",
        "demo_age_start": 35,
        "demo_age_end": 55,
        "demo_gender": "Any",
        "interest_attributes": "Enterprise software, Cloud computing, AI/ML"
      }
    ]
  }
}
```

#### Field Mapping:
| v2.0 Field | v3.0 Field | Notes |
|------------|------------|-------|
| `audience_name` | `name` | Required field in audience object |
| `audience_age_start` | `demo_age_start` | Optional |
| `audience_age_end` | `demo_age_end` | Optional |
| `audience_gender` | `demo_gender` | Optional, same enum values |
| `audience_interests` (array) | `interest_attributes` (string) | Convert array to comma-separated string |

#### Systematic Name Generation Rules:

**Rule 1: When to create target_audiences**
```python
# Only create target_audiences array if ANY audience field has data
if audience_name or audience_age_start or audience_age_end or audience_gender or audience_interests:
    # Create target_audiences array with one object
else:
    # Omit target_audiences field entirely
```

**Rule 2: Generate name field**
```python
if audience_name:
    name = audience_name  # Use existing name directly
else:
    # Generate from available components
    if audience_gender and audience_gender != "Any":
        prefix = f"{audience_gender}s"  # "Males" or "Females"
    else:
        prefix = "Adults"

    if audience_age_start and audience_age_end:
        name = f"{prefix} {audience_age_start}-{audience_age_end}"
    elif audience_age_start:
        name = f"{prefix} {audience_age_start}+"
    elif audience_age_end:
        name = f"{prefix} up to {audience_age_end}"
    else:
        name = prefix if prefix != "Adults" else "General Audience"
```

**Examples:**
- `audience_name="Tech Executives"` → `name="Tech Executives"`
- `audience_gender="Male"`, `age_start=35`, `age_end=55` → `name="Males 35-55"`
- `audience_gender="Female"`, `age_start=25` → `name="Females 25+"`
- `audience_gender="Any"`, `age_start=18`, `age_end=65` → `name="Adults 18-65"`
- `audience_gender="Female"`, no age → `name="Females"`
- `audience_gender="Any"`, no age → `name="General Audience"`
- No audience fields at all → Omit `target_audiences` entirely

---

### Step 3: Migrate Campaign Location Fields

**Location**: `campaign` object

#### Fields to Remove:
- `location_type` (string, enum: Country/State)
- `locations` (array of strings)

#### Field to Add:
- `target_locations` (array of location objects)

#### Migration Logic:

**v2.0 Format:**
```json
{
  "campaign": {
    "location_type": "Country",
    "locations": ["United States", "Canada", "United Kingdom"]
  }
}
```

**v3.0 Format:**
```json
{
  "campaign": {
    "target_locations": [
      {
        "name": "North America and UK",
        "location_type": "Country",
        "location_list": ["United States", "Canada", "United Kingdom"]
      }
    ]
  }
}
```

#### Field Mapping:
| v2.0 Field | v3.0 Field | Notes |
|------------|------------|-------|
| N/A | `name` | Required field - use descriptive name or concatenate location names |
| `location_type` | `location_type` | Same field name, expanded enum (Country, State, DMA, County, Postcode, Radius, POI) |
| `locations` (array) | `location_list` (array) | Same structure, renamed field |

#### Systematic Name Generation Rules:

**Rule 1: When to create target_locations**
```python
# Only create target_locations array if locations has data
if locations and len(locations) > 0:
    # Create target_locations array with one object
else:
    # Omit target_locations field entirely
```

**Rule 2: Generate name field**
```python
if len(locations) == 1:
    name = locations[0]
elif len(locations) == 2:
    name = f"{locations[0]} and {locations[1]}"
elif len(locations) == 3:
    name = f"{locations[0]}, {locations[1]}, and {locations[2]}"
else:  # 4+ locations
    # Concatenate all with commas, truncate at 50 chars
    full_name = ", ".join(locations)
    if len(full_name) <= 50:
        name = full_name
    else:
        name = full_name[:47] + "..."  # 47 + 3 = 50 chars total
```

**Rule 3: Map location_type (optional)**
```python
# Only include location_type if it exists in v2.0
if location_type:
    # Include in target_locations object
else:
    # Omit location_type field (it's optional in v3.0)
```

**Examples:**
- `locations=["United States"]` → `name="United States"`
- `locations=["United States", "Canada"]` → `name="United States and Canada"`
- `locations=["United States", "Canada", "Mexico"]` → `name="United States, Canada, and Mexico"`
- `locations=["US", "CA", "MX", "UK", "FR", "DE", "IT", "ES"]` → `name="US, CA, MX, UK, FR, DE, IT, ES"` (44 chars)
- `locations=["United States", "Canada", "Mexico", "United Kingdom", "France"]` → `name="United States, Canada, Mexico, United Kingdom..."` (50 chars)
- No locations → Omit `target_locations` entirely

---

### Step 4: Rename Dictionary Custom Dimensions

**Location**: `dictionary` object

#### Field to Rename:
- `custom_dimensions` → `lineitem_custom_dimensions`

#### Migration Logic:

**v2.0 Format:**
```json
{
  "dictionary": {
    "custom_dimensions": {
      "dim_custom1": {
        "status": "enabled",
        "caption": "Business Type"
      },
      "dim_custom2": {
        "status": "enabled",
        "caption": "Content Strategy"
      }
    },
    "custom_metrics": {
      "metric_custom1": {
        "status": "enabled",
        "caption": "Brand Lift"
      }
    },
    "custom_costs": {
      "cost_custom1": {
        "status": "enabled",
        "caption": "Agency Fee"
      }
    }
  }
}
```

**v3.0 Format:**
```json
{
  "dictionary": {
    "lineitem_custom_dimensions": {
      "dim_custom1": {
        "status": "enabled",
        "caption": "Business Type"
      },
      "dim_custom2": {
        "status": "enabled",
        "caption": "Content Strategy"
      }
    },
    "custom_metrics": {
      "metric_custom1": {
        "status": "enabled",
        "caption": "Brand Lift"
      }
    },
    "custom_costs": {
      "cost_custom1": {
        "status": "enabled",
        "caption": "Agency Fee"
      }
    }
  }
}
```

**Note**: The structure inside remains identical, only the parent key name changes.

#### Special Cases:

**If no dictionary present in v2.0:**
- No action needed

**If dictionary exists but no custom_dimensions:**
- No action needed

---

## Complete Migration Example

This example shows a full v2.0 document transformed to v3.0, demonstrating all four required changes in context.

### Before (v2.0):
```json
{
  "meta": {
    "id": "mp_2025_q1_campaign",
    "schema_version": "2.0",
    "name": "Q1 2025 Campaign"
  },
  "campaign": {
    "id": "camp_001",
    "name": "Product Launch Campaign",
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "budget_total": 500000,
    "audience_name": "Enterprise Decision Makers",
    "audience_age_start": 35,
    "audience_age_end": 65,
    "audience_gender": "Any",
    "audience_interests": ["Business software", "Cloud computing"],
    "location_type": "Country",
    "locations": ["United States", "Canada"]
  },
  "lineitems": [
    {
      "id": "li_001",
      "name": "Digital Display",
      "start_date": "2025-01-01",
      "end_date": "2025-03-31",
      "cost_total": 250000
    }
  ],
  "dictionary": {
    "custom_dimensions": {
      "dim_custom1": {
        "status": "enabled",
        "caption": "Business Unit"
      }
    }
  }
}
```

### After (v3.0):
```json
{
  "meta": {
    "id": "mp_2025_q1_campaign",
    "schema_version": "3.0",
    "name": "Q1 2025 Campaign"
  },
  "campaign": {
    "id": "camp_001",
    "name": "Product Launch Campaign",
    "start_date": "2025-01-01",
    "end_date": "2025-03-31",
    "budget_total": 500000,
    "target_audiences": [
      {
        "name": "Enterprise Decision Makers",
        "demo_age_start": 35,
        "demo_age_end": 65,
        "demo_gender": "Any",
        "interest_attributes": "Business software, Cloud computing"
      }
    ],
    "target_locations": [
      {
        "name": "North America",
        "location_type": "Country",
        "location_list": ["United States", "Canada"]
      }
    ]
  },
  "lineitems": [
    {
      "id": "li_001",
      "name": "Digital Display",
      "start_date": "2025-01-01",
      "end_date": "2025-03-31",
      "cost_total": 250000
    }
  ],
  "dictionary": {
    "lineitem_custom_dimensions": {
      "dim_custom1": {
        "status": "enabled",
        "caption": "Business Unit"
      }
    }
  }
}
```

---

## Migration Checklist

### Required Changes:
- [ ] Update `meta.schema_version` from "2.0" to "3.0"
- [ ] Remove campaign fields: `audience_name`, `audience_age_start`, `audience_age_end`, `audience_gender`, `audience_interests`
- [ ] Add campaign field: `target_audiences` array with mapped audience data
- [ ] Remove campaign fields: `location_type`, `locations`
- [ ] Add campaign field: `target_locations` array with mapped location data
- [ ] Rename `dictionary.custom_dimensions` to `dictionary.lineitem_custom_dimensions`

### Validation:
- [ ] Ensure each audience object has a `name` field (required)
- [ ] Ensure each location object has a `name` field (required)
- [ ] Verify `target_audiences` and `target_locations` are arrays (even if single item)
- [ ] Confirm all other fields remain unchanged
- [ ] Run validation tests: `pytest tests/test_examples.py`

---

## Summary

**Total Required Changes**: 4 steps
1. Schema version update (1 field)
2. Audience migration (5 fields → 1 array field)
3. Location migration (2 fields → 1 array field)
4. Dictionary rename (1 key rename)

**Unchanged**: All meta fields (except schema_version), all campaign fields (except audiences/locations), all lineitem fields, all other dictionary sections

**Result**: A v3.0-compatible document with identical functionality to the v2.0 source, ready for optional v3.0 feature adoption.

---

## Implementation Considerations

### Data Preservation

The migration process is **non-destructive**:
- All existing data is preserved
- No information is lost during transformation
- Field mappings are 1:1 where possible
- Array conversions maintain all original values

### Validation After Migration

After migrating a document, validate it against the v3.0 schema:

**Using Python with jsonschema:**
```python
import json
import jsonschema

# Load v3.0 schema
with open('schemas/3.0/mediaplan.schema.json') as f:
    schema = json.load(f)

# Load migrated document
with open('migrated_mediaplan_v3.0.json') as f:
    document = json.load(f)

# Validate
jsonschema.validate(instance=document, schema=schema)
print("✓ Document is valid v3.0")
```

**Using MediaPlanPy SDK:**
```python
from mediaplanpy import MediaPlan

# Load and validate
media_plan = MediaPlan.load_from_json('migrated_mediaplan_v3.0.json')
print("✓ Document is valid v3.0")
```

### Edge Cases to Handle

**Empty or Missing Fields:**
- If v2.0 has no audience fields → omit `target_audiences` in v3.0
- If v2.0 has no location fields → omit `target_locations` in v3.0
- If v2.0 has no dictionary → no dictionary in v3.0
- Empty arrays in v2.0 (e.g., `locations: []`) → omit corresponding v3.0 array

**Partial Data:**
- Audience with only `audience_name` → Create minimal audience object with just `name`
- Audience with only age/gender → Generate name from available fields
- Location with no `location_type` → Omit `location_type` in v3.0 object (it's optional)

**String Conversions:**
- `audience_interests` array → Join with ", " for `interest_attributes` string
- Long location names → Truncate at 50 characters with "..." suffix

### Testing Your Migration

Test with various document types:
1. **Minimal document**: Only required fields
2. **Full document**: All v2.0 fields populated
3. **Partial audience**: Mix of populated/empty audience fields
4. **Multiple locations**: 1, 2, 3, and 10+ locations to test name generation
5. **No dictionary**: Document without dictionary section
6. **Empty arrays**: Documents with empty `locations: []`

---

## Related Documentation

For a complete field-by-field comparison and details on optional v3.0 features, see:
- **[CHANGELOG_V2_TO_V3.md](CHANGELOG_V2_TO_V3.md)** - Complete schema comparison with all additions and changes

For schema definitions and examples:
- **Schema files**: `schemas/3.0/*.schema.json`
- **Example v3.0 document**: `examples/example_mediaplan_v3.0.json`
- **Example v2.0 document**: `examples/example_mediaplan_v2.0.json`
