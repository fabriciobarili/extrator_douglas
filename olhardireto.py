import time
from builtins import len
from typing import Dict

from bs4 import BeautifulSoup
from scrapfly import ScrapeConfig, ScrapflyClient

import funcoes_douglas


async def getListaNoticias(termo : str, client : ScrapflyClient,  economia : str, **BASE : any) -> Dict:

    #A partir do termo, descobrimos quantas páginas existem
    URL = f"https://olhardireto.com.br/busca/index.asp?busca=%20{termo}%20"
    PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
    soup = BeautifulSoup(PAGINA.content, "lxml")

    #Na página de busca, encontrei um elemento no final da página que é uma DIV da classe abaixo
    #A estrutura dela é "1 de 100" páginas. Aí eu pego esse texto, explodo por " de " e sei que a segunda parte dele contém a quantidade de páginas
    btn_paginas = soup.findAll("li", attrs={"class": "numero"})
    pg = ""
    for b in btn_paginas:
        pg = b.text

    pgs = int(pg)

    if economia != "S":
        paginas = int(pgs)
    else:
        paginas = int(pgs / 4)

    print(f'Total de páginas para esta busca: {paginas}')

    #Cria uma lista de 0 até o total de páginas, para iniciar o loop
    array_paginas = []
    for i in range(paginas):
        array_paginas.append(i)

    #Inínio do Loop
    for j in array_paginas:
        URL = f"https://olhardireto.com.br/busca/index.asp?busca=%20{termo}%20&pagina={j}"
        print(f'Iniciando o Scrap pela página: {URL}')
        PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
        soup = BeautifulSoup(PAGINA.content, "lxml")


        divs = soup.findAll("ul", attrs={"class": "lista-noticias"})
        URLS = []


        titulo = divs[0].findAll("a")
        data = divs[0].findAll("span", attrs={"class": "datahora"})
        urls = divs[0].findAll("a", href=True)  # aqui pega todas as URL's. A cada 3, 1 é diferente.

        tamanho = int(len(titulo))
        #print(tamanho)
        print(titulo)
        print(data)
        print(urls)
        for t in range(tamanho):
            print(f"Título: {titulo[t].text} \n"
                  f"Data: {data[t].text} \n"
                  f"URL: https://olhardireto.com.br/{urls[t]['href']} \n")
            funcoes_douglas.insert_noticia_pt1(titulo[t].text, f"https://olhardireto.com.br/{urls[t]['href']}",
                                               data[t].text)

        print(f"Fim da página {j}/{paginas}")

    return "sucesso"

async def getConteudo(client : ScrapflyClient, **BASE : any) -> Dict:
    #Agora que os resultados estão armazenados, hora de pegar o conteúdo deles.
    #Inicialmente eu pego todas as notícias que tenho só a primeira parte dela, sem o conteúdo
    noticias = funcoes_douglas.getNoticias()

    for n in noticias:
        PAGINA = await client.async_scrape(ScrapeConfig(n[0], **BASE))
        print(n[0])
        soup = BeautifulSoup(PAGINA.content, "lxml")
        CONTEUDO = soup.findAll("div", attrs={"class": "html texto"})
        for C in CONTEUDO:
            print(C.text)
            funcoes_douglas.insert_noticia(n[1], C.text)
        time.sleep(1)

    return "Sucesso"