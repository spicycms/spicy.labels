from django.db import models


class AbstractLabelsConsumer(models.Model):
    class Meta:
        abstract = True

    @property
    def labels(self):
        return self.label_set.all()

    @labels.setter
    def labels(self, ids):
        """
        Set labels from ids.
        """
        self.label_set.clear()
        from .models import Label

        for label_id in ids:
            Label.objects.get(pk=label_id).consumers.add(self)
