# Walmart Reviews Scraper
The project is intended to scrape the reviews of any product on the Walmart website and save it as a CSV file. 
As there are thousands of reviews for many products and only recent reviews are helpful, the scraper is programmed to sort the reviews from newest to oldest and then stop at the date defined in the condition. 
As Walmart's website uses a bot detection program to stop bots from scraping the website with a simple "click and hold" button for the randomized duration, there were challenges to work with this scraper as the human verification would pop up at any time. 

On analyzing trends after several trials, a pattern was noticed that the scraper would generally pop up just after sorting the reviews and, if reloaded, it would open a full page for human verification. 
Once after verifying it manually, the bot would not appear at least one time for a product no matter how many reviews are accessed. 

To find a workaround, the scraper is designed to do the following:

1. Open the product webpage from the provided URL.

2. If directly human detection page is opened, then the user is notified using a beep sound every 5 seconds to pass the human verification process. Then the product webpage loads.

3. If directly product webpage is opened, then the page is scrolled down, clicked on see reviews, and reviews are sorted according to newest to oldest. A human verification popup could load here. In that case, the webpage is reloaded to open the full human verification page. After passing the human verification, the product webpage is loaded again.

4. Almost every time, once after passing the human verification page, another human verification never pops up for the same product. In that case, the scraper does its works and scrapes all the reviews.

5. The scraper then saves the scraped data in a CSV file.


The scraper saves the following data for each review:

1. Date

2. Reviewer Name

3. Review Title (blank if not present)

4. Review Description

5. Rating (out of 5)


The CSV file is saved as output.csv
