from pyramid.compat import escape

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    HTTPForbidden,
    )

from pyramid.view import view_config
from pyramid.request import Response

from pprint import pprint
from datetime import datetime

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

    removeshow = None
    for show in queryshows:
        time = None
        nextepisode = None
        running = False
        episodedata = api.show.get(show.showId)
        #print (vars(episodedata))
        if 'nextepisode' in episodedata._links:
            episodeurl = episodedata._links['nextepisode']['href']
            episodedata = api.episode.get(episodeurl.rsplit('/', 1)[1])

            time = datetime.strptime(episodedata.airdate + ' ' + episodedata.airtime, '%Y-%m-%d %H:%M')
            nextepisode = episodedata.number
            running = True

        #Update show var with new info
        show.time = time
        show.nextepisode = nextepisode
        show.running = running

        if 'shows.watchlist.remove.' + show.name in request.POST:
            #usershow = request.dbsession.query(UserShows).filter_by(user=request.user, showId=show.id).first()
            request.dbsession.delete(show)
            removeshow = show
            #queryshows.remove(show)

    if removeshow is not None:
        queryshows.remove(removeshow)

    #sort shows to be listed
    sortedshows = sorted(queryshows, key=lambda r: r.time if (r and hasattr(r, 'time') and r.time) else datetime.max)

    return dict(
        watchedshows=sortedshows,
    )