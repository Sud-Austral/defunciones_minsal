import pandas as pd
import http.client
import zipfile
import time
import requests
import os
import datetime

def getZIP():
    log = df.read_excel("log_descarga.xlsx")
    fechaActual = datetime.datetime.now().strftime("%d%m%Y")
    # Definir los parámetros de la solicitud
    host = "repositoriodeis.minsal.cl"
    path = f"/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_2021_2024_{fechaActual}.zip"
    #path = f"/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_2021_2024_12032024.zip"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    # Configurar el tiempo de espera
    timeout = 10000  # Tiempo de espera en segundos
    # Realizar la solicitud GET con timeout
    proxy_host = '45.225.207.186'
    proxy_port = 999  # Reemplazar con el puerto de tu proxy
    proxy = {
        'http': f'http://{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_host}:{proxy_port}'
    }
    flag = True
    for _ in range(30):
        try:
            # Realizar la solicitud GET con timeout
            response = requests.get(f"https://{host}{path}", headers=headers, timeout=timeout, proxies=proxy)

            # Verificar el código de estado de la respuesta
            if response.status_code == 200:
                with open("descarga.zip", "wb") as f:
                    f.write(response.content)
                log.loc[len(log)] = {"fecha":datetime.datetime.now(),"descarga":"Descargado"}
                flag = False
                print("Archivo descargado exitosamente.")
                break  # Si la descarga es exitosa, sal del bucle
            else:
                print("Error al descargar el archivo:", response.status_code)

        except requests.Timeout:
            print("Se ha agotado el tiempo de espera durante la solicitud.")

        except requests.RequestException as e:
            print("Error durante la solicitud:", e)

    if flag:
        log.loc[len(log)] = {"fecha":datetime.datetime.now(),"descarga":"No Descargado"}
    return fechaActual


        
def descomprimir():
    # Ruta del archivo ZIP
    archivo_zip = "descarga.zip"
    # Abre el archivo ZIP en modo lectura
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        # Lista los contenidos del archivo ZIP
        contenidos = zip_ref.namelist()
        # Extrae todos los archivos del ZIP en la carpeta actual
        zip_ref.extractall()
        return contenidos

if __name__ == '__main__':
    
    fechaActual = getZIP()
    contenidos = descomprimir()
    df = pd.read_csv(f"DEFUNCIONES_FUENTE_DEIS_2021_2024_{fechaActual}.csv", encoding='latin-1',sep=";", header=None)
    df.columns = ['Año', 'Fecha', 'Sexo', 'Frecuencia', 'Edad', 'Codcom', 'Comuna',
       'Región', 'ID_DP', 'ID_Nivel 1', 'Nivel 1', 'ID_Nivel 2', 'Nivel 2',
       'ID_Nivel 3', ' Diagnóstico Principal', 'ID_DP1',
       ' Diagnóstico Principal INT', 'ID_OTRO', 'ID_CEXT (S-N)',
       'Causas externas (S-N)', 'ID_CEXTGRAL', 'Causas externas Gral',
       'ID_CEXTDETALLE', 'Causas externas de morbilidad y de mortalidad',
       'ID_CEXTDETALLEint',
       'Causas externas de morbilidad y de mortalidad INT', 'Lugar']
    for file in contenidos:
        print(file)
        if os.path.exists(file):
            # Borra el archivo
            os.remove(file)
            print(f"El archivo '{file}' ha sido borrado exitosamente.")
        else:
            print(f"El archivo '{file}' no existe.")
    df = df[df["Año"] == 2024]
    df.to_excel("difuntos.xlsx",index=False)