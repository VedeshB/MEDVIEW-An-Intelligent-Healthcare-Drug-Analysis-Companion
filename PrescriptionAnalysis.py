import base64
import requests

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Encode your local image
def prescriptionanalysis(path):
    image_path = path
    base64_image = encode_image(image_path)

    # Groq API endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Your Groq API key
    api_key = "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"
    prompt="""Extract the medicine names from this prescription and give the details about for what purpose they are used for all the medicines in a list format.
                format 
                Ensure that the text should not contain any symbols like'*'
                the sentence break should be with full stop
                each medicine name also should contain break with fullstop"""

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Data payload for the request
    data = {
        "model": "llama-3.2-90b-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "temperature": 0,
        "max_completion_tokens": 150,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    # Send the request
    response = requests.post(url, headers=headers, json=data)

    # Parse the response
    if response.status_code == 200:
        result = response.json()
        extracted_text = result['choices'][0]['message']['content']
        print(extracted_text)
        temp_str=''
        per_list=[]
        for i in extracted_text:
            if i=='.'  or i.isdigit()==True:
                if temp_str:
                    per_list.append(temp_str)
                    temp_str=''
                else:
                    continue
            else:
                temp_str+=i
        print("Extracted Medicine Names:", per_list)
    else:
        print("Error:", response.status_code, response.text)
    return per_list