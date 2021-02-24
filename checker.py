from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.firefox.options import Options as FOptions
from selenium import webdriver
firefox_options = FOptions()
firefox_options.add_argument("--headless")


# Best buy urls:
bb_url = "https://www.bestbuy.ca/en-ca/product/asus-rog-zephyrus-g15-15-6-gaming-laptop-grey-amd-ryzen-9-5900hs-1tb-ssd-16gb-ram-rtx-3060-eng/15264484"
cc_url = "https://www.canadacomputers.com/product_info.php?cPath=710_1925_1920_1923&item_id=187885"
cc_url = "www.canadacomputers.com"

load_dotenv()
chrome_options = Options()

# first condition just for debugging locally
if os.getenv("ENVIRONMENT") == "dev":
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--kiosk") # use this for debugging on Linux/Mac
    # chrome_options.add_argument("--window-size=1920,1080") # use this for debugging on Windows
    chrome_options.add_argument("--window-size=3072,1920") # use this for debugging on Windows 3072 x 1920
else:
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--kiosk") # use this for debugging on Linux/Mac
    chrome_options.add_argument("--window-size=3072,1920") # use this for debugging on Windows 3072 x 1920

# driver = webdriver.Chrome(os.getenv("WEBDRIVER_PATH"), options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
with webdriver.Firefox(options=firefox_options) as driver:
    # driver.get("http://localhost:8080")
    driver.get(bb_url)


try:
    driver.implicitly_wait(5)
    # BEST BUY
    print("Checking BB..")
    try:
        print(bb_url)
        availability = driver.find_elements_by_class_name("unavailableContainer_302Lh")
        if len(availability) < 2:
            print(len(availability))
            print("Less than two available elements..")
            raise
        print("Unavailable at best buy..")
    except:
        print("Available at bestbuy!")
        exit(1)

    # # CANADA COMPUTERS
    print("Opening CC website..")
    driver.set_page_load_timeout(15)

    finished = 0
    while finished == 0:
        try:
            driver.get("https://www.canadacomputers.com")
            finished = 1
        except:
            print("trying again..")
            time.sleep(5)
    print("Checking CC..")
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
