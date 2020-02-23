"""Provides exception classes."""


class Error(Exception):
    pass


class AuthenticationError(Error):
    """Authentication problem."""


class InvalidUsername(AuthenticationError):
    """No player with that username found."""


class InvalidPassword(AuthenticationError):
    """Invalid password for that player."""


class CommandError(Error):
    """An error pertaining to the commands subsystem."""


class PermissionsError(CommandError):
    """Insufficient permissions."""


class MustBeAdmin(PermissionsError):
    """You are not an administrator."""


class NotWhileLoggedIn(PermissionsError):
    """You cannot use this command after logging in."""
