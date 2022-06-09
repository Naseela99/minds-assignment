# Web scraping and sentiment analysis

This repo is structured in four modules or components:
- ```Scraping https://www.aljazeera.com/where/mozambique/ to get 10 most recent articles from the website```
- ```Pre-processing the data```
-  ```Performing sentiement analysis```
-   ``` Visualizing the results```

## Installation
Clone the repo:

```shell
git clone https://github.com/Naseela99/minds-assignment.git
```

```shell
cd minds-assignment
```

For conda:
```shell
conda env create -n minds_env --file environment.yml
conda activate minds_env
```

For pypi:
```shell
pip install -r requirements.txt
```
(This was tested on `python 3.10.4`)




## Run
```shell
python -m src.engine
```

```
downloading data...
 71%|██████████████████████████████████████████████████████████                   | 10/14 [00:08<00:03,  1.16it/s]
initialising sentiment analyser...
analysing data...
100%|████████████████████████████████████████████████████████████████████████████████| 10/10 [00:01<00:00,  7.88it/s]
Results saved to data/results.json
Time taken: 44.502 seconds
```

## Scraping the webiste

The entire repository has used python and associated libraries. To access the given URL we use the ```requests``` package from python. And to access the data from the URL we use the  ```BeautifulSoup``` library. The data is saved in the json in the following format:

- For every article we have three components, **content**, **article** and **image**
- The content, represents the news card on the website having - ```title```, ```excerpt``` and ```date of publication```. The title holds the news headline and the link to the article.
- The link in the content is fetched to gather the article data. Every article has ```header```, ```figure``` and ```body```. The header contains the title and sub-heading. The body of the article contains the full-text, that has been saved in paragraphs. The article figure has the link to the image, it's alternate name and the caption.
- For every news card, there is an image associate with it. The **img** in the file has the image url and it's alternate text.

## Pre-processing the data
To perform the sentiment analysis, we need to pre-process the data. For pre-processing the following has been done:
- The text that we need for sentiment analysis is the article title, the article subtitle and the article paragraph. These are concatenated.
- All non-english words and letters are removed from the concatenated text.

## Sentiment Analysis

For sentiment analysis, pretrained ```distilbert``` has been used from the **transformers** library of python. Since we know that the model can take upto 512 tokens, the text is truncated to the 512 characters. The article title, it's ```sentiment score``` and ```label``` have been stored to json for the purpose of plotting and drawing conclusions.

## Results

Out of the 10 articles that we collected, 9 had a negative label and one had a positive label. The plot shows the results

![](figures/results.png)

