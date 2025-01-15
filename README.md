# Product image OCR to extract size and model information with Upstage and Amazon Bedrock 

---
## Introduction

This repository contains sample code that:
1. Splits vertically oriented images that are very long to multiple images with overlap
2. Perform OCR on split images using either Upstage OCR API directly, or using Upstage OCR deployed on Amazon SageMaker Endpoint.
3. Aggregate the processed text into a single aggregated JSON file.
4. Use the JSON file to extract product size information and model information using Amazon Bedrock.

Although modern multimodal models have the capability to extract text from images, they still struggle in extracting languages other than English which is why Upstage OCR comes in to play.

---

## How to run

1. The functions assume that your directory is set up like the sample directory. Make sure your directory follows the same structure, or modify functions so that they will work properly. 
```
sample_directory
├── item_cd=1234
    └── product images
```

2. Modify the `.env.example` file so that values reflect your environment and rename to `.env`
3. Run `test.py`
---
## How to use with Amazon SageMaker
`test.py` is configured to run with Upstage API in default. You may change this to use Upstage OCR deployed on SageMaker.

Add the endpoint name to `.env` and modify the `ocr_function` parameter of `ocr_all_images` to use `ocr_image_sagemaker`. 

This function assumes that the proper AWS credentials are configured in a profile named upstage.

Append the following to your `~/.aws/credentials` for setup.

```
[upstage]

aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

The profile must have an Upstage SageMaker endpoint deployed.

---
# ⚠️ PROOF OF CONCEPT WARNING ⚠️

This code is a Proof of Concept (PoC) implementation intended for demonstration purposes only. It:
- May contain bugs and incomplete error handling
- Is not optimized for performance
- Lacks proper security measures
- Has not undergone thorough testing

DO NOT USE THIS CODE IN PRODUCTION ENVIRONMENTS.