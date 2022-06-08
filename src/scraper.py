from typing import Dict
import requests
from bs4 import BeautifulSoup, element
import json

class Scraper:
    def __init__(self, url: str, tag: str = "div", attrs: Dict[str, str] = {}):
        """DataLoader constructor

        Args:
            url (str): url of the page to scrape.
            tag (str, optional): tags to scrape. Defaults to "div".
            attrs (Dict[str, str], optional): attributes to scrape. Defaults to {}.
        """
        self.url = url
        self.tag = tag
        self.attrs = attrs

    def scrape_data(self) -> element.ResultSet:
        """scrapes raw data from the url with the given tag and attributes

        Returns:
            element.ResultSet: data scraped from the url
        """

        page = requests.get(self.url)

        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find_all(self.tag, attrs=self.attrs)

        return results

    def parse_data(self, data: element.ResultSet) -> Dict[str, str]:
        """parses raw data from the url with the given tag and attributes

        Args:
            data (element.ResultSet): data scraped from `self.url`

        Returns:
            Dict[str, str]: data parsed from the url.
        """
        
        parsed_data = []

        for result in data:
            current_data = {}
            content = result.find("div", class_="gc__content")
            if content:
                current_data["content"] = {}
                title = content.find("h3", class_="gc__title")
                current_data["content"]["title"] = {}
                current_data["content"]["title"]["text"] = title.text.replace("\xad", "")
                current_data["content"]["title"]["href"] = title.find("a")["href"]

                excerpt = content.find("div", class_="gc__excerpt")
                current_data["content"]["excerpt"] = excerpt.text.replace("\xad", "")

                published_date = content.find("div", class_="gc__date--published")
                current_data["content"]["published_date"] = published_date.text.replace("\xad", "")
            else:
                raise Exception("No content found")
            img = result.find("img", class_="gc__image")
            if img:
                current_data["img"] = {}
                current_data["img"]["src"] = img["src"]
                current_data["img"]["alt"] = img["alt"]
            else:
                raise Exception("No image found")
            parsed_data.append(current_data)

        return parsed_data

    def parse_and_save(self, save_path: str):
        """parses and saves data as json from the url with the given tag and attributes

        Args:
            save_path (str): path to save the parsed data.
        """

        data = self.parse_data(self.scrape_data())
        with open(save_path, "w") as f:
            json.dump(data, f)

