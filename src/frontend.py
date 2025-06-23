import streamlit as st
from PIL import Image
import io
from api_client import predict_tumor_api

def image_upload():
    uploaded_file = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        analyze = st.button('Analyze', disabled=uploaded_file is None)
        if analyze:
            with st.spinner('Analyzing...'):
                result = predict_tumor_api(uploaded_file)
                st.image(result)

def main():
    st.title('Tumor Detection')
    image_upload()

if __name__ == "__main__":
    main()
