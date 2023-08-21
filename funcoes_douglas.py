import mysql.connector
import openpyxl
from datetime import date


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="douglas"
)
mycursor = mydb.cursor()


def insert_noticia_pt1(titulo: str, url: str, data: str):
    sql = "INSERT INTO `tb_noticias` (`TITULO`, `URL`, `DATA`) VALUES (%s, %s, %s)"
    val = (titulo, url, data)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Sucesso"


def getNoticias(site: str):
    sql = "SELECT `url`, `id` FROM `tb_noticias` where not EXISTS (select 1 from tb_texto where ID_NOTICIA = `tb_noticias`.`ID`)"

    myresult = mycursor.fetchall()

    return myresult


def insert_noticia(id: str, texto: str):
    sql = "INSERT INTO `tb_texto` (`ID_NOTICIA`, `TEXTO`) VALUES (%s, %s)"
    val = (id, texto)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Sucesso"

def insert_imagens(id: str, texto: str):
    sql = "INSERT INTO `tb_imagens` (`id_noticia`, `url`) VALUES (%s, %s)"
    val = (id, texto)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Sucesso"

def UpdateData_Noticia(id : str, texto : str):
    sql = "UPDATE `tb_noticias` set  `DATA` = %s WHERE ID = %s"
    val = (texto, id)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Sucesso"

def getNoticiasFolhamax(site:str):
    sql = f"SELECT `url`, `id` FROM `tb_noticias` where not EXISTS (select 1 from tb_texto where ID_NOTICIA = `tb_noticias`.`ID`) and `url` like (%s)"
    val = (f"%{site}%")
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    return myresult


def ExportExcel(nome : str):

    book = openpyxl.Workbook()
    sheet = book.active
    sql = f"SELECT A.TITULO, A.DATA, B.TEXTO, B.IMAGEM from tb_noticias as A inner join tb_texto as B on a.ID = b.ID_NOTICIA"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    i = 0
    for row in myresult:
        i += 1
        j = 1
        for col in row:
            cell = sheet.cell(row=i, column=j)
            cell.value = col
            j += 1



    book.save(f"arquivos/{nome}_{date.today()}.xlsx")

    book = openpyxl.Workbook()
    sheet = book.active
    sql = f"SELECT id_noticia, url from tb_imagens"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    i = 0
    for row in myresult:
        i += 1
        j = 1
        for col in row:
            cell = sheet.cell(row=i, column=j)
            cell.value = col
            j += 1

    book.save(f"arquivos/{nome}_{date.today()}_imgs.xlsx")

    return "Sucesso"