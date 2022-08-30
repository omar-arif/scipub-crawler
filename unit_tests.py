from re import S
import pytest
from arxiv_scraper import ArXivCrawler
from scholar_scraper import ScholarCrawler
# file to run unit tests

class TestClassInstanciation:

    def test_instanciate_full(self):
        ac = ArXivCrawler()
        assert ac.author_df == None
        assert ac.query_df == None
        assert ac.proxy_df == None
        assert ac.empty_dict == {"Author(s)":[], "Title":[], "Abstract":[], "Field(s)":[], "Date":[]}
        sc = ScholarCrawler()
        assert sc.author_df == None
        assert sc.query_df == None
        assert sc.author_df == None
        assert sc.empty_dict == {"author(s)":[], "title":[], "abstract_sample":[], "publication_link":[]}

    def test_instanciate_no_proxy(self):
        pass
    def test_instanciate_no_query(self):
        pass
    def test_instanciate_empty(self):
        pass


class TestClassCommonMethods:

    def test_proxy_switch(self):
        pass
    def test_whith_proxy_response(self):
        pass
    def test_no_proxy_response(self):
        pass
    def test_get_search_results(self):
        # right args and wrong args for both classes
        # whith case empty results
        pass


class TestClassPostProccess:
    pass

class TestClassNextQuery:
    pass

class TestClassBasics:
    def test_set_next_page_url(self):
        pass
    def test_set_next_query_url(self):
        pass
    def test_loop_breaking_cond(self):
        pass

class TestClassLoopPages:
    pass