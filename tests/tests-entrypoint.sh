#!/usr/bin/env bash
pip install -r /tests/test_requirements.txt
python3 /tests/healthcheck.py
pytest /tests/functional/src --durations=3 > /tests/logs/pytest.output.log
