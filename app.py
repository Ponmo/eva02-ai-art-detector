import gradio as gr
import requests
from PIL import Image
import os


API_URL = "https://koj7q6d5hdy4h5tm.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + str(os.getenv('hf')),
    "Content-Type": "application/json"
}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def process_input(image=None, url=None):
    if url and url.strip():  # Input is a URL
        payload = {"inputs": [url.strip()]}
    elif image:  # Input is an uploaded image
        # Convert PIL Image to Base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        payload = {"inputs": [img_str]}  # Sending Base64-encoded image
    else:
        return {"error": "No valid input provided!"}

    # Call the API
    try:
        response = query(payload)
        return response
    except Exception as e:
        return {"error": str(e)}

# Gradio app
with gr.Blocks() as app:
    gr.Markdown("# Image Upload or URL Input App")
    gr.Markdown(
        "Upload an image or provide an image URL to process the input and get the API response."
    )

    with gr.Row():
        image_input = gr.Image(label="Upload Image", type="pil")  # PIL Image for uploaded images
        url_input = gr.Textbox(label="Image URL", placeholder="Enter image URL")
    
    output = gr.JSON(label="API Response")

    process_button = gr.Button("Process")

    process_button.click(process_input, inputs=[image_input, url_input], outputs=output)

app.launch(share=True)
