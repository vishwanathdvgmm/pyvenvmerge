# pyvenvmerge

A CLI utility that safely merges multiple Python virtual environments by reconstructing dependencies instead of modifying venv internals.

---

## Features (v0.4.0)

- Validates input virtual environments
- Enforces Python version consistency
- Extracts dependencies using `pip freeze`
- Structured dependency parsing (PEP 508 compliant)
- Specifier-based dependency merging
- Accurate conflict detection using constraint intersection
- Multiple conflict resolution strategies:
    - `highest` (default)
    - `strict`
    - `unpinned`
- Deterministic environment rebuild
- Dependency integrity verification (`pip check`)
- Dry-run mode
- Conflict reporting
- JSON merge plan output
- Support for **editable installs (`-e`)**
- Support for **Git dependencies (`git+...`)**
- Support for **file-based dependencies (`package @ file://...`)**
- Safe handling of non-PyPI dependencies during merge
- Two-phase installation pipeline:
    - PyPI dependencies installed first.
    - Special depedencies installed separately.
- Conflict detection for incompatible non-PyPI dependencies.

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

---

# Conflict Resolution Strategies:

```bash
pyvenvmerge envA envB -o mergedEnv --strategy highest
# default

pyvenvmerge envA envB -o mergedEnv --strategy strict

pyvenvmerge envA envB -o mergedEnv --strategy unpinned
```

---

# Dry-Run Mode

Preview the merge plan without creating an environment:

```bash
pyvenvmerge envA envB --dry-run
```

---

# JSON Report

```bash
pyvenvmerge envA envB --dry-run --report json
```

---

### Limitations

Current limitations:

- No deep resolution for Git/file dependencies.
- Dependency markers are not fully evaluated..
- Extra merging is basic.

These will be improved in future versions.

---

### Version Note

v0.4 extends the system to handle real-world environments:

- Introduces support for non-PyPI depenencies.
- Improves installation correctness with staged installs.
- Adds safety checks for incompatible external dependencies..

## This version makes the tool usable on practical projects.

### Architecture

Detailed architecture documentation:

[ARCHITECTURE](https://github.com/vishwanathdvgmm/pyvenvmerge/blob/main/ARCHITECTURE.md)

---

### License

MIT License
