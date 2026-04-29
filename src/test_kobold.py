import requests
import sseclient
import json

url = "http://localhost:5001/api/extra/generate/stream"
payload = {
    "prompt": "Write a short story about a kobold:",
    "max_context_length": 4096,
    "max_length": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "rep_pen": 1.1
}

response = requests.post(url, json=payload, stream=True)
client = sseclient.SSEClient(response)
for event in client.events():
    if event.event == "message":
        data = json.loads(event.data)
        if 'token' in data:
            print(data['token'], end='', flush=True)