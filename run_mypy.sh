#! /bin/bash
# Run Mypy type checking on this package

mypy . --strict-optional --ignore-missing-imports
