import streamlit as st
from PIL import Image
import os
from openai import OpenAI
import base64

client = OpenAI()
st.set_page_config(layout="wide")


st.title("料理のレシピを生成するアプリ")


uploaded_image = st.file_uploader("料理の写真をアップロードしてください", type=["jpg", "jpeg", "png"])

col1, col2, col3 = st.columns([13, 20, 13])

if uploaded_image is not None:
    col1.image(uploaded_image, caption="アップロードされた画像", use_column_width=True)

    image_content = uploaded_image.read()
    image_base64 = base64.b64encode(image_content).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "この料理のレシピを教えてください．料理名，材料，調理の手順を書いてください．それ以外は何も書かないでください．だいたい300字に収まるように応えてください.材料を羅列するときは、各行に2つの要素を列挙してください.たとえば・A 改行・B 改行・C 改行・D 改行じゃなくて・A ・B 改行・C ・D 改行 みたいな感じで"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            }
        ],
        max_tokens=600,
    )

    if response.choices[0]:
        result_message = response.choices[0].message.content
        col2.subheader("生成されたレシピ:")
        # col2.write(result_message)
        col2.markdown(f'<span style="font-size:15px; color:black;">{result_message}</span>', unsafe_allow_html=True)
    else:
        col2.error("APIへのリクエストが失敗しました。")


    response_image = client.images.generate(
    model="dall-e-3",
    prompt = "以下のレシピで出来上がる料理" + result_message,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response_image.data[0].url
    col3.image(image_url)
