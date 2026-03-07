# pyvenvmerge

A CLI utility that safely merges multiple Python virtual environments by reconstructing dependencies instead of modifying venv internals.

## Features (v0.2.0)

- Validates input virtual environments.
- Enforces Python version consistency.
- Extracts dependencies using `pip freeze`.
- Multiple conflict resolution strategies:
    - `highest` (default)
    - `strict`
    - `unpinned`
- Determines environment rebuild.
- Dependencies integrity verification (`pip check`).
- **Dry-run mode**
- **Conflict reporting**
- **JSON merge plan output**

## Installation

```bash
pip install pyvenvmerge
```

## Usage

```bash
pyvenvmerge envA envB -o mergedEnv
```

# Conflict Resolution Strategies:

```bash
pyvenvmerge envA envB -o mergedEnv --strategy highest
# default

pyvenvmerge envA envB -o mergedEnv --strategy strict

pyvenvmerge envA envB -o mergedEnv --strategy unpinned
```

# Dry-Run Mode

Preview the merge plan without creating an environment:

```bash
pyvenvmerge envA envB --dry-run
```

# JSON Report

```bash
pyvenvmerge envA envB --dry-run --report json
```

### Limitations

Current limitations:

- Editable installs not supported.
- Git dependencies not supported.
- File dependencies not supported.

Support for these may be added in future versions.

### Architecture

Detailed architecture documentation:

[ARCHITECTURE](https://github.com/vishwanathdvgmm/pyvenvmerge/blob/main/ARCHITECTURE.md)

Key fixes:

- Version updated to **0.2.0**
- Dry-run and JSON features added
- Absolute GitHub architecture link (fixes PyPi 404)

### License

MIT License
