from abstract_scraper import KeywordWebCrawler

class SemanticCrawler(KeywordWebCrawler):

    def __init__(self, query):
        self.query = query
        self.page_var = 0 #max pages == 101
        url = f"https://www.semanticscholar.org/search?q={self.query}&sort=relevance&page={self.page_var}"   
        dict_structure = {"author(s)":[], "title":[], "abstract_sample":[], "publication_link":[]}
        super().__init__(url, dict_structure)
    
    def set_next_page_url(self):
        self.page_var += 1
        self.query_url = f"https://www.semanticscholar.org/search?q={self.query}&sort=relevance&page={self.page_var}"

    def post_process_results(self, output_dict):
        output_dict = super().post_process_results(output_dict)
        # process
        output_dict.to_csv("EmanticScholar_" + "_".join(self.query.split()) + ".csv")
        return output_dict

    # solve issue of query_url being in attributes (should be as argument of this method istead)
    def loop_through_pages(self):
        
        output_dict = self.empty_dict

        while True:

            self.get_response()
            if self.request_response.status_code != 200: #or self.page_var > 101:
                print(self.request_response.status_code)
                break
            
            # get results
            #results = self.get_search_results('div', 'gs_r gs_or gs_scl')
            # solve no results case
            
            # fill up dict

            self.set_next_page_url()

        return output_dict