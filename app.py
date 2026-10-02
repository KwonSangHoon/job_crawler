from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0"
}


def crawl_incruit(keyword):
    url = f"https://search.incruit.com/list/search.asp?col=job&kw={quote(keyword)}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for item in soup.select(".c_row"):
        title = item.select_one(".cell_mid")

        if title:
            jobs.append({
                "site": "인크루트",
                "title": title.get_text(strip=True)
            })

    return jobs[:10]


def crawl_jobkorea(keyword):
    url = f"https://www.jobkorea.co.kr/Search/?stext={quote(keyword)}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # 잡코리아 검색 결과의 제목 링크를 찾음
    for item in soup.select("a"):
        title = item.get_text(" ", strip=True)

        if keyword.lower() in title.lower() and len(title) > 3:
            jobs.append({
                "site": "잡코리아",
                "title": title
            })

    return jobs[:10]


@app.route("/")
def home():
    keyword = request.args.get("keyword", "")

    jobs = []

    if keyword:
        jobs += crawl_incruit(keyword)
        jobs += crawl_jobkorea(keyword)

    return render_template(
        "index.html",
        jobs=jobs,
        keyword=keyword
    )


if __name__ == "__main__":
    app.run()
