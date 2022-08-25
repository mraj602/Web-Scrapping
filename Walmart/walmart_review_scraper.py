from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import winsound
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# defining constants for the program.

# 'url' is the url of product on walmart to scrape
URL = "https://www.walmart.com/ip/Clorox-Disinfecting-Wipes-225-Count-Value-Pack-Crisp-Lemon-and-Fresh-Scent-3-Pack-75-Count-Each/14898365"
# 'target_date is the date till which to scrape the reviews
target_date = datetime.strptime("December 01, 2020", "%B %d, %Y")


def escape_verifer(driver):
    """
    The function notifies the user with a beep
    that a human verification page has popped up
    and requests the user to complete the verification.
    The user is notified every 5 seconds with a beep
    to complete the verification process.
    :param driver: Chrome webdriver currently active
    :return:
    """
    print("BLOCKED. Please Verify")
    print("Waiting for verifying captcha")
    # looping indefinitely till the user completes the verification
    # when the verification element is not found and an exception is raised,
    # the function returns
    while True:
        try:
            winsound.Beep(3000, 1000)
            driver.find_element_by_xpath('//*[@id="px-captcha"]')
            # time.sleep(5)
        except:
            pass
            return


def start_scraping(url):
    """
    The function starts scraping the walmart product url
    :url: the url to scrape
    :return:
    """
    target_reached = False  # used to determine if the target date or total reviews have ended while scraping
    # driver = webdriver.Chrome()

    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome('chromedriver.exe', options=option)
    # running indefinitely so if an exception is raised in middle of scraping, the process can be restarted
    # after human verification
    while True:
        try:
            rows = []
            driver.get(url)
            # checking if the website is redirected to human verification page
            # print("blocked" in str(driver.current_url))
            # while False:
            #     print("in false")
            while "blocked" in str(driver.current_url):
                escape_verifer(driver)
            # scrolling down to the customer review heading
            element = driver.find_element("xpath","//*[@id='item-review-section']/header/h2")
            driver.execute_script("arguments[0].scrollIntoView()", element)
            # waiting for few seconds as the system might hang and error pops up
            time.sleep(4)

            # opening the customer reviews page
            driver.find_element("xpath","//*[@id='item-review-section']/div[2]/a[1]").click()

            # sorting the reviews according to 'new to old'
            dropdown_select = Select(driver.find_element("xpath",
                "//*[@id='maincontent']/main/section/div[2]/div[2]/div[3]/button"))
            dropdown_select.select_by_visible_text("newest to oldest")
            time.sleep(5)  # waiting for the initial reviews to load

            # finding the total number of reviews of the
            # product in order to check later if reviews
            # have ended before target date is reached
            total_rev = int(str(driver.find_element("xpath",
                '//*[@id="maincontent"]/main/section/div[2]/div[2]/div[1]').text).split(
                ' ')[0])
            rev_counter = 0

            # the element path for 'next page' is different on 1st and rest of the pages.
            # using a flag to determine this
            counter = False
            while not target_reached:
                # waiting for each of the review page to load
                time.sleep(1.25)

                # as the number of reviews in a page is limited to 20,
                # loop is fixed to run for scraping 20 reviews in each page
                # and an if statement is used to check for total reviews ending in middle of page
                for i in range(1, 21):
                    rev_counter = rev_counter + 1
                    # checking if total number of reviews on product has been scraped
                    if rev_counter > total_rev:
                        print("Total Review ended before reaching target date.")
                        target_reached = True
                        break

                    row = []
                    # finding the date of the review and checking with our required target date
                    date_element = driver.find_element("xpath",
                        "/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{}]/div/div[1]/div/div[2]/span".
                            format(i))
                    date = datetime.strptime(date_element.text, "%B %d, %Y")
                    if date < target_date:
                        target_reached = True
                        break

                    # many reviews have empty title of the review.
                    # Therefore if a NoSuchElementException is raised while
                    # scraping the title of the review, an empty string is
                    # used as title
                    rating = driver.find_element("xpath",
                        "/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{}]/div/div[1]/div/div[1]/div["
                        "1]/div/div/span[3]/span[2]".format(
                            i)).text
                    try:
                        title = (driver.find_element("xpath",
                            "/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{}]/div/div[1]/div/div["
                            "1]/div[1]/h3".format(
                                i)).text)
                    except NoSuchElementException:
                        title = ""

                    description = driver.find_element("xpath",
                        "/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{}]/div/div[1]/div/div[3]".format(
                            i)).text
                    name = driver.find_element("xpath",
                        "/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[{}]/div/div[1]/div/div["
                        "4]/div/div/span[2]".format(
                            i)).text
                    row = [date.date(), name, title, description, float(rating)]
                    rows.append(row)

                # checking if the target is still not reached then opening the next page of reviews
                if not target_reached:
                    # if the first review page is opened, then different button path is clicked
                    if not counter:
                        driver.find_element("xpath",
                            '/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[2]/div/div/button').click()
                        counter = True
                    else:
                        driver.find_element("xpath",
                            '/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[2]/div/div/button[2]').click()
            driver.close()
            break
        except Exception as err:
            # if in between of scraping the reviews human verification pops up
            # (mostly happens only during sorting of reviews), the page is reloaded
            # in order to open the full human verification page and then it is handled
            # by escape_verify() function
            driver.refresh()
            print(err)
            escape_verifer(driver)
    create_csv(rows)


def create_csv(rows):
    """
    Creates a csv file and names it output.csv. Also contains
    the header of the file
    :param rows: 2D Array with each element inside being a row
    format: Date, Name, Title, Description, Rating(float)
    :return:
    """
    filename = 'output.csv'
    columns = ['Date', 'Name', 'Title', 'Description', 'Rating']
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(columns)
        csvwriter.writerows(rows)

    print("Successfully saved {} records in output.csv".format(len(rows)))


# calling the start_scraping method with the url defined.
start_scraping(URL)
