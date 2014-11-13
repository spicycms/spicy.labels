from django.conf import settings

USE_DEFAULT_LABEL_MODEL = getattr(settings, 'USE_DEFAULT_LABEL_MODEL', True)
CUSTOM_LABEL_MODEL = (
    'labels.Label' if USE_DEFAULT_LABEL_MODEL else
    settings.CUSTOM_LABEL_MODEL)


LABELS_CONSUMER = getattr(settings, 'LABELS_CONSUMER', None)
LABEL_CHOICE_COLOR_DEFAULT = getattr(
    settings, 'LABEL_CHOICE_COLOR_DEFAULT', 'tag-1')
LABEL_CHOICE_COLOR = getattr(
    settings, 'LABEL_CHOICE_COLOR', (('tag-1', 'tag-1'),
    ('tag-2', 'tag-2'), ('tag-3', 'tag-3'), ('tag-4', 'tag-4')))
