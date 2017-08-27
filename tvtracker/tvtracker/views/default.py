from pyramid.compat import escape

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPForbidden,
    )

from pyramid.view import view_config
from pyramid.request import Response

from ..models import User, UserShows

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home(request):
    next_url = request.route_url('login')
    return HTTPFound(location=next_url)

@view_config(route_name='view_show')
def view_show(request):
    return { 'a' }

@view_config(route_name='watchlist', renderer='../templates/watchlist.jinja2')
def watchlist(request):
    user = request.user
    if user is None:
        return HTTPFound(location=request.route_url('login'))



    return { 'hi ' : request.user.name }