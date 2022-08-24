from abstract_scraper import KeywordWebCrawler

class ScholarCrawler(KeywordWebCrawler):

    def __init__(self, query, **kwargs):
        self.query = query
        self.page_var = 0
        url = f"https://scholar.google.com/scholar?start={self.page_var}&q={self.query}&num=20"   
        dict_structure = {"author(s)":[], "title":[], "abstract_sample":[], "publication_link":[]}
        
        try:
            if len(kwargs) == 1:
                super().__init__(url, dict_structure, query_csv=kwargs['query_csv'])
            elif len(kwargs) == 2:
                super().__init__(url, dict_structure, query_csv=kwargs['query_csv'], author_csv=kwargs['author_csv'])
            elif len(kwargs) == 3:
                super().__init__(url, dict_structure, query_csv=kwargs['query_csv'], author_csv=kwargs['author_csv'], proxy_csv=kwargs['proxy_csv'])
            else:
                super().__init__(url, dict_structure)
        except KeyError:
            print("one or more kwargs are not named correctly, should be 'query_csv', 'author_csv' and 'proxy_csv'")
    
    def set_next_page_url(self):
        self.page_var += 20
        self.query_url = f"https://scholar.google.com/scholar?start={self.page_var}&q={self.query}&num=20"

    def post_process_results(self, output_dict):
        output_dict = super().post_process_results(output_dict)
        output_dict["journal/year"] = output_dict["author(s)"].apply(lambda x: x.split("-")[1])
        output_dict["author(s)"] = output_dict["author(s)"].apply(lambda x: x.split("-")[0])
        #output_dict["year"] = output_dict["conference/journal"].apply(lambda x: x.split(",")[1])
        output_dict.to_csv("GoogleScholar_" + "_".join(self.query.split()) + ".csv")
        return output_dict

    # solve issue of query_url being in attributes (should be as argument of this method istead)
    def loop_through_pages(self):
        
        output_dict = self.empty_dict

        # loop through slef.query_df and self.author_df

        while True:
            # switch_proxy every now and then (at time 0 included)

            self.get_response()
            if self.request_response.status_code != 200 or self.page_var > 1000:
                print(self.request_response.status_code)
                break

            results = self.get_search_results('div', 'gs_r gs_or gs_scl')
            # solve no results case

            for r in results:
                output_dict["author(s)"].append(r.find('div', class_="gs_a").get_text())
                output_dict["title"].append(r.find('h3').get_text())
                output_dict["abstract_sample"].append(r.find('div', class_="gs_rs").get_text())
                output_dict["publication_link"].append(r.find('a')["href"])
                        
            self.set_next_page_url()

        return output_dict