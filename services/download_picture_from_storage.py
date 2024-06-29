from google.cloud import storage

client = storage.Client(project='photo-viewer-407717')
bucket = client.get_bucket('photo-viewer-407717.appspot.com')
