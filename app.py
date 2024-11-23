import gradio as gr
import requests
from PIL import Image
import os
import base64
from io import BytesIO

# Define the API URL and headers
API_URL = "https://koj7q6d5hdy4h5tm.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    "Authorization": f"Bearer {os.getenv('hf')}",
    "Accept": "application/json",
    # Note: 'Content-Type' is omitted because it will be set automatically based on the payload
}

def query(url=None, image=None):
    """
    Sends a request to the API endpoint with either a URL or an image file.

    Args:
        url (str): The URL of the image to process.
        image (PIL.Image): The uploaded image to process.

    Returns:
        dict: The JSON response from the API or an error message.
    """
    try:
        if url:
            # Prepare the payload for a URL input
            payload = {"inputs": url.strip()}
            response = requests.post(API_URL, headers=headers, json=payload)
        elif image:
            # Convert the PIL Image to bytes
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            buffered.seek(0)  # Move to the beginning of the buffer

            # Prepare the files payload for an image upload
            files = {"file": ("image.png", buffered, "image/png")}
            response = requests.post(API_URL, headers=headers, files=files)
        else:
            return {"error": "No valid input provided!"}

        # Raise an HTTPError if the response was unsuccessful
        response.raise_for_status()

        # Return the JSON response from the API
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}

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
        "Upload an image or provide an image URL to process the input and get the API response."
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
        fn=process_input,          # Function to execute
        inputs=[image_input, url_input],  # Inputs to the function
        outputs=output             # Output component to update
    )

# Launch the Gradio app
app.launch(share=True)
