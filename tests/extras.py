"""Helper methods for tests."""
import os

USERNAME = 'foo'
PASSWORD = 'secret'
CONTROLLER_SERIAL = 'ABCDEFGH'
CONTROLLER_NAME = 'Controller001'
CONTROLLER_TIMESTAMP = '02:00 AM'
CSRFTOKEN = 'AbCdEFJeCDnkC2pdmrywqBAbN9999999'
FAUCET_NAME = 'Faucet001'
FAUCET_SERIAL = '1234'


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    with open(path) as fdp:
        return fdp.read()
