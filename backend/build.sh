#!/bin/bash
# temp script to push images for this backend
gcloud builds submit . --config="$(pwd)/cloudbuild.yaml" --substitutions _IMAGE_NAME=ltt-backend:latest