# Changelog

All notable changes to **pyvenvmerge** are documented in this file.

The project follows incremental internal releases while maintaining stable public milestones.

---

# v0.9.0

## Added

- Compatibility scoring integrated into merge plans
- Merge risk classification system
- Quantified merge safety analysis
- Risk-aware dry-run diagnostics
- JSON compatibility metrics output
- Enhanced CLI diagnostics visibility

## Diagnostics

- Compatibility Score (0–100)
- Risk Level:
    - LOW
    - MEDIUM
    - HIGH

## Improved

- Dry-run reporting clarity
- Merge safety visibility
- Warning aggregation logic

## Example

```bash
Compatibility Score: 82/100
Risk Level: MEDIUM
```

---

# v0.8.0

## Added

- Compatibility scoring engine
- Merge risk classification
- Quantified merge safety analysis
- Risk-aware dry-run diagnostics
- JSON safety metrics output

## Diagnostics

- Compatibility Score (`0–100`)
- Risk Levels:
    - `LOW`
    - `MEDIUM`
    - `HIGH`

## Improved

- Dry-run reporting clarity
- Merge safety visibility
- Warning aggregation logic

## Example

```bash
Compatibility Score: 72/100
Risk Level: MEDIUM
```

---

# v0.7.0

## Added

- Semantic dependency validation
- Accurate dependency constraint verification
- Semantic version compatibility checks

## Integrated

- `packaging.version.Version`
- `packaging.specifiers.SpecifierSet`

## Improved

- Dependency warning precision
- Invalid dependency selection detection
- Planner validation accuracy

## Example

Detects invalid merges such as:

```text
package requires numpy<2.0
selected version: numpy==2.4.2
```

---

# v0.6.0

## Added

- Dependency graph analysis
- Transitive dependency inspection
- Constraint violation warnings

## Integrated

- `importlib.metadata`

## Improved

- Planner intelligence
- Dependency relationship analysis
- Merge validation depth

## Capabilities

- Detect indirect dependency incompatibilities
- Warn before environment execution
- Analyze package dependency relationships

---

# v0.5.0

## Added

- Conflict classification system
- Warning generation engine
- Structured merge diagnostics

## Conflict Types

- `VERSION_CONFLICT`
- `PARTIAL_SPECIFIER`

## Improved

- Dry-run diagnostics
- JSON reporting
- Planner visibility
- Merge analysis output

## Reporting

Dry-run output now includes:

- Conflict classifications
- Per-conflict warnings
- Global warnings
- Structured JSON warnings

---

# v0.4.0

## Added

- Editable install support (`-e`)
- Git dependency support (`git+...`)
- File dependency support (`package @ file://...`)

## Improved

- Non-PyPI dependency handling
- Two-phase installation pipeline
- External dependency merge safety

## Installation Pipeline

Phase 1:

```text
PyPI dependencies
```

Phase 2:

```text
External dependencies
```

---

# v0.3.0

## Added

- Structured dependency parsing
- PEP 508 compliant requirement handling
- Specifier-based merge logic

## Improved

- Dependency resolution architecture
- Requirement normalization
- Internal parsing reliability

## Integrated

- `packaging.requirements`
- `SpecifierSet`
- `Marker`

---

# v0.2.0

## Added

- Dry-run mode
- Conflict reporting
- JSON merge plan output

## Improved

- Merge visibility
- CLI diagnostics
- Planning workflow

## Reporting

Supported outputs:

- Console reports
- JSON reports

---

# v0.1.0

## Initial Release

### Core Features

- Virtual environment inspection
- Python version validation
- Dependency extraction using `pip freeze`
- Environment reconstruction
- Conflict resolution strategies
- Integrity validation using `pip check`

### Supported Strategies

- `highest`
- `strict`
- `unpinned`
