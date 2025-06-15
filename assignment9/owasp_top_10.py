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

    try:
        driver.get(link)

        a_elements = driver.find_elements(By.XPATH, "//section[@class='page-body']/ul/li/a")
        if a_elements:
            for a_element in a_elements:
                title = a_element.text
                href = a_element.get_attribute('href')

                results.append({
                    "Title": title if title else "Not title",
                    "Href": href if href else "Not href",
                })
    except Exception as e:
        print("Couldn't get the web page")
        print_exception_info(e)
    finally:
        driver.quit()

    return results

# Task 6: Scraping Structured Data
results = parse_site("https://owasp.org/www-project-top-ten")
result_df = pd.DataFrame(results)
print(result_df)
result_df.to_csv("owasp_top_10.csv")
