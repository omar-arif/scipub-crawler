from abc import ABC, abstractmethod
from weakref import proxy
from bs4 import BeautifulSoup
import requests
import pandas as pd
from numpy import nan
from random import randint

class KeywordWebCrawler(ABC):
    '''
        Abstract class representing a crawler/scraper of a website
    '''

    def __init__(self, query_url, dict_structure, **kwargs):
        # initialize query url (url of the first page of the search query)
        self.query_url = query_url
        self.empty_dict = dict_structure
        self.request_response = None
        self.current_proxy = None
        # add proxy attribute (of type "{'http':'ip:port}")
        try:
            self.query_df = pd.open_csv(kwargs['query_csv'])
        except:
            self.query_df = None
        
        try:
            self.author_df = pd.open_csv(kwargs['author_csv'])
        except:
            self.author_df = None

        try:
            self.proxy_df = pd.open_csv(kwargs['proxy_csv'])
        except:
            self.proxy_df = None
        # do a multi args constructor see : https://www.geeksforgeeks.org/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python/
        # add exception handling (cases of empty result list for example)
    
    @abstractmethod
    def set_next_page_url(self):
        pass

    def format_proxy(proxy):
        return {'http': proxy}

    def switch_proxy(self):
        if self.proxy_df != None:
            self.current_proxy = self.format_proxy(self.proxy_df.iloc[randint(0,self.proxy_df.shape[0])])
    
    def get_response(self):
        '''
            Get the response to a GET request for a given URL (which represents the URL of a search query in the website's search engine)
        '''
        if self.current_proxy == None:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}
            self.request_response = requests.get(self.query_url, headers=headers)
        else:
            self.request_response = requests.get(self.query_url, proxies=self.current_proxy)

    
    def get_search_results(self, tag, class_):
        '''
            A method that parses the html_code of a web page and returns the part containing the results of the search query
        '''
        soup = BeautifulSoup(self.request_response.content, "lxml")
        return soup.find_all(tag, class_=class_)

    @abstractmethod
    def post_process_results(self, output_dict):
        output_dict = pd.DataFrame(output_dict)
        output_dict = output_dict.replace('\n','', regex=True).replace('  ','', regex=True)
        output_dict.fillna(value=nan, inplace=True)
        return output_dict
    
    @abstractmethod
    def loop_through_pages(self):
        pass
    
    def scrape_website(self):
        return self.post_process_results(self.loop_through_pages())
