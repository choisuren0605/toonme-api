import requests
import streamlit as st
from PIL import Image
from io import BytesIO
import time

# Step 1: Create a Streamlit app
st.title("ToonMe Image Processing")

# Step 2: Upload the image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Process the uploaded image when the user clicks a button
    if st.button("Process Image"):
        # Step 3: Upload the image to ToonMe API
        upload_url = "https://toonme-api.p.rapidapi.com/upload/"
        upload_files = {
            "file1": ("image1.png", uploaded_file, 'image/png')
        }
        upload_headers = {
            "X-RapidAPI-Key": "0de60f51b8mshc2fefc0e4ab7c49p105831jsnf0fc410f564b",
            "X-RapidAPI-Host": "toonme-api.p.rapidapi.com"
        }

        upload_response = requests.post(upload_url, files=upload_files, headers=upload_headers)
        upload_data = upload_response.json()

        if upload_response.status_code == 200:
            image_url = upload_data.get('result')
            if image_url:
                st.success(f"Image uploaded successfully. Processing...")

                # Step 4: Process the uploaded image
                process_url = "https://toonme-api.p.rapidapi.com/toonme/v1/"
                process_payload = {
                    "id": "6352",
                    "image_url": image_url
                }
                process_headers = {
                    "content-type": "application/x-www-form-urlencoded",
                    "X-RapidAPI-Key": "0de60f51b8mshc2fefc0e4ab7c49p105831jsnf0fc410f564b",
                    "X-RapidAPI-Host": "toonme-api.p.rapidapi.com"
                }

                process_response = requests.post(process_url, data=process_payload, headers=process_headers)
                process_data = process_response.json()

                if process_response.status_code == 200:
                    request_id = process_data['image_process_response']['request_id']

                    # Step 5: Retrieve the processed image
                    result_url = "https://toonme-api.p.rapidapi.com/toonme/v1/result/"

                    while True:
                        result_payload = {
                            "request_id": request_id
                        }
                        result_response = requests.post(result_url, data=result_payload, headers=process_headers)
                        result_data = result_response.json()

                        if result_response.status_code == 200:
                            status = result_data['image_process_response']['status']

                            if status == 'OK':
                                result_image_url = result_data['image_process_response']['result_url']

                                result_response = requests.get(result_image_url)

                                # Check if the request was successful
                                if result_response.status_code == 200:
                                    # Read the image from the response content
                                    image_data = BytesIO(result_response.content)

                                    # Open the image using PIL (Pillow)
                                    img = Image.open(image_data)

                                    # Display the processed image
                                    st.image(img, caption="Processed Image", use_column_width=True)
                                    break
                            elif status == 'InProgress':
                                st.warning("Image processing is still in progress. Please wait...")
                                time.sleep(10)  # Wait for 10 seconds before checking again
                            else:
                                st.error(f"Image processing failed with status: {status}")
                                break
                        else:
                            st.error("Error: Unable to retrieve the processed image.")
                            break
                else:
                    st.error("Error during image processing.")
            else:
                st.error("Error: No image URL in the response.")
        else:
            st.error("Error during image upload.")
