import keepa
import asyncio
import openpyxl 
import traceback
from datetime import datetime
import KeepaV2Utils as KUtils

# hora inicio
hora_inicio = datetime.now()

config = KUtils.getConfig()   
# url_base = config['keepa']['url']
api_key = config['keepa']['api_key']
dominio = config['keepa']['domain']    
mode = int(config['keepa']['modo'])
timeout = int(config['keepa']['timeout'])
if timeout < 10:
    timeout = 10
cantidad_maxima_productos = int(config['keepa']['cantidad_maxima_productos'])
buybox_int = int(config['keepa']['buybox'])
if buybox_int == 0:
    buybox_ = False
elif buybox_int == 1:
    buybox_ = True
else:
    buybox_ = False
if mode == 0 :
    categoria = config['bestSeller']['categoria']
    year = config['bestSeller']['year']
    month = config['bestSeller']['month']
elif mode == 1 :
    pass
elif mode == 2 :
    file_path = config['file']['ubicacion_archivo']
# api.best_sellers_query
total_token = 0
    
async def GetProducts(asins:list, domain:str, buybox:bool, days:int) :
    global total_token
    api_async = await keepa.AsyncKeepa.create(api_key, timeout=timeout)
    total_token = api_async.tokens_left
    print(f'tokens:{total_token}')
    return await api_async.query(asins, domain=domain, buybox=buybox, days=days, stats=180)
    
if __name__ == '__main__':
    print(f"Iniciando...")
    batch_size = 100
    procesados = 0
    producs = {}
    asins_list = []
    # BestSeller
    if mode == 0:
        wb_ = KUtils.generarExcel(categoria,dominio,f"{year}-{month}")
        asins_list = KUtils.BestSellers(dominio, categoria, month, year)  #Canada 6205517011
        # asins_list = ['B00002EQAF']
    # ArchivoExcel
    if mode == 2:
        wb_ = KUtils.generarExcel('',dominio,'')
        asins_list = KUtils.import_excel(file_path)
    if len(asins_list) > cantidad_maxima_productos:
        asin_max = asins_list[:cantidad_maxima_productos]
    else:
        asin_max = asins_list

    total = len(asin_max)
    try:
        for i in range(0,len(asin_max),batch_size):
            batch = asin_max[i:i+batch_size]
            if dominio == '1':
                dom = 'US'
            elif dominio == '6':
                dom = 'CA'
            productos  = asyncio.run(GetProducts(batch, dom, buybox_, 365))
            if mode == 0:
                products_dict, prod_new_dia, prod_amazon_dia = KUtils.process_products(productos,month=int(month), year=int(year)) 
            else:   
                products_dict, prod_new_dia, prod_amazon_dia = KUtils.process_products(productos)
            KUtils.agregarProductosExcel(wb_, products_dict, prod_new_dia, prod_amazon_dia)
            procesados += batch_size 
            print(f"Guardando Productos...{procesados}/{total}")

    except Exception as e:
        traceback.print_exc()
    finally:
        fname = ''
        if mode == 0:
            fname = f'BestSeller{month}-{year}'
        if mode == 2:
            fname = f'Asins'

        KUtils.guardarExcel(wb_, fname)
        print(f'Finalizando...')
        hora_fin = datetime.now()
        duracion = (hora_fin - hora_inicio).total_seconds()
        print(f"Hora de inicio: {hora_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Hora de finalización: {hora_fin.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duración: {duracion} segundos ({duracion / 60} minutos)")