#!/bin/bash
python scrape_common_terms_polish.py 2>&1 | grep ERROR | tee logs/scrape_common_terms_polish.log
