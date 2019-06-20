import pandas, json, requests, csv
from bs4 import BeautifulSoup
from config import url, flipkart, TITLE, output_files

SlNo = 1 # to print count infrond of product name (console)
_header = True
json_data = {}
json_data_temp = {}
PageNo = 0


def make_csv(datas):
    global  _header
    dict = {
            'product name' :          datas[0], # pr_names
            'Product review' :        datas[1], # pr_avg_rev,
            'Selling price' :         datas[2], # pr_price_selling,
            'Original price' :        datas[3], # pr_price_original
            'Product Description' :   datas[4], # pr_disc
            'Product specification' : datas[5], # pr_Spec
            'Product url' :           datas[6], # pr_url
            'Image links' :           datas[7], # links
            }

    # generating csv file using pandas
    df = pandas.DataFrame(dict)
    with open('testcsv.csv', 'w', encoding="utf-8", newline='') as csvfile:

        # to check for titile
        if _header is True:
            df.to_csv(csvfile, index=False, header=True)
            _header = False
        else:
            df.to_csv(csvfile, index=False, header=False)


def make_json(datas):
    global json_data
    dict = {
            'Product review' :        datas[1], # pr_avg_rev,
            'Selling price' :         datas[2], # pr_price_selling,
            'Original price' :        datas[3], # pr_price_original
            'Product Description' :   datas[4], # pr_disc
            'Product specification' : datas[5].replace('\n', ' '), # pr_Spec
            'Product url' :           datas[6], # pr_url
            'Image links' :           datas[7], # links
            }
    json_data_temp.update({datas[0]: dict})


def product_spider(product_url):
    global SlNo
    product_names = []
    product_price_original = []
    product_price_selling = []
    product_disc = []
    product_Spec = []
    product_avg_rev = []
    product_image_links = []
    product_urls = []
    links = []
    get_product_page = requests.get(product_url)
    product_page_soup = BeautifulSoup(get_product_page.text, 'html.parser')

    # product name
    if type(product_page_soup.find('span', {'class':'_35KyD6'})) != type(None):
        pr_names = str(str(SlNo)+'. ' + product_page_soup.find('span', {'class':'_35KyD6'}).text).replace(',', '')
    else:
        pr_names = 'Not available try again'
    SlNo += 1
    print(pr_names)

    # user reviews and rating
    if type(product_page_soup.find('div', {'class':'_1i0wk8'})) != type(None):
        pr_avg_rev = str(product_page_soup.find('div', {'class':'_1i0wk8'}).text) +' stars from '+ str(product_page_soup.find('div', {'class':'row _2yc1Qo'}).text).replace('&', '').replace(',', '')
    else:
        pr_avg_rev = 'Not available try again'
    # print(pr_avg_rev)

    # product selling price
    if type(product_page_soup.find('div', {'class':'_1vC4OE _3qQ9m1'})) != type(None):
        pr_price_selling = str(product_page_soup.find('div', {'class':'_1vC4OE _3qQ9m1'}).text).replace('₹', 'Rs ')
    else:
        pr_price_selling = 'Not available try again'
    # print(pr_price_selling)

    # product original price
    if type(product_page_soup.find('div', {'class':'_3auQ3N _1POkHg'})) != type(None):
        pr_price_original = str(product_page_soup.find('div', {'class':'_3auQ3N _1POkHg'}).text).replace('₹', 'Rs ')
    else:
        pr_price_original = 'Not available try again'
    # print(pr_price_original)

    # Product Description
    if type(product_page_soup.find('div', {'class':'_1y9a40'})) != type(None):
        pr_disc =str(product_page_soup.find('div', {'class':'_1y9a40'}).text).replace(',', ' ').replace('Read More', '').replace('Description', '').replace('NA', 'No discription available').replace('\n', '')
    else:
        pr_disc = 'Not available try again'
    # print(pr_disc)

    # specifications with the main heading
    data = product_page_soup.findAll('table', {'class': '_3ENrHu'})
    prdisc = {}
    pr_Spec = ''
    for tbody in data:
        prdisc[str(tbody.find(class_ = '_3-wDH3 col col-3-12').text)] = str(tbody.find(class_ = '_3YhLQA').text)
    for key, val in prdisc.items():
        pr_Spec = pr_Spec+key+': '+val+'\n'
    # print(pr_Spec)

    # product URL
    pr_url = product_url
    # print(pr_url)

    # product display images
    data = product_page_soup.findAll('div', {'class':'_2_AcLJ'})
    for div in data:
        link = div['style'].replace('background-image:url(','').replace('?q=','')
        links.append(str(link)[:-3])
    # print(links)

    # call to make csv file
    if output_files == 1:
        make_csv([pr_names,
              pr_avg_rev,
              pr_price_selling,
              pr_price_original,
              pr_disc,
              pr_Spec,
              pr_url,
              [links]])

    # call to make json file
    elif output_files == 2:
        make_json([pr_names,
              pr_avg_rev,
              pr_price_selling,
              pr_price_original,
              pr_disc,
              pr_Spec,
              pr_url,
              [links]])
    else:
        make_csv([pr_names,
              pr_avg_rev,
              pr_price_selling,
              pr_price_original,
              pr_disc,
              pr_Spec,
              pr_url,
              [links]])
        make_json([pr_names,
              pr_avg_rev,
              pr_price_selling,
              pr_price_original,
              pr_disc,
              pr_Spec,
              pr_url,
              [links]])



def page_spider():
    page = 1
    global json_data_temp, json_data
    i = 0
    while(True):
        print('\n<-------- crowling page', page, '-------->\n')
        get_flipkart_page = requests.get(url+str(page))
        flipkart_soup = BeautifulSoup(get_flipkart_page.text, 'html.parser')
        data = flipkart_soup.findAll('div', {'class': '_3O0U0u'})
        if data != []: #last page's data will be empty, by this we dont need to worry about pagination
            for div in data:
                links = div.findAll('a')
                for a in links:
                    product_spider(flipkart+a['href'])

        #these three line adds page number in json file
        json_data['page :'+str(page)] = ''
        json_data['page :'+str(page)] = json_data_temp
        json_data_temp = {}

        page += 1


if __name__ == '__main__':
    try:
        page_spider()
        # generating json file
        if output_files >= 2:
            with open('data.json', 'w', encoding="utf-8") as jsonfile:
                json.dump(json_data, jsonfile, indent=2)
    except KeyboardInterrupt:
        print("\nGood Bye..!")
    except requests.exceptions.MissingSchema: 
        print("\nError: Check URL again..!")
    except:
        print('some error occurred, try again..')