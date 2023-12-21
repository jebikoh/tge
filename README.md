# Terminal Graphics Engine

Set up with `poetry install` and active the environment with `poetry shell`.

Build the docs with `mkdocs build` or serve it with `mkdocs serve`.

## Status

The main rendering pipeline (for perspective projection) is done and working. Things left to do are:

-   Optimize scan conversion (slowest part)
-   Add caching
-   Add animation manager
-   Add additional lights, etc

## Command line tests

Parameterized tests can be found in the `tests` directory and sample models in `tests/models`. You can run tests from the root directory via:
 - `python -m tests.<test_name> <path_to_model> <options>`

Argument information can be found with:
 - `python -m tests.<test_name> -h`.
