import configparser
import openpyxl

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

def SaveBestSellerList(asins_l, category, domain, date):
    wb = openpyxl.Workbook()
    ws = wb.active
    dom = ''
    if domain == 1:
        dom = 'USA'
    elif domain == 6:
        dom = 'CANADA'
    ws.title = f'BestSeller_ASINS_{dom}_{category}'
    ws.append(['ASINS'])
    for key,value in enumerate(asins_l, start=2):
        ws.cell(row=key, column=1, value=value)
        # ws.append(value)
    wb.save(f'BestSeller_{dom}_{date}.xlsx')   


if __name__ == '__main__':
    pass