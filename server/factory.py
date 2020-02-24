"""Provides the MindspaceFactory instance."""

from os.path import getmtime, join, sep

from mindspace_web import MindspaceFactory
from random_password import random_password
from twisted.web.static import File

from .db import Player
from .parsers import parser
from .websockets import WebSocket

factory = MindspaceFactory(websocket_class=WebSocket, parser=parser)
app = factory.klein_app


@app.route('/static/', branch=True)
def static(request):
    """Return the static directory."""
    return File('static')


@app.route('/register/', methods=['GET', 'POST'])
def register(request):
    """Register for an account."""
    error = None
    if request.method == b'POST':
        data = request.args
        username = data.get(b'username', [b''])[0].decode()
        name = data.get(b'name', [b''])[0].decode()
        password = data.get(b'password', [b''])[0].decode()
        if Player.count(username=username):
            error = 'There is already a player with that username.'
        elif Player.count(name=name):
            error = 'There is already a player with that name.'
        elif not username or not password or not name:
            error = 'Please fill in all fields.'
        else:
            admin = not Player.count()
            p = Player.create(username, password, name)
            p.admin = admin
            p.save()
            return app.render_template(
                'created.html', username=p.username, name=p.name
            )
    return app.render_template(
        'register.html', password=random_password(), error=error
    )


def make_url(name):
    """Convert a name like "static/main.js" to "/static/js/main.js?12345"."""
    path = join('static', name.replace('/', sep))
    src = path.replace(sep, '/')
    t = int(getmtime(path))
    return f'/{src}?{t}'


factory.klein_app.environment.filters['make_url'] = make_url
