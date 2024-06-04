import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# %%
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }
def get_url(url):

    web_scrap = requests.get(url,
            headers=headers).text
    web_scrap
    soup = BeautifulSoup(web_scrap,features="lxml")
    etiqueta = soup.find('meta', attrs={'http-equiv': 'refresh'})
    url = etiqueta.get('content').split(';')[1]
    return 'https://www.zara.com' + url[6:-1]

# %%
def get_it_list(url_):
    pagina = 1
    url = f'{url_}&page={pagina}'
    url = get_url(url)
    web = requests.get(
        url = url,
        headers = headers
    )
    soup = BeautifulSoup(web.text,features="lxml")
    semana = soup.find('html').get('id')
    lista = []
    l = [etiqueta.get('href') for etiqueta in soup.find_all('a',class_='product-link product-grid-product__link link')]
    while len(l) > 0:
        print('.',end='',flush=True)
        lista.extend(l)
        pagina += 1
        url = f'{url_}&page={pagina}'
        url = get_url(url)
        web = requests.get(
            url = url,
            headers = headers
        )
        soup = BeautifulSoup(web.text,features="lxml")
        l = [etiqueta.get('href') for etiqueta in soup.find_all('a',class_='product-link product-grid-product__link link')]
    lista = set(lista)
    print('')
    return list(lista), semana
    

# %%
def get_info(url):
    url = get_url(url)
    web_item = requests.get(
        url,
        headers = headers
    ).text
    soup = BeautifulSoup(web_item,features="lxml")
    articulo = soup.find('h1',class_='product-detail-info__header-name').text
    precio = soup.find('span',class_='money-amount__main').text
    descripcion = soup.find('p').text
    tallas = [etiqueta.text for etiqueta in soup.find_all('div',class_='product-size-info__main-label')]
    lista_colores = soup.find('ul',class_='product-detail-color-selector__colors')
    if lista_colores:
        colores = [etiqueta.text for etiqueta in lista_colores.find_all('span',class_='screen-reader-text')]
    else:
        colores = []
    return articulo, precio, descripcion, tallas, colores

# %%
def generar_df(url):
    enlaces, semana = get_it_list(url)
    articulos, precios, descripciones, tallas, colores = [], [], [], [], []
    for enlace in enlaces:
        print(f'\tProcesando: {enlace[:40]}...')
        try:
            articulo, precio, descripcion, talla, color = get_info(enlace)
            articulos.append(articulo)
            precios.append(precio)
            descripciones.append(descripcion)
            tallas.append(talla)
            colores.append(color)
        except:
            articulos.append(pd.NA)
            precios.append(pd.NA)
            descripciones.append(pd.NA)
            tallas.append(pd.NA)
            colores.append(pd.NA)
    df = pd.DataFrame({
        'extracción':pd.Timestamp('today'),
        'articulo':articulos,
        'precio':precios,
        'descripcion':descripciones,
        'grupo_web':semana,
        'tallas':tallas,
        'colores':colores,
        'enlace':list(enlaces),
        'marca':'ZARA'
    })
    df['grupo'] = df['articulo'].str.extract(r'(\w+)\s',expand=False)
    return df

# %%
urls = [
    'https://www.zara.com/es/es/mujer-nuevo-l1180.html?v1=2352540&regionGroupId=105',
    'https://www.zara.com/es/es/hombre-nuevo-en-coleccion-l6164.html?v1=2351219&regionGroupId=105'
]

# %%
dfs = []
for url in urls:
    print(f'Procesando: {url[:40]}...',end='',flush=True)
    dfs.append(generar_df(url))

# %%
df = pd.concat(dfs,ignore_index=True)

# %%
df.dropna(inplace=True)

# %%
df['seccion'] = df['grupo_web'].str.split('-',expand=True)[1]

# %%
df['precio'] = (
    df
    ['precio']
    .str.extract(r'(\d+\,\d+)',expand=False)
    .str.replace(',','.')
    .astype(float)
)

# %%
df.drop_duplicates(subset=['descripcion','enlace'],inplace=True)

# %%
df.to_csv('../data/ZARA_db.csv',index=False)
print(f'\nSE HAN RESGISTRADO {len(df)} PRENDAS DIFERENTES')

