import base64
import streamlit as st
import openai
import os

# Retrieve OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Streamlit page configuration
st.set_page_config(
    page_title="DALL·E 2 Image Generator",
    page_icon="🎨",
    layout="wide",
)

# Custom CSS styles for the download button
st.markdown(
    """
    <style>
    .download-button {
        background-color: #221e5b;
        color: #ffffff;
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        font-weight: bold;
    }

    .download-button:hover {
        background-color: #ff5588;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title("DALL·E 2 Image🖼️ Generator")

# Initialize session state
if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = []

# Prompt input with character limit
prompt = st.text_area("Enter the prompt:👇 (max 200 characters)", max_chars=200, height=5)

# Image size selection
size_options = ["256x256", "512x512", "1024x1024"]
selected_size = st.selectbox("Select image size:", size_options)

# Number of images to generate
num_images = st.slider("Number of images to generate:", 1, 5, 1)

# Button to generate the image
if st.button("See Magic🪄"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating images..."):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=num_images,
                    size=selected_size,
                    response_format="b64_json",
                )

                # Check if response contains image data
                if response["data"]:
                    for image_info in response["data"]:
                        image_data = base64.b64decode(image_info["b64_json"])
                        st.session_state["generated_images"].append(image_data)

                    # Display images
                    for image_data in st.session_state["generated_images"]:
                        st.image(image_data, use_column_width=True)

                        # Create download button
                        b64_image = base64.b64encode(image_data).decode()
                        href = f'<a class="download-button" href="data:image/png;base64,{b64_image}" download="generated_image.png">Download</a>'
                        st.markdown(href, unsafe_allow_html=True)
                else:
                    st.warning("No images generated.")
            except openai.error.AuthenticationError:
                st.error("Authentication error: Please check your OpenAI API key.")
            except openai.error.OpenAIError as e:
                st.error(f"An error occurred: {e}")

# Clear generated images
if st.button("Clear Images"):
    st.session_state["generated_images"] = []
    st.success("Images cleared.")
