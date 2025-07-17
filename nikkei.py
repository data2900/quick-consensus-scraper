import scrapy


class NikkeiSpider(scrapy.Spider):
    name = "nikkei"
    allowed_domains = ["www.nikkei.com"]
    start_urls = ["https://www.nikkei.com/markets/company/search/consensus/"]

    def parse(self, response):
        rows = response.xpath('//*[@id="CONTENTS_MARROW"]/div[2]/div/table/tbody/tr')
        for row in rows:
            code = row.xpath('./td[1]/a/text()').get()
            name = row.xpath('./td[2]/a/text()').get()

            if code and name:
                yield {
                    "証券コード": code,
                    "銘柄名": name,
                    "日本経済新聞": f"https://www.nikkei.com/nkd/company/?scode={code}",
                    "QUICK Money World": f"https://moneyworld.jp/stock/{code}"
                }

        # 次のページへ（ページネーション）
        next_page = response.xpath('//*[@id="CONTENTS_MARROW"]/div[2]/div/div[1]/div/ul/li/a[text()="次へ"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
