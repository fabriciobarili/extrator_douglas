import time
from builtins import len
from typing import Dict

from bs4 import BeautifulSoup
from scrapfly import ScrapeConfig, ScrapflyClient

import funcoes_douglas


async def getListaNoticias(termo: str, client: ScrapflyClient, economia: str, **BASE: any) -> Dict:

    if economia == "S":
        print(f"Iniciando a pesquisa no site O Globo pelo termo {termo} com economia de API")
    elif economia == "N":
        print(f"Iniciando a pesquisa no site O Globo pelo termo {termo} sem economia de API")

    # A partir do termo, descobrimos quantas páginas existem
    URL = f"https://oglobo.globo.com/busca/?q=+{termo}+"
    PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
    soup = BeautifulSoup(PAGINA.content, "lxml")

    #O site O GLOBO permite até 40 páginas
    array_paginas = []
    for i in range(39):
        array_paginas.append(i+1)

    # Inínio do Loop
    for j in array_paginas:
        #No site OGLobo, eles retiram o ++ do termo. Aí é saber se deseja o termo lula ou a palavra lula
        URL = f"https://oglobo.globo.com/busca/?q=+{termo}+&page={j}"
        print(f'Iniciando o Scrap pela página: {URL}')
        PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
        soup = BeautifulSoup(PAGINA.content, "lxml")

        divs = soup.findAll("ul", attrs={"class": "results__list"})
        URLS = []
        for d in divs:
            titulo = d.findAll("div", attrs={"class": "widget--info__title product-color"})
            data = "TBD"
            urls = d.findAll("div", attrs={"class": "widget--info__text-container"})  # aqui pega todas as URL's. A cada 2, 1 é diferente.

        #CONSERTAR AS URL'S##
        #só pegar as que são PAR
        k=0
        print(urls[0].contents[3]['href'])
        url_final = []

        for d in urls:
            url_vdd = d.contents[3]['href']
            if ((str(url_vdd).find("p=0")) == -1) and ((str(url_vdd).find("conteudo-de-marca") == -1)):
                url_final.append(url_vdd)
            k=k+1
        print(url_final)
        tamanho = int(len(titulo))
        # print(tamanho)
        print(titulo)
        print(data)
        for t in range(tamanho):
            #No Globo, o primeiro link
            i_url_tratada = int(url_final[t].find("u=")+2)
            f_url_tratada = url_final[t].find("&syn=")
            url_tratada = str(url_final[t][i_url_tratada:f_url_tratada])
            url_decode = url_tratada.replace("%3A", ":").replace("%2F", "/")
            print(f"Título: {titulo[t].text} \n"
                  f"Data: TBD \n"
                  f"URL: https://oglobo.globo.com/{url_decode} \n")
            funcoes_douglas.insert_noticia_pt1(titulo[t].text, f"{url_decode}",
                                               "TBD")

        print(f"Fim da página {j}/{array_paginas}")
        time.sleep(10)
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

        CONTEUDO = soup.findAll("div", attrs={"wrap"})
        IMAGENS = soup.findAll("img")
        texto = ""
        for C in CONTEUDO:
            print(C.text)
            funcoes_douglas.insert_noticia(n[1], C.text)

        for I in IMAGENS:
            print(I['src'])
            if "https://s2.glbimg.com/" in I['src']:
                funcoes_douglas.insert_imagens(n[1], I['src'])
        time.sleep(1)

    return "Sucesso"
