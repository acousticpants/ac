# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from gluon.tools import Mail
mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'atomcogs@gmail.com'
mail.settings.login = 'atomcogs@gmail.com:@w3e4r5t'

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('The Potassium Channel'))

def jmol():
    return dict(message=T('A Molecule'))

def editor():
    response.files.insert(0,URL('static', 'ckeditor/ckeditor.js'))
    return dict(message=T('Write Your Things Here'))

def funcplot():

    response.files.insert(0,URL('static', 'js/funcplot.js'))
    response.files.insert(1,URL('static', 'css/funcplot.css'))
    # response.write(("onload="DoOnLoad()")") need this command in opening <body> tag to initialise plot
    return dict(message=T('Graph to your heart\'s content'))

def newpage():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Hello World from newpage'))

def about():

    return dict(message=T('Why atomcogs exists'))

def molecule_videos():

    return dict(message=T('Atomcogs Molecule Videos'))

def contact():

    form = SQLFORM.factory(Field('name', requires=IS_NOT_EMPTY()),
                           Field('email', requires=[IS_EMAIL(error_message='invalid email!'), IS_NOT_EMPTY()]),
                           Field('message', requires=IS_NOT_EMPTY(), type='text'),
                           captcha_field())
    if form.process().accepted:
        session.name = form.vars.name
        session.email = form.vars.email
        session.message = form.vars.message

        x = mail.send(to=['atomcogs@gmail.com'],
            subject = 'atomcogs visitor left a message!',
            message = 'From ' + session.name + ' ' + session.email + ':\n' + session.message
        )

        if x == True:
            response.flash = 'Message sent! We\'ll get back to you shortly'
        else:
            response.flash = 'Failed to send email, so sorry. Please try again.'
    elif form.errors:
        response.flash = 'Sorry, this form is broken right now'

    return dict(message=T('Leave a message'),form=form)

def aggregator():
    import gluon.contrib.feedparser as feedparser
    response.generic_patterns = ['.rss']

    feeds = ["http://www.natureasia.com/en/rss/research",
             "http://feeds.reuters.com/reuters/scienceNews",
             "http://www.worldscientific.com/action/showFeed?type=etoc&feed=rss&jc=ijm",
             "http://www.worldscientific.com/action/showFeed?type=etoc&feed=rss&jc=ijfcs",
             "http://rss.slashdot.org/Slashdot/slashdot/to",
             "http://feeds.reuters.com/reuters/technologyNews"]
    d = feedparser.parse(feeds[0])
    e = feedparser.parse(feeds[1])
    f = feedparser.parse(feeds[2])
    g = feedparser.parse(feeds[3])
    h = feedparser.parse(feeds[4])
    i = feedparser.parse(feeds[5])
    return dict(message=T('All the science news'),content=d.entries + e.entries + f.entries + g.entries + h.entries + i.entries)
"""

def user():
    
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    
    return dict(form=auth())
"""
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


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
