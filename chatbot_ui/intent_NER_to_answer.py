# call selnium for automated testing
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import googletrans

def make_answer(intent_predict,NER_predict):
    try:
        # create options
        options = webdriver.ChromeOptions()
        # add option to hide browser window
        options.add_argument("headless")
        driver = webdriver.Chrome("./chromedriver.exe" )
        driver.set_window_size(50, 50)
        # url to connect to
        url = "https://www.google.com"

        # try to connect
        driver.get(url)

        # Little bit of time is required for the webpage to load, so use sleep to wait
        time.sleep(0.5) 

        if intent_predict == "atis_airfare": 
            # price of ticket to destination

            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict[0]} to {NER_predict[1]} flight ticket price")
            element.submit()
            time.sleep(0.5)

            # get page url
            answer = "Please check the following link >> " + driver.current_url 
            
        elif intent_predict == "atis_airline": 
            # give website of the airline or give information about the airline (link for the airline webpage)

            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict}")
            element.submit()
            # get page url
            answer = "Please check the following link >> " + driver.current_url

        elif intent_predict == "atis_flight": 
            # list of flights that are going to the destination 

            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict[0]} to {NER_predict[1]} flight")
            element.submit()
            time.sleep(0.5)
            answer = "Please check the following link >> " + driver.current_url

        elif intent_predict == "atis_flight_time": 
            # search how long the flight takes and gives answer to the user.

            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict[0]} to {NER_predict[1]} flights")
            element.submit()

            time.sleep(3)
            answer = "Please check the following link >> " + driver.current_url

        elif intent_predict == "current_location": 
            # search current location information using selenium and use it to answer the question.

            # url to connect to
            url = "https://www.gps-coordinates.net/my-location"
            # try to connect
            driver.get(url)
            # it takes some time for the webpage to load, so use sleep to wait.
            time.sleep(5)
            # get page source
            html = driver.page_source

            # put it into soup
            soup = BeautifulSoup(html, 'html.parser')
            print(soup.find("span",{"id":"addr"}))
            answer = soup.find("span",{"id":"addr"}).text   

        elif intent_predict == "distance": 
            # use google maps to get distance between two cities.

            # search 
            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict[0]} and {NER_predict[1]} distance")
            element.submit()

            # get page source
            html = driver.page_source

            # put it into soup
            soup = BeautifulSoup(html, 'html.parser')

            answer = soup.find("div", class_="dDoNo FzvWSb vk_bk").text

            # translate Korea to English
            translator = googletrans.Translator()

            answer = translator.translate(answer, src='ko', dest='en').text


        elif intent_predict == "timezone": 
            # search timezone
            # search
            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict} time")
            element.submit()

            # get page source
            html = driver.page_source

            # put it into soup
            soup = BeautifulSoup(html, 'html.parser')

            result = soup.find("div", class_="gsrt vk_bk FzvWSb YwPhnf").text

            if result[0:2]=="오전":
                answer = "AM"+result[2:]
            else: 
                answer = "PM"+result[2:]

        elif intent_predict == "travel_suggestion" : 
            # find tourist attractions (use current location to find tourist attraction using google)

            element = driver.find_element("name", "q")
            element.send_keys("Attractions near my location")
            element.submit()

            time.sleep(3)

            # get page source
            html = driver.page_source

            # put it into source
            soup = BeautifulSoup(html, 'html.parser')

            result = soup.find("div", class_="N60sec")
            result = result.findAll("span", class_="OSrXXb")
            
            # translate Korean to English
            translator = googletrans.Translator()

            # change result to list
            result = list(map(lambda x: "/".join(x).replace('<span class="OSrXXb">',""), result))[:-1]
            answer= ", ".join(list(map(lambda x: translator.translate(x, src='ko', dest='en').text, result)))


        elif intent_predict == "weather": 
            # weather of city the user gave to chatbot

            element = driver.find_element("name", "q")
            element.send_keys(f"{NER_predict} weather")
            element.submit()

            time.sleep(0.5)
            # get page source 
            html = driver.page_source

            # put it into soup 
            soup = BeautifulSoup(html, 'html.parser')
            answer = soup.find("span",{"id":"wob_dc"}).text

            # translate Korea to English
            translator = googletrans.Translator()

            answer = translator.translate(answer, src='ko', dest='en').text

        # if there is no answer for the question
        else:
            answer = "Not found."

        # if there was an error while finding the answer
    except:
            answer = "Not found."

    return answer 