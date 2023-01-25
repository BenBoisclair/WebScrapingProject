This project is made for my Siam Piwat Internship.

Its purpose is to scrape social media websites to find posts that is relevant to the keywords you're trying to find, which is a way of social listening. 

The website that this is focused on is Facebook.

## Technologies
Python
Selenium
BeautifulSoup
Pandas

## How to use
1. Clone the Project and make a file in the root called "facebook_credentials.txt".
2. Enter your credentials in this format:
email = "EMAIL"
password = "PASSWORD"
3. Change the keywords and pages you want to scrape in the WebScrape.py
4. Type "python3/python WebScrape.py" in the Terminal
5. The output will be a data.xlsx file which includes all the data in an excel sheet

## Limitations
Since Facebook is always updating their code and this program relies heavily on BeautifulSoup to work, you may need to update the class names to successfully scrape the correct elements. Scraping on Facebook is against the TOS and this project is only for Educational Purposes. It can only scrape Likes and Descriptions. 