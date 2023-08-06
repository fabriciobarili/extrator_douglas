import mysql.connector

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


def getNoticias():
    sql = "SELECT `url`, `id` FROM `tb_noticias` where not EXISTS (select 1 from tb_texto where ID_NOTICIA = `tb_noticias`.`ID`)"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult


def insert_noticia(id: str, texto: str):
    sql = "INSERT INTO `tb_texto` (`ID_NOTICIA`, `TEXTO`) VALUES (%s, %s)"
    val = (id, texto)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Sucesso"

def UpdateData_Noticia(id : str, texto : str):
    sql = "UPDATE `tb_noticias` set  `DATA` = %s WHERE ID = %s"
    val = (texto, id)
    print(sql)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Sucesso"

def getNoticiasFolhamax():
    sql = f"SELECT `url`, `id` FROM `tb_noticias` where not EXISTS (select 1 from tb_texto where ID_NOTICIA = `tb_noticias`.`ID`)"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult
