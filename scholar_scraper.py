from abstract_scraper import KeywordWebCrawler

class ScholarCrawler(KeywordWebCrawler):
    '''
        Class representing a crawler/scraper of the Google Scholar website
    '''

    def __init__(self,**kwargs):
        self.page_var = 0
        dict_structure = {"author(s)":[], "title":[], "abstract_sample":[], "publication_link":[]}
        
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
        self.page_var += 20
        self.query_url = f"https://scholar.google.com/scholar?start={self.page_var}&q={self.query}&num=20"

    def set_next_query_url(self):
        self.page_var = 0
        self.query = super().get_next_query()
        if self.query == None:
            return False
        self.query_url = f"https://scholar.google.com/scholar?start={self.page_var}&q={self.query}&num=20"
        return True

    def post_process_results(self, output_dict):
        output_dict = super().post_process_results(output_dict)
        output_dict["journal/year"] = output_dict["author(s)"].apply(lambda x: x.split("-")[1])
        output_dict["author(s)"] = output_dict["author(s)"].apply(lambda x: x.split("-")[0])
        output_dict.to_csv("GoogleScholar_data.csv", index=False)
        return output_dict

    def loop_breaking_cond(self):
        bool_ = self.request_response.status_code != 200 or self.page_var >= 1000
        return bool_

    def fill_up_dict(self, output_dict):
        try:
            results = self.get_search_results('div', 'gs_r gs_or gs_scl')
        except:
            return None

        if len(results) == 0:
            return None

        for r in results:
            output_dict["author(s)"].append(r.find('div', class_="gs_a").get_text())
            output_dict["title"].append(r.find('h3').get_text())
            output_dict["abstract_sample"].append(r.find('div', class_="gs_rs").get_text())
            output_dict["publication_link"].append(r.find('a')["href"])
        
        return output_dict

