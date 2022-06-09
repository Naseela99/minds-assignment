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
 71%|████████████████████████████████████████████████████████████               | 10/14 [00:07<00:02,  1.39it/s]
initialising sentiment analyser...
analysing data...
100%|████████████████████████████████████████████████████████████████████████████████| 10/10 [00:01<00:00,  7.05it/s]
Results saved to data/results.json
Time taken: 31.648754320995067
```

## Scraping the webiste

The entire repository has used python and associated libraries. To access the given URL and to get the contents of the URL

## Results
![](figures/results.png)

