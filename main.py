#Author: Kayes Fahim
#Email: kiddykayes@gmail.comk
#Python 3.11
#Selenium 4
#Contact For Custome Scraper


import time, mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('headless')
driver = webdriver.Chrome(options = options , service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.marinetraffic.com/")
time.sleep(3)

#Pop Up Close
Agree = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'
driver.find_element("xpath", Agree).click()


connection = mysql.connector.connect(host='localhost', user='root', password='',database='marine')
cursor = connection.cursor()


shipListById = ["7635976","7635980","7635982","7635986","7635990","7635991","7635992", "7635994", "7635996"]

ShipDetails ='https://www.marinetraffic.com/en/ais/home/oldshipid'

# Iterate over the list of ships
for ship in shipListById:

    ShipIdUrl =f"{ShipDetails}:{ship}/olddate:lastknown"
    driver.get(ShipIdUrl)
    time.sleep(3)

    #Ship Name
    ShipNameXpath = '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div/div/div/div[1]/div/div/div[3]/div/a'
    ShipNameText = driver.find_element("xpath", ShipNameXpath)
    ShipName = ShipNameText.text
    print("Shipname value:", ShipName)

    #Speed/Course
    SpeedCourseXpath ='//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/table/tbody/tr[1]/td[2]'
    SpeedCourseText = driver.find_element("xpath", SpeedCourseXpath)
    SpeedCourse = SpeedCourseText.text
    print("SpeedCourse value:", SpeedCourse)

    #Latitude/Longitude
    LatitudeLongitudeXpath ='//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/table/tbody/tr[2]/td[2]'
    LatitudeLongitudeText = driver.find_element("xpath", LatitudeLongitudeXpath)
    LatitudeLongitude = LatitudeLongitudeText.text
    print("Latitude/Longitude value:", LatitudeLongitude)

    #NavigationalStatus
    NavigationalStatusXpath ='//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/table/tbody/tr[3]/td[2]'
    NavigationalStatusText = driver.find_element("xpath", NavigationalStatusXpath)
    NavigationalStatus = NavigationalStatusText.text
    print("NavigationalStatus value:", NavigationalStatus)

    #LastDataRecieved
    LastDataRecievedXpath ='//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/div[2]/strong/div'
    LastDataRecievedText = driver.find_element("xpath", LastDataRecievedXpath)
    LastDataRecieved = LastDataRecievedText.text
    print("LastDataRecieved value:", LastDataRecieved)

    #DB Connection

    insert_query = "INSERT INTO data (name, speed, ll, ns, ldr) VALUES (%s, %s, %s, %s, %s)"
    data_to_insert = (ShipName, SpeedCourse, LatitudeLongitude,NavigationalStatus,LastDataRecieved)
    cursor.execute(insert_query, data_to_insert)
    connection.commit()
    print("Data Added Successfully : "+ShipName)
