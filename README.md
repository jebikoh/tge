# Terminal Graphics Engine

Set up with `poetry install` and active the environment with `poetry shell`.

Build the docs with `mkdocs build` or serve it with `mkdocs serve`.

When running tests, run from root directory (e.g. `python -m tests.test`)

## Status

The main rendering pipeline (for perspective projection) is done and working. Things left to do are:

-   Optimize scan conversion (slowest part)
-   Add animation manager
-   Clean up tests
