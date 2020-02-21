"""Provides exception classes."""


class Error(Exception):
    pass


class AuthenticationError(Error):
    """Authentication problem."""


class InvalidUsername(AuthenticationError):
    """No player with that username found."""


class InvalidPassword(AuthenticationError):
    """Invalid password for that player."""
