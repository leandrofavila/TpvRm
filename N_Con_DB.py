from sqlalchemy import create_engine, and_, or_, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Definir a Base
Base = declarative_base()


# Definir as tabelas correspondentes ao seu esquema de banco de dados
class TITENS_EMPR(Base):
    __tablename__ = 'TITENS_EMPR'
    __table_args__ = {'schema': 'FOCCO3I'}

    id = Column(Integer, primary_key=True)
    COD_ITEM = Column(String)
    ITEM_ID = Column(Integer)


class TITENS_ENGENHARIA(Base):
    __tablename__ = 'TITENS_ENGENHARIA'
    __table_args__ = {'schema': 'FOCCO3I'}

    id = Column(Integer, primary_key=True)
    ITEMPR_ID_ITEM_BASE = Column(Integer)


class TITENS(Base):
    __tablename__ = 'TITENS'
    __table_args__ = {'schema': 'FOCCO3I'}

    id = Column(Integer, primary_key=True)
    DESC_TECNICA = Column(String)


class TITENS_PDM(Base):
    __tablename__ = 'TITENS_PDM'
    __table_args__ = {'schema': 'FOCCO3I'}

    id = Column(Integer, primary_key=True)
    CONTEUDO_ATRIBUTO = Column(String)
    ITEM_ID = Column(Integer)
    ATRIBUTO_ID = Column('ATRIBUTO_ID', Integer)


class TATRIBUTOS(Base):
    __tablename__ = 'TATRIBUTOS'
    __table_args__ = {'schema': 'FOCCO3I'}

    id = Column('ID', Integer, primary_key=True)
    DESCRICAO = Column('DESCRICAO', String)


engine = create_engine('oracle://focco_consulta:consulta3i08@10.40.3.10:1521/f3ipro')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Escrever a consulta usando a API de consulta do SQLAlchemy
query_result = session.query(
    TITENS_EMPR.COD_ITEM,
    TITENS.DESC_TECNICA,
    TITENS_PDM.CONTEUDO_ATRIBUTO.label('MED_X'),
    TITENS_PDM.CONTEUDO_ATRIBUTO.label('MED_Y'),
    TITENS_PDM.CONTEUDO_ATRIBUTO.label('MED_Z'),
    TITENS_PDM.CONTEUDO_ATRIBUTO.label('ESPESSURA')) \
    .join(TITENS_ENGENHARIA, TITENS_ENGENHARIA.ITEMPR_ID_ITEM_BASE == TITENS_EMPR.id) \
    .join(TITENS_EMPR, TITENS_EMPR.id == TITENS_ENGENHARIA.ITEMPR_ID_ITEM_BASE) \
    .join(TITENS, TITENS.id == TITENS_EMPR.ITEM_ID) \
    .join(TITENS_PDM, and_(TITENS_PDM.ITEM_ID == TITENS_EMPR.ITEM_ID,
                           TITENS_PDM.ATRIBUTO_ID == TATRIBUTOS.id,
                           or_(TATRIBUTOS.DESCRICAO.like('%MEDIDA_X%'),
                               TATRIBUTOS.DESCRICAO.like('%MEDIDA_Y%'),
                               TATRIBUTOS.DESCRICAO.like('%MEDIDA_Z%'),
                               TATRIBUTOS.DESCRICAO.like('%ESP%')))) \
    .filter(TITENS_EMPR.COD_ITEM == 12624,
            or_(TITENS_PDM.CONTEUDO_ATRIBUTO.between(5594 - 1, 5594 + 1),
                TITENS_PDM.CONTEUDO_ATRIBUTO.between(5594 - 1, 5594 + 1),
                TITENS_PDM.CONTEUDO_ATRIBUTO.between(5594 - 1, 5594 + 1))

)

# Executar a consulta e iterar sobre os resultados
for result in query_result:
    print(result)
