import io

import streamlit as st
from api_client import predict_tumor_api
from PIL import Image


def image_upload():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    response_image = None
    if uploaded_file is not None:
        analyze = st.button("Analyze", disabled=uploaded_file is None)
        if analyze:
            with st.spinner("Analyzing..."):
                result = predict_tumor_api(uploaded_file)
                response_image = result
    if uploaded_file is not None and response_image is None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    if response_image is not None:
        st.image(response_image, caption="Response Image", use_column_width=True)


def main():
    st.title("Tumor Detection")
    image_upload()


if __name__ == "__main__":
    main()
