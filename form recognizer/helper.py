from azure.storage.blob import BlobServiceClient
import os
import requests, uuid, json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient



def download_blob(sturl,stkey,cname,blobname,path):
    '''
       About:
       ---------
       Download a file from Blob Storage in Azure
        Return the difference in days between the current date and game release date.

        Parameter
        ---------
        sturl : str
            Release date in string format.
        stkey : str
            Key of the Storage account. HIGHLY Restricted
        cname : str
            Container name of the Storage account
        blobname : str
            Blob name to download
        path : str
            Path from which file to download
        

        Returns
        -------
        string

    
    '''

    STORAGEACCOUNTURL = sturl
    STORAGEACCOUNTKEY = stkey
    CONTAINERNAME = cname
    BLOBNAME = blobname
    path_blob = path+blobname

    DESTINATION_PATH = os.path.expanduser(path_blob)

    # Create a BlobServiceClient instance
    blob_service_client_instance = BlobServiceClient(
        account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)

    # Get a BlobClient instance for the specified blob
    blob_client_instance = blob_service_client_instance.get_blob_client(
        CONTAINERNAME, BLOBNAME)

    # Download the blob to the local file
    with open(DESTINATION_PATH, "wb") as local_file:
        blob_data = blob_client_instance.download_blob()
        blob_data.readinto(local_file)

    return (f"file downloaded and saved to {DESTINATION_PATH}")





def analyze_document(endpoint, key, downloaded_file_path):
    
    '''
       About:
       ---------
       This takes downloaded file as input along with form recognizer credentials.
      

        Parameter
        ---------
        endpoint : str
            Endpoint url of form recognizer
        key : str
            Key of the form recognizer. HIGHLY Restricted
        downloaded_file_path : str
            file path of the file downloaded from download blob

        

        Returns
        -------
        dict

        returns a dictionary with the "key_value_pairs" and "text_extracted" 

    
    '''


    try:
        # Read the content of the local document
        with open(downloaded_file_path, "rb") as local_file:
            document_content = local_file.read()

        # Initialize Form Recognizer client
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        # Analyze the document using Form Recognizer
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", document_content)
        result = poller.result()

        # Process and return the analysis results
        analysis_results = {
            "key_value_pairs": [],
            "text_extracted": []
        }

        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                analysis_results["key_value_pairs"].append({
                    "key": kv_pair.key.content,
                    "value": kv_pair.value.content
                })
            else:
                analysis_results["key_value_pairs"].append({
                    "key": kv_pair.key.content,
                    "value": None
                })

        for page in result.pages:
            for line in page.lines:
                analysis_results["text_extracted"].append(line.content)

        return analysis_results

    except Exception as e:
        return {"error": str(e)}
