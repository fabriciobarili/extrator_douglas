import folha_sp
import funcoes_douglas
import midianews
import olhardireto
import OGlobo

CHAVE = "scp-live-a24d530459964e38bf761bb889862785"

import asyncio

from scrapfly import ScrapflyClient

client = ScrapflyClient(key=CHAVE, max_concurrency=5)

BASE_CONFIG = {
    "country": "BR",
    "asp": False,
    "render_js": False
}


async def run():
    # Aqui você insere o termo que deseja procurar

    # Define a variable to store the input
    TERMO = input("Insira o terpo de pesquisa: ")
    SAVE_MODE = input("Deseja habilitar economia de API? S-SIM, N-NÃO ").upper()
    # Print the input
    txt = 'sem economia de API'
    if SAVE_MODE != "S" or SAVE_MODE != "N":
        print("Valor de economia de API incompatível, habilitando para Ativo por questão de segurança")
        SAVE_MODE = "S"

    if SAVE_MODE == "S":
        txt = 'com economia de API'

    print("Iniciando a busca nos sites Gazeta, Folha Max e Olhar Direto pelo termo: " + TERMO + " " + txt + ".")

    #primeiro faz a busca pelo termo nos sites Gazeta Digital, Folha Max e Olhar Direto
    #r = await gazetadigital.getListaNoticias(TERMO, client,SAVE_MODE, **BASE_CONFIG)
    #r = await folhamax.getListaNoticias(TERMO, client,SAVE_MODE, **BASE_CONFIG)
    #r = await olhardireto.getListaNoticias(TERMO, client, SAVE_MODE, **BASE_CONFIG)
    #r = await midianews.getListaNoticias(TERMO, client, SAVE_MODE, **BASE_CONFIG)
    #r = await OGlobo.getListaNoticias(TERMO, client, SAVE_MODE, **BASE_CONFIG)
    #r = await folha_sp.getListaNoticias(TERMO, client, SAVE_MODE, **BASE_CONFIG)

    #depois, em cada notícia encontrada, pega o conteúdo dela
    #r = await gazetadigital.getConteudo(client, **BASE_CONFIG)
    #r = await folhamax.getConteudo(client, **BASE_CONFIG)
    #r = await olhardireto.getConteudo(client, **BASE_CONFIG)
    #r = await midianews.getConteudo(client, **BASE_CONFIG)
    #r = await OGlobo.getConteudo(client, **BASE_CONFIG)
    #r = await folha_sp.getConteudo(client, **BASE_CONFIG)

    #SALVAR TUDO O QUE ESTÁ NA BASE DE DADOS
    #funcoes_douglas.ExportExcel("arquivo")


if __name__ == "__main__":
    asyncio.run(run())
