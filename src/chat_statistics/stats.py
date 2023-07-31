import json
from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
from hazm import *
from wordcloud import WordCloud

from src.Data import DATA_DIR


class ChatStatistics:
    def __init__(self, data: str):
        self.data = data
        self.stop = self.stop_words()
        self.content = self.words()
        self.content = self.content_normalize(self.content)
        self.content = self.content_tokenize(self.content)
        self.wordcloud = self.generate_wordcloud(background_color="#E5FFCC")

    def stop_words(self):
        with open(DATA_DIR / "persian.txt") as f:
            stop = f.read().split("\n")
            return stop

    def words(self):
        content = ""
        for msg in self.data["messages"]:
            if type(msg["text"]) == str:
                content += msg["text"] + " "
            elif type(msg["text"]) == list:
                for sub_msg in msg["text"]:
                    if type(sub_msg) == str:
                        content += sub_msg + " "

        return content

    def content_normalize(self, content):
        normalizer = Normalizer()
        content = normalizer.normalize(content)
        stemer = Stemmer()
        content = stemer.stem(content)
        return content

    def content_tokenize(self, content):
        content = word_tokenize(content)
        return content

    def generate_wordcloud(
        self,
        background_color="white",
        font_path=str(DATA_DIR / "NotoNaskhArabic-Regular.ttf"),
    ):
        wordcloud = WordCloud(
            width=800,
            height=800,
            max_font_size=200,
            stopwords=self.stop,
            background_color=background_color,
            font_path=font_path,
        ).generate(" ".join(self.content))
        return wordcloud
