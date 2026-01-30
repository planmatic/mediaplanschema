# Changelog: v2.0 to v3.0

This document provides a comprehensive field-by-field comparison between v2.0 and v3.0 schemas.

---

## Summary Statistics

| Schema | v2.0 Fields | v3.0 Fields | Net Change |
|--------|-------------|-------------|------------|
| Meta | 10 | 16 | +6 fields |
| Campaign | 25 | 36 | +11 fields (but 7 removed, 18 added) |
| Line Item | 78 | 98 | +20 fields |
| Dictionary | 3 groups | 5 groups | +2 groups, renamed 1 |

**Total**: v2.0 had ~116 fields, v3.0 has ~155 fields (+39 fields net)

---

## Breaking Changes

### 1. Campaign Schema - Audience Fields

**REMOVED** (v2.0):
- `audience_name` (string)
- `audience_age_start` (integer)
- `audience_age_end` (integer)
- `audience_gender` (string, enum)
- `audience_interests` (array of strings)

**ADDED** (v3.0):
- `target_audiences` (array of objects)
  - Each object structure:
    - `name` (string, **required**)
    - `description` (string)
    - `demo_age_start` (integer)
    - `demo_age_end` (integer)
    - `demo_gender` (string, enum: Male/Female/Any)
    - `demo_attributes` (string)
    - `interest_attributes` (string)
    - `intent_attributes` (string)
    - `purchase_attributes` (string)
    - `content_attributes` (string)
    - `exclusion_list` (string)
    - `extension_approach` (string)
    - `population_size` (integer)

---

### 2. Campaign Schema - Location Fields

**REMOVED** (v2.0):
- `location_type` (string, enum: Country/State)
- `locations` (array of strings)

**ADDED** (v3.0):
- `target_locations` (array of objects)
  - Each object structure:
    - `name` (string, **required**)
    - `description` (string)
    - `location_type` (string, enum: Country/State/DMA/County/Postcode/Radius/POI)
    - `location_list` (array of strings)
    - `exclusion_type` (string, enum: Country/State/DMA/County/Postcode/Radius/POI)
    - `exclusion_list` (array of strings)
    - `population_percent` (number, 0-1)

---

### 3. Dictionary Schema - Custom Dimensions Rename

**RENAMED**:
- v2.0: `custom_dimensions`
- v3.0: `lineitem_custom_dimensions`

---

## Additive Changes (Non-Breaking)

### Meta Schema

**NEW FIELDS** (all optional):
- `dim_custom1` (string)
- `dim_custom2` (string)
- `dim_custom3` (string)
- `dim_custom4` (string)
- `dim_custom5` (string)
- `custom_properties` (object)

---

### Campaign Schema

**NEW FIELDS** (all optional):
- `kpi_name1` (string)
- `kpi_value1` (number)
- `kpi_name2` (string)
- `kpi_value2` (number)
- `kpi_name3` (string)
- `kpi_value3` (number)
- `kpi_name4` (string)
- `kpi_value4` (number)
- `kpi_name5` (string)
- `kpi_value5` (number)
- `dim_custom1` (string)
- `dim_custom2` (string)
- `dim_custom3` (string)
- `dim_custom4` (string)
- `dim_custom5` (string)
- `custom_properties` (object)

---

### Line Item Schema

**NEW FIELDS** (all optional):

**Buy Information:**
- `kpi_value` (number)
- `buy_type` (string)
- `buy_commitment` (string)

**Aggregation:**
- `is_aggregate` (boolean)
- `aggregation_level` (string)

**Multi-Currency:**
- `cost_currency_exchange_rate` (number)

**Budget Constraints:**
- `cost_minimum` (number)
- `cost_maximum` (number)

**New Metrics (11 new):**
- `metric_view_starts` (number)
- `metric_view_completions` (number)
- `metric_reach` (number)
- `metric_units` (number)
- `metric_impression_share` (number)
- `metric_page_views` (number)
- `metric_likes` (number)
- `metric_shares` (number)
- `metric_comments` (number)
- `metric_conversions` (number)

**Formulas:**
- `metric_formulas` (object)
  - Keys: metric names (e.g., "metric_leads", "metric_clicks")
  - Values: formula configuration objects
    - `formula_type` (string) - e.g., "power_function", "conversion_rate", "cost_per_unit", "constant"
    - `base_metric` (string) - e.g., "cost_total", "metric_impressions"
    - `coefficient` (number)
    - `parameter1` (number)
    - `parameter2` (number)
    - `parameter3` (number)
    - `comments` (string)

**Extensibility:**
- `custom_properties` (object)

---

### Dictionary Schema

**NEW GROUPS** (all optional):

**meta_custom_dimensions** (new):
- Configures dim_custom1-5 for meta level
- Structure: `custom_field_config` (status, caption)

**campaign_custom_dimensions** (new):
- Configures dim_custom1-5 for campaign level
- Structure: `custom_field_config` (status, caption)

**standard_metrics** (new):
- Configures formula support for standard metrics
- Structure: `metric_formula_config` (formula_type, base_metric)
- Contains 25 formula-capable metrics

**custom_metrics** (enhanced):
- Added formula support fields
- Structure: `custom_metric_config` (status, caption, formula_type, base_metric)

---

## Field Reference Tables

### Meta Fields Comparison

| v2.0 Field | v3.0 Field | Status | Type |
|------------|------------|--------|------|
| id | id | Unchanged | string |
| schema_version | schema_version | **Updated value** | string |
| name | name | Unchanged | string |
| created_by_id | created_by_id | Unchanged | string |
| created_by_name | created_by_name | Unchanged | string |
| created_at | created_at | Unchanged | string (datetime) |
| comments | comments | Unchanged | string |
| is_current | is_current | Unchanged | boolean |
| is_archived | is_archived | Unchanged | boolean |
| parent_id | parent_id | Unchanged | string |
| - | dim_custom1 | **NEW** | string |
| - | dim_custom2 | **NEW** | string |
| - | dim_custom3 | **NEW** | string |
| - | dim_custom4 | **NEW** | string |
| - | dim_custom5 | **NEW** | string |
| - | custom_properties | **NEW** | object |

---

### Campaign Fields Comparison

| v2.0 Field | v3.0 Field | Status | Type |
|------------|------------|--------|------|
| id | id | Unchanged | string |
| name | name | Unchanged | string |
| objective | objective | Unchanged | string |
| start_date | start_date | Unchanged | string (date) |
| end_date | end_date | Unchanged | string (date) |
| budget_currency | budget_currency | Unchanged | string |
| budget_total | budget_total | Unchanged | number |
| agency_id | agency_id | Unchanged | string |
| agency_name | agency_name | Unchanged | string |
| advertiser_id | advertiser_id | Unchanged | string |
| advertiser_name | advertiser_name | Unchanged | string |
| product_id | product_id | Unchanged | string |
| product_name | product_name | Unchanged | string |
| product_description | product_description | Unchanged | string |
| campaign_type_id | campaign_type_id | Unchanged | string |
| campaign_type_name | campaign_type_name | Unchanged | string |
| **audience_name** | - | **REMOVED** | - |
| **audience_age_start** | - | **REMOVED** | - |
| **audience_age_end** | - | **REMOVED** | - |
| **audience_gender** | - | **REMOVED** | - |
| **audience_interests** | - | **REMOVED** | - |
| - | **target_audiences** | **NEW** | array[object] |
| **location_type** | - | **REMOVED** | - |
| **locations** | - | **REMOVED** | - |
| - | **target_locations** | **NEW** | array[object] |
| workflow_status_id | workflow_status_id | Unchanged | string |
| workflow_status_name | workflow_status_name | Unchanged | string |
| - | kpi_name1 | **NEW** | string |
| - | kpi_value1 | **NEW** | number |
| - | kpi_name2 | **NEW** | string |
| - | kpi_value2 | **NEW** | number |
| - | kpi_name3 | **NEW** | string |
| - | kpi_value3 | **NEW** | number |
| - | kpi_name4 | **NEW** | string |
| - | kpi_value4 | **NEW** | number |
| - | kpi_name5 | **NEW** | string |
| - | kpi_value5 | **NEW** | number |
| - | dim_custom1 | **NEW** | string |
| - | dim_custom2 | **NEW** | string |
| - | dim_custom3 | **NEW** | string |
| - | dim_custom4 | **NEW** | string |
| - | dim_custom5 | **NEW** | string |
| - | custom_properties | **NEW** | object |

---

### Line Item Fields Comparison

| v2.0 Field | v3.0 Field | Status | Type |
|------------|------------|--------|------|
| id | id | Unchanged | string |
| name | name | Unchanged | string |
| start_date | start_date | Unchanged | string (date) |
| end_date | end_date | Unchanged | string (date) |
| channel | channel | Unchanged | string |
| channel_custom | channel_custom | Unchanged | string |
| vehicle | vehicle | Unchanged | string |
| vehicle_custom | vehicle_custom | Unchanged | string |
| partner | partner | Unchanged | string |
| partner_custom | partner_custom | Unchanged | string |
| media_product | media_product | Unchanged | string |
| media_product_custom | media_product_custom | Unchanged | string |
| location_type | location_type | Unchanged | string (enum) |
| location_name | location_name | Unchanged | string |
| target_audience | target_audience | Unchanged | string |
| adformat | adformat | Unchanged | string |
| adformat_custom | adformat_custom | Unchanged | string |
| kpi | kpi | Unchanged | string |
| kpi_custom | kpi_custom | Unchanged | string |
| - | kpi_value | **NEW** | number |
| dayparts | dayparts | Unchanged | string |
| dayparts_custom | dayparts_custom | Unchanged | string |
| inventory | inventory | Unchanged | string |
| inventory_custom | inventory_custom | Unchanged | string |
| - | buy_type | **NEW** | string |
| - | buy_commitment | **NEW** | string |
| dim_custom1 | dim_custom1 | Unchanged | string |
| dim_custom2 | dim_custom2 | Unchanged | string |
| dim_custom3 | dim_custom3 | Unchanged | string |
| dim_custom4 | dim_custom4 | Unchanged | string |
| dim_custom5 | dim_custom5 | Unchanged | string |
| dim_custom6 | dim_custom6 | Unchanged | string |
| dim_custom7 | dim_custom7 | Unchanged | string |
| dim_custom8 | dim_custom8 | Unchanged | string |
| dim_custom9 | dim_custom9 | Unchanged | string |
| dim_custom10 | dim_custom10 | Unchanged | string |
| - | is_aggregate | **NEW** | boolean |
| - | aggregation_level | **NEW** | string |
| cost_currency | cost_currency | Unchanged | string |
| - | cost_currency_exchange_rate | **NEW** | number |
| cost_total | cost_total | Unchanged | number |
| cost_media | cost_media | Unchanged | number |
| cost_buying | cost_buying | Unchanged | number |
| cost_platform | cost_platform | Unchanged | number |
| cost_data | cost_data | Unchanged | number |
| cost_creative | cost_creative | Unchanged | number |
| cost_custom1-10 | cost_custom1-10 | Unchanged | number (×10) |
| - | cost_minimum | **NEW** | number |
| - | cost_maximum | **NEW** | number |
| metric_impressions | metric_impressions | Unchanged | number |
| metric_clicks | metric_clicks | Unchanged | number |
| metric_views | metric_views | Unchanged | number |
| - | metric_view_starts | **NEW** | number |
| - | metric_view_completions | **NEW** | number |
| - | metric_reach | **NEW** | number |
| - | metric_units | **NEW** | number |
| - | metric_impression_share | **NEW** | number |
| metric_engagements | metric_engagements | Unchanged | number |
| metric_followers | metric_followers | Unchanged | number |
| metric_visits | metric_visits | Unchanged | number |
| metric_leads | metric_leads | Unchanged | number |
| metric_sales | metric_sales | Unchanged | number |
| metric_add_to_cart | metric_add_to_cart | Unchanged | number |
| metric_app_install | metric_app_install | Unchanged | number |
| metric_application_start | metric_application_start | Unchanged | number |
| metric_application_complete | metric_application_complete | Unchanged | number |
| metric_contact_us | metric_contact_us | Unchanged | number |
| metric_download | metric_download | Unchanged | number |
| metric_signup | metric_signup | Unchanged | number |
| - | metric_page_views | **NEW** | number |
| - | metric_likes | **NEW** | number |
| - | metric_shares | **NEW** | number |
| - | metric_comments | **NEW** | number |
| - | metric_conversions | **NEW** | number |
| metric_max_daily_spend | metric_max_daily_spend | Unchanged | number |
| metric_max_daily_impressions | metric_max_daily_impressions | Unchanged | number |
| metric_audience_size | metric_audience_size | Unchanged | number |
| metric_custom1-10 | metric_custom1-10 | Unchanged | number (×10) |
| - | metric_formulas | **NEW** | object |
| - | custom_properties | **NEW** | object |

---

### Dictionary Groups Comparison

| v2.0 Group | v3.0 Group | Status | Structure |
|------------|------------|--------|-----------|
| - | meta_custom_dimensions | **NEW** | custom_field_config (dim_custom1-5) |
| - | campaign_custom_dimensions | **NEW** | custom_field_config (dim_custom1-5) |
| **custom_dimensions** | **lineitem_custom_dimensions** | **RENAMED** | custom_field_config (dim_custom1-10) |
| - | standard_metrics | **NEW** | metric_formula_config (25 metrics) |
| custom_metrics | custom_metrics | **Enhanced** | custom_metric_config (added formula fields) |
| custom_costs | custom_costs | Unchanged | custom_field_config (cost_custom1-10) |

---

## Enum Changes

### location_type (expanded)

**v2.0**: `["Country", "State"]`

**v3.0**: `["Country", "State", "DMA", "County", "Postcode", "Radius", "POI"]`

---

## New Object Structures

### target_audiences item

```json
{
  "name": "string (required)",
  "description": "string",
  "demo_age_start": "integer",
  "demo_age_end": "integer",
  "demo_gender": "string (enum: Male/Female/Any)",
  "demo_attributes": "string",
  "interest_attributes": "string",
  "intent_attributes": "string",
  "purchase_attributes": "string",
  "content_attributes": "string",
  "exclusion_list": "string",
  "extension_approach": "string",
  "population_size": "integer"
}
```

### target_locations item

```json
{
  "name": "string (required)",
  "description": "string",
  "location_type": "string (enum)",
  "location_list": ["string"],
  "exclusion_type": "string (enum)",
  "exclusion_list": ["string"],
  "population_percent": "number (0-1)"
}
```

### metric_formulas value

```json
{
  "metric_leads": {
    "formula_type": "string",
    "base_metric": "string",
    "coefficient": "number",
    "parameter1": "number",
    "parameter2": "number",
    "parameter3": "number",
    "comments": "string"
  }
}
```

---

## Related Documents

- **README.md** - Full v3.0 feature documentation
- **Schema files** - schemas/3.0/*.schema.json
- **Example file** - examples/example_mediaplan_v3.0.json
