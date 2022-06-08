from .scraping import Scraper
from tqdm import tqdm
from .preprocessing import Preprocessor

##* 2.
##* Collect 10 most recent articles from https://www.aljazeera.com/where/mozambique/
##* Include collected articles as a JSON file in your submission repository.
scraper = Scraper("https://www.aljazeera.com/where/mozambique/",
                tag="article",
                )
scraper.save("data/aljazeera.json")

##* 3.
##* Pre-process the data. Remove anything that is not part of the article itself, e.g. comments,
##* publishing date, images, etc. Make sure the articles are in English and can be processed by
##* the sentiment analysis library.
preprocessor = Preprocessor("data/aljazeera.json")
data = preprocessor.preprocess()

print(data)
