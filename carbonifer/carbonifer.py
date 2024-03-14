from flask import Flask, request
from queue import Queue
import threading
import json
import requests
import tarfile
import os
import boto3

app = Flask(__name__)
job_queue = Queue()

def process_job(payload):
    print("Received payload:", payload)
    # You can perform any processing on the payload here

def handle_jobs():
    while True:
        payload = job_queue.get()
        process_job(payload)
        job_queue.task_done()

# Start a background thread to handle jobs
job_thread = threading.Thread(target=handle_jobs)
job_thread.daemon = True
job_thread.start()

@app.route('/', methods=['POST'])
def receive_payload():
    if request.method == 'POST':
        try:
            payload = request.json
            job_queue.put(payload)
            return "OK", 200
        except Exception as e:
            print("Error processing payload:", e)
            return "Error", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

##Testing the Lambda function with a simple Hello World
def lambda_handler_test(event, context):
    result = "Hello World"
    return {
        'statusCode' : 200,
        'body': result
    }


def download_file(url, auth_header, destination_file):
    """
    Download a file from a URL with authorization header.
    
    Args:
        url (str): The URL of the file to download.
        auth_header (str): The authorization header value.
        destination_file (str): The path where the downloaded file will be saved.
    
    Returns:
        bool: True if the download is successful, False otherwise.
    """
    try:
        response = requests.get(url, headers={'Authorization': auth_header})
        if response.status_code == 200:
            with open(destination_file, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully to {destination_file}")
            return True
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def extract_tar_gz(file_path, destination_dir):
    """
    Extract a tar.gz file to a destination directory.
    
    Args:
        file_path (str): The path to the tar.gz file.
        destination_dir (str): The directory where the contents will be extracted.
    
    Returns:
        bool: True if extraction is successful, False otherwise.
    """
    try:
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(destination_dir)
        print(f"Extraction completed successfully to {destination_dir}")
        return True
    except Exception as e:
        print(f"Error extracting file: {e}")
        return False
    
def send_patch_request(url, auth_header, data=None):
    """
    Send a PATCH request with an authorization header and validate the response.
    
    Args:
        url (str): The URL to send the PATCH request to.
        auth_header (str): The authorization header value.
        data (dict): Optional data to include in the request payload.
    
    Returns:
        bool: True if the request is successful and response status code is 200, False otherwise.
    """
    try:
        headers = {'Authorization': auth_header}
        response = requests.patch(url, headers=headers, json=data)
        
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)
        
        # Validate response status code and body
        if response.status_code == 200:
            print("PATCH request successful.")
            return True
        else:
            print(f"PATCH request failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending PATCH request: {e}")
        return False


