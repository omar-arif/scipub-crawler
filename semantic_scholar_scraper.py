from abstract_scraper import KeywordWebCrawler

class SemanticCrawler(KeywordWebCrawler):
    '''
        Class representing a crawler/scraper of the Semantic Scholar website
    '''

    def __init__(self, **kwargs):
        self.page_var = 1
        dict_structure = {"author(s)":[], "title":[], "abstract":[], "date":[]}
        
        try:
            if len(kwargs) == 1:
                super().__init__(dict_structure, author_csv=kwargs['author_csv'])
            elif len(kwargs) == 2:
                try:
                    super().__init__(dict_structure, author_csv=kwargs['author_csv'], query_csv=kwargs['query_csv'])
                except:
                    super().__init__(dict_structure, author_csv=kwargs['author_csv'], proxy_csv=kwargs['proxy_csv'])
            elif len(kwargs) == 3:
                super().__init__(dict_structure, author_csv=kwargs['author_csv'], query_csv=kwargs['query_csv'], proxy_csv=kwargs['proxy_csv'])
            else:
                super().__init__(dict_structure)
        except KeyError:
            print("one or more kwargs are not named correctly, should be 'query_csv', 'author_csv' and 'proxy_csv'")

    
    def set_next_page_url(self):
        self.page_var += 1
        self.query_url = f"https://www.semanticscholar.org/search?q={self.query}&sort=relevance&page={self.page_var}"

    def set_next_query_url(self):
        self.page_var = 0
        self.query = super().get_next_query()
        if self.query == None:
            return False
        self.query_url = f"https://www.semanticscholar.org/search?q={self.query}&sort=relevance&page={self.page_var}"
        return True

    def post_process_results(self, output_dict):
        output_dict = super().post_process_results(output_dict)
        # process
        output_dict.to_csv("SemanticScholar_" + "_".join(self.query.split()) + ".csv")
        return output_dict

    def loop_breaking_cond(self):
        bool_ = self.request_response.status_code != 200 or self.page_var >= 1000
        return bool_

    def fill_up_dict(self, output_dict):
        try:
            results = self.get_search_results('div', 'cl-paper-row serp-papers__paper-row paper-row-normal')
        except:
            return None

        for r in results:
            output_dict["author(s)"].append(r.find('a', class_="cl-paper-authors").get_text())
            output_dict["title"].append(r.find('h2', class_="cl-paper-title").get_text())
            output_dict["abstract"].append(r.find('div', class_="tldr-abstract-replacement text-truncator").get_text())
            output_dict["date"].append(r.find('span', class_="cl_paper_pubdates").get_text())
        
        return output_dict