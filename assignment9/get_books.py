import json
import traceback
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def print_exception_info(e):
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


def parse_site(link):
    driver = setup_driver()
    results = []
    base_link = link

    try:
        while True:
            print(f"Parsing {link}")
            driver.get(link)
            results = results + parse_books(driver)

            if is_last_page(driver):
                break

            current_page_element = get_current_page_element(driver)
            if not current_page_element:
                break

            link = get_next_page_link(base_link, current_page_element)

            sleep(2)

    except Exception as e:
        print("Couldn't get the web page")
        print_exception_info(e)
    finally:
        driver.quit()

    return results


def get_next_page_link(base_link, current_page_element):
    next_page = int(current_page_element.text) + 1
    full_link = base_link + f"&page={next_page}"
    return full_link


def get_current_page_element(driver):
    current_page_element = driver.find_element(
        By.CSS_SELECTOR,
        "li.cp-pagination-item.pagination__page-number.pagination-item--current span.pagination__page-number--desktop"
    )
    return current_page_element


def is_last_page(driver):
    is_last_page = bool(driver.find_elements(
        By.CSS_SELECTOR,
        "li.cp-pagination-item.pagination__next-chevron.pagination-item--disabled"
    ))
    return is_last_page


def parse_books(driver):
    results = []

    try:
        li_elements = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
        if li_elements:
            for li_element in li_elements:
                title = get_title(li_element)
                authors = get_authors(li_element)
                format_year = get_format_year(li_element)

                results.append({
                    "Title": title,
                    "Author": authors,
                    "Format-Year": format_year
                })
    except Exception as e:
        print("Couldn't get the web page")
        print_exception_info(e)

    return results


def get_format_year(li_element):
    format_year = li_element.find_element(By.CSS_SELECTOR, "span.display-info-primary").text

    return format_year if format_year else "No Format-Year"


def get_authors(li_element):
    author_info_list = li_element.find_elements(By.CSS_SELECTOR, "a.author-link")
    if len(author_info_list) > 0:
        authors_list = []
        for author in author_info_list:
            authors_list.append(author.text)
        return ";".join(authors_list)
    else:
        return "No author"


def get_additional_title(li_element):
    additional_title = ""
    additional_titles = li_element.find_elements(By.CSS_SELECTOR, "span.cp-subtitle")
    if len(additional_titles) > 0:
        additional_titles_list = []
        for additional_title in additional_titles:
            additional_titles_list.append(additional_title.text)
        additional_title = ";".join(additional_titles_list)

    return additional_title


def get_title(li_element):
    title = li_element.find_element(By.CSS_SELECTOR, "span.title-content").text
    additional_title = get_additional_title(li_element)

    if title:
        return f"{title}: {additional_title}" if additional_title else title

    return additional_title if additional_title else "Not title"


def save_data_to_json(data):
    with open('get_books.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Task 3: Write a Program to Extract this Data
results = parse_site("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")
result_df = pd.DataFrame(results)
print(result_df)

# Task 4: Write out the Data
result_df.to_csv("get_books.csv", sep="|")
save_data_to_json(results)
