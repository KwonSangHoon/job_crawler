from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0"
}


# 인크루트 크롤링
def crawl_incruit(keyword):
    url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}"

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

    return jobs


# 잡코리아 크롤링
def crawl_jobkorea(keyword):
    url = f"https://www.jobkorea.co.kr/Search/?stext={keyword}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for item in soup.select(".list-post"):
        title = item.select_one(".post-list-info .title")

        if title:
            jobs.append({
                "site": "잡코리아",
                "title": title.get_text(strip=True)
            })

    return jobs


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
