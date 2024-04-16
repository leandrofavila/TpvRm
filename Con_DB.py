import pandas as pd
import cx_Oracle


class DB:
    def __init__(self):
        self.db_connection = None

    @staticmethod
    def get_connection():
        dsn = cx_Oracle.makedsn("10.40.3.10", 1521, service_name="f3ipro")
        connection = cx_Oracle.connect(user=r"focco_consulta", password=r'consulta3i08', dsn=dsn, encoding="UTF-8")
        cur = connection.cursor()
        return cur


    def dim_itens(self, cod_item, dimensao, variacao):
        #print(cod_item, dimensao, variacao)
        if variacao is None:
            variacao = 0

        if dimensao is None:
            com_dim = ''
        else:
            com_dim = (
                r"WHERE (TABELA.MED_X BETWEEN "+str(dimensao)+" - "+str(variacao)+" AND "+str(dimensao)+" + "+str(variacao)+") "
                r"OR (TABELA.MED_Y BETWEEN "+str(dimensao)+" - "+str(variacao)+" AND "+str(dimensao)+" + "+str(variacao)+") "
                r"OR (TABELA.MED_Z BETWEEN "+str(dimensao)+" - "+str(variacao)+" AND "+str(dimensao)+" + "+str(variacao)+") "
            )
        print(com_dim)
        cur = self.get_connection()
        cur.execute(
            r"SELECT *  FROM ( "
            r"SELECT ENG.COD_ITEM, TIT.DESC_TECNICA, "
            r"         (SELECT TO_NUMBER(REPLACE(PDM.CONTEUDO_ATRIBUTO,',', '.')) "
            r"            FROM FOCCO3I.TITENS_PDM PDM "
            r"            INNER JOIN FOCCO3I.TATRIBUTOS ATR ON ATR.ID = PDM.ATRIBUTO_ID "
            r"            WHERE ATR.DESCRICAO LIKE '%MEDIDA_X%' AND PDM.ITEM_ID = EMPF.ITEM_ID) AS MED_X, "
            r"         (SELECT TO_NUMBER(REPLACE(PDM.CONTEUDO_ATRIBUTO,',', '.')) "
            r"            FROM FOCCO3I.TITENS_PDM PDM "
            r"            INNER JOIN FOCCO3I.TATRIBUTOS ATR ON ATR.ID = PDM.ATRIBUTO_ID "
            r"            WHERE ATR.DESCRICAO LIKE '%MEDIDA_Y%' AND PDM.ITEM_ID = EMPF.ITEM_ID) AS MED_Y, "
            r"         (SELECT TO_NUMBER(REPLACE(PDM.CONTEUDO_ATRIBUTO,',', '.')) "
            r"            FROM FOCCO3I.TITENS_PDM PDM "
            r"            INNER JOIN FOCCO3I.TATRIBUTOS ATR ON ATR.ID = PDM.ATRIBUTO_ID "
            r"            WHERE ATR.DESCRICAO LIKE '%MEDIDA_Z%' AND PDM.ITEM_ID = EMPF.ITEM_ID) AS MED_Z "
            r"FROM FOCCO3I.TITENS_EMPR EMP "
            r"INNER JOIN FOCCO3I.TITENS_ENGENHARIA ENG ON ENG.ITEMPR_ID_ITEM_BASE = EMP.ID "
            r"INNER JOIN FOCCO3I.TITENS_EMPR EMPF ON EMPF.ID = ENG.ITEMPR_ID "
            r"INNER JOIN FOCCO3I.TITENS TIT ON TIT.ID = EMPF.ITEM_ID "
            r"WHERE EMP.COD_ITEM = "+str(cod_item)+""
            r"AND TIT.SIT = 1) TABELA "
            r""+com_dim+" "
        )

        dim_itens = pd.DataFrame(cur.fetchall(), columns=["COD_ITEM", "DESC_TECNICA", "MED_X", "MED_Y", "MED_Z"])
        cur.close()
        return dim_itens


    def item_base(self, cod_item):
        cur = self.get_connection()
        cur.execute(
            r"SELECT IND_ITEM_BASE FROM FOCCO3I.TITENS TIT WHERE COD_ITEM = "+str(cod_item)+" "
        )
        result = cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False


    def find_item_base(self, cod_item):
        cur = self.get_connection()
        cur.execute(
            r"SELECT EMP.COD_ITEM  "
            r"FROM FOCCO3I.TITENS_ENGENHARIA ENG  "
            r"INNER JOIN FOCCO3I.TITENS_EMPR EMP  ON EMP.ID = ENG.ITEMPR_ID_ITEM_BASE "
            r"WHERE ENG.COD_ITEM = "+str(cod_item)+" "
        )
        item_base = cur.fetchone()
        return item_base[0]
