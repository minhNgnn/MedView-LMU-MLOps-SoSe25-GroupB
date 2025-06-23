import io

import streamlit as st
from PIL import Image


def image_upload():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # TODO: Add function to predict the image & display the image with the prediction only


def main():
    st.title("Hello, world!")
    image_upload()


if __name__ == "__main__":
    main()
