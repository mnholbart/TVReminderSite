from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import User


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    next_url = request.params.get('next', request.route_url('watchlist'))
    message = ''
    login = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        username = request.dbsession.query(User).filter_by(name=login).first()
        if username is not None and username.check_password(password):
            headers = remember(request, username.id)
            return HTTPFound(location=next_url, headers=headers)
        message = 'Failed login'

    return dict(
        name='Login',
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        password=''
    )
