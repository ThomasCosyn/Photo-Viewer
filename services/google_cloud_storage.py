from google.cloud import storage


def create_storage_client():
    """
    Creates a storage client.

    Returns:
        A storage client object.
    """
    return storage.Client()


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = create_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print(f'Blob {blob_name} deleted.')


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = create_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f'Blob {source_blob_name} downloaded to {destination_file_name}.')


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = create_storage_client()
    blobs = storage_client.list_blobs(bucket_name)

    return blobs


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = create_storage_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name}.')
