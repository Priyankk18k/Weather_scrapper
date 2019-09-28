from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import io
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By


def get_data(div_container1,div_container_details):
    state1 = []
    temp1 = []
    status1 = []
    feels_like_temp1 =[]
    uv_index1 = []
    time1 = []
    wind1 = []
    humidity1 =[]
    dew_point1 = []
    pressure1 = []
    visibility1 = []
    for one, two in zip(div_container1,div_container_details):
        state = one.find_all("h1", class_='h4 today_nowcard-location')[0].text
        temp = one.find_all("div", class_='today_nowcard-temp')[0].text
        status = one.find_all("div", class_='today_nowcard-phrase')[0].text
        feels_like_temp = "Feels Like" + " "+ one.find_all("span", class_='deg-feels')[0].text
        uv_index = one.find_all("span", class_='')[5].text
        time = one.find_all("span", class_='')[1].text
        wind = two.find_all("span", class_='')[0].text
        humidity = two.find_all("span", class_='')[1].text
        dew_point = two.find_all("span", class_='')[3].text
        pressure = two.find_all("span", class_='')[4].text
        visibility = two.find_all("span", class_='')[5].text
        state1.append(state)
        temp1.append(temp)
        status1.append(status)
        feels_like_temp1.append(feels_like_temp)
        uv_index1.append(uv_index)
        time1.append(time)
        wind1.append(wind)
        humidity1.append(humidity)
        dew_point1.append(dew_point)
        pressure1.append(pressure)
        visibility1.append(visibility)


    data = {'state':state1,'temp':temp1,'status':status1,'feels_like_temp':feels_like_temp1,'uv_index':uv_index1,'time':time1,'wind':wind1,
           'humidity':humidity1,'dew_point':dew_point1,'pressure':pressure1,'visibility':visibility1}

    df = pd.DataFrame(data)
    return df

if __name__== "__main__":
    driver = webdriver.Chrome(executable_path=r'C:\Users\Priyank\PycharmProjects\selenium\chromedriver.exe')
    driver.get("https://weather.com/en-IN/")
    print(driver.title)
    time.sleep(5)
    properties = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(
        '//*[@id="header-TwcHeader-144269fc-62bc-4d06-bc79-e158594b14ff"]/div/div/div/div[2]/div/div[1]/div/input'))
    city_name = input("Enter the city for which you want to search :-")
    #     city_name = 'Delhi, DL, INDIA'
    properties.send_keys(city_name)
    time.sleep(5)
    properties.send_keys(Keys.RETURN)
    time.sleep(10)
    first_result = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(
        '//*[@id="main-EnhancedLocalSearch-e6dd8357-0c66-41b7-8c28-e3723fbe0cc8"]/div/div/ul/li[1]/a')).click()

    data = driver.page_source
    html_soup = BeautifulSoup(data, 'html.parser')
    div_container1 = html_soup.find_all('div',
                                        class_="today_nowcard-main component panel today-card-night-cloudy-mostly")
    div_container_details = html_soup.find_all('div', class_="today_nowcard-sidecar component panel")
    dataFrame = get_data(div_container1,div_container_details)
    print(dataFrame)