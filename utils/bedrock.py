from pathlib import Path
from utils.bedrock_models import BedrockModel
from utils.prompts import JSON_GENERATE_PROMPT, VALIDATE_PROMPT
from dotenv import load_dotenv
import boto3
import json
import base64
import os

load_dotenv()

BEDROCK_REGION=os.getenv("BEDROCK_REGION")

bedrock_client = boto3.client(region_name=BEDROCK_REGION, service_name='bedrock-runtime')

def generate_json_with_ocr(ocr_text, model=BedrockModel.CLAUDE_3_5_HAIKU_1_0):
    sys_prompt = [{"text": JSON_GENERATE_PROMPT}]
    user_prompt = [
        {
            "role": "user",
            "content": [
                {
                    "text": f"<text_input>{ocr_text}</text_input>"
                }
            ]
        }
    ]

    response = bedrock_client.converse(
        modelId=model.value,
        messages=user_prompt,
        system=sys_prompt
    )

    return response['output']['message']['content'][0]['text']


def generate_json_with_ocr_and_image(ocr_text, image_data, model=BedrockModel.CLAUDE_3_HAIKU_1_0):
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"<instructions>{JSON_GENERATE_PROMPT}</instructions\n<ocr_text_input>{ocr_text}</ocr_text_input>"
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64.b64encode(image_data).decode('utf-8')
                        }
                    }
                ]
            }
        ],
        "temperature": 0,
        "top_p": 0.999,
        "top_k": 250,
    }

    response = bedrock_client.invoke_model(
        modelId=model.value,
        body=json.dumps(request_body)
    )

    response_body = json.loads(response["body"].read())

    return response_body["content"][0]["text"]


def validate_with_image(image_data, text_data, response, model=BedrockModel.CLAUDE_3_5_SONNET_2_0):
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"<instructions>{VALIDATE_PROMPT}</instructions\n<text_input>{text_data}</text_input>\n<generated_json>{response}</generated_json>"
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64.b64encode(image_data).decode('utf-8')
                        }
                    }
                ]
            }
        ],
        "temperature": 0,
        "top_p": 0.999,
        "top_k": 250,
    }

    response = bedrock_client.invoke_model(
        modelId=model.value,
        body=json.dumps(request_body)
    )

    response_body = json.loads(response["body"].read())

    return response_body["content"][0]["text"]


def process_product(input_json_path, output_json_path, model):
    input_json_path = Path(input_json_path)
    path_name = input_json_path.name
    item_cd = path_name.split('/')[1].split('_')[0] if '/' in path_name else path_name.split('_')[0]

    with open(input_json_path) as f:
        text_data = json.loads(f.read())

    extracted_data = generate_json_with_ocr(text_data, model)

    try:
        extracted_data_json = json.loads(extracted_data.strip())

        if 'size_info' in extracted_data_json:
            if extracted_data_json['size_info']:
                print(f"Processed item_cd: {item_cd}")
                extracted_data_json["item_cd"] = item_cd
                with open(f'{output_json_path}/{item_cd}-{model.value}.json', mode='w', encoding='utf-8') as f:
                    json.dump(extracted_data_json, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"item_cd {item_cd} failed with: {e}. Response was: {extracted_data}")

    return extracted_data_json


def process_all_products(input_directory, output_directory, model=BedrockModel.CLAUDE_3_5_HAIKU_1_0):
    for filename in Path(input_directory).rglob('*.json'):
        print(filename.name)
        process_product(filename, output_directory, model)
