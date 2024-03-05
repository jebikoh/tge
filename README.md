# Terminal Graphics Engine

Set up with `poetry install` and active the environment with `poetry shell`.

Build the docs with `mkdocs build` or serve it with `mkdocs serve`.

I started working on a new version written in C: [JTX](https://github.com/jebikoh/jtx)

## Sample

Here is a sample of a spinning taurus. Run this via: `python -m tests.a_dir tests/models/taurus.obj`

https://github.com/jebikoh/tge/assets/12992023/4f67c66f-7d0a-4bdf-a085-a18f921b332a



## To-Do
-   Optimize scan conversion (slowest part)
-   Add caching
-   Add animation manager
-   Add additional lights, etc

## Command line tests

Parameterized tests can be found in the `tests` directory and sample models in `tests/models`. You can run tests from the root directory via:
 - `python -m tests.<test_name> <path_to_model> <options>`

Argument information can be found with:
 - `python -m tests.<test_name> -h`.

NOTE: The program will crash if the model is too large. Use the scale parameters to scale the models down.
