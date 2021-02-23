from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Best buy urls:
bb_url = "https://www.bestbuy.ca/en-ca/product/asus-rog-zephyrus-g15-15-6-gaming-laptop-grey-amd-ryzen-9-5900hs-1tb-ssd-16gb-ram-rtx-3060-eng/15264484"
cc_url = "https://www.canadacomputers.com/product_info.php?cPath=710_1925_1920_1923&item_id=187885"
cc_url = "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=181376"

load_dotenv()
chrome_options = Options()

# first condition just for debugging locally
if os.getenv("ENVIRONMENT") == "dev":
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--kiosk") # use this for debugging on Linux/Mac
    # chrome_options.add_argument("--window-size=1920,1080") # use this for debugging on Windows
    chrome_options.add_argument("--window-size=3072,1920") # use this for debugging on Windows 3072 x 1920
else:
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--kiosk") # use this for debugging on Linux/Mac
    chrome_options.add_argument("--window-size=3072,1920") # use this for debugging on Windows 3072 x 1920

driver = webdriver.Chrome(os.getenv("WEBDRIVER_PATH"), options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.set_page_load_timeout(10)
t = time.time()
try:
    driver.get(cc_url)
except TimeoutException:
    driver.execute_script("window.stop();")
print("Time consuming:", time.time() - t)


try:
    driver.implicitly_wait(5)
    # BEST BUY
    # print("Checking BB..")
    # try:
    #     print(bb_url)
    #     availability = driver.find_elements_by_class_name("unavailableContainer_302Lh")
    #     if len(availability) < 2:
    #         print(len(availability))
    #         print("Less than two available elements..")
    #         raise
    #     print("Unavailable at best buy..")
    # except:
    #     print("Available at bestbuy!")
    #     exit(1)

    # # CANADA COMPUTERS
    print("Opening CC website..")
    # driver.get(cc_url)
    print("Checking CC..")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 4);")
    try:
        print(cc_url)
        driver.implicitly_wait(5)
        availability = driver.find_element_by_class_name("border-danger")
        print("Unavailable at Canada Computers..")
    except:
        print("Available at Canada Computers!")
        exit(1)

    exit(0)

except Exception as err:
    print("Outer error?")
    print(err)
finally:
    driver.quit()
