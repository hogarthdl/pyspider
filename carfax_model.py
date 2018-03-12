import csv
import requests
import time
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

'''
https://www.carfax.com/Used-Acura_m1&225
https://www.carfax.com/Used-Audi_m2&280
https://www.carfax.com/Used-BMW_m3&665
https://www.carfax.com/Used-Buick_m4&229
https://www.carfax.com/Used-Cadillac_m5&260
https://www.carfax.com/Used-Chevrolet_m6&1647
https://www.carfax.com/Used-Chrysler_m7&283
https://www.carfax.com/Used-Dodge_m8&485
https://www.carfax.com/Used-Ford_m9&1869
https://www.carfax.com/Used-GMC_m10&505
https://www.carfax.com/Used-Honda_m11&953
https://www.carfax.com/Used-Hyundai_m13&560
https://www.carfax.com/Used-Infiniti_m14&189
https://www.carfax.com/Used-Jaguar_m15&34
https://www.carfax.com/Used-Jeep_m16&959
https://www.carfax.com/Used-Kia_m17&367
https://www.carfax.com/Used-Land-Rover_m18&78
https://www.carfax.com/Used-Lexus_m19&319
https://www.carfax.com/Used-Lincoln_m20&139
https://www.carfax.com/Used-Mazda_m21&215
https://www.carfax.com/Used-Mercedes-Benz_m22&524
https://www.carfax.com/Used-Mini_m24&85
https://www.carfax.com/Used-Mitsubishi_m25&72
https://www.carfax.com/Used-Nissan_m26&1106
https://www.carfax.com/Used-Pontiac_m27&43
https://www.carfax.com/Used-Porsche_m28&75
https://www.carfax.com/Used-Ram_m29&321
https://www.carfax.com/Used-Subaru_m32&410
https://www.carfax.com/Used-Tesla_m60&1
https://www.carfax.com/Used-Toyota_m33&1267
https://www.carfax.com/Used-Volkswagen_m34&394
https://www.carfax.com/Used-Volvo_m35&144
https://www.carfax.com/Used-AM-General_m36&1
https://www.carfax.com/Used-Alfa-Romeo_m37&2
https://www.carfax.com/Used-Aston-Martin_m38&3
https://www.carfax.com/Used-Bentley_m39&7
https://www.carfax.com/Used-Daewoo_m40&1
https://www.carfax.com/Used-Datsun_m41&1
https://www.carfax.com/Used-Eagle_m42&1
https://www.carfax.com/Used-Ferrari_m43&9
https://www.carfax.com/Used-Fiat_m44&23
https://www.carfax.com/Used-Freightliner_m46&2
https://www.carfax.com/Used-Geo_m47&1
https://www.carfax.com/Used-Hummer_m12&14
https://www.carfax.com/Used-Isuzu_m48&2
https://www.carfax.com/Used-Lamborghini_m49&2
https://www.carfax.com/Used-Lotus_m50&1
https://www.carfax.com/Used-Maserati_m51&19
https://www.carfax.com/Used-Maybach_m52&1
https://www.carfax.com/Used-Mclaren_m53&2
https://www.carfax.com/Used-Mercury_m23&25
https://www.carfax.com/Used-Oldsmobile_m54&4
https://www.carfax.com/Used-Plymouth_m55&1
https://www.carfax.com/Used-Rolls-Royce_m56&2
https://www.carfax.com/Used-Saab_m57&8
https://www.carfax.com/Used-Saturn_m30&24
https://www.carfax.com/Used-Scion_m31&36
https://www.carfax.com/Used-Smart_m58&5
https://www.carfax.com/Used-Suzuki_m59&8
'''

url_list = ['https://www.carfax.com/Used-Toyota_m33&1267',
            'https://www.carfax.com/Used-Land-Rover_m18&16',
            'https://www.carfax.com/Used-Lexus_m19&94',
            'https://www.carfax.com/Used-Lincoln_m20&15',
            'https://www.carfax.com/Used-Mazda_m21&57']
            
file_count = 0

for item in url_list:
    address, max_page = item.split('&')
    start = item.find('Used-') + 5
    end = item.find('_m', start)
    the_make = item[start:end]
    print the_make
    print address
    print max_page

    outfile = open("./carfax_data_"+str(the_make)+'.csv', "wb")
    writer = csv.writer(outfile)
    

    driver = webdriver.Chrome('/home/hogarth/Desktop/chromedriver')
    driver.get(address)

    inputElement = driver.find_element_by_name('zip')
    inputElement.send_keys('10001')

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
                #list_of_cells.append(' '.join(info[2:]).encode('utf-8')) # model
                list_of_cells.append((info[2]).encode('utf-8')) # model 

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
                str1 = [list_of_cells[:-1]] # writer.writerows need list of list
                writer.writerows(str1)
                outfile.flush()
            
            # next pages
            try:
                element = driver.find_element_by_class_name('next')
                driver.execute_script("arguments[0].click();", element)
            except NoSuchElementException:
                return
            
            page = driver.page_source
            soup = BeautifulSoup(page)

    scraper(soup, count, list_of_rows)
    file_count +=1
