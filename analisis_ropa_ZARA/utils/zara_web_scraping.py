# %%
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
def get_it_list(url):
    web = requests.get(
        url = url,
        headers = headers
    )
    soup = BeautifulSoup(web.text,features="lxml")
    lista = [etiqueta.get('href') for etiqueta in soup.find_all('a',class_='product-link product-grid-product__link link')]
    lista = set(lista)
    semana = soup.find('html').get('id')
    return lista, semana
    

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
    url = get_url(url)
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
        'semana':semana,
        'tallas':tallas,
        'colores':colores,
        'enlace':list(enlaces),
        'marca':'ZARA'
    })
    df['grupo'] = df['articulo'].str.extract(r'(\w+)\s',expand=False)
    return df

# %%
urls = [
    'https://www.zara.com/es/es/mujer-nuevo-l1180.html?v1=2352540',
    # 'https://www.zara.com/es/es/hombre-nuevo-en-coleccion-l6164.html?v1=2351219',
    # 'https://www.zara.com/es/es/hombre-lino-l708.html?v1=2351649',
    # 'https://www.zara.com/es/es/hombre-camisas-l737.html?v1=2351464',
    # 'https://www.zara.com/es/es/hombre-camisetas-l855.html?v1=2351543',
    # 'https://www.zara.com/es/es/hombre-polos-l733.html?v1=2351616',
    # 'https://www.zara.com/es/es/hombre-pantalones-l838.html?v1=2351278',
    # 'https://www.zara.com/es/es/hombre-jeans-l659.html?v1=2351397',
    # 'https://www.zara.com/es/es/hombre-bermudas-l592.html?v1=2351786',
    # 'https://www.zara.com/es/es/hombre-traje-l808.html?v1=2351572',
    # 'https://www.zara.com/es/es/hombre-beachwear-l590.html?v1=2378240',
    # 'https://www.zara.com/es/es/man-crochet-l6272.html?v1=2351800',
    # 'https://www.zara.com/es/es/hombre-prendas-exterior-l715.html?v1=2378740',
    # 'https://www.zara.com/es/es/hombre-sudaderas-l821.html?v1=2351429',
    # 'https://www.zara.com/es/es/hombre-punto-l681.html?v1=2351499',
    # 'https://www.zara.com/es/es/hombre-sobrecamisas-l3174.html?v1=2351642',
    # 'https://www.zara.com/es/es/hombre-blazers-l608.html?v1=2351609',
    # 'https://www.zara.com/es/es/man-total-look-l5490.html?v1=2351762',
    # 'https://www.zara.com/es/es/hombre-pantalones-cargo-l1780.html?v1=2351761',
    # 'https://www.zara.com/es/es/hombre-zapatos-zapatillas-l797.html?v1=2389259',
    # 'https://www.zara.com/es/es/hombre-bolsos-l563.html?v1=2352310',
    # 'https://www.zara.com/es/es/hombre-accesorios-l537.html?v1=2352367',
    # 'https://www.zara.com/es/es/woman-party-l4824.html?v1=2352607',
    # 'https://www.zara.com/es/es/mujer-blazers-l1055.html?v1=2352684',
    # 'https://www.zara.com/es/es/mujer-vestidos-l1066.html?v1=2352823',
    # 'https://www.zara.com/es/es/mujer-tops-l1322.html?v1=2353011',
    # 'https://www.zara.com/es/es/mujer-prendas-exterior-chalecos-l1204.html?v1=2352738',
    # 'https://www.zara.com/es/es/mujer-faldas-l1299.html?v1=2353253',
    # 'https://www.zara.com/es/es/mujer-pantalones-shorts-l1355.html?v1=2353279',
    # 'https://www.zara.com/es/es/mujer-punto-l1152.html?v1=2353051',
    # 'https://www.zara.com/es/es/mujer-zapatos-l1251.html?v1=2353418',
    # 'https://www.zara.com/es/es/mujer-bolsos-l1024.html?v1=2353495',
    # 'https://www.zara.com/es/es/mujer-conjuntos-l1061.html?v1=2353302',
    # 'https://www.zara.com/es/es/mujer-chaquetas-l1114.html?v1=2352724',
    # 'https://www.zara.com/es/es/mujer-punto-l1152.html?v1=2352849',
    # 'https://www.zara.com/es/es/mujer-beachwear-l1052.html?v1=2353512',
    # 'https://www.zara.com/es/es/mujer-accesorios-l1003.html?v1=2353548',
    # 'https://www.zara.com/es/es/mujer-ropa-interior-l4021.html?v1=2353568',
    # 'https://www.zara.com/es/es/woman-linen-l2447.html?v1=2354108'
]

# %%
dfs = []
for url in urls:
    print(f'Procesando: {url[:40]}...')
    dfs.append(generar_df(url))

# %%
df = pd.concat(dfs,ignore_index=True)

# %%
df.dropna(inplace=True)

# %%
df['seccion'] = df['semana'].str.split('-',expand=True)[1]

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

