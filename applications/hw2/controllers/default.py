# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def list():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    def star(row):
                myquery = (db.r_starred.f_productid == row.id) & (db.r_starred.f_user == auth.user.id)
                if db(myquery).select().first() is None:
                    return SPAN(A(I(_class='fa fa-star-o'), 
                        _href = URL('default', 'toggle_star', args=[row.id, auth.user.id], user_signature=True)))
                    
                    #return 'x'
                else:
                    
                    return SPAN(A(I(_class='fa fa-star'), 
                        _href = URL('default', 'toggle_star', args=[row.id, auth.user.id], user_signature=True)))
                    
                    #return 'y'
    links = []
    links.append(
            dict( header = 'profit', body = lambda row:
                row.f_sold *(row.f_price - row.f_cost) 
            )
    )
    if auth.user is not None:
        links.append(
            dict( header='', 
                body = lambda row: 
                SPAN(A('+1', 
                   _class='btn', 
                    _href = URL('default', 'inc', args=[row.id], user_signature=True)))
            )
        )

        links.append(
            dict( header='', 
                body = lambda row: 
                SPAN(A('-1', 
                    _class='btn', 
                    _href = URL('default', 'dec', args=[row.id], user_signature=True)))
            )
        )

        links.append(
            dict( header='', 
                body = star 
            )
        )
    
    db.r_products.id.readable = False    
    #db.r_products.id.writable = False    
    return dict(grid=SQLFORM.grid(db.r_products, links=links))
    #return dict(grid=SQLFORM.grid(db.r_products))



def products():
    return dict(grid=SQLFORM.grid(db.r_products))

def starred():
    return dict(grid=SQLFORM.grid(db.r_starred))

def inc():
    r = db.r_products(request.args[0])
    if r is None:
        redirect(URL('default', 'list'))
    r.f_stock = r.f_stock + 1
    r.update_record()
    redirect(URL('default', 'list'))

def dec():
    r = db.r_products(request.args[0])
    if r is None:
        redirect(URL('default', 'list'))
    if r.f_stock > 0:
        r.f_sold = r.f_sold + 1
        r.f_stock = r.f_stock - 1
        r.update_record()
    redirect(URL('default', 'list'))

def toggle_star():
    if db((db.r_starred.f_user == auth.user.id) & (db.r_starred.f_productid == request.args[0])).select().first() is None:
        db.r_starred.insert(f_user=auth.user.id, f_productid=request.args[0] ) 
        print 'hi'
    else:
        print 'bye'
        db((db.r_starred.f_user == auth.user.id) & (db.r_starred.f_productid == request.args[0])).delete()

    redirect(URL('default', 'list'))

def user():
    return dict(form=auth())

#@auth.requires_login()
def index():
    if auth.user is None: 
        return dict(rows=None)
    #rows='log in to see starred products')
    else:
        #db.r_products.f_name.label = 'Name'
        return dict(rows=db((db.r_products.id == db.r_starred.f_productid) & (auth.user.id == db.r_starred.f_user)).select(db.r_products.f_name, db.r_products.f_price))

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


