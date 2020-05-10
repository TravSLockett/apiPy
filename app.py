from flask import Flask, request
from flask import jsonify
from selenium import webdriver
from bs4 import BeautifulSoup as bs
app = Flask('test')
import time

@app.route('/getCourse')
def hofDynamic():
    semester = request.args.get('semester')
    print(semester)
    start = time.perf_counter()
    browser = webdriver.Chrome()
    browser.get('https://hofstraonline.hofstra.edu/pls/HPRO/bwckschd.p_disp_dyn_sched')
    browser.maximize_window()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select').click()

    if(semester == "MedFall2020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[2]').click()
    elif(semester == "Fall2020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[3]').click()
    elif(semester == "Summer32020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[4]').click()
    elif(semester == "Summer22020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[5]').click()
    elif(semester == "Summer12020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[6]').click()
    elif(semester == "MedSpring2020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[7]').click()
    elif(semester == "ParaSpring2020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[8]').click()
    elif (semester == "Spring2020"):
        browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[9]').click()
    else:
        browser.quit()
        return "Are you tripping about which semester you are in?"

    #browser.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/div/div[2]/form/div/table/tbody/tr/td/select/option[4]').click()
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
        cleanClassInfo = {"crn": cleanClass[1], "subject": cleanClass[2], "course": cleanClass[3], "credits": cleanClass[6], "title": cleanClass[7], "days": cleanClass[8], "time": cleanClass[9], "remainSeats": cleanClass[12], "prof": cleanClass[19] }
        fullSchedule.append(cleanClassInfo)

    print(fullSchedule)
    stop = time.perf_counter()
    print(f"Processed the request in {stop - start:0.4f} seconds")

    #f = open('hofClass.json', 'w')
    #dump(fullSchedule, f, indent=4)
    #f.close()
    browser.quit()

    data = jsonify(fullSchedule)
    return data

app.run(host="0.0.0.0", port="9999")
