![PyPI](https://img.shields.io/pypi/v/pyvenvmerge)
![Python](https://img.shields.io/pypi/pyversions/pyvenvmerge)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

# pyvenvmerge

A Python CLI utility for safely merging multiple virtual environments through deterministic dependency reconstruction instead of direct venv modification.

---

## Features

### Environment Analysis

- Virtual environment validation
- Python version compatibility checks
- Dependency extraction using `pip freeze`

### Dependency Resolution

- PEP 508 compliant parsing
- Specifier-based merging
- Conflict detection and resolution
- Semantic dependency validation

### Merge Intelligence

- Dependency graph analysis
- Conflict classification
- Risk analysis and compatibility scoring
- Dry-run diagnostics

### Dependency Support

- PyPI packages
- Editable installs (`-e`)
- Git dependencies (`git+...`)
- File dependencies (`package @ file://...`)

### Reliability

- Deterministic environment rebuild
- Two-phase installation pipeline
- Integrity verification using `pip check`
- JSON merge reports

### Reporting & Reproducibility

- Structured merge report generation
- JSON report export
- Deterministic lockfile export
- Resuable report generation layer
- Serializable merge metadata artifacts

### Example

```bash
pyvenvmerge envA envB --dry-run
```

Example output:

```text
Compatibility Score : 82/100
Risk Level          : MEDIUM

Warnings:
⚠ pandas requires numpy<2.0 but selected version is 2.4.2
```

---

## Installation

```bash
pip install pyvenvmerge
```

---

## Usage

```bash
pyvenvmerge envA envB -o mergedEnv
```

### Save structured data

```bash
pyvenvmerge envA envB --dry-run --save-report report.json
```

### Export deterministic lockfile

```bash
pyvenvmerge envA envB --dry-run --export-lock requirements.lock
```

---

## Conflict Resolution Strategies

```bash
pyvenvmerge envA envB -o mergedEnv --strategy highest
# default

pyvenvmerge envA envB -o mergedEnv --strategy strict

pyvenvmerge envA envB -o mergedEnv --strategy unpinned
```

---

## Dry-Run Mode

Preview the merge plan without creating an environment:

```bash
pyvenvmerge envA envB --dry-run
```

---

## JSON Report

```bash
pyvenvmerge envA envB --dry-run --report json
```

---

## Limitations

Current limitations:

- No deep resolution for Git/file dependencies.
- Environment markers are partially evaluated.
- Extra merging is basic.
- Advanced specifiers such as !=, ~=, === are not fully optimized yet.
- Complex specifier combination are not fully optimized yet.

These will be improved in future versions.

---

## Documentation

Detailed documentation:

[ARCHITECTURE](https://github.com/vishwanathdvgmm/pyvenvmerge/blob/main/ARCHITECTURE.md)
[CHANGELOG](https://github.com/vishwanathdvgmm/pyvenvmerge/blob/main/CHANGELOG.md)

---

## License

MIT License
