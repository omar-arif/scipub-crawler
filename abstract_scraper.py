from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import pandas as pd
from numpy import nan

class KeywordWebCrawler(ABC):
    '''
        Abstract class representing a crawler/scraper of a website
    '''

    def __init__(self, query_url, dict_structure):
        # initialize query url (url of the first page of the search query)
        self.query_url = query_url
        self.empty_dict = dict_structure
        self.request_response = None
        # add proxy attribute (of type "{'http':'ip:port}")
        # add user-agent attribute (https://rayobyte.com/blog/most-common-user-agents/#:~:text=How%20to%20rotate%20user%20agents%3F%C2%A0)
        # do a multi args constructor see : https://www.geeksforgeeks.org/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python/
        # add exception handling (cases of empty result list for example)
    
    @abstractmethod
    def set_next_page_url(self):
        pass
    
    def get_response(self):
        '''
            Get the response to a GET request for a given URL (which represents the URL of a search query in the website's search engine)
        '''
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'}
        self.request_response = requests.get(self.query_url, headers=headers)
    
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
