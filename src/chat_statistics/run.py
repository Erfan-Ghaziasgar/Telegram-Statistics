import io
import json
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

from chat_statistics.stats import ChatStatistics

st.title("Chat Statistics")
st.write("This is a dashboard to visualize your chat statistics.")

uploaded_file = st.file_uploader("Choose a JSON file", type="json")


if uploaded_file is not None:
    data = json.loads(uploaded_file.getvalue().decode())
    chat_statistics = ChatStatistics(data)
    # Create a new figure and display the wordcloud
    fig, ax = plt.subplots()
    ax.imshow(chat_statistics.wordcloud, interpolation="bilinear")
    ax.axis("off")

    # Display the figure in streamlit
    st.pyplot(fig)

    # Save wordcloud to file (with appropriate extension)
    wordcloud_image_path = Path.cwd() / f"{Path(uploaded_file.name).stem}.png"
    chat_statistics.wordcloud.to_file(wordcloud_image_path)

    # Create a download button of the image file
    img_byte_arr = io.BytesIO()
    Image.open(wordcloud_image_path).save(img_byte_arr, format="PNG")
    st.download_button(
        label=":red[Download wordcloud image]",
        data=img_byte_arr.getvalue(),
        file_name=f"{Path(uploaded_file.name).stem}_wordcloud.png",
        mime="image/png",
    )
else:
    st.write("Please upload a JSON file.")
