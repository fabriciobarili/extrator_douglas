import midianews
import olhardireto
import folhamax
import gazetadigital

CHAVE = "scp-test-7741b22fda044fa08e29e77039a4655e"

import asyncio

from scrapfly import ScrapflyClient



client = ScrapflyClient(key=CHAVE, max_concurrency=5)

BASE_CONFIG = {
    "country": "BR",
    "asp": False,
    "render_js":False
}

async def run():

    #Aqui você insere o termo que deseja procurar

    # Define a variable to store the input
    TERMO = input("Insira o terpo de pesquisa: ")
    # Print the input
    print("Iniciando a busca nos sites Gazeta, Folha Max e Olhar Direto pelo termo: " + TERMO + ".")


    #primeiro faz a busca pelo termo nos sites Gazeta Digital, Folha Max e Olhar Direto
    #r = await gazetadigital.getListaNoticias(TERMO, client, **BASE_CONFIG)
    #r = await folhamax.getListaNoticias(TERMO, client, **BASE_CONFIG)
    #r = await olhardireto.getListaNoticias(TERMO, client, **BASE_CONFIG)

    #em desenvolvimento >> r = await midianews.getListaNoticias(TERMO, client, **BASE_CONFIG)

    #depois, em cada notícia encontrada, pega o conteúdo dela
    #r = await gazetadigital.getConteudo(client, **BASE_CONFIG)
    #r = await folhamax.getConteudo(client, **BASE_CONFIG)
    #r = await olhardireto.getConteudo(client, **BASE_CONFIG)

if __name__ == "__main__":
    asyncio.run(run())