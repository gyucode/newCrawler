
class SearchNaver():
    def __init__(self, search):
        self.page = 1
        self.search = search
        self.url = self.makeUrl(self.search, self.page)

    def makeUrl(self, search, page):
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search}&start={page}"
        return url

    def pageUp(self):
        self.page = self.page+1
        self.url = self.makeUrl(self.search, self.page)
        