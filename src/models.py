from typing import Any, Dict
from transformers import pipeline

class SentimentAnalyser:
    def __init__(self):
        print("initialising sentiment analyser...")
        self.pipeline = pipeline(
            "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.max_len = self.pipeline.tokenizer.model_max_length // 2

    def preprocess(self, text: str) -> str:
        text = " ".join(text.split()[:self.max_len])
        return text

    def analyse(self, text: str) -> Dict[str, Any]:
        text = self.preprocess(text)
        return self.pipeline([text])


if __name__ == '__main__':
    # debug
    analyser = SentimentAnalyser()
    print(analyser.analyse("This is a very bad movie "))
