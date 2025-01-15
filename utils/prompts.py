JSON_GENERATE_PROMPT = """You are an expert NLP engineer specializing in feature extraction and data transformation to analyze unstructured text with high precision.
The provided text is in a json format. The field name is the image file mapped to the resulting text obtained by OCR on that image. Keep this in mind when you are reading the text. The text can be in a table format, a list, or any form in fact.
You are also given the original image for reference. The text in the image is Korean.
You have the following objectives. 
<objectives>
1. Size Feature Extraction
   - Identify measurement-related properties
   - Extract numeric values and units. Range is not permitted.
   - Map English terms to Korean equivalents
2. Model Information Extraction  
   - Find first female model's measurements
   - Extract height, weight, worn size
   - Validate data completeness
3. Confidence
   - Provide your confidence on the extraction a scale between 0 and 1
   - You are not confident if you need to guess in any way. If you are not sure of the results you must report low confidence.
   - Deductions to the score must be made. Follow the guidelines of the validation section encapsulated in <validation_rules> </validation_rules>.
   - If any one guideline is not met, your confidence must be 0. Do not forcefully adjust your output to get high confidence.
</objectives>
<processing_steps>
1. Scan text for measurement patterns
2. Validate numeric values and units
3. Map to standardized Korean terms
4. Extract and validate model data
5. Construct final JSON output
6. Calculate confidence score
</processing_steps>
Construct a JSON with the gathered information with the structure below:
<structure>
{
    "size_info": [
        {
            "size_name": "string",
            "size_values": {
                "사이즈_항목_1": "float or int",
                ...
            }
        },
        ...
    ]
    "model_info": {
        "height": "float or int",
        "weight": "float or int",
        "wearing_size": "string",
    },
    "filenames": {
        "size_info": "The filename that contains size information",
        "model_info": "The filename that contains model information",
    },
    "confidence": "float",
} 
</structure>
<rules>
You must apply these rules:
1. Return an empty JSON if you cannot find any size related features in the given text.
2. You must strictly follow the structure. Do not generate any new fields other than the subfields of "size_info".
3. If there are multiple sizes, create separate entries in the "size_info" list.
4. The subfield names of the "size_values" field must be in Korean. Translate to Korean if the original text is in English.
5. Place null if there is no model size info. 
6. Provide the completed JSON structure only and do NOT include any other text in your response.
7. If there are many models, extract details from only the first female model in the text. 
</rules>
<example_text_1>
TM N N 
PRODUCT NAME 
Dual Tone Sleeve Cardigan 
COLOR 
Blue 
SIZE (cm) * 사이즈는 측정 방법에 따라 오차가 있을 수 있습니다. 
SIZE 어깨 가슴 밑단 소매길이 소매통 
FREE 43 48 35 66 17.5 
소매단 총기장 
10 55 
COMPOSITON 
Poly 45%, Recycled poly33%, Acrylic13%, Wool 6%, Span 3% 
MODEL INFO 
Hight 170.5cm / Bust 29.5 Hight 175cm / Bust 30.5 
Waist 20 / Hips 32.7 Waist22 / Hips 34 
NOTICE 
드라이 
드라이클리닝 
사용하는 모니터 해상도에 따라 실제 색상과 다소 차이가 있을 수 있습니다. 
드라이 크리닝 ONLY 
형광 염료, 표백성분 세제 사용 금지 
다림질을 할 수 없음 / 그늘에 건조, 바닥에 뉘어서 건조 / 건조기 사용 금지
</example_text_1>
<example_output_1>
{
    "size_info": [
        {
            "size_name": "free",
            "size_values": {
                "어꺠": "43",
                "가슴": "48",
                "밑단": "35",
                "소매길이": "66",
                "소매통": "17.5",
                "소매단": "10",
                "총기장": "55"
            }
        }
    ]
    "model_info": {
        "height": "170.5",
        "weight": null,
        "wearing_size": "free",
    }
    "confidence": 0.8,
}
</example_output_1>
<example_text_2>
My s tic 
e I I e 1 N ig h I S 
am. 
OUR NEW COLLECTION 
A TAPESTRY OF SOPHISTICATION, 
SPUN IN AUTUMN S WISTFUL 
AFFECTION TRAN SPORT YOURSELF 
TO AN ERA OF TIMELESS 
EXPLORE THE 
HARMONIOUS BLEND 
OF FORMAL AND CHIC 
STYLES. 
C O  T RO C T I O 
GA 
RTWOR GALLER 
Binnying 
GALLER 
RTWOR  PRODUCT INFO PRODUCT INFO 
FABRIC POLYESTER 89% COTTON 11% 
COLOR BLACK 
DETAIL INFO SIZE (cm) 
S: Length 122 Shoulder length 49 Bust 74 
Waistline 64 Hip circumference 76 
Hem circumference 98 Sleeve length 58 
M: Length 123 Shoulder length 50 Bust 78 
Waistline 68 Hip circumference 80 
Hem circumference 102 Sleeve length 59 
사이즈는 재는 위치에 따라 1~3cm의 오차가 생길 수 있습니다. 
There may be 1~3cm difference on the measuring method / location 
WASHING TIP 
가벼운 손세탁이나 드라이클리닝을 권장해드립니다. 
MODEL SIZE 
HEIGHT 
170cm 
FITTING SIZE 
Size S"
</example_text_2>
<example_output_2>
{
    "size_info": [
        {
            "사이즈명": "S",
            "길이": "122",
            "어깨길이": "49",
            "바스트": "74",
            "허리": "64",
            "힙둘레": "76",
            "밑단둘레": "98",
            "소매길이": "58"
        },
        {
            "사이즈명": "M",
            "길이": "123",
            "어깨길이": "50",
            "바스트": "78",
            "허리라인": "68",
            "힙둘레": "80",
            "밑단둘레": "102",
            "소매길이": "59"
        }
    ]
    "model_info": {
        "height": "170",
        "weight": null,
        "wearing_size": "S",
    },
    "confidence": 0.86,
}
<validation_rules>
- Korean terms must use standard industry terminology
- Output is pure JSON with no other text or encapsulation like ```json
- There must be one size per item in size_value. 
- Size values must be a single number, and not multiple numbers or lists.
- If the table structure is not properly translated to JSON.
</validation_rules>
<ocr_text_input>
"""

VALIDATE_PROMPT = """
You have previously generated a JSON document from text that was scanned from an image.
Your job is to validate the JSON document with the original image that contained the text.
Use the original text and the original image to validate the JSON document created from the text.
The previous prompt is encapsulated in <instructions></instructions.
The original text is encapsulated in <text_input></text_input>
The JSON document is encapsulated in <generated_json></generated_json>.
Look for subtle details that might be incorrect.
1. Make sure the size fields are properly set. OCR might not properly reflect tables with empty values.
2. Make sure the size values are properly set. OCR might not properly reflect tables with empty values. 
3. Make sure the model info correctly uses the first female model's info when there are many models.
Make corrections to size_info and model_info as necessary by comparing the JSON document to the image.
If there are no changes simply return "validated" with no other text.
If there are changes, return the modified JSON document and the JSON only with no other text.
"""
