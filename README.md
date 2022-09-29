# scipub-crawler
A crawler that scrapes scientific publication from websites like Google Scholar (through the ScholarCrawler class), ArXiv (through the ArXivCrawler class) 
Semantic Scholar website version is non final

## intall required Python modules
run: pip install requirements.txt

## format of input data
In order to use this app, you need to have:
- a csv file containing the authors which publications you want to search in the column named "author" (necessary)
- a csv file containing the fields or key word you want ot add to the search in the column named "query" (not necessary)
- a csv file containing a list of proxys (not necessary) with proxies adress' written in format: 'ip:port' in the column named "proxies"
- if the proxies need authentification, another column is required named "userpass" containg the username and password of the proxy in format 'user:password'

## output data
The data is returned in a pandas Dataframe and a csv file is created based on that same Dataframe containg fields such as publication authors, date, field, abstract and/or publication url (depending on which website you choose to scrape)

## How to run the scraping script (example)

```
from arxiv_scraper import ArXivCrawler
from scholar_scraper import ScholarCrawler

s = ArXivCrawler(proxy_csv=proxy_list_csv_path, author_csv=authors_csv_path, query_csv=queries_csv_path)

p = s.scrape_website()
```