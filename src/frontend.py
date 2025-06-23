import streamlit as st
from api_client import predict_tumor_api

def image_upload():
    uploaded_file = st.file_uploader(
        "Choose an MRI image", 
        type=["png", "jpg", "jpeg"], 
        help="Accepted formats: .jpg, .jpeg, .png | Max size: 10MB"
    )

    if 'response_image' not in st.session_state:
        st.session_state['response_image'] = None

    if uploaded_file is not None and st.session_state['response_image'] is None:
        st.image(uploaded_file, caption="Preview of Uploaded Image", use_column_width=True)
        if st.button("Analyze Image", use_container_width=True, type="primary"):
            with st.spinner("Analyzing image for tumor presence..."):
                result = predict_tumor_api(uploaded_file)
                st.session_state['response_image'] = result
                st.rerun()
    elif st.session_state['response_image'] is not None:
        st.success("Analysis complete! See the result below.")
        st.image(st.session_state['response_image'], caption="AI-Processed MRI Result", use_column_width=True)
        if st.button("Reset", use_container_width=True):
            st.session_state['response_image'] = None
            st.rerun()
    else:
        st.info("Please upload a brain MRI image to begin analysis.")

def main():
    st.title("🧠 Brain Tumor Detection")
    st.caption("Upload a brain MRI scan (JPG/PNG) for AI-based tumor analysis.")
    st.divider()
    image_upload()

if __name__ == "__main__":
    main()
