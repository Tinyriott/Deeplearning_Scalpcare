from playwright.sync_api import sync_playwright
import csv
import time
from bs4 import BeautifulSoup

def crawl_suncushion_list_html(playwright_page, page):

    # 린스
    # url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000400080002&fltDispCatNo=&prdSort=01&pageIdx={page}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat1000001000400080002_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EB%A6%B0%EC%8A%A4%2F%EC%BB%A8%EB%94%94%EC%85%94%EB%84%88&smallCategory=%EC%86%8C_%EB%A6%B0%EC%8A%A4%2F%EC%BB%A8%EB%94%94%EC%85%94%EB%84%88&checkBrnds=&lastChkBrnd="
    # 샴프바
    url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000400080005&fltDispCatNo=&prdSort=01&pageIdx={page}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat1000001000400080005_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EC%83%B4%ED%91%B8%EB%B0%94%2F%EB%93%9C%EB%9D%BC%EC%9D%B4%EC%83%B4%ED%91%B8&smallCategory=%EC%86%8C_%EC%83%B4%ED%91%B8%EB%B0%94%2F%EB%93%9C%EB%9D%BC%EC%9D%B4%EC%83%B4%ED%91%B8&checkBrnds=&lastChkBrnd="
    # 트리트먼트
    # url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100040007&fltDispCatNo=&prdSort=01&pageIdx={page}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100040007_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%ED%8A%B8%EB%A6%AC%ED%8A%B8%EB%A8%BC%ED%8A%B8%2F%ED%8C%A9&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd="
    # 에센스
    # url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100040013&fltDispCatNo=&prdSort=01&pageIdx={page}&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100040013_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%ED%97%A4%EC%96%B4%EC%97%90%EC%84%BC%EC%8A%A4&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd="

    playwright_page.goto(url)
    time.sleep(3)
    html = playwright_page.content()
    return html

def parse_suncushion_list(html, page):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select(".prd_info")
    data = []
    for item in items:
        brand = item.select_one(".tx_brand").get_text(strip = True)
        name = item.select_one(".tx_name").get_text(strip = True)
        link = item.select_one("a")["href"]

        data.append({
            "page" : page,
            "brand_name" : brand,
            "product_name" : name,
            "product_link" : link
        })
    return data

def write_data(data):
    with open("./data/bar_link_241021.csv", "w", encoding="utf-8") as fw:
        writer = csv.DictWriter(fw, fieldnames=["page", "brand_name", "product_name", "product_link"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    num_pages = 2
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        playwright_page = browser.new_page()
        total_data = []
        for i in range(num_pages):
            html = crawl_suncushion_list_html(playwright_page, i+1)
            data = parse_suncushion_list(html, i+1)
            total_data.extend(data)
    write_data(total_data)
    print("collected:", len(total_data))