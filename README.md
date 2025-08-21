📈 NIKKEI Financial - 日本経済新聞 銘柄情報スクレイピングツール

このリポジトリは、日本経済新聞（https://www.nikkei.com/）に掲載されている QUICKコンセンサス対象銘柄 を対象に、以下の情報を自動収集するPythonスクリプトです。
	•	証券コード
	•	銘柄名
	•	関連リンク（日本経済新聞、QUICK Money World、SBI証券）

⸻

🔧 主な機能
	•	✔ 証券コードと銘柄名の自動抽出
	•	✔ 日本経済新聞・QUICK・SBI証券のリンクを自動生成
	•	✔ ページネーション対応（全ページを再帰的にクロール）
	•	✔ SQLiteデータベースへの保存

⸻

🚀 使い方

1. 環境構築

pip install scrapy

2. 実行方法

scrapy runspider nikkei.py -a target_date=YYYYMMDD

例:

scrapy runspider nikkei.py -a target_date=20250821

3. 出力先

データは SQLite データベース market_data.db に保存されます（ルート直下に作成）。
保存テーブル：consensus_url

⸻

🗄 データベース構造

テーブル名: consensus_url

カラム名	内容
target_date	実行日（YYYYMMDD）
code	証券コード
name	銘柄名
nikkeiurl	日本経済新聞リンク
quickurl	QUICK Money Worldリンク
sbiurl	SBI証券リンク


⸻

⚙️ 設定について
	•	DB の保存先は nikkei.py 内の DB_PATH で指定しています（デフォルトは ./market_data.db）。
	•	必要に応じて環境変数で変更できます:

DB_PATH = os.getenv("NIKKEI_DB_PATH", os.path.abspath("./market_data.db"))


	•	polite crawl 設定推奨（例: DOWNLOAD_DELAY=1.5, AUTOTHROTTLE_ENABLED=True）

⸻

⚠️ 注意事項・免責事項
	•	このスクリプトは日本経済新聞の 一般公開ページ の情報を対象としており、ログイン・API等は使用していません。
	•	サイト構造が変更された場合、スクリプトは動作しなくなる可能性があります。
	•	利用規約や robots.txt を遵守のうえ、個人学習・研究用途に限定してご利用ください。
	•	本スクリプトの使用により生じたいかなる損害についても、作者は責任を負いません。

⸻

🗓 更新履歴
	•	2025/07/17 - 日本経済新聞・QUICKのリンクを自動生成
	•	2025/07/25 - SBI証券リンクの自動生成機能を追加
	•	2025/07/31 - SQLite対応（CSV管理から移行）
	•	2025/08/21 - DB保存処理・実行方法を整理
