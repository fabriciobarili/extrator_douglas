import time
from builtins import len
from typing import Dict

from bs4 import BeautifulSoup
from scrapfly import ScrapeConfig, ScrapflyClient

import funcoes_douglas


async def getListaNoticias(termo: str, client: ScrapflyClient, economia: str, **BASE: any) -> Dict:
    # A partir do termo, descobrimos quantas páginas existem
    URL = f"https://www.gazetadigital.com.br/busca.php?pageNum_Busca=1&keyword=+{termo}+"
    PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
    soup = BeautifulSoup(PAGINA.content, "lxml")

    # Na página de busca, encontrei um elemento no final da página que é uma DIV da classe abaixo
    # A estrutura dela é "1 de 100" páginas. Aí eu pego esse texto, explodo por " de " e sei que a segunda parte dele contém a quantidade de páginas
    btn_paginas = soup.findAll("div", attrs={"class": "btn-pesquisa btn btn-success mr8"})
    de_total = str(btn_paginas[0].text).split(" de ")
    if economia != "S":
        paginas = int(de_total[1])
    else:
        paginas = int(int(de_total[1]) / 4)

    print(f'Total de páginas para esta busca: {paginas}')

    # Cria uma lista de 0 até o total de páginas, para iniciar o loop
    array_paginas = []
    for i in range(paginas):
        array_paginas.append(i)

    # Inínio do Loop
    for j in array_paginas:
        URL = f"https://www.gazetadigital.com.br/busca.php?pageNum_Busca={j}&keyword=+{termo}"
        print(f'Iniciando o Scrap pela página: {URL}')
        PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
        soup = BeautifulSoup(PAGINA.content, "lxml")

        divs = soup.findAll("div", attrs={"class": "linespacing PaginacaoIndex"})
        URLS = []
        for d in divs:

            titulo = d.findAll("p", attrs={"class": "listagem-com-foto-title-con"})
            data = d.findAll("p", attrs={"class": "listagem-com-foto-dat"})
            urls = d.findAll("a", href=True)  # aqui pega todas as URL's. A cada 3, 1 é diferente.
            # então, faço um Loop de 3 em 3 pra montar um array de URL
            urls_unicas = []

            multiplos = []
            mult = 0
            for m in range(len(titulo)):
                multiplos.append(mult)
                mult = mult + 3

            # A cada 3 links, 1 é diferente. Então, pego o múltiplos de 3 pq essas serão as posições dos arrays
            for mul in multiplos:
                urls_unicas.append(f"https://www.gazetadigital.com.br/{urls[mul]['href']}")

            # Pronto, a cada 3, vai se sobrescrevendo e montando as URL's únicas e inserem no array urls_unicas
            tamanho = int(len(titulo))
            for t in range(tamanho):
                print(f"Título: {titulo[t].text} \n"
                      f"Data: {data[t].text} \n"
                      f"URL: {urls_unicas[t]} \n")
                funcoes_douglas.insert_noticia_pt1(titulo[t].text, urls_unicas[t], data[t].text)

        print(f"Fim da página {j}/{paginas}")

    return "sucesso"


async def getConteudo(client: ScrapflyClient, **BASE: any) -> Dict:
    # Agora que os resultados estão armazenados, hora de pegar o conteúdo deles.
    # Inicialmente eu pego todas as notícias que tenho só a primeira parte dela, sem o conteúdo
    noticias = funcoes_douglas.getNoticias()

    for n in noticias:
        PAGINA = await client.async_scrape(ScrapeConfig(n[0], **BASE))
        print(n[0])
        soup = BeautifulSoup(PAGINA.content, "lxml")
        CONTEUDO = soup.findAll("div", attrs={"id": "text-content"})
        for C in CONTEUDO:
            print(C.text)
            funcoes_douglas.insert_noticia(n[1], C.text)
        time.sleep(1)

    return "Sucesso"
