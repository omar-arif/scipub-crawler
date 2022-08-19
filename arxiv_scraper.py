from abstract_scraper import KeywordWebCrawler
from pandas import to_datetime

class ArXivCrawler(KeywordWebCrawler):

    def __init__(self, query):
        self.query = query
        self.page_var = 0
        url = f"https://arxiv.org/search/?query={self.query}&searchtype=all&size=200&start={self.page_var}"
        dict_structure = {"Author(s)":[], "Title":[], "Abstract":[], "Field(s)":[], "Date":[]}
        super().__init__(url, dict_structure)
    
    def set_next_page_url(self):
        self.page_var += 200
        self.query_url = f"https://arxiv.org/search/?query={self.query}&searchtype=all&size=200&start={self.page_var}"

    def post_process_results(self, output_dict):
        output_dict = super().post_process_results(output_dict)
        output_dict["Author(s)"] = output_dict["Author(s)"].apply(lambda x: x[8:])
        output_dict["Date"] = output_dict["Date"].apply(lambda x: x.split(';')[0][10:])
        output_dict["Date"] = to_datetime(output_dict["Date"], format='%d %B, %Y')
        output_dict.to_csv("ArXiv_" + "_".join(self.query.split()) + ".csv")
        return output_dict

    # solve issue of query_url being in attributes (should be as argument of this method istead)
    def loop_through_pages(self):
        output_dict = self.empty_dict

        while True:

            self.get_response()
            if self.request_response.status_code != 200:
                print(self.request_response.status_code)
                break
            
            results = self.get_search_results('li', "arxiv-result")
            # solve no results case

            for r in results:
                output_dict["Author(s)"].append(r.find('p', class_="authors").get_text())
                output_dict["Title"].append(r.find('p', class_="title is-5 mathjax").get_text())
                output_dict["Abstract"].append(r.find('span', class_="abstract-full has-text-grey-dark mathjax").get_text())
                output_dict["Date"].append(r.find('p', class_="is-size-7").get_text())
                
                other_fields = r.find_all('span', class_="tag is-small is-grey tooltip is-tooltip-top")
                main_fields = r.find_all('span', class_="tag is-small is-link tooltip is-tooltip-top")
                fields = ""
                if len(main_fields) > 0:
                    for f in main_fields:
                        fields +=  f['data-tooltip'] + ', '
                if len(other_fields) > 0:
                    for f in other_fields:
                        fields +=  f['data-tooltip'] + ', '
                else :
                    fields = None
                    
                output_dict["Field(s)"].append(fields)
            
            self.set_next_page_url()

        return output_dict


