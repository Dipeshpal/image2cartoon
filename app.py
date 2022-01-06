import streamlit as st
import requests
import base64
from PIL import Image
import os
import webbrowser

st.title("Convert Your Image to Cartoon")


def app(image_path):
    with open(image_path, "rb") as img_file:
        b = base64.b64encode(img_file.read()).decode('utf-8')

    r = requests.post(url='https://hf.space/gradioiframe/akhaliq/AnimeGANv2/+/api/predict',
                      json={"data": [f"data:image/png;base64,{b}",
                                     "version 2 (\ud83d\udd3a robustness,\ud83d\udd3b stylization)"]})

    b64response = base64.b64decode(r.json()['data'][0][22:])

    with open("image.png", "wb") as f:
        f.write(b64response)

    return "image.png", b64response


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Converting...")
    image = image.save("temp.jpg")
    ans, _ = app(os.path.join("temp.jpg"))
    ans_img = Image.open(ans)
    st.image(ans_img, caption='Your Cartoon Image.', use_column_width=True)
    with open("image.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name=f"{uploaded_file.name.split('.')[0]}_cartoon.png",
            mime="image/png"
        )

    url = 'https://youtube.com/techportofficial'

    if st.button('Say Thanks!!!'):
        webbrowser.open_new_tab(url)
    