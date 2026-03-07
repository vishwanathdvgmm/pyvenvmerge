# 🏗️ High-Level System Architecture

```mermaid
flowchart TD
CLI[CLI Layer] --> Orchestrator[Application Orchestrator]

    Orchestrator --> Core[Core Services]

    Core --> EnvInspector[Environment Inspector]
    Core --> ReqExtractor[Requirement Extractor]
    Core --> DepMerger[Dependency Merger]
    Core --> ConflictResolver[Conflict Resolver]
    Core --> Executor[Environment Builder]
    Core --> IntegrityValidator[Integrity Validator]

    Core --> Infra[Infrastructure Layer]

    Infra --> SubprocessRunner[Subprocess Runner]
    Infra --> FileUtils[File System Utilities]
    Infra --> Logging[Logging]
```

---

# 📁 Final Project Structure

```
Pyvenvmerge/
├── 📁 src
│   └── 📁 pyvenvmerge
│       ├── 📁 core
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 executor.py
│       │   ├── 🐍 extractor.py
│       │   ├── 🐍 inspector.py
│       │   ├── 🐍 merger.py
│       │   ├── 🐍 planner.py
│       │   ├── 🐍 resolver.py
│       │   └── 🐍 validator.py
│       ├── 📁 infra
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 exceptions.py
│       │   └── 🐍 subprocess_runner.py
│       ├── 📁 models
│       │   ├── 🐍 __init__.py
│       │   ├── 🐍 conflict.py
│       │   ├── 🐍 environment.py
│       │   ├── 🐍 merge_plan.py
│       │   ├── 🐍 merge_report.py
│       │   └── 🐍 requirement.py
│       ├── 🐍 __init__.py
│       ├── 🐍 __main__.py
│       ├── 🐍 cli.py
│       └── 🐍 orchestrator.py
├── ⚙️ .gitignore
├── 📝 ARCHITECTURE.md
├── 📄 LICENSE
├── 📝 README.md
└── ⚙️ pyproject.toml
```

---

# 🔷 Layer 1 — CLI Layer

`cli.py`

Responsibilities:

- Parse arguments
- Validate input paths
- Pass config to orchestrator
- Handle exit codes

No business logic here.

---

# 🔷 Layer 2 — Orchestrator

`orchestrator.py`

Central control flow.

Pseudo-flow:

```
1. Inspect environments
2. Extract dependencies
3. Merge dependency sets
4. Resolve conflicts
5. Create MergePlan
6. Execute plan (create environment + install packages)
7. Run integrity check
8. Generate report
```

The orchestrator coordinates modules — it does not implement logic.

---

# 🔷 Layer 3 — Core Modules

### 1️⃣ inspector.py

Validates:

- Path exists
- pyvenv.cfg exists
- Python executable exists
- Python version compatibility

Returns:

```Python
Environment(
path: Path,
python_version: str,
interpreter_path: Path
)
```

---

### 2️⃣ extractor.py

Uses subprocess:

```bash
python -m pip freeze
```

Returns:

```python
dict[str, Requirement]
```

Handles:

- editable installs
- git installs
- file installs

---

### 3️⃣ merger.py

Combines multiple requirement dictionaries.

Output:

```
MergedRequirements
```

Does not resolve conflicts — just aggregates.

---

### 4️⃣ resolver.py

Implements strategy pattern.

Strategies:

- HighestVersionStrategy
- StrictStrategy
- UnpinnedStrategy

Uses:

```
packaging.version.Version
```

Returns:

```
ResolvedRequirements
ConflictReport
```

---

### 5️⃣ executor.py

Responsibilities:

- Create venv
- Upgrade pip/setuptools/wheel
- Write temp requirements file
- Install dependencies

No merging logic here.

---

### 6️⃣ validator.py

Runs:

```bash
pip check
```

Returns:

```
ValidationResult
```

Ensures:

- No broken requirements
- No dependency conflicts

---

# 🔷 Infrastructure Layer

### subprocess_runner.py

Centralized wrapper:

- Capture stdout
- Capture stderr
- Handle non-zero exit
- Timeout handling

Prevents scattered subprocess logic.

---

### filesystem.py

Utilities:

- Write temporary requirement file
- Remove temp files
- Validate directory structure

---

### logger.py

Optional but recommended.

- Structured logging
- Verbosity control
- Debug mode

---

# 🔷 Models Layer

Keep data structured.

### requirement.py

Represents:

```
name
version
source_type (pypi, git, editable, file)
raw_line
```

---

### environment.py

Represents validated venv.

---

### merge_report.py

Tracks:

- Conflicts
- Selected versions
- Ignored packages
- Warnings

Useful for dry-run mode.

---

# 🔄 Data Flow

```mermaid
flowchart TD
    A[User Input]
    B[CLI]
    C[Orchestrator]

    D[Inspector]
    E[Extractor]
    F[Merger]
    G[Resolver]

    H[Builder]
    I[Validator]
    J[Report to CLI]

    A --> B --> C
    C --> D
    D --> E --> F --> G
    G --> H --> I --> J
```

---

# 🧠 Design Principles

1. No direct filesystem editing of venv internals
2. Deterministic rebuild
3. Strategy-based conflict resolution
4. Clean separation of logic
5. Reusable core independent of CLI
6. Reproducibility over cleverness

---

# 📦 Future Extensibility

You can later add:

- Lockfile generation
- JSON output mode
- Dry-run report mode
- Interactive conflict resolution
- Support for pyproject.toml export
- Parallel pip install
- Caching layer

Architecture already supports that.

---

# 🔐 Failure Handling Design

Every stage must:

- Fail fast
- Provide clear error
- Return structured result

Exit codes:

| Code | Meaning                        |
| ---- | ------------------------------ |
| 0    | Success                        |
| 1    | Invalid environment            |
| 2    | Version conflict (strict mode) |
| 3    | Installation failure           |
| 4    | Validation failure             |
