import json
import os
import time
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

        self.plot_results(os.path.join(self.data_path, "results.json"))

    def plot_results(self, json_path: str):
        with open(json_path, "r") as f:
            results = json.load(f)
        
        fig = go.Figure(layout=dict(title="Sentiment Analysis", xaxis_title="Sentiment", yaxis_title="Score"))
        scores = []
        labels = []
        for title, sentiment in results.items():
            scores.append(sentiment["score"])
            labels.append(sentiment["label"])
        fig.add_trace(go.Scatter(y=scores, x=labels,
                                        mode="markers"), )

        fig.write_image(os.path.join(self.figure_path, "results.png"))
        fig.write_html(os.path.join(self.figure_path, "results.html"))


if __name__ == "__main__":
    st = time.perf_counter()
    engine = Engine("https://www.aljazeera.com/where/mozambique/",
                    "data/", "figures/")
    engine.process()
    print("Time taken:", time.perf_counter() - st)
