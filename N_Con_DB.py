from sqlalchemy import create_engine, and_, or_, Column, Integer, String, ForeignKey, Boolean, MetaData
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('oracle://focco_consulta:consulta3i08@10.40.3.10:1521/f3ipro')

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class TITENS_EMPR(Base):
    __tablename__ = 'TITENS_EMPR'
    __table_args__ = {'schema': 'FOCCO3I'}

    ID = Column(Integer, primary_key=True)
    COD_ITEM = Column(Integer)
    ITEM_ID = Column(Integer, ForeignKey('TITENS'))

    def __init__(self, ID, COD_ITEM, ITEM_ID):
        self.ID = ID
        self.COD_ITEM = COD_ITEM
        self.ITEM_ID = ITEM_ID

    def __repr__(self):
        return f"({self.ID} {self.COD_ITEM} {self.ITEM_ID})"


class TITENS_ENGENHARIA(Base):
    __tablename__ = 'TITENS_ENGENHARIA'
    __table_args__ = {'schema': 'FOCCO3I'}

    ID = Column(Integer, primary_key=True)
    ITEMPR_ID_ITEM_BASE = Column(Integer, ForeignKey('TITENS_EMPR.ID'))
    ITEMPR_ID = Column(Integer, ForeignKey('TITENS_EMPR.ID'))

    def __init__(self, ID, ITEMPR_ID_ITEM_BASE, ITEMPR_ID):
        self.ID = ID
        self.ITEMPR_ID_ITEM_BASE = ITEMPR_ID_ITEM_BASE
        self.ITEMPR_ID = ITEMPR_ID

    def __repr__(self):
        return f"({self.ID} {self.ITEMPR_ID_ITEM_BASE} {self.ITEMPR_ID})"


class TITENS(Base):
    __tablename__ = 'TITENS'
    __table_args__ = {'schema': 'FOCCO3I'}

    ID = Column(Integer, primary_key=True)
    DESC_TECNICA = Column(String)
    SIT = Column(Boolean)
    COD_ITEM = Column(Integer)

    def __init__(self, ID, DESC_TECNICA, SIT, COD_ITEM):
        self.ID = ID
        self.DESC_TECNICA = DESC_TECNICA
        self.SIT = SIT
        self.COD_ITEM = COD_ITEM

    def __repr__(self):
        return f"({self.ID} {self.DESC_TECNICA} {self.SIT} {self.COD_ITEM})"


class TITENS_PDM(Base):
    __tablename__ = 'TITENS_PDM'
    __table_args__ = {'schema': 'FOCCO3I'}

    ID = Column(Integer, primary_key=True)
    CONTEUDO_ATRIBUTO = Column(String)
    ITEM_ID = Column(Integer)
    ATRIBUTO_ID = Column('ATRIBUTO_ID', Integer)

    def __init__(self, ID, CONTEUDO_ATRIBUTO, ITEM_ID, ATRIBUTO_ID):
        self.ID = ID
        self.CONTEUDO_ATRIBUTO = CONTEUDO_ATRIBUTO
        self.ITEM_ID = ITEM_ID
        self.ATRIBUTO_ID = ATRIBUTO_ID

    def __repr__(self):
        return f"({self.ID} {self.CONTEUDO_ATRIBUTO} {self.ITEM_ID} {self.ATRIBUTO_ID})"


class TATRIBUTOS(Base):
    __tablename__ = 'TATRIBUTOS'
    __table_args__ = {'schema': 'FOCCO3I'}

    ID = Column('ID', Integer, primary_key=True)
    DESCRICAO = Column(String)

    def __init__(self, ID, DESCRICAO):
        self.ID = ID
        self.DESCRICAO = DESCRICAO

    def __repr__(self):
        return f"({self.ID} {self.DESCRICAO})"


Base.metadata.create_all(engine)

tit = session.query(TITENS).filter(TITENS.COD_ITEM == 10050)

for vals in tit.all():
    print(vals)
