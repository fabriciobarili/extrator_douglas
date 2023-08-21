import time
from builtins import len
from typing import Dict

from bs4 import BeautifulSoup
from scrapfly import ScrapeConfig, ScrapflyClient

import funcoes_douglas


async def getListaNoticias(termo: str, client: ScrapflyClient, economia: str, **BASE: any) -> Dict:

    if economia == "S":
        print(f"Iniciando a pesquisa no site Folhamax pelo termo {termo} com economia de API")
    elif economia == "N":
        print(f"Iniciando a pesquisa no site Folhamax pelo termo {termo} sem economia de API")

    # A partir do termo, descobrimos quantas páginas existem
    URL = f"https://www.folhamax.com/busca.php?pageNum_Busca=1&keyword=+{termo}+"
    PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
    soup = BeautifulSoup(PAGINA.content, "lxml")

    btn_paginas = soup.findAll("button", attrs={"class": "btn btn-outline-danger mr10"})
    de_total = str(btn_paginas[0].text).split(" de ")
    if economia != "S":
        paginas = int(de_total[1])
    else:
        paginas = int(int(de_total[1]) / 4)

    print(f'Total de páginas para esta busca: {paginas}')

    # Cria uma lista com todas as páginas
    array_paginas = []
    for i in range(paginas):
        array_paginas.append(i)

    for j in array_paginas:

        URL = f"https://www.folhamax.com/busca.php?pageNum_Busca={j}&keyword=+Lula+"
        print(URL)
        PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE))
        soup = BeautifulSoup(PAGINA.content, "lxml")

        divs = soup.findAll("div", attrs={"class": "linespacing PaginacaoIndex"})
        URLS = []
        for d in divs:

            titulo = d.findAll("a", attrs={"class": "text-dark text-uppercase h5 m-0 py-3"})
            data = d.findAll("span", attrs={"class": "text-danger small"})
            urls = d.findAll("a", attrs={"class": "black"},
                             href=True)  # aqui pega todas as URL's. A cada 3, 1 é diferente.

            tamanho = int(len(titulo))
            print(tamanho)
            for t in range(tamanho):
                print(f"Título: {titulo[t].text} \n"
                      f"Data: {data[t].text} \n"
                      f"URL: https://www.folhamax.com/{urls[t]['href']} \n")
                funcoes_douglas.insert_noticia_pt1(titulo[t].text, f"https://www.folhamax.com/{urls[t]['href']}",
                                                   data[t].text)

        print(f"Fim da página {j}/{paginas}")

    return "sucesso"


async def getConteudo(client: ScrapflyClient, **BASE: any) -> Dict:
    noticias = funcoes_douglas.getNoticiasFolhamax()
    for n in noticias:
        PAGINA = await client.async_scrape(ScrapeConfig(n[0], **BASE))
        print(n[0])
        soup = BeautifulSoup(PAGINA.content, "lxml")
        CONTEUDO = soup.findAll("div", attrs={"id": "text-content"})
        IMAGENS = soup.findAll("img", attrs={"class": "img-content"})
        for C in CONTEUDO:
            print(C.text)
            funcoes_douglas.insert_noticia(n[1], C.text)

        for I in IMAGENS:
            print(I['src'])
            if "storage/webdisco" in I['src']:
                funcoes_douglas.insert_imagens(n[1], {I['src']})
        time.sleep(1)

    return "Sucesso"
