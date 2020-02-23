"""Provides general commands."""

from ..parsers import parser


@parser.command
def echo(con, message):
    """Send a message right back to a connected client."""
    con.message(message)
