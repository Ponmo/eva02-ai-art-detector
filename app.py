import gradio as gr
import requests
from PIL import Image

API_URL = "https://koj7q6d5hdy4h5tm.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + str(os.getenv('hf')),
    "Content-Type": "application/json"
}

def query(payload):
    print(payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def process_input(input):
    if isinstance(input, str) and input.startswith("http"):
        # Input is a URL
        payload = {"inputs": [input]}
    elif isinstance(input, Image.Image):
        # Input is a PIL Image
        payload = {"inputs": input}  # Assuming the API can handle raw image objects
    else:
        return {"error": "Invalid input type. Provide a valid URL or image."}
    
    response = query(payload)
    return response

# Gradio app
with gr.Blocks() as app:
    gr.Markdown("# Image Upload App")
    gr.Markdown(
        "Upload an image file or provide an image URL. The app will process the input and call the API."
    )

    with gr.Row():
        image_input = gr.Image(label="Upload Image", type="pil")  # PIL Image for uploaded images
        url_input = gr.Textbox(label="Image URL", placeholder="Enter image URL")
    
    output = gr.JSON(label="API Response")

    process_button = gr.Button("Process")

    def handle_input(image, url):
        if url.strip():  # If URL is provided
            return process_input(url.strip())
        elif image:  # If image is uploaded
            return process_input(image)
        else:
            return {"error": "No valid input provided!"}

    process_button.click(handle_input, inputs=[image_input, url_input], outputs=output)

app.launch()
