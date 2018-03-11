import csv
import requests
import time
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

url_list = ['https://www.carfax.com/Used-Mercedes-Benz_m22&121','https://www.carfax.com/Used-Subaru_m32&113']

file_count = 0
for item in url_list:
    address, max_page = item.split('&')
    start = item.find('Used-') + 5
    end = item.find('_m', start)
    the_make = item[start:end]
    print the_make
    print address
    print max_page
    

    driver = webdriver.Chrome('/home/hogarth/Desktop/chromedriver')
    driver.get(address)

    inputElement = driver.find_element_by_name('zip')
    inputElement.send_keys('97330')

    select_radius = Select(driver.find_element_by_name('radius'))
    select_radius.select_by_visible_text('500')

    driver.find_element_by_id("make-model-form-submit").click()

    page = driver.page_source
    soup = BeautifulSoup(page)

    options_list = []
    list_of_rows = []
    vin_number = []
    count = 0

    # number of pages
    def scraper(soup, count, list_of_rows):
        for i in range(int(max_page)):

            table = soup.find('div', {'id': 'react-app'})

            for row in table.findAll('article',{'class': 'srp-list-item'}):
                vin = row.find('a').attrs[0][1] # to get the vin number
                url = 'https://www.carfax.com' + vin

                if vin in vin_number:
                    continue
                else:
                    vin_number.append(vin)
                # pages for one vin number
                list_of_cells = []
                response = requests.get(url)
                html = response.content
                soup_vin = BeautifulSoup(html)

                # store year, make, model
                car = soup_vin.find('h1', {'class': 'vehicle-title'})
                print car.text
                info = car.text.split()
                list_of_cells.append(info[0]) # year
                list_of_cells.append(info[1]) # make
                list_of_cells.append(info[2]) # model

                # to get carfax title info
                snapshot = soup_vin.find('div', {'class': 'carfax-snapshot-box'})
                report = snapshot.findAll('div', {'class': 'column'})

                condition1 = 'No accidents reported to CARFAX'
                condition2 = 'No other damage reported to CARFAX'
                if str(report[0].text) == condition1 and str(report[1].text) == condition2:
                    title = 'clean'
                else:
                    title = 'dirty'
                list_of_cells.append(title)


                # detail info
                table_info = soup_vin.find('table', {'class': 'infoTable-table'})
                for row in table_info.findAll('td'):
                    
                    if '/' in row.text:
                        tmp = row.text.replace('/', ' ').split()
                        list_of_cells.append(tmp[0])
                        list_of_cells.append(tmp[1])
                    elif 'Cyl' in row.text:
                        tmp = row.text.split()
                        list_of_cells.append(tmp[0] + tmp[1])
                        list_of_cells.append(tmp[2] + tmp[3])
                    elif '$' in row.text:
                        list_of_cells.append(row.text.replace(',','').replace('$', ''))
                    elif ' miles' in row.text:
                        list_of_cells.append(row.text.replace(',','').replace(' miles', ''))
                    else:
                        list_of_cells.append(row.text.replace(',',''))

                count += 1
                print count
                list_of_rows.append(list_of_cells[:-1])
            
            # next pages
            element = driver.find_element_by_class_name('next')
            driver.execute_script("arguments[0].click();", element)
            '''
            try:
                element = driver.find_element_by_class_name('next')
                driver.execute_script("arguments[0].click();", element)
            except NoSuchElementException:
                return
            '''

            page = driver.page_source
            soup = BeautifulSoup(page)

    scraper(soup, count, list_of_rows)

    outfile = open("./carfax_data_"+str(the_make)+'.csv', "wb")
    file_count +=1
    writer = csv.writer(outfile)
    writer.writerows(list_of_rows)