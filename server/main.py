"""Provides the main function."""

from logging import basicConfig, getLogger
from sys import stdout
from time import time

from .db import Base, load, dump
from .factory import factory
from .parsers import load_commands
from .util import pluralise


def main():
    started = time()
    basicConfig(stream=stdout, level='INFO')
    logger = getLogger(__name__)
    logger.info('Server starting.')
    Base.metadata.create_all()
    try:
        load()
        logger.info('Objects loaded: %d.', Base.number_of_objects())
    except FileNotFoundError:
        logger.info('Starting with a blank database.')
    logger.info('Database loaded in %.2f seconds.', time() - started)
    load_commands()
    logger.info('Running the factory.')
    factory.run()
    started = time()
    logger.info('Dumping the database.')
    dump()
    n = Base.number_of_objects()
    logger.info(
        'Dumped %d %s in %.2f seconds.', n, pluralise(n, 'object'),
        time() - started
    )
