import io
import json
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

from src.chat_statistics.stats import ChatStatistics
from collections import Counter

st.title("Chat Statistics")
st.write("This is a dashboard to visualize your chat statistics.")

# Create a file uploader
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

# If a file is uploaded, create a ChatStatistics object and generate a wordcloud
if uploaded_file is not None:
    data = json.loads(uploaded_file.getvalue().decode())
    chat_statistics = ChatStatistics(data)
    # Create a new figure and display the wordcloud
    fig, ax = plt.subplots()
    ax.imshow(chat_statistics.wordcloud, interpolation="bilinear")
    ax.axis("off")

    # Display the figure in streamlit
    st.pyplot(fig)

    # write 100 most common words that are not stop words
    if st.checkbox("Show words in wordcloud"):
        st.write("Words in wordcloud:")
        st.write(list(filter(lambda x: x[0] not in chat_statistics.stop, Counter(
            chat_statistics.content).most_common(300))))[:100]

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
    # Show Users with their number of replies
    for user, value in chat_statistics.users_with_reply().items():
        st.write(f"{user}: {len(value)}")

else:
    st.write("Please upload a JSON file.")
