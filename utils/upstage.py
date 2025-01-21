from pathlib import Path
from time import sleep
from dotenv import load_dotenv
import requests
import json
import boto3
import os

load_dotenv()

UPSTAGE_API_KEY=os.getenv("UPSTAGE_API_KEY")
UPSTAGE_OCR_ENDPOINT=os.getenv("UPSTAGE_OCR_ENDPOINT")
UPSTAGE_DOCPARSE_ENDPOINT=os.getenv("UPSTAGE_DOCPARSE_ENDPOINT")

SAGEMAKER_OCR_ENDPOINT_NAME=os.getenv("SAGEMAKER_OCR_ENDPOINT_NAME")

if SAGEMAKER_OCR_ENDPOINT_NAME:
    session = boto3.Session(profile_name='upstage')
    client = session.client(service_name='sagemaker-runtime', region_name='ap-northeast-2')


def ocr_image_upstage(file_path, api_key=UPSTAGE_API_KEY):
    """
    Performs OCR usign Upstage OCR API.
    An API key is required.

    :param file_path: The file path of the image to perform OCR
    :param api_key: Upstage API Key
    :return: Resulting Python dictionary of OCR
    """
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(file_path, 'rb') as image:
        files = {"document": image.read()}

    response = requests.post(UPSTAGE_OCR_ENDPOINT, headers=headers, files=files)

    return response.json()


def docparse_image_upstage(file_path, api_key=UPSTAGE_API_KEY):
    """
    Performs docparse using Upstage OCR API.
    An API key is required.

    :param file_path: The file path of the image to perform docparse
    :param api_key: Upstage API Key
    :return: Resulting Python dictionary of docparse
    """
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(file_path, 'rb') as image:
        files = {"document": image.read(), "output_formats": ["html", "markdown"]}

    response = requests.post(UPSTAGE_DOCPARSE_ENDPOINT, headers=headers, files=files)

    return response.json()


def ocr_image_sagemaker(file_path):
    """
    Performs OCR usign Upstage OCR deployed in SageMaker.
    Access to the endpoint is required.

    :param file_path: The file path of the image to perform OCR
    :return: Resulting Python dictionary of OCR
    """
    with open(file_path, "rb") as image:
        byte_image = image.read()
        response = client.invoke_endpoint(
            EndpointName=SAGEMAKER_OCR_ENDPOINT_NAME,
            ContentType="image/jpeg",
            Body=byte_image,
        )


    return json.loads(response['Body'].read())


def ocr_all_images(directory, ocr_function=ocr_image_upstage):
    """
    This function assumes the directory structure described in README,
    and peforms OCR over all images that are present in the directory using the OCR function of choice.
    It saves all resulting json files to the image directory, and returns all results.

    :param ocr_function: OCR function (Upstage or SageMaker) to use
    :param directory: Image directory to use
    :return:
    """
    results = []

    for file_path in Path(directory).rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:

            print(f"Processing {file_path}")

            try:
                result = ocr_function(file_path)
                # Retry every five seconds
                while "error" in result:
                    sleep(5)
                    result = ocr_function(str(file_path))

                print(f"Successfully parsed {file_path}")


            except Exception as e:
                result = {"file_path": str(file_path), "error": str(e)}
                print(f"Failed to parse {file_path}: {e}")

            with open(str(file_path.with_suffix(".json")), "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

    return results
