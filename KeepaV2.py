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
if (mode == 0) or (mode == 3) :
    categoria = config['bestSeller']['categoria']
    year = config['bestSeller']['year']
    month = config['bestSeller']['month']
elif mode == 1 :
    pass
elif (mode == 2) or (mode == 4) :
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
    if (mode == 0):
        wb_ = KUtils.generarExcel(categoria,dominio,f"{year}-{month}")
        asins_list = KUtils.BestSellers(dominio, categoria, month, year)  #Canada 6205517011
        # asins_list = ['B00002EQAF']
    # ArchivoExcel
    elif (mode == 2):
        wb_ = KUtils.generarExcel('',dominio,'')
        asins_list = KUtils.import_excel(file_path)
    elif mode == 3:
        wb_ = KUtils.generarExcel(categoria,'1',f"{year}-{month}")
        wb_CA = KUtils.generarExcel(categoria,'6',f"{year}-{month}")
        asins_list = KUtils.BestSellers(dominio, categoria, month, year)  #Canada 6205517011
    elif (mode == 4):
        wb_ = KUtils.generarExcel('','1','')
        wb_CA = KUtils.generarExcel('','6','')
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
            if (mode == 3) or (mode == 4):
                productos  = asyncio.run(GetProducts(batch, 'US', buybox_, 365))
                productos_ca  = asyncio.run(GetProducts(batch, 'CA', buybox_, 365))
            else:
                productos  = asyncio.run(GetProducts(batch, dom, buybox_, 365))
            
            if mode == 0:
                products_dict, prod_new_dia, prod_amazon_dia, prod_bb_dia = KUtils.process_products(productos,month=int(month), year=int(year)) 
            elif mode == 2: 
                products_dict, prod_new_dia, prod_amazon_dia, prod_bb_dia = KUtils.process_products(productos)
            elif mode == 3:
                products_dict, prod_new_dia, prod_amazon_dia, prod_bb_dia = KUtils.process_products(productos,month=int(month), year=int(year)) 
                products_dict_ca, prod_new_dia_ca, prod_amazon_dia_ca, prod_bb_dia_ca = KUtils.process_products(productos_ca,month=int(month), year=int(year)) 
            elif mode == 4:
                products_dict, prod_new_dia, prod_amazon_dia, prod_bb_dia = KUtils.process_products(productos)
                products_dict_ca, prod_new_dia_ca, prod_amazon_dia_ca, prod_bb_dia_ca = KUtils.process_products(productos_ca)

            KUtils.agregarProductosExcel(wb_, products_dict, prod_new_dia, prod_amazon_dia, prod_bb_dia)
            if (mode == 3) or (mode ==4):
                KUtils.agregarProductosExcel(wb_CA, products_dict_ca, prod_new_dia_ca, prod_amazon_dia_ca, prod_bb_dia_ca)

            procesados += batch_size 
            print(f"Guardando Productos...{procesados}/{total}")

    except Exception as e:
        traceback.print_exc()
    finally:
        fname = ''
        if mode == 0:
            fname = f'BestSeller{month}-{year}'
        elif mode == 2:
            fname = f'Asins'
        elif mode == 3:
            fname = f'BestSeller_US_{month}-{year}'
            fname_ca = f'BestSeller_CA_{month}-{year}'
        elif mode == 4:
            fname = f'Asins_US'
            fname_ca = f'Asins_CA'

        KUtils.guardarExcel(wb_, fname)
        if (mode == 3) or (mode == 4):
            KUtils.guardarExcel(wb_CA, fname_ca)
            
        print(f'Finalizando...')
        hora_fin = datetime.now()
        duracion = (hora_fin - hora_inicio).total_seconds()
        print(f"Hora de inicio: {hora_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Hora de finalización: {hora_fin.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duración: {duracion} segundos ({duracion / 60} minutos)")