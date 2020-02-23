"""Provides the MindspaceFactory instance."""

from os.path import getmtime, join, sep

from mindspace_web import MindspaceFactory
from twisted.web.static import File

from .parsers import login_parser, main_menu_parser, main_parser
from .websockets import WebSocket


class CustomMindspaceFactory(MindspaceFactory):
    def get_parser(self, connection):
        """Return login_parser if connection is not authenticated, otherwise
        main_parser."""
        if connection.player_id is None:
            return login_parser
        elif connection.player.location_id is None:
            return main_menu_parser
        else:
            return main_parser


factory = CustomMindspaceFactory(websocket_class=WebSocket)


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
