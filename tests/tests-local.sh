#!/usr/bin/env bash
python ./healthcheck.py
pytest ./functional/src > ./logs/pytest.output.log