import os

from google.cloud import secretmanager_v1


def get_secret(secret_name):

    client = secretmanager_v1.SecretManagerServiceClient()
    full_secret_name = (
        f"projects/{os.getenv('PROJECT_ID')}/secrets/{secret_name}/"
        "versions/latest"
    )
    response = client.access_secret_version(name=full_secret_name)
    return response.payload.data.decode('UTF-8')
