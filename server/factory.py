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


def make_script_tag(name):
    """Convert a name like "main.js" to
    "<script src="/static/js/main.js?12345"></script>"."""
    path = join('static', 'js', name)
    src = path.replace(sep, '/')
    t = int(getmtime(path))
    return f'<script src="/{src}?{t}"></script>'


factory.klein_app.environment.filters['script'] = make_script_tag
