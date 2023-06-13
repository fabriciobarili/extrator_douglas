import olhardireto

CHAVE = "scp-test-7741b22fda044fa08e29e77039a4655e"

import asyncio

from scrapfly import ScrapflyClient

import folhamax
import gazetadigital

client = ScrapflyClient(key=CHAVE, max_concurrency=5)

BASE_CONFIG = {
    "country": "BR",
    "asp": False,
    "render_js":False
}

async def run():

    #Aqui você insere o termo que deseja procurar

    # Define a variable to store the input
    #TERMO = input("Insira o termpo de pesquisa: ")
    # Print the input
    #print("Iniciando a busca nos sites Gazeta e Folha Max pelo termo: " + TERMO + ".")


    #primeiro faz a busca pelo termo nos sites Gazeta Digital e Folha Max
    #r = await gazetadigital.getListaNoticias(TERMO, client, **BASE_CONFIG)
    #r = await folhamax.getListaNoticias(TERMO, client, **BASE_CONFIG)
    #r = await olhardireto.getListaNoticias("Lula", client, **BASE_CONFIG)

    #depois, em cada notícia encontrada, pega o conteúdo dela
    #r = await gazetadigital.getConteudo(client, **BASE_CONFIG)
    #r = await folhamax.getConteudo(client, **BASE_CONFIG)
    r = await olhardireto.getConteudo(client, **BASE_CONFIG)

if __name__ == "__main__":
    asyncio.run(run())