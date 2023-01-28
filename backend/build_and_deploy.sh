#!/bin/bash
docker build -t gcr.io/language-training-toolkit-dev/ltt-backend .
docker push gcr.io/language-training-toolkit-dev/ltt-backend