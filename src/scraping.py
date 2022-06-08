from typing import Dict
import requests
from bs4 import BeautifulSoup, element
import json
import urllib.parse
from tqdm import tqdm


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

    def get_and_parse_article(self, url: str) -> str:
        """parses an article link

        Args:
            url (str): url of the article to scrape.

        Returns:
            str: article parsed from the url.
        """
        output = {}
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')

        content = soup.find("main", attrs={"id": "main-content-area"})
        if content:
            header = content.find("header", class_="article-header")
            if header:
                output["header"] = {}
                title = header.find("h1")
                output["header"]["title"] = title.text
                sub_heading = header.find("p", class_="article__subhead")
                if sub_heading:
                    output["header"]["sub_heading"] = sub_heading.text.replace(
                        "\xad", "")
                else:
                    output["header"]["sub_heading"] = ""
            else:
                raise Exception("No header found")
            figure = content.find("figure", class_="article-featured-image")
            output["figure"] = {}
            if figure:
                image = figure.find("img")
                output["figure"]["image"] = urllib.parse.urljoin(
                    url, image["src"])
                output["figure"]["alt"] = image["alt"]
                caption = figure.find("figcaption")
                output["figure"]["caption"] = caption.text

            body = content.find("div", class_="wysiwyg--all-content")
            if body:
                output["body"] = {}
                paragraphs = body.find_all("p")
                output["body"]["paragraphs"] = []
                for p in paragraphs:
                    output["body"]["paragraphs"].append(
                        p.text)
            else:
                raise Exception("No body found")
        else:
            raise Exception("No content found")

        return output

    def parse_data(self, data: element.ResultSet) -> Dict[str, str]:
        """parses raw data from the url with the given tag and attributes

        Args:
            data (element.ResultSet): data scraped from `self.url`

        Returns:
            Dict[str, str]: data parsed from the url.
        """

        parsed_data = []

        for count, result in enumerate(tqdm(data), 1):
            if count > 10:
                break

            current_data = {}
            content = result.find("div", class_="gc__content")
            if content:
                current_data["content"] = {}
                title = content.find("h3", class_="gc__title")
                current_data["content"]["title"] = {}
                current_data["content"]["title"]["text"] = title.text.replace(
                    "\xad", "")
                current_data["content"]["title"]["link"] = urllib.parse.urljoin(
                    self.url, title.find("a")["href"])
                current_data["content"]["article"] = self.get_and_parse_article(
                    current_data["content"]["title"]["link"])

                excerpt = content.find("div", class_="gc__excerpt")
                current_data["content"]["excerpt"] = excerpt.text.replace(
                    "\xad", "")

                published_date = content.find(
                    "div", class_="gc__date--published")
                current_data["content"]["published_date"] = published_date.text.replace(
                    "\xad", "")
            else:
                raise Exception("No content found")
            img = result.find("img", class_="gc__image")
            if img:
                current_data["img"] = {}
                current_data["img"]["src"] = urllib.parse.urljoin(
                    self.url, img["src"])
                current_data["img"]["alt"] = img["alt"]
            else:
                raise Exception("No image found")
            parsed_data.append(current_data)

        return parsed_data

    def save(self, save_path: str):
        """parses and saves data as json from the url with the given tag and attributes

        Args:
            save_path (str): path to save the parsed data.
        """

        data = self.parse_data(self.scrape_data())
        with open(save_path, "w") as f:
            json.dump(data, f, indent=4)
