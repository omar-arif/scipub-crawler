from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import pandas as pd
from numpy import nan
from random import randint

class KeywordWebCrawler(ABC):
    '''
        Abstract class representing a crawler/scraper of a website
    '''

    def __init__(self, dict_structure, **kwargs):
        self.empty_dict = dict_structure
        self.query_index = 0
        self.author_index = 0
        self.query_url = None
        self.request_response = None
        self.current_proxy = None
        try:
            self.query_df = pd.read_csv(kwargs['query_csv'])
        except:
            self.query_df = pd.DataFrame()
        
        try:
            self.author_df = pd.read_csv(kwargs['author_csv'])
        except:
            self.author_df = pd.DataFrame()

        try:
            self.proxy_df = pd.read_csv(kwargs['proxy_csv'])
        except:
            self.proxy_df = pd.DataFrame()
    

    @abstractmethod
    def set_next_page_url(self):
        pass


    @abstractmethod
    def set_next_query_url(self):
        pass


    def switch_proxy(self):
        if self.proxy_df.empty == False:
            r = randint(0,self.proxy_df.shape[0]-1)
            self.current_proxy = {'http' : self.proxy_df['proxies'].iloc[r]}

    
    def get_response(self):
        '''
            Get the response to a GET request for a given URL (which represents the URL of a search query in the website's search engine)
        '''

        if self.current_proxy == None:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'}
            self.request_response = requests.get(self.query_url, headers=headers)
        else:
            self.request_response = requests.get(self.query_url, proxies=self.current_proxy)

    
    def get_next_query(self):
        # return True if success or not done else False
        # if no authors 
        if self.author_df.empty:
            # maybe handle this case by error : should have author df
            return None
        
        # if authors but no fields (query)
        elif self.query_df.empty:
            # if not done looping through authors
            if self.author_index != self.author_df.shape[0]:
                # handle key error
                q = self.author_df['author'].iloc[self.author_index]
                self.author_index += 1
                self.switch_proxy()
                return q

            # if done looping through queries
            return None

        # if authors and queries availabale
        else:
            # if not done looping through queries
            if self.query_index != self.query_df.shape[0] and self.author_index != self.author_df.shape[0]:
                q = self.author_df['author'].iloc[self.author_index] + " " + self.query_df['query'].iloc[self.query_index]
                self.query_index += 1
                self.switch_proxy()
                return q

            # if done looping through queries
            else:
                self.query_index = 0
                # if not done looping through authors
                if self.author_index != self.author_df.shape[0]:
                    q = self.author_df['author'].iloc[self.author_index] + " " + self.query_df['query'].iloc[self.query_index]
                    self.author_index += 1
                    self.switch_proxy()

                    return q
                # if done looping through authors
                return None
            

    
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
    def fill_up_dict(self, output_dict):
        pass

    @abstractmethod
    def loop_breaking_cond(self):
        pass
    
    # solve issue of query_url being in attributes (should be as argument of this method istead)
    def loop_through_pages(self):

        output_dict = self.empty_dict
        self.switch_proxy()

        # loop through slef.query_df and self.author_df
        while self.set_next_query_url():
            print("hey")
            while True:
                # switch_proxy every now and then (at time 0 included)
                # try to get_response and switch proxy if error or code 403 or every k steps or after every author search?

                self.get_response()
                if self.request_response.status_code == 403 or self.request_response.status_code == 429:
                    # maybe remove proxy if error or code 403
                    self.switch_proxy()
                    self.get_response()
                    if self.request_response.status_code == 403 or self.request_response.status_code == 429:
                        raise Exception('Proxy list is not good enough / Too many requests / Banned by the website')
                elif self.loop_breaking_cond():
                    print(self.request_response.status_code)
                    break
                
                out = self.fill_up_dict(output_dict)
                if out == None:
                    break
                else:
                    output_dict = out
                self.set_next_page_url()

        return output_dict
        

    
    def scrape_website(self):
        return self.post_process_results(self.loop_through_pages())
