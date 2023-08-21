import time
from builtins import len
from typing import Dict

from bs4 import BeautifulSoup
from scrapfly import ScrapeConfig, ScrapflyClient

import funcoes_douglas


async def getListaNoticias(termo: str, client: ScrapflyClient, economia: str, **BASE: any) -> Dict:

    if economia == "S":
        print(f"Iniciando a pesquisa no site Mídia News pelo termo {termo} com economia de API")
    elif economia == "N":
        print(f"Iniciando a pesquisa no site Mídia News pelo termo {termo} sem economia de API")

    # A partir do termo, descobrimos quantas páginas existem
    URL = f"https://www.midianews.com.br/busca.php?pageNum_Busca=0&keyword=+{termo}+"
    PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
    soup = BeautifulSoup(PAGINA.content, "lxml")

    # Cada página contém 30 notícias. No entanto, não existe um 'Página X de Y', só uma imagem de 'próximo' e 'último'.
    # Essas imagens não tem classe, mas, se eu pegar todos os HREF's e encontrar o valor de 'totalRows_Busca', sei quantos resultados tem e é só / 30 para saber a quantidade de páginas.

    # <a href="/busca.php?pageNum_Busca=119&keyword=+termo+&totalRows_Busca=3588"><img src="images/__btnLast.gif" border="0"></a>
    botao = soup.findAll('a', href=True)
    InicioPaginacao = botao[51].attrs['href'].find('&totalRows_Busca=')+17
    TotalDePaginas = botao[51].attrs['href'][InicioPaginacao:len(botao[51].attrs['href'])]

    if economia != "S":
        paginas = TotalDePaginas
    else:
        paginas = int(int(TotalDePaginas) / 4)



    print(f'Total de páginas para esta busca: {paginas}')

    # Cria uma lista de 0 até o total de páginas, para iniciar o loop
    array_paginas = []
    for i in range(paginas):
        array_paginas.append(i)

    # Inínio do Loop
    for j in array_paginas:
        URL = f"https://www.midianews.com.br/busca.php?pageNum_Busca={j}&keyword=+{termo}+"
        print(f'Iniciando o Scrap pela página: {URL}')
        PAGINA = await client.async_scrape(ScrapeConfig(URL, **BASE, proxy_pool='public_residential_pool'))
        soup = BeautifulSoup(PAGINA.content, "lxml")



        titulo = soup.findAll("a", attrs={"class": "ConteudoTitulo2"})
        data = soup.findAll("td", attrs={"class": "ConteudoData"})
        urls = soup.findAll("a", attrs={"class": "ConteudoTitulo2"},  href=True)

        tamanho = int(len(titulo))
        print(tamanho)
        for t in range(tamanho):
            print(f"Título: {titulo[t].text} \n"
                  f"Data: {data[t].text} \n"
                  f"URL: https://www.midianews.com.br/{urls[t]['href']} \n")
            funcoes_douglas.insert_noticia_pt1(titulo[t].text, f"https://www.midianews.com.br/{urls[t]['href']}",
                                               data[t].text)

        print(f"Fim da página {j}/{paginas}")

    return "sucesso"


async def getConteudo(client: ScrapflyClient, **BASE: any) -> Dict:
    # Agora que os resultados estão armazenados, hora de pegar o conteúdo deles.
    # Inicialmente eu pego todas as notícias que tenho só a primeira parte dela, sem o conteúdo
    noticias = funcoes_douglas.getNoticias()

    for n in noticias:
        PAGINA = await client.async_scrape(ScrapeConfig(n[0], **BASE))

        soup = BeautifulSoup(PAGINA.content, "lxml")
        CONTEUDO = soup.findAll("div", attrs={"id": "texto"})
        IMAGENS = soup.findAll("img", attrs={"id": "img_conteudo"})
        for C in CONTEUDO:

            funcoes_douglas.insert_noticia(n[1], C.text)

            #atualizaData
            DataNoticia = soup.findAll("div", attrs={"class": "row espaco-conteudo"})
            for d in DataNoticia:
                txt = d.text

                LocalDaData = txt.find(" | ")
                Dt = txt[LocalDaData-10:LocalDaData]

                funcoes_douglas.UpdateData_Noticia(n[1], Dt)

        for I in IMAGENS:
            print(I['src'])
            funcoes_douglas.insert_imagens(n[1], I['src'])

        time.sleep(1)

    return "Sucesso"
