from .scraper import Scraper


dl = Scraper("https://www.aljazeera.com/where/mozambique/",
                tag="article",
                )

print(dl.scrape_data())
