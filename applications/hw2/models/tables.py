# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#db.r_products.drop()

db.define_table('r_products', 
                Field('f_name'),
                Field('f_description'),
                Field('f_stock', 'integer'),
                Field('f_sold', type='integer', default=0),
                Field('f_price', 'double'),
                Field('f_cost', 'double' ),
                Field('f_creator', readable=False, writable=False), 
                redefine = True
                )
#db.r_starred.drop()
db.r_products.f_description.label = 'Description'
db.r_products.f_name.label = 'Name'
db.r_products.f_stock.label = 'Stock'
db.r_products.f_sold.label = 'Sold'
db.r_products.f_price.label = 'Price'
db.r_products.f_cost.label = 'Cost'
db.r_products.f_price.requires = IS_FLOAT_IN_RANGE(0, 10000000000)
db.r_products.f_cost.requires = IS_FLOAT_IN_RANGE(0, 10000000000)
db.r_products.f_stock.requires = IS_INT_IN_RANGE(0, 10000000000)
db.r_products.f_sold.writable = False

db.define_table('r_starred', 
                Field('f_user' , 'integer'),
                Field('f_productid', 'integer'),
                redefine = True
                )
# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
