#!/bin/bash

coverage run -m pytest tests/
coverage html
