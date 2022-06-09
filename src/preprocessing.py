import json
from typing import Dict, List
from copy import deepcopy


class Preprocessor:
    def __init__(self, input_file: str):
        """Preprocessor constructor

        Args:
            input_file (str): path to the input file.
        """
        self.input_file = input_file
        with open(self.input_file, "r") as f:
            self.data = json.load(f)

    def combine_text(self, data: dict) -> str:

        texts = [data["header"]["title"], data["header"]["sub_heading"]]
        texts = texts + data["body"]["paragraphs"]

        return "\n".join(texts)

    def only_english(self, text: str) -> str:
        """removes non-english characters from the text

        Args:
            text (str): text to preprocess.

        Returns:
            str: preprocessed text.
        """
        return "".join(c for c in text if ord(c) < 128)

    def preprocess(self) -> List[Dict[str, str]]:
        """preprocesses the data

        Returns:
            List[Dict[str, str]]: format: {"title": str, "text": str}
        """
        preprocessed_data = []
        for page in deepcopy(self.data):
            article = page["article"]
            article.pop("figure")
            text = self.combine_text(article)
            text = self.only_english(text)
            title = page["content"]["title"]['text']
            preprocessed_data.append({"title": title, "text": text})
        return preprocessed_data
