import csv
import requests
import time
from BeautifulSoup import BeautifulSoup

# For database guy 
# 14 elements one line of csv, some are empty
# year, make, model, VIN, odometer, condition, cylinders, drive, fuel, pain color, size, title status, transmission, type

car_list = []
pages = 2
count = 0
url_list = []
for i in range(pages): 
    main_url = 'https://corvallis.craigslist.org/search/cta?s=' + str(i*120)
    main_response = requests.get(main_url)
    main_html = main_response.content

    soup = BeautifulSoup(main_html)
    table = soup.find('ul', {'class': 'rows'}).findAll('a')

    for ad in table:
        url = ad['href']
        if url != '#' and url not in url_list:
            url_list.append(url)

print 'number of cars: ' + str(len(url_list))

# for each car
for url in url_list:
    count += 1
    response = requests.get(url)
    html = response.content
    soup_vin = BeautifulSoup(html)

    vehicle = soup_vin.find('span', {'id': 'titletextonly'})
    price = soup_vin.find('span', {'class': 'price'})
    
    info = ['']*14
    raw_info = soup_vin.findAll('p', {'class': 'attrgroup'})

    tmp1 = raw_info[0].text.split('<br />')[0]  # year + make + model
    tmp2 = raw_info[1].findAll('span')          # detail info

    year = tmp1.split()[0]
    info[0] = year
    make = tmp1.split()[1]
    model = ' '.join(tmp1.split()[2:])
    info[1] = make
    info[2] = model

    for ele in tmp2:
        tmp = ele.text.split(':')
        if tmp[0] == 'VIN':
            info[3] = tmp[1]
        elif tmp[0] == 'odometer':
            info[4] = tmp[1]
        elif tmp[0] == 'condition':
            info[5] = tmp[1]
        elif tmp[0] == 'cylinders':   
            info[6] = tmp[1]     
        elif tmp[0] == 'drive':
            info[7] = tmp[1]
        elif tmp[0] == 'fuel':
            info[8] = tmp[1]
        elif tmp[0] == 'paint color':
            info[9] = tmp[1]
        elif tmp[0] == 'size':
            info[10] = tmp[1]
        elif tmp[0] == 'title status':
            info[11] = tmp[1]
        elif tmp[0] == 'transmission':
            info[12] = tmp[1]
        elif tmp[0] == 'type':
            info[13] = tmp[1]

        #print ele.text
    print info[0] +' '+ info[1]+' '+ info[2]
    print count
    car_list.append(info)

outfile = open('./craigslist_data.csv', 'wb')
writer = csv.writer(outfile)
writer.writerows(car_list)