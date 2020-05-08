from flask import Flask
from flask import jsonify
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
from json import dump
app = Flask('test')
import time

@app.route('/getCourse')
def hofDynamic():

    start = time.perf_counter()
    browser = webdriver.Chrome()
    browser.get('https://hofstraonline.hofstra.edu/pls/HPRO/bwckschd.p_disp_dyn_sched')
    browser.maximize_window()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select').click()
    browser.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[4]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/button[1]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[3]/form/button[1]').click()

    web = bs(browser.page_source, 'html.parser')
    test = web.find_all('tr', id='section_row')

    fullSchedule = []
    for idx in range(len(test)):
        oneClass = test[idx].find_all('td', class_='dddefault')
        cleanClass= []
        for n in range(len(oneClass) - 1):
            cleanClass.append(oneClass[n].get_text())
        #oriClassObj = []
        #oriClassObj.append(cleanClass)
        #print(oriClassObj[0])
        #print(cleanClass)
        cleanClassInfo = [cleanClass[1], cleanClass[2], cleanClass[3], cleanClass[6], cleanClass[7], cleanClass[8], cleanClass[9], cleanClass[12], cleanClass[19] ]
        fullSchedule.append(cleanClassInfo)

    print(fullSchedule)
    stop = time.perf_counter()
    print(f"Processed the request in {stop - start:0.4f} seconds")

    f = open('hofClass.json', 'w')
    dump(fullSchedule, f, indent=4)
    f.close()
    browser.quit()
    json.dumps(fullSchedule)
    print(type(fullSchedule))


    return fullSchedule

app.run(host="0.0.0.0", port="9999")