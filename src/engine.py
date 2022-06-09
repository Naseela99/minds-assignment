import json
import os
from tqdm import tqdm
from .scraping import Scraper
from .preprocessing import Preprocessor
from .models import SentimentAnalyser
from plotly import graph_objects as go


class Engine:
    def __init__(self, url: str, data_path: str, figure_path: str):
        """Constructor for the Engine class

        Args:
            url (str): url of the page to scrape.
            data_path (str): path to the data folder
            figure_path (str): path to the figure folder
        """
        self.url = url
        self.data_path = data_path
        self.figure_path = figure_path
        self.scraper = Scraper(url, tag="article")
        print("downloading data...")
        self.scraper.save(os.path.join(data_path, "data.json"))
        self.preprocessor = Preprocessor(os.path.join(data_path, "data.json"))
        self.analyser = SentimentAnalyser()

    def process(self):
        """Saving the preprocessed data to a json file and plotting the results"""

        data = self.preprocessor.preprocess()
        print("analysing data...")
        results = {}
        for item in tqdm(data):
            title = item["title"]
            text = self.preprocessor.only_english(item["text"])
            sentiment = self.analyser.analyse(text)
            results[title] = sentiment

        with open(os.path.join(os.path.dirname(self.data_path), "results.json"), "w") as f:
            json.dump(results, f, indent=4)

        print("Results saved to", os.path.join(self.data_path, "results.json"))




if __name__ == "__main__":
    engine = Engine("https://www.aljazeera.com/where/mozambique/",
                    "data/", "figures/")
    engine.process()
