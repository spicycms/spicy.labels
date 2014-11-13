# coding = utf-8
from django.utils.translation import ugettext_lazy as _
from spicy.core.service import api
from spicy.utils.models import get_custom_model_class
from . import defaults


class LabelService(api.Interface):
    name = 'label'
    label = _('Label provider service')

    def __init__(self):
        self.label_model = get_custom_model_class(defaults.CUSTOM_LABEL_MODEL)

        api.Interface.__init__(self)

    def get_label(self, manager='objects', **kwargs):
        model_manager = getattr(self.label_model, manager)
        return model_manager.get(**kwargs)

    def get_labels(self, manager='objects', **kwargs):
        model_manager = getattr(self.label_model, manager)
        return model_manager.filter(**kwargs)
