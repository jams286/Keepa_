import openpyxl.workbook
import requests
import configparser
import openpyxl
import csv
json_keys =  [
    "asin", "domainId", "imagesCSV", "title", "monthlySold", "csv.[1].[1]", "csv.[0].[1]",
    "fbafees.pickAndPackFee", "packageWeight", "referralFeePercent", "hazardousMaterials",
    "csv.[11].[1]", "csv.[10].[1]", "manufacturer", "brand"
]

def getConfig()->configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        # url_base = config['keepa']['url']
        # api_key = config['keepa']['api_key']
        # domain = config['keepa']['domain']
        # asin = 'B0CFV4WLY6'
    except Exception as e:
        print(e)
        return None
    else:
        return config
    
def saveConfig(config:configparser.ConfigParser)->bool:    
    try:
        with open('config.ini','w') as configFile:
            config.write(configFile)
    except Exception as e:
        print(e)
        return False
    else:
        return True
    
def load_excel_data(filename)-> openpyxl.workbook:
    try:
        # Cargar el archivo Excel
        wb = openpyxl.load_workbook(filename)       
    except Exception as e:
        print(f"Error al cargar el archivo Excel: {e}")
    else:
        return wb
    
def load_csv_data(filename)-> openpyxl.workbook:
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        with open(filename) as f:
            reader = csv.reader(f, delimiter=',')
            for row_index, row in enumerate(reader, start=1):
                for column_index, cell_value in enumerate(row, start=1):
                    ws.cell(row=row_index, column=column_index).value=cell_value    
                       
    except Exception as e:
        print(f"Error al cargar el archivo csv: {e}")
    else:
        return wb

def RequestProducts(asin_list:list)->dict:      
    # columnas_excel =  [
    #                 "asin", "domainId", "imagesCSV", "title", "monthlySold", "csv.[1].[1]", "csv.[0].[1]",
    #                 "fbafees.pickAndPackFee", "packageWeight", "referralFeePercent", "hazardousMaterials",
    #                 "csv.[11].[1]", "csv.[10].[1]", "manufacturer", "brand"
    #              ]
    config = getConfig()    
    url_base = config['keepa']['url']
    api_key = config['keepa']['api_key']
    asins = ','.join(asin_list)  
    url = f"{url_base}/product?key={api_key}&domain=1&days={365}&asin={asins}"
    payload = {}
    headers = {}
    asins_response = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()
        
        for product in response_json['products']:
            new_current = 0
            amazon_current = 0
            new_offer_count_current = 0
            lowest_fba_seller = 0
            asin = product['asin']
            domainId = product['domainId']            
            imagesCSV = product['imagesCSV']
            title = product['title']
            monthlySold = product['monthlySold']
            if product['csv'][1] is not None:
                new_current = product['csv'][1][1]/100
            if product['csv'][0] is not None:
                amazon_current = product['csv'][0][1]/100
            fbafees = product['fbaFees']['pickAndPackFee']/100
            packageWeight = product['packageWeight']/453.59290944
            referralFeePercent = product['referralFeePercent']
            csv_values = product.get('csv',[])
            for index, value in enumerate(csv_values):
                if value is not None:
                    print('')
                else:
                    print('')
            hazardousMaterials = ''
            if 'hazardousMaterials' in product:
                hazardousMaterials_list = product['hazardousMaterials']
                aspect_dict = {}            
                for hazard in hazardousMaterials_list:
                    aspect = hazard['aspect']
                    value = hazard['value']
                    if aspect in aspect_dict:
                        aspect_dict[aspect].append(value)
                    else:
                        aspect_dict[aspect] = [value]
                
                hazardousMaterials = '; '.join([f"{aspect}: {','.join(values)}" for aspect, values in aspect_dict.items()])            
            if product['csv'][11] is not None:
                new_offer_count_current = product['csv'][11][1]/100 
            if product['csv'][10] is not None:
                lowest_fba_seller = product['csv'][10][1]/100
            manufacturer = product['manufacturer']
            brand = product['brand']
            values = [asin,domainId, imagesCSV, title, monthlySold, new_current, amazon_current, fbafees, packageWeight, referralFeePercent, hazardousMaterials,
                      new_offer_count_current, lowest_fba_seller, manufacturer, brand]
            asins_response[asin] = values
    else:
        print(f"Error: {response.status_code}")
    return asins_response

if __name__ == '__main__':
    pass
    # from datetime import datetime
    # import time
    # a = 21564000
    # b = 60
    # c = 7107952
    # ts = (c+a)*b
    # # ts = 1720335619.1508439
    # print(datetime.fromtimestamp(ts))
