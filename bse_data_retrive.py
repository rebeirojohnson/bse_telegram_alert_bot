import json
import requests
import datetime
import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36",
    "accept":"application/json",
    "accept-encoding":"gzip, deflate, zstd",
    "accept-language":"en-US,en;q=0.9",
    "dnt":"1",
    "origin":"https://www.bseindia.com",
    "priority":"u=1, i",
    "referer":"https://www.bseindia.com/",
    "sec-ch-ua":"'Google Chrome';v='129', 'Not=A?Brand';v='8', 'Chromium';v='129'",
    "sec-ch-ua-mobile":"?1",
    "sec-ch-ua-platform":"Android",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-site"
}

order_url = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"


LAST_NEWS_ID = ""

def get_latest_orders_for_company():

    todays_date = datetime.datetime.now().strftime("%Y%m%d")

    query_param = {
        "pageno": "1",
        "strCat": "Company Update",
        "strPrevDate": todays_date,
        "strScrip": "",
        "strSearch": "P",
        "strToDate": todays_date,
        "strType": "C",
        "subcategory": "Award of Order / Receipt of Order",
    }
    response = requests.get(url=order_url,headers=headers,params=query_param)

    try:
        list_of_stocks = response.json()
        
        latest_update = list_of_stocks['Table'][0]

        news_id = latest_update['NEWSID']

        company_name = latest_update['SLONGNAME']

        stock_url = latest_update['NSURL']

        stock_id = latest_update['SCRIP_CD']

        data_to_return = {
            "news_id":news_id,
            "company_name":company_name,
            "stock_url":stock_url,
            "stock_id":stock_id
        }

        return data_to_return
    
    except:
        print(response.headers)

        response = response.content

def get_stock_data_by_id(stock_id):

    stock_nse_url = f"https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?Debtflag=&scripcode={stock_id}&seriesid="

    response = requests.get(url=stock_nse_url,headers=headers)

    response = response.json()

    current_price = response['CurrRate']['LTP']

    todays_price_change = response['CurrRate']['Chg']

    todays_price_change_percent = response['CurrRate']['PcChg']

    today_open_price = response['Header']['Open']

    today_high_price = response['Header']['High']

    today_low_price = response['Header']['Low']

    data_to_return = {
        "current_price":current_price,
        "todays_price_change":todays_price_change,
        "todays_price_change_percent":todays_price_change_percent,
        "today_open_price":today_open_price,
        "today_high_price":today_high_price,
        "today_low_price":today_low_price    
    }


    with open('stock_data.json', 'w') as f:
        f.write(json.dumps(response, indent=4))

    return data_to_return


if __name__ == "__main__":

    last_news_id = ""

    while True:

        data = get_latest_orders_for_company()
        
        latest_news_id = data['news_id']

        if latest_news_id != last_news_id:

            last_news_id = latest_news_id

            print(json.dumps(data, indent=4))

            stock_data = get_stock_data_by_id(data['stock_id'])

            print(json.dumps(stock_data, indent=4))
        else:
            print("No new Updates")
            
        time.sleep(2)