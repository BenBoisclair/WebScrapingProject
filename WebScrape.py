# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Beautiful Soup Imports
from bs4 import BeautifulSoup

# Other Imports
import time, json
import matplotlib.pyplot as plt
import pandas as pd

# Scroll Function
def _count_needed_scrolls(browser, infinite_scroll, numOfPost):
    if infinite_scroll:
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
        )
    else:
        # roughly 8 post per scroll kindaOf
        lenOfPage = int(numOfPost / 8)
    print("Number Of Scrolls Needed " + str(lenOfPage))
    return lenOfPage

def _scroll(browser, infinite_scroll, lenOfPage):
    lastCount = -1
    match = False

    while not match:
        if infinite_scroll:
            lastCount = lenOfPage
        else:
            lastCount += 1

        # wait for the browser to load, this time can be changed slightly ~3 seconds with no difference, but 5 seems
        # to be stable enough
        time.sleep(5)

        if infinite_scroll:
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")

        if lastCount == lenOfPage:
            match = True

# Get Login Credentials from txt file
with open('facebook_credentials.txt') as file:
        EMAIL = file.readline().split('"')[1]
        PASSWORD = file.readline().split('"')[1]
        
# Options
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument('--disable-notifications')

# Start Driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://www.facebook.com")
driver.maximize_window()

# Explicit Wait
wait = WebDriverWait(driver, 10)

# Insert login credentials
email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
email_field.send_keys(EMAIL)
    
pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
pass_field.send_keys(PASSWORD)

# Press return 
pass_field.send_keys(Keys.RETURN)

time.sleep(5)

# list of words to search for
words_to_search = ['Siam', 'สยาม', 'Paragon', 'พารากอน', 'Siam Discovery', 'สยามดิสคัฟเวอรี่', 'ICON', 'ไอคอน', 'Siam Center', 'สยามเซ็นเตอร์', 'Central', 'เซ็นทรัล', 'Central Embassy', 'เซ็นทรัลเอ็มบาสซี่', 'Central Chidlom', 'เซ็นทรัลชิดลม', 'EmQuartier','เอ็มควอเทียร์', 'Emporium','เอ็มโพเรียม']
pages_to_search = ['MallBangkok', 'punpromotion', 'groups/164856035504544', 'globebangkok']

def searchForWord(words_to_search, pages_to_search):
    resultCollection = []
    for page in pages_to_search:
        # Go to page
        driver.get(f"https://www.facebook.com/{page}")
        
        # Scroll down
        lenOfPage = _count_needed_scrolls(driver, False, 100)
        _scroll(driver, False, lenOfPage)
        
        time.sleep(3)
        
        # Grab HTML of page
        source_data = driver.page_source

        # parse with BS
        bs_data = BeautifulSoup(source_data, 'html.parser')

        # Make a file with soup
        with open('./bs.html',"w", encoding="utf-8") as file:
            file.write(str(bs_data.prettify()))
            
        for words in words_to_search:
            
            for post in bs_data.find_all("div", {"class":"x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"}):
                wordCount = {}
                results = {}
                descriptionText = ''
                date = ''
                likeCount = 0
                if words.lower() in post.text.lower():
                    # for dates in post.find_all("a", {"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"}):
                    #     aria_label = dates.get("aria-label")
                    #     if aria_label:
                    #         date = aria_label
                            
                    for description in post.find_all("span", {"class":"x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"}):
                        descriptionText = description.text
                        
                    for likes in post.find_all("span", {"class":"xt0b8zv x1e558r4"}):
                        likeCount = likes.text
                        
                    for word in words_to_search:
                        count = 0
                        if word.lower() in post.text.lower():
                            count += 1
                            wordCount[word] = count
                        else:
                            wordCount[word] = 0      
                
                if (descriptionText):
                    if(page == "groups/164856035504544"):
                        page = 'EventBox'
                    results = {"Page": page, "Description": descriptionText, "Likes": likeCount}
                    results.update(wordCount)
                if(results):
                    if results not in resultCollection:
                        resultCollection.append(results)
    print(resultCollection)            
    return resultCollection

data = searchForWord(words_to_search, pages_to_search)

json_data = json.dumps(data)

# open a text file for writing
with open("results.txt", "w") as f:
    # write the JSON string to the text file
    f.write(json_data)

# convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(data)

# write the DataFrame to an Excel file
df.to_excel('data.xlsx', index=False, encoding='TIS-620')