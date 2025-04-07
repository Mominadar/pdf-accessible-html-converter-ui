import io
import os
import sys
import zipfile
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

sys.path.append(".")

from services.object_store.S3Client import S3Client


load_dotenv()

folders_to_zip = ['./services', './utils', './pandoc', '.'] # '.' mean current directory

# lambda config 
LAMBDA_REGION_NAME = "eu-north-1"
BUCKET_NAME="pdf-accessible-html-converter"

lambda_map = {
    'pdf-accessible-html-convertor': 'main_lambda',
    'pdf-accessible-html-convertor-async': 'file_lambda',
    'pdf-to-accessible-html-step-1-divide-into-chunks': 'split_file_into_chunks',
    "pdf-accessible-html-step-3-merge-chunks": "merge_chunks",
    "pdf-accessible-html-error-handler": "converter_error_handler"
}

client = boto3.client('lambda', region_name=LAMBDA_REGION_NAME)

def zip_folder(folder_path, zipf, is_recursive=True):
    """
    Adds files from the given folder to the zip file.

    Args:
        folder_path (str): Path to the folder to be zipped.
        zipf (zipfile.ZipFile): Open zip file object.
        is_recursive (bool): If True, adds files from subdirectories recursively.
    """
    if is_recursive:
        # Recursively add all .py files from folder and subfolders
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file == 'pandoc-3.6.4-1-amd64.deb' or file=="pandoc" or file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.getcwd())
                    zipf.write(file_path, arcname)
    else:
        # Add only .py files from the given folder (non-recursive)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if (file == 'pandoc-3.6.4-1-amd64.deb' or file=="pandoc" or file.endswith('.py')) and os.path.isfile(file_path):
                zipf.write(file_path, os.path.basename(file_path))

def zip_current_folder(zip_name, lambda_dir):
    """
    Zips specific folders and files into a zip archive.

    Args:
        zip_name (str): Name of the output zip file.
    """
    current_dir = os.getcwd()

    # Create a zip file with compression
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Step 1: Add .py files from the root directory (non-recursive)
        zip_folder(current_dir, zipf, is_recursive=False)

        # Step 2: Add subdirectories recursively (e.g., 'lambda-layer/')
        dirs_to_copy = ['./services','./utils', './pandoc']
        for directory in dirs_to_copy:
            subfolder = os.path.join(current_dir, directory)
            if os.path.exists(subfolder):
                zip_folder(subfolder, zipf, is_recursive=True)

        # Step 3: Add 't.py' from '/deploy/lambda/' to the root of the zip
        lambda_entrypoint = 'lambda_function.py'
        lambda_file = os.path.join(current_dir, 'deploy', 'lambda', lambda_dir, lambda_entrypoint)
        if os.path.isfile(lambda_file):
            zipf.write(lambda_file, lambda_entrypoint)

    print(f"Files zipped successfully into '{zip_name}'.")

def upload_zip_to_lambda(zip_name, function_name):

    try:
        with open(zip_name, 'rb') as zip_file:
            zip_content = zip_file.read()

        response = client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )

        print(f"Successfully uploaded the zip to Lambda function '{function_name}'.")
        return response

    except NoCredentialsError:
        print("AWS credentials not available.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def deploy_lambda(lambda_function_name, zip_name):
    """Create or update the Lambda function from S3."""
    try:
        # Check if the function exists
        client.get_function(FunctionName=lambda_function_name)
        print("ℹ️ Lambda function exists. Updating...")

        # Update the function code
        response = client.update_function_code(
            FunctionName=lambda_function_name,
            S3Bucket=BUCKET_NAME,
            S3Key=zip_name,
        )
        print("✅ Lambda function updated:", response["FunctionArn"])

    except Exception as e:
        print("ℹ️ Error", e)

def upload(name):
    # Specify the zip file name
    lambda_dir = lambda_map[name]
    zip_name = f'lambda_function_code_{lambda_dir}.zip'
    
    # Call the function to zip the folder
    zip_current_folder(zip_name, lambda_dir)
        
    # Upload the zip file to AWS Lambda
    #upload_zip_to_lambda(zip_name, LAMBDA_FUNCTION_NAME)
    s3 = S3Client()
    file = os.path.join(os.getcwd(),zip_name)
    with open(file, "rb") as rb_file:
        file_bytes = io.BytesIO(rb_file.read())

    s3.upload_file(zip_name, file_bytes, bucket=BUCKET_NAME)
    deploy_lambda(name, zip_name)
    # remove zip file
    os.remove(zip_name)

# To run locally
if __name__ == "__main__":
    # upload("pdf-accessible-html-convertor")
    # upload("pdf-accessible-html-convertor-async")
    # upload("pdf-to-accessible-html-step-1-divide-into-chunks")
    # upload("pdf-accessible-html-step-3-merge-chunks")
    upload("pdf-accessible-html-error-handler")
