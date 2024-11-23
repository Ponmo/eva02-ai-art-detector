import gradio as gr
import requests
from PIL import Image
import os
from io import BytesIO
import json

# Define the API URL and base headers (excluding Content-Type)
API_URL = "https://koj7q6d5hdy4h5tm.us-east-1.aws.endpoints.huggingface.cloud"
BASE_HEADERS = {
    "Authorization": f"Bearer {os.getenv('hf')}",
    "Accept": "application/json"
}

def query(url=None, image=None):
    """
    Sends a request to the API endpoint with either a URL or an image.

    Args:
        url (str): The URL of the image to process.
        image (PIL.Image): The uploaded image to process.

    Returns:
        dict: The JSON response from the API or an error message.
    """
    try:
        if url and url.strip():
            # Prepare headers and payload for URL input
            headers = BASE_HEADERS.copy()
            headers["Content-Type"] = "application/json"
            payload = {"inputs": url.strip()}
            
            # Send POST request with JSON payload
            response = requests.post(API_URL, headers=headers, json=payload)

        elif image:
            # Prepare headers for image upload
            headers = BASE_HEADERS.copy()
            headers["Content-Type"] = "image/png"  # Change if using a different format
            
            # Convert PIL Image to bytes
            buffered = BytesIO()
            image.save(buffered, format="PNG")  # Ensure format matches Content-Type
            image_bytes = buffered.getvalue()
            
            # Send POST request with raw image bytes
            response = requests.post(API_URL, headers=headers, data=image_bytes)
        
        else:
            return {"error": "No valid input provided!"}

        # Raise an exception for HTTP error codes
        response.raise_for_status()

        # Attempt to return JSON response
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Failed to decode JSON response from the API."}

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}

def process_input(image=None, url=None):
    """
    Determines whether to process a URL or an image upload.

    Args:
        image (PIL.Image): The uploaded image.
        url (str): The URL of the image.

    Returns:
        dict: The response from the API.
    """
    return query(url=url, image=image)

# Define the Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# Image Upload or URL Input App")
    gr.Markdown(
        "Upload an image or provide an image URL to process the input and get the API response. The server may have a cold start."
    )

    with gr.Row():
        # Image input component
        image_input = gr.Image(label="Upload Image", type="pil")  # PIL Image for uploaded images
        # URL input component
        url_input = gr.Textbox(label="Image URL", placeholder="Enter image URL")
    
    # Output component to display the API response
    output = gr.JSON(label="API Response")

    # Button to trigger processing
    process_button = gr.Button("Process")

    # Define the action when the button is clicked
    process_button.click(
        fn=process_input,                  # Function to execute
        inputs=[image_input, url_input],    # Inputs to the function
        outputs=output                       # Output component to update
    )

# Launch the Gradio app
app.launch(share=True)
