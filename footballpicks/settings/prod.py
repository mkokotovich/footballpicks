# flake8: noqa
from footballpicks.settings.common import *


DEBUG = False

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
