import time
from builtins import len
from typing import Dict

from bs4 import BeautifulSoup
from scrapfly import ScrapeConfig, ScrapflyClient

import funcoes_douglas


async def getListaNoticias(termo: str, client: ScrapflyClient, economia: str, **BASE: any) -> Dict:

    if economia == "S":
        print(f"Iniciando a pesquisa no site Folha de SP pelo termo {termo} com economia de API")
    elif economia == "N":
        print(f"Iniciando a pesquisa no site Folha de SP pelo termo {termo} sem economia de API")

    # A partir do termo, descobrimos quantas páginas existem
    URL = f"https://search.folha.uol.com.br/search?q=+{termo}+&periodo=todos&sd=&ed=&site=todos"
    PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
    soup = BeautifulSoup(PAGINA.content, "lxml")
    print (URL)
    btn_paginas = soup.findAll("div", attrs={"class": "col col--1-1 col--md-1-2 col--lg-1-2 c-search__result"})
    de_total = str(btn_paginas[0].text).split(" ")
    if economia != "S":
        paginas = int(de_total[36])
    else:
        paginas = int(int(de_total[36]) / 4)

    print(f'Total de páginas para esta busca: {paginas}')

    # Cria uma lista com todas as páginas
    array_paginas = []
    for i in range(paginas):
        array_paginas.append(i)

    for j in array_paginas:

        URL = f"https://search.folha.uol.com.br/search?q=+{termo}+&periodo=todos&sd=&ed=&site=todos&sr={j * 25 + 1}"
        print(URL)
        PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE))
        soup = BeautifulSoup(PAGINA.content, "lxml")

        divs = soup.findAll("ol", attrs={"class": "u-list-unstyled c-search"})
        URLS = []
        for d in divs:

            titulo = d.findAll("h2", attrs={"class": "c-headline__title"})
            data = d.findAll("time", attrs={"class": "c-headline__dateline"})
            url = d.findAll("div", attrs={"class": "c-headline__content"})  # aqui pega todas as URL's. A cada 3, 1 é diferente.

            urls = []
            for u in url:
                valor = u.contents[1]['href']
                urls.append(valor)

            tamanho = int(len(titulo))
            print(tamanho)
            for t in range(tamanho):
                print(f"Título: {titulo[t].text.strip()} \n"
                      f"Data: {data[t].text.strip()} \n"
                      f"URL: {urls[t].strip()} \n")
                funcoes_douglas.insert_noticia_pt1(titulo[t].text.strip(), f"{urls[t].strip()}",
                                                   data[t].text.strip())

        print(f"Fim da página {j}/{paginas}")

    return "sucesso"


async def getConteudo(client: ScrapflyClient, **BASE: any) -> Dict:
    # Agora que os resultados estão armazenados, hora de pegar o conteúdo deles.
    # Inicialmente eu pego todas as notícias que tenho só a primeira parte dela, sem o conteúdo
    noticias = funcoes_douglas.getNoticias()

    for n in noticias:
        #Para tirar o Paywall, usei o serviço Leiaisso.net, passando a URL da notícia como parâmetro. Aí eu só extraio o conteúdo da div class=Wrap
        PAGINA = await client.async_scrape(ScrapeConfig("https://leiaisso.net/"+n[0], **BASE))

        soup = BeautifulSoup(PAGINA.content, "lxml")
        #print(f"https://leiaisso.net/{n[0]}")

        CONTEUDO = soup.findAll("div", attrs={"content"})
        IMAGENS = soup.findAll("img", attrs={"class": "img-responsive c-lazyload c-image-aspect-ratio__image"})

        for C in CONTEUDO:
            print(C.text)
            funcoes_douglas.insert_noticia(n[1], C.text)

        for I in IMAGENS:
            print(I['src'])
            funcoes_douglas.insert_imagens(n[1], I['src'])
        time.sleep(1)

    return "Sucesso"
