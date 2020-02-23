from pytest import raises

from server.exc import MustBeAdmin
from server.parsers import parser


def test_admin_required(con):
    with raises(MustBeAdmin):
        parser.handle_command('shutdown', con)
