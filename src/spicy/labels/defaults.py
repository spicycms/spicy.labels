from django.conf import settings

LABELS_CONSUMER = getattr(settings, 'LABELS_CONSUMER', None)
LABEL_CHOICE_COLOR_DEFAULT = getattr(
    settings, 'LABEL_CHOICE_COLOR_DEFAULT', 'tag-1')
LABEL_CHOICE_COLOR = getattr(
    settings, 'LABEL_CHOICE_COLOR', (('tag-1', 'tag-1'),
    ('tag-2', 'tag-2'), ('tag-3', 'tag-3'), ('tag-4', 'tag-4')))
