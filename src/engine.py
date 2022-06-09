import json
import os
from tqdm import tqdm
from .scraping import Scraper
from .preprocessing import Preprocessor
from .models import SentimentAnalyser


class Engine:
    def __init__(self, url: str, save_path: str):
        """_summary_

        Args:
            url (str): url of the page to scrape.
        """
        self.url = url
        self.save_path = save_path
        self.scraper = Scraper(url, tag="article")
        print("downloading data...")
        self.scraper.save(save_path)
        self.preprocessor = Preprocessor(save_path)
        self.analyser = SentimentAnalyser()

    def process(self):
        data = self.preprocessor.preprocess()
        print("analysing data...")
        results = {}
        for item in tqdm(data):
            title = item["title"]
            text = self.preprocessor.only_english(item["text"])
            sentiment = self.analyser.analyse(text)
            results[title] = sentiment

        with open(os.path.join(os.path.dirname(self.save_path), "results.json"), "w") as f:
            json.dump(results, f, indent=4)

        print("Results saved to", os.path.join(
            os.path.dirname(self.save_path), "results.json"))


if __name__ == "__main__":
    engine = Engine("https://www.aljazeera.com/where/mozambique/",
                    "data/aljazeera.json")
    engine.process()
