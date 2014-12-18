import os
import sys
import warnings

SERVER = {
    'HOST': 'localhost',
    'PORT': 6667,
}

LOG_LEVEL = 'DEBUG'

# Channel logging. Set CHANNEL_LOGGING_DIR
CHANNEL_LOGGING = False
CHANNEL_LOGGING_DIR = '.logs'

NICK = 'helga'
CHANNELS = [
    ('#bots',),
]

AUTO_RECONNECT = True
AUTO_RECONNECT_DELAY = 5
RATE_LIMIT = None

OPERATORS = ['sduncan']

# MongoDB settings
DATABASE = {
    'HOST': 'localhost',
    'PORT': 27017,
    'DB': 'helga',
}

TIMEZONE = 'US/Eastern'

# The default set of plugins enabled on any channel.
# By default, potentially noisy plugins are disabled
ENABLED_PLUGINS = [
    'dubstep',
    'facts',
    'help',
    'jira',
    'logger',
    'loljava',
    'manager',
    'meant_to_say',
    'oneliner',
    'operator',
    'poems',
    'reminders',
    'reviewboard',
    'stfu',
    'webhooks',
    'wiki_whois',

    # Sometimes, giphy may give back a gif of questionable content
    # 'giphy',

    # These can get super annoying in public channels
    # 'icanhazascii',

    # Generally, olga isn't being used
    # 'no_more_olga',
]

# A list of webhook names that should be enabled on process startup.
# If this value is None, then all webhooks loaded via entry points
# are run. An empty list will not load any webhooks
ENABLED_WEBHOOKS = None

# Set to False if all responses returned by plugins should be returned
# over IRC. If True, the first responding plugin will send a response
PLUGIN_FIRST_RESPONDER_ONLY = True

# If set to True, a command can be run by asking directly.
# For example `helga foo`
COMMAND_PREFIX_BOTNICK = True

# If non-empty, this char can be used to invoke a command without
# requiring the bot's nick. For example `helga foo` could be run with
# `!foo` instead
COMMAND_PREFIX_CHAR = '!'

# MISC PLUGIN SETTINGS
FACTS_REQUIRE_NICKNAME = False

# Jira settings. If JIRA_FULL_DESCRIPTION is false, only links to the Jira
# ticket will be shown. Otherwise, the ticket title will be pulled and shown.
# JIRA_USERNAME and JIRA_PASSWORD are optional if authentication is required
JIRA_URL = 'http://localhost/{ticket}'
JIRA_REST_API = ''
JIRA_SHOW_FULL_DESCRIPTION = True
JIRA_AUTH = ('', '')

REVIEWBOARD_URL = 'http://localhost/{review}'
WIKI_URL = 'http://localhost/{user}'

# WEBHOOKS SETTINGS
WEBHOOKS_PORT = 8080
WEBHOOKS_CREDENTIALS = []  # Tuples of (user, pass)


if 'HELGA_SETTINGS' in os.environ:  # pragma: no cover
    try:
        path = os.environ['HELGA_SETTINGS']
        overrides = __import__(path, {}, {}, [path.split('.')[-1]])
    except ImportError:
        warnings.warn('Unabled to import HELGA_SETTINGS override. Is it on sys.path?')
    else:
        this = sys.modules[__name__]
        for attr in filter(lambda x: not x.startswith('_'), dir(overrides)):
            setattr(this, attr, getattr(overrides, attr))
