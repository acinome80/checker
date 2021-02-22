from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from pytz import timezone
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import traceback

def restart():
    import sys
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    os.execv(sys.executable, ['python3'] + sys.argv)

load_dotenv()
# set permissions for local chromedriver to test locally
start_url = "https://myfit4less.gymmanager.com/portal/login.asp"
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

#driver = webdriver.Chrome(os.getenv("WEBDRIVER_PATH"), options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(start_url)

any_booked = False
try:
    # Login
    email_input = driver.find_element_by_id("emailaddress")
    password_input = driver.find_element_by_id("password")
    driver.implicitly_wait(5)
    email_input.send_keys(os.getenv("F4L_LOGIN"))
    password_input.send_keys(os.getenv("F4L_PASSWORD"))
    
    any_slots_available = False
    booked_appointment = False
    curr_dt = datetime.now(timezone('est'))

    if curr_dt.hour == 23 and curr_dt.minute >= 58:
        print("Waiting for 12:00AM..")
        while datetime.now(timezone('est')).hour == 23:            
            time.sleep(0.5)
        print("Reached 12:00AM!")            
    
    
    driver.implicitly_wait(5)
    password_input.send_keys(Keys.ENTER)
    driver.implicitly_wait(5)
    print("Logged In!")

    # Find your club
    # if "F4L_CLUB" in os.environ:
    #     driver.find_element_by_id("btn_club_select").click()
    #     driver.implicitly_wait(3)
    #     all_clubs = driver.find_element_by_id("modal_clubs").find_element_by_class_name("dialog-content").find_elements_by_class_name("button")
    #     for club in all_clubs:
    #         if os.getenv("F4L_CLUB") == club.text:
    #             print("Club found: ", club.text)
    #             club.click()
    #             break
    #     driver.implicitly_wait(5)

    attempts = 0
    while booked_appointment == False:
        curr_dt = datetime.now(timezone('est'))
        curr_time = datetime.strptime(str(curr_dt.hour) + ":" + str(curr_dt.minute), '%H:%M')   
        days_list = [int(x) for x in os.getenv("DAYS").split(",")]  
        for i in days_list:        
            booking_date = curr_dt.date() + timedelta(days=i)
            curr_day = booking_date.weekday() # 0-4 is weekday, 5-6 is weekend
            
            driver.find_element_by_id("btn_date_select").click()  # day selector
            driver.implicitly_wait(3)
            driver.find_element_by_id("date_" + str(booking_date)).click()
            driver.implicitly_wait(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(1)

            # Check current reservations
            already_have_reservation = False
            try:            
                driver.implicitly_wait(0.5)
                reserved_slots = driver.find_element_by_class_name("reserved-slots").find_elements_by_class_name("time-slot-box")      
                for slot in reserved_slots:                
                    if str(curr_dt.day + i) == str(slot.text).split()[4]:
                        print("Already have reservation for the day: ", booking_date)
                        already_have_reservation = True
                        break
            except:
                pass # No reserved appointments
            if already_have_reservation == True:
                continue
                            
            # check available_slots class 2nd index -> see if child elements exist
            available_slots = None
            try:
                available_slots = driver.find_elements_by_class_name("available-slots")[1].find_elements_by_class_name("time-slot-box")
            except:
                print("No more hours would be available for this day.")
                continue
            if len(available_slots) == 0:
                print("No available time slots for ", booking_date)
                continue
            else:
                any_slots_available = True
            
            # define range of wanted time periods
            start_range = 13 if curr_day >= 5 else 19 #datetime.strptime("7:00PM", '%I:%M%p')
            end_range = 18 if curr_day >= 5 else 22 #datetime.strptime("10:00PM", '%I:%M%p')       
                        
            # check the available slots.
            for slot in available_slots[::-1]:
                a_slot = datetime.strptime(str(slot.text).split()[5] + str(slot.text).split()[6], '%I:%M%p')
                
                if a_slot.hour == curr_time.hour or abs((a_slot - curr_time).total_seconds() / 60) <= 30:
                    print("Time slot: {} is too close to current time. Curr time: {}".format(a_slot.strftime("%I:%M %p"), curr_time.strftime("%I:%M %p")))
                    continue
                    
                if start_range <= a_slot.hour and end_range >= a_slot.hour:
                    slot.find_element_by_xpath('..').click()
                    driver.implicitly_wait(3)
                    driver.find_element_by_id("dialog_book_yes").click()
                    driver.implicitly_wait(5)
                    any_booked = True
                    print("Booked {} on {}".format(a_slot.strftime("%I:%M %p"),booking_date))
                    booked_appointment = True
                    break
                else:
                    print("Skipping slot: {}".format(a_slot.strftime("%I:%M %p")))
        attempts = attempts + 1
        if attempts == 100:
            restart()
        else:
            time.sleep(2)

    if any_slots_available == False:
        print("No available slots at all")
    elif booked_appointment == False:
        print("No appointment booked.")
    else:
        exit(1)

except Exception as err:
    print("Seems like we're fully booked!")
    print(traceback.format_exc())
    if any_booked == True:
        exit(1)
finally:
    driver.quit()
