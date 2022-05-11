from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from datetime import date, datetime
from termcolor import colored
import vlc  # pip install python-vlc


url_twitter = "https://twitter.com/elonmusk"
matches = ["shib", "dog", "doge", "btc", "bitcoin", "eth", "ethereum", "bnb", "binance", "crypto", "coin"]
tweets = []
tweet_filter = True

alarm_higher = "alarm_higher.mp3"
alarm_lower = "alarm_lower.mp3"

def Sound(sound):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(sound)
    player.set_media(media)
    player.audio_set_volume(80)
    player.play()
    # time.sleep(1.5)
    # duration = player.get_length() / 1000
    # time.sleep(duration)

def scraping(url):
    try:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.headless = True
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
        driver = webdriver.Chrome('chromedriver', service_log_path='/dev/null', options=chrome_options)    # service_log_path='/dev/null' to disable logging, otherwise errors occur
        driver.set_page_load_timeout(10)

        try:
            driver.get(url)
        except (TimeoutException, WebDriverException) as e:
            print("Exception in driver.get(url) - " + e.msg)

        time.sleep(10)

        cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')

        time_now = datetime.now()
        todays_day = date.today().day

        for card in cards:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
            postdate_day = str(postdate).split("-")[2].split("T")[0].strip()
            tweet = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text

            if tweet_filter and any(x in str(tweet).lower() for x in matches) and (str(todays_day) == postdate_day or str(int(todays_day)-1) == postdate_day):
                # print("POST DATE: " + postdate)
                if not tweets.__contains__(tweet):
                    tweets.append(tweet)
                    Sound(alarm_lower)
                    print(colored("\n" + "************************************************************************************************", 'red'))
                    print(colored("TWEET {}: {}".format(tweets.index(tweet), tweet), 'red'))   # print new tweet in yellow warning color
                    print(colored("************************************************************************************************", 'red'))
                else:
                    print("\n" + "************************************************************************************************")
                    print("TWEET {}: {}".format(tweets.index(tweet), tweet))
                    print("************************************************************************************************")

            if not tweet_filter:
                if not tweets.__contains__(tweet):
                    tweets.append(tweet)
                    Sound(alarm_lower)
                    print(colored("\n" + "************************************************************************************************", 'red'))
                    print(colored("TWEET {}: {}".format(tweets.index(tweet), tweet), 'red'))   # print new tweet in yellow warning color
                    print(colored("************************************************************************************************", 'red'))
                else:
                    print("\n" + "************************************************************************************************")
                    print("TWEET {}: {}".format(tweets.index(tweet), tweet))
                    print("************************************************************************************************")


        driver.close()
        driver.quit()
        print("\n" + "Sleep 10s... [ " + time_now.strftime("%d/%m/%Y %H:%M:%S") + " ] \n")
        time.sleep(10)
    except:
        print("Scraping exception [ " + time_now.strftime("%d/%m/%Y %H:%M:%S") + " ]")
        driver.close()
        driver.quit()

if __name__ == "__main__":
    while True:
        scraping(url_twitter)
