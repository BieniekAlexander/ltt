#!/bin/bash
docker build -t gcr.io/language-training-toolkit-dev/ltt-backend .
docker push gcr.io/language-training-toolkit-dev/ltt-backend

# TODO add step to push thing to Cloud Run
gcloud run deploy ltt-backend \
    --image=gcr.io/language-training-toolkit-dev/ltt-backend \
    --region=us-central1 \
    --project=language-training-toolkit-dev
gcloud run services update-traffic --region us-central1 ltt-backend --to-latest
