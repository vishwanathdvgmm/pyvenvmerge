# pyvenvmerge

Safely merge multiple Python virtual environments by reconstructing dependencies.

## Features (v0.1.0)

- Validates input virtual environments
- Enforces Python version consistency
- Extracts dependencies using `pip freeze`
- Conflict resolution strategies:
    - highest (default)
    - strict
    - unpinned
- Rebuilds merged environment cleanly
- Runs `pip check` for validation

## Installation

```bash
pip install pyvenvmerge
```

## Usage

```bash
pyvenvmerge envA envB -o mergedEnv
```

With strategy:

```bash
pyvenvmerge envA envB -o mergedEnv --strategy highest
# default

pyvenvmerge envA envB -o mergedEnv --strategy strict

pyvenvmerge envA envB -o mergedEnv --strategy unpinned
```

### Limitations(v0.1.0)

- Editable installs not supported.
- Git dependencies not supported.
- File dependencies not supported.
- No dry-run mode yet.

### Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for design details.

### License

MIT License
