aws s3 cp index.html s3://www.youjustgotslapped.com/index.html
aws s3 cp style.css s3://www.youjustgotslapped.com/style.css
aws s3 cp tab.js s3://www.youjustgotslapped.com/tab.js
gsutil cp slaps.json gs://zach-slaps/slaps.json
gcloud functions deploy function-2 --gen2 --region=us-east4 --runtime=python312 --source=slaps_function --entry-point=hello_http --trigger-http
gcloud functions deploy function-1 --gen2 --region=us-east4 --runtime=python312 --source=stats_function --entry-point=hello_http --trigger-http
echo "hello"