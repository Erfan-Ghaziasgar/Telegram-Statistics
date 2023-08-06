from hazm import *
from wordcloud import WordCloud

from src.Data import DATA_DIR

from pathlib import Path


class ChatStatistics:
    '''
    This class is used to generate statistics from a chat. It takes a JSON object as input. The JSON object should be in the format of the JSON file exported from Telegram. The JSON object should have the following structure:
    {
        "messages": [
            {
                "id": 1,
                "type": "message",
                "date": "2020-01-01T00:00:00",
                "from": "John Doe",
                "from_id": 123456789,
                "text": "Hello World!"
            }
            ]
    }
    '''
    def __init__(self, data: str):
        '''
        :param data: JSON object in the format of the JSON file exported from Telegram.
        :return: None
        '''
        self.data = data
        self.stop = self.stop_words()
        self.content = self.words()
        self.content = self.content_normalize(self.content)
        self.content = self.content_tokenize(self.content)
        self.wordcloud = self.generate_wordcloud(background_color="#E5FFCC")

    def stop_words(self):
        '''
        :return: A set of stop words.
        '''
        with open(DATA_DIR / "persian.txt") as f:
            stop = f.read().split("\n")
            return set(stop)

    def words(self):
        '''
        :return: A string of all the words in the chat.
        '''
        content = []
        for msg in self.data["messages"]:
            if isinstance(msg["text"], str):
                content.extend(msg["text"].split())
            elif isinstance(msg["text"], list):
                for sub_msg in msg["text"]:
                    if isinstance(sub_msg, str):
                        content.extend(sub_msg.split())
                    elif isinstance(sub_msg, dict):
                        if "text" in sub_msg:
                            content.extend(sub_msg["text"].split())

        return " ".join(content)


    def content_normalize(self, content):
        '''
        :param content: A string of all the words in the chat.
        :return: A string of all the words in the chat after normalization.
        '''
        normalizer = Normalizer()
        content = normalizer.normalize(content)
        stemer = Stemmer()
        content = stemer.stem(content)
        return content

    def content_tokenize(self, content):
        '''
        :param content: A string of all the words in the chat after normalization.
        :return: A list of all the words in the chat after normalization and tokenization.
        '''
        content = word_tokenize(content)
        return content

    def generate_wordcloud(
        self,
        background_color="white",
        # font_path=str(Path(DATA_DIR / "NotoNaskhArabic-Regular.ttf")),
        font_path="~/usr/share/fonts/truetype/Times_New_Roman.ttf",
    ):
        '''
        :param background_color: The background color of the wordcloud.
        :param font_path: The path to the font file.
        :return: A wordcloud object.
        '''
        wordcloud = WordCloud(
            width=800,
            height=800,
            max_font_size=200,
            stopwords=self.stop,
            background_color=background_color,
            font_path=font_path,
        ).generate(" ".join(self.content))
        return wordcloud

