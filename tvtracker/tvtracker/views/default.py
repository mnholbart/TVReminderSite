from pyramid.compat import escape

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPForbidden,
    )

from pyramid.view import view_config
from pyramid.request import Response

from tvmaze.api import Api

from ..models import User, UserShows

api = Api()


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    queryshows = None
    search = ''
    watchedshows = {}

    if 'form.submitted' in request.params and 'form.search' in request.params:
        search = request.params['form.search']
        queryshows = api.search.shows(search)

        for show in queryshows:
            if 'shows.submitted.' + show.name in request.POST:
                #print(show)
                return HTTPFound(location=request.route_url('view_show', show_id=show.name))

        for show in queryshows:
            if request.user is not None and 'shows.watchlist.add.' + show.name in request.POST:
                show = UserShows(name=show.name, showId=show.id, user=request.user)
                request.dbsession.add(show)

        for show in queryshows:
            if request.user is not None and 'shows.watchlist.remove.' + show.name in request.POST:
                usershow = request.dbsession.query(UserShows).filter_by(user=request.user, showId=show.id).first()
                print(usershow)
                request.dbsession.delete(usershow)

        usershows = request.dbsession.query(UserShows).filter_by(user=request.user).all()
        userIds = set(s.showId for s in usershows)
        watchedshows = [q for q in queryshows if q.id in userIds]


    return dict(
        shows=queryshows,
        userwatchlist = watchedshows,
        search=search,
    )



@view_config(route_name='view_show', renderer='../templates/show.jinja2')
def view_show(request):
    return { 'a' : '' }


@view_config(route_name='watchlist', renderer='../templates/watchlist.jinja2')
def watchlist(request):
    user = request.user
    if user is None:
        return HTTPFound(location=request.route_url('login'))

    queryshows = request.dbsession.query(UserShows).filter_by(user=request.user).all()

    for show in queryshows:
        if request.user is not None and 'shows.watchlist.remove.' + show.name in request.POST:
            #usershow = request.dbsession.query(UserShows).filter_by(user=request.user, showId=show.id).first()
            request.dbsession.delete(show)
            queryshows.remove(show)

    return dict(
        watchedshows=queryshows,
    )