import gradio as gr
import requests

API_URL = "https://koj7q6d5hdy4h5tm.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer hf_XXXXX",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def process_file_or_image(file):
    if file is None:
        return "No file provided!"
    
    # Assuming API accepts file content as input
    with open(file.name, "rb") as f:
        file_content = f.read()
        
    # Sending the content to the API
    response = query({
        "inputs": file_content.decode("utf-8", errors="ignore"),  # Adjust as per API expectations
        "parameters": {}
    })
    
    return response

# Gradio app
with gr.Blocks() as app:
    gr.Markdown("# File/Image Upload App")
    gr.Markdown("Upload an image or file and send its content to the API.")
    
    file_input = gr.File(label="Upload an Image or File", type="file")
    output = gr.JSON(label="API Response")
    
    process_button = gr.Button("Process")
    process_button.click(process_file_or_image, inputs=file_input, outputs=output)

app.launch()
