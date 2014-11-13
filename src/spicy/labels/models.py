from . import defaults, abs

if defaults.USE_DEFAULT_LABEL_MODEL:
    class Label(abs.AbstractLabel):

        class Meta(abs.AbstractLabel.Meta):
            abstract = False
