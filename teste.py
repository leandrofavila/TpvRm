import locale

locale.setlocale(locale.LC_NUMERIC, "en_UK.UTF-8")

print(locale.atof('3,14'))

#from sqlalchemy import create_engine, MetaData, Table
#
#engine = create_engine('oracle://focco_consulta:consulta3i08@10.40.3.10:1521/f3ipro')
#
#metadata = MetaData()
#
#itens_table = Table('titens', metadata, autoload_with=engine, schema='FOCCO3I')
#
#query = itens_table.select()
#
#with engine.connect() as connection:
#    result = connection.execute(query)
#    for row in result:
#        print(row)
#