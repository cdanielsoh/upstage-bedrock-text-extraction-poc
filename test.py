from dotenv import load_dotenv
import os

import utils.image_processing as image
import utils.bedrock as bedrock
import utils.text_processing as tp
from utils.upstage import ocr_all_images, ocr_image_sagemaker, ocr_image_upstage
from utils.bedrock_models import BedrockModel

load_dotenv()

SOURCE_DIRECTORY=os.getenv('SOURCE_DIRECTORY')
IMAGE_PROCESS_DIRECTORY=os.getenv('IMAGE_PROCESS_DIRECTORY')
DATA_DIRECTORY="results"


def run():

    image.process_images_in_directory(SOURCE_DIRECTORY, IMAGE_PROCESS_DIRECTORY, crop_height=5000, overlap=100)

    ocr_all_images(IMAGE_PROCESS_DIRECTORY, ocr_image_upstage)

    tp.aggregate_text_per_image(IMAGE_PROCESS_DIRECTORY)
    tp.aggregate_json_files(IMAGE_PROCESS_DIRECTORY, DATA_DIRECTORY)

    bedrock.process_all_products(DATA_DIRECTORY, DATA_DIRECTORY, BedrockModel.CLAUDE_3_5_HAIKU_1_0)


if __name__ == '__main__':
    run()