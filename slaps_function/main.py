import functions_framework
from google.cloud import storage

@functions_framework.http
def hello_http(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Methods": "POST"
    }
    if request.method == "OPTIONS":
        return ("", 200, headers)
    client = storage.Client()
    bucket = client.get_bucket('zach-slaps')
    blob = bucket.get_blob('slaps.json')
    return(blob.download_as_text(), 200, headers)
