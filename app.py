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

def process_file(filepath):
    if not filepath:
        return {"error": "No file provided!"}

    # Assuming the API takes file content as input
    with open(filepath, "rb") as f:
        file_content = f.read()
        
    response = query({
        "inputs": file_content.decode("utf-8", errors="ignore"),  # Adjust encoding as per API expectations
        "parameters": {}
    })
    
    return response

# Gradio app
with gr.Blocks() as app:
    gr.Markdown("# File Upload App")
    gr.Markdown("Upload a file and send its content to the API.")
    
    file_input = gr.File(label="Upload a File", type="filepath")  # Use 'filepath' to pass the file path
    output = gr.JSON(label="API Response")
    
    process_button = gr.Button("Process")
    process_button.click(process_file, inputs=file_input, outputs=output)

app.launch()
