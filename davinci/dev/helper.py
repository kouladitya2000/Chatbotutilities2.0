import os
from azure.storage.blob import BlobServiceClient

def upload_file_to_blob(file, STORAGEACCOUNTURL, STORAGEACCOUNTKEY, CONTAINERNAME):
    """
    Uploads a file to Azure Blob Storage.
    
    Parameters:
        file: Uploaded file object from Streamlit.
        STORAGEACCOUNTURL: Azure Storage Account URL.
        STORAGEACCOUNTKEY: Azure Storage Account Key.
        CONTAINERNAME: Azure Blob Storage container name.

    Returns:
        str: The name of the uploaded file.
    """
    if file:
        file_name = file.name

        blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)

        blob_client_instance = blob_service_client_instance.get_blob_client(container=CONTAINERNAME, blob=file_name)

        with file as data:
            blob_client_instance.upload_blob(data, overwrite=True)

        return file_name

def read_blob_data(STORAGEACCOUNTURL, STORAGEACCOUNTKEY, CONTAINERNAME, file_name):
    """
    Reads and returns data from Azure Blob Storage.

    Parameters:
        STORAGEACCOUNTURL: Azure Storage Account URL.
        STORAGEACCOUNTKEY: Azure Storage Account Key.
        CONTAINERNAME: Azure Blob Storage container name.
        file_name: Name of the blob to read.

    Returns:
        str: The contents of the blob as a string.
    """
    blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
    blob_client_instance = blob_service_client_instance.get_blob_client(container=CONTAINERNAME, blob=file_name)
    blob_data = blob_client_instance.download_blob()
    data = blob_data.readall().decode('utf-8')
    return data
