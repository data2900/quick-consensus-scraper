import scrapy
import sqlite3
from datetime import datetime
import os

# データベースファイルの絶対パス
DB_PATH = os.path.abspath("/market_data.db")

class NikkeiSpider(scrapy.Spider):
    name = "nikkei"
    allowed_domains = ["www.nikkei.com"]
    start_urls = ["https://www.nikkei.com/markets/company/search/consensus/"]

    def __init__(self, target_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # target_dateは scrapy runspider -a target_date=YYYYMMDD で受け取る
        if not target_date:
            raise ValueError("実行時に -a target_date=YYYYMMDD の形式で日付を指定してください")

        try:
            datetime.strptime(target_date, "%Y%m%d")
        except ValueError:
            raise ValueError("日付の形式が正しくありません。YYYYMMDD形式で指定してください")

        self.target_date = target_date

        # SQLite DB初期化
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS consensus_url (
                target_date TEXT,
                code TEXT,
                name TEXT,
                nikkeiurl TEXT,
                quickurl TEXT,
                sbiurl TEXT,
                PRIMARY KEY (target_date, code)
            )
        """)
        self.conn.commit()

    def closed(self, reason):
        # クローズ時にDB接続を閉じる
        self.conn.close()

    def parse(self, response):
        rows = response.xpath('//table//tr')
        for row in rows:
            code = row.xpath('./td[1]/a/text()').get()
            name = row.xpath('./td[2]/a/text()').get()

            if code and name:
                nikkei_url = f"https://www.nikkei.com/nkd/company/?scode={code}"
                quick_url = f"https://moneyworld.jp/stock/{code}"
                sbi_url = (
                    f"https://site3.sbisec.co.jp/ETGate/?_ControlID=WPLETsiR001Control"
                    f"&_PageID=WPLETsiR001Idtl10&_DataStoreID=DSWPLETsiR001Control"
                    f"&_ActionID=stockDetail&s_rkbn=2&s_btype=&i_stock_sec={code}&i_dom_flg=1"
                    f"&i_exchange_code=JPN&i_output_type=0&exchange_code=TKY&stock_sec_code_mul={code}"
                    f"&ref_from=1&ref_to=20"
                )

                self.cursor.execute("""
                    INSERT OR IGNORE INTO consensus_url (
                        target_date, code, name, nikkeiurl, quickurl, sbiurl
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    self.target_date, code, name, nikkei_url, quick_url, sbi_url
                ))

        self.conn.commit()

        # 「次へ」リンクがあればページ遷移
        next_page = response.xpath('//a[text()="次へ"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
