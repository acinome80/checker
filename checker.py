from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Best buy urls:
cc_url = "https://www.canadacomputers.com/product_info.php?cPath=710_1925_1920_1923&item_id=187885"
bb_g15_3060_url = "https://www.bestbuy.ca/en-ca/product/asus-rog-zephyrus-g15-15-6-gaming-laptop-grey-amd-ryzen-9-5900hs-1tb-ssd-16gb-ram-rtx-3060-eng/15264484"
bb_g15_3070_url = "https://www.bestbuy.ca/en-ca/product/asus-rog-zephyrus-g15-15-6-gaming-laptop-grey-amd-ryzen-9-5900hs-1tb-ssd-16gb-ram-rtx-3070-eng/15264485"
bb_g14_3060_url = "https://www.bestbuy.ca/en-ca/product/asus-rog-zephyrus-g14-14-gaming-laptop-grey-amd-ryzen-9-5900hs-1tb-ssd-16gb-ram-rtx-3060-win-10/15264488"
bb_g14_3060_white_url = "https://www.bestbuy.ca/en-ca/product/asus-rog-zephyrus-g14-14-gaming-laptop-white-amd-ryzen-9-5900hs-1tb-ssd-32gb-ram-rtx-3060-eng/15264483"

bb_links = [bb_g15_3060_url, bb_g15_3070_url, bb_g14_3060_url, bb_g14_3060_white_url]

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

try:
    driver.implicitly_wait(5)
    # BEST BUY
    something_available = False
    print("Checking BB..")
    for url in bb_links:
        driver.get(url)
        try:
            print(url)
            availability = driver.find_elements_by_class_name("unavailableContainer_302Lh")
            if len(availability) < 2:
                print(len(availability))
                print("Less than two available elements..")
                raise
            print("Unavailable at best buy..")
        except:
            print("Available at bestbuy!")
            something_available = True
            exit(1)
        print("")

    if something_available:
        exit(1)
    # # CANADA COMPUTERS
    # print("Opening CC website..")
    # driver.set_page_load_timeout(15)

    # finished = 0
    # while finished == 0:
    #     try:
    #         driver.get("https://www.canadacomputers.com")
    #         finished = 1
    #     except:
    #         print("trying again..")
    #         time.sleep(5)
    # print("Checking CC..")
    # try:
    #     print(cc_url)
    #     driver.implicitly_wait(5)
    #     availability = driver.find_element_by_class_name("border-danger")
    #     print("Unavailable at Canada Computers..")
    # except:
    #     print("Available at Canada Computers!")
    #     exit(1)

    exit(0)

except Exception as err:
    print("Outer error?")
    print(err)
finally:
    driver.quit()
