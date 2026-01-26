import requests, base64

invoke_url = "https://ai.api.nvidia.com/v1/cv/baidu/paddleocr"

with open("rr.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

assert len(image_b64) < 180_000, \
  "To upload larger images, use the assets API (see docs)"

headers = {
  "Authorization": "Bearer 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",
  "Accept": "application/json"
}

payload = {
  "input": [
    {
      "type": "image_url",
      "url": f"data:image/png;base64,{image_b64}"
    }
  ]
}

response = requests.post(invoke_url, headers=headers, json=payload)

print(response.json())
