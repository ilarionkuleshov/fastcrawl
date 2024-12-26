#!/bin/bash

generate_html_report=true
coverage_file=".coverage"

for option in "$@"; do
    case $option in
    --generate-html-report=*)
        generate_html_report="${option#*=}"
        shift
        ;;
    --coverage-file=*)
        coverage_file="${option#*=}"
        shift
        ;;
    *)
        echo "Unknown option: $option"
        exit 1
        ;;
    esac
done

coverage run --data-file=$coverage_file -m pytest tests/

if [ "$generate_html_report" == "true" ]; then
    coverage html --data-file=$coverage_file
fi
