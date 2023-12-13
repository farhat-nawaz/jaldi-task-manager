from pony import orm

db = orm.Database()

db.bind(provider='mysql', host='', user='', passwd='', db='')
db.generate_mapping(create_tables=True)



