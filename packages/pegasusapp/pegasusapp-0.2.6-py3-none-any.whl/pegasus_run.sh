#!/usr/bin/env bash

conda activate base
pip install -r /tmp/extracted_code/requirements.txt
python /tmp/extracted_code/train.py