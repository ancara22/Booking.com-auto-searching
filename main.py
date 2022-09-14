import time
from datetime import timedelta, date
from selenium import webdriver
from selenium.webdriver.common.by import By

fromPlace = "LON.CITY"
toPlace = "KIV.AIRPORT"
fromCountry = "GB"
toCountry = "MD"
fromLocationName = "London"
toLocationName = "Chișinău"


class FLightSearch:
    def __init__(self, fromPlace, toPlace, fromCountry, toCountry, fromLocationName, toLocationName):
        self.fromPlace = fromPlace
        self.toPlace = toPlace
        self.fromCountry = fromCountry
        self.toCountry = toCountry
        self.fromLocationName = fromLocationName
        self.toLocationName = toLocationName
        self.driver = None
        self.final_result = []
        self.prices = []

    def FindFlight(self, departure_date, i):

        url = f"https://flights.booking.com/flights/{self.fromPlace}-{self.toPlace}/?type=ONEWAY&adults=1&cabinClass=ECONOMY&children=&from={self.fromPlace}&to={self.toPlace}&fromCountry={self.fromCountry}&toCountry={self.toCountry}&fromLocationName={self.fromLocationName}&toLocationName={self.toLocationName}+International+Airport&stops=0&depart={departure_date}&sort=BEST&aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaFCIAQGYAQm4AQfIAQ3YAQPoAQGIAgGoAgO4Ave8g5kGwAIB0gIkODE1YTgzNTMtYzk4Ny00YWFiLTkzMmUtOTQ1MmYyODM5ZWY22AIE4AIB"
        self.driver.get(url)

        try:
            btn = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            btn.click()
        except:
            pass

        try:
            time.sleep(3)
            mydivs = self.driver.find_elements(By.CLASS_NAME, "css-4o3ibe")

            res = []
            for el in mydivs:
                str_g = el.text\
                    .replace("\n", "").replace("Total price for all travelersSee flight", "")\
                    .replace("Direct", " ").replace("Included: personal item", " ")\
                    .replace(", cabin bag", "").replace(" . ", "")\
                    .replace((departure_date.strftime("%B")[0:4]+departure_date.strftime(" %d")), " ")\
                    .replace((departure_date.strftime("%B")[0:3]+departure_date.strftime(" %d")), " ")\
                    .replace("£", " £").replace("PM", "PM  ").replace("AM", "AM  ")

                res.append(str_g.split())

            prices_array = [float(price[-1].replace("£", "")) for price in res]
            pos_min = prices_array.index(min(prices_array))
            print(f"Success {i}")
            text_to_save = f"\n\n{i}) Date: {departure_date}\n   " + " ".join(res[pos_min])
            self.final_result.append(text_to_save)

            with open(file=f"{self.fromPlace}-{self.toPlace}.txt", mode="a") as resultFile:
                resultFile.write(text_to_save)
                resultFile.close()
        except:
            print("Slow internet")
            pass

    def start_searching_flights(self):
        with open(file=f"{self.fromPlace}-{self.toPlace}.txt", mode="w") as resultFile:
            resultFile.write("")
            resultFile.close()

        driver_path = "/Users/dinisbarcari/Documents/chromedriver"
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(driver_path, options=op)

        for i in range(1, 90):
            next_day = date.today() + timedelta(days=i)
            self.FindFlight(next_day, i)

        for element in self.final_result:
            self.prices.append(float(element.split()[-1].replace("£", "")))

        min_price = min(self.prices)
        index_of = self.prices.index(min_price)

        with open(file=f"{self.fromPlace}-{self.toPlace}.txt", mode="a") as resultFile:
            resultFile.write(f"\n\n\n--------Cheapest Flight:--------{self.final_result[index_of]}\n------------------------")
            resultFile.close()


ldn_kiv = FLightSearch(fromPlace, toPlace, fromCountry, toCountry, fromLocationName, toLocationName)

ldn_kiv.start_searching_flights()