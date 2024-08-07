import os

from google.api_core import exceptions
from google.cloud import secretmanager_v1


def get_secret(secret_name, version_id="latest"):

    client = secretmanager_v1.SecretManagerServiceClient()
    full_secret_name_with_id = (
        f"projects/{os.getenv('PROJECT_ID')}/secrets/{secret_name}/"
        f"versions/{version_id}"
    )
    full_secret_name_with_name = (
        f"projects/{os.getenv('PROJECT_NAME')}/secrets/{secret_name}/"
        f"versions/{version_id}"
    )
    full_secret_name_without_version = (
        f"projects/{os.getenv('PROJECT_ID')}/secrets/{secret_name}"
    )
    full_secret_name_without_version_name = (
        f"projects/{os.getenv('PROJECT_NAME')}/secrets/{secret_name}"
    )
    try:
        response = client.access_secret_version(name=full_secret_name_with_id)
    except exceptions.PermissionDenied:
        try:
            response = client.access_secret_version(
                name=full_secret_name_with_name
                )
        except exceptions.PermissionDenied:
            try:
                response = client.access_secret_version(
                    name=full_secret_name_without_version
                    )
            except exceptions.PermissionDenied:
                response = client.access_secret_version(
                    name=full_secret_name_without_version_name
                    )
    return response.payload.data.decode('UTF-8')
