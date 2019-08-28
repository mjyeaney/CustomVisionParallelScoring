#!/bin/bash

echo "Running unit tests..."
python -m unittest src/tests/*.py
echo "Unit tests runner complete"