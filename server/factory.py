"""Provides the MindspaceFactory instance."""

from os.path import getmtime, join, sep

from mindspace_web import MindspaceFactory
from twisted.web.static import File

from .parsers import parser
from .websockets import WebSocket

factory = MindspaceFactory(websocket_class=WebSocket, parser=parser)


@factory.klein_app.route('/static/', branch=True)
def static(request):
    """Return the static directory."""
    return File('static')


def make_url(name):
    """Convert a name like "static/main.js" to "/static/js/main.js?12345"."""
    path = join('static', name.replace('/', sep))
    src = path.replace(sep, '/')
    t = int(getmtime(path))
    return f'/{src}?{t}'


factory.klein_app.environment.filters['make_url'] = make_url
