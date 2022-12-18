#!/bin/bash
# this function packages cloud function code and dependencies into a temporary directory, zips it, writes it to cloud storage, and pushes it
# TODO maybe clean up what is being packaged, and how
cf_name="scrape-term"
tmp_dir=$(mktemp -d -t cf_${cf_name}_XXXXXXXX)
cp -r ../../../* $tmp_dir
cp -r ../../../../requirements.txt $tmp_dir
cp main.py $tmp_dir

# Zip the temporary directory
pushd $tmp_dir
zip -r $cf_name.zip .
popd

# Upload the zip to GCS
gsutil cp $tmp_dir/$cf_name.zip gs://language-training-toolkit-dev-cloud-functions/$cf_name.zip

# Upload zip to cloud functions
gcloud functions deploy $cf_name \
    --gen2 \
    --region=us-central1 \
    --runtime=python39 \
    --stage-bucket=language-training-toolkit-dev-cloud-functions \
    --source=gs://language-training-toolkit-dev-cloud-functions/$cf_name.zip \
    --entry-point=scrape_term \
    --trigger-http \
    --allow-unauthenticated