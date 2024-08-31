import keepa
import asyncio
import requests
import KeepaV2Utils as KUtils

config = KUtils.getConfig()   
url_base = config['keepa']['url']
api_key = config['keepa']['api_key']    
api = keepa.Keepa(api_key)
# api.best_sellers_query

async def GetProductos(asins:list, domain:str, buybox:bool, days:int) :
    api_async = await keepa.AsyncKeepa.create(api_key)
    return await api_async.query(asins, domain=domain, buybox=buybox, days=days)
    

def BestSellers(domain:int, category:str, range:int, mont:int, year:int)->list:
    asins_l = []
    tokens_left = api.tokens_left
    while tokens_left < 50:
        api.wait_for_tokens()
        tokens_left = api.tokens_left
    print(tokens_left)  
    url = f"{url_base}/bestsellers?key={api_key}&domain={domain}&category={category}&range={range}&month={mont}&year={year}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        if 'bestSellersList' in response_json:
            if response_json['bestSellersList'] is not None:
                asins_l = response_json['bestSellersList']['asinList']
    print(len(asins_l))
    return asins_l



if __name__ == '__main__':
    pass
    #BestSellers US
    # bs_us_l = BestSellers(1, '165793011',30,11,2023)
    # #BestSellers CA
    # bs_ca_l = BestSellers(6,'165793011',30,11,2023)
    # KUtils.SaveBestSellerList(bs_us_l, '165793011',1,'2023-11')
    # KUtils.SaveBestSellerList(bs_ca_l, '165793011',6,'2023-11')

    # #BestSellers US
    # bs_us_l = BestSellers(1, '165793011',30,12,2023)
    # #BestSellers CA
    # bs_ca_l = BestSellers(6,'165793011',30,12,2023)
    # KUtils.SaveBestSellerList(bs_us_l, '165793011',1,'2023-12')
    # KUtils.SaveBestSellerList(bs_ca_l, '165793011',6,'2023-12')