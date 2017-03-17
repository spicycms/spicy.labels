# Подключение модуля spicy.labels

## settings.py:

    SERVICES = (
        ...
        'spicy.labels.services.LabelService',
        ...
    )

    INSTALLED_APPS = [
        ...
        'spicy.labels',
        ...
    ]

    LABELS_CONSUMER = 'webapp.<Model_name>'

## urls.py:

    url(r'^', include('spicy.labels.urls', namespace='labels')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

## webapp/models.py:

    from spicy.labels.abs import AbstractLabelsConsumer

    class <Model_name>(AbstractLabelsConsumer):
        pass

## кастомизация меток:

### settings.py:

    USE_DEFAULT_LABEL_MODEL = False
    CUSTOM_LABEL_MODEL = 'webapp.Label'

### webapp/models.py:

    from spicy.labels.abs import AbstractLabel

    class Label(AbstractLabel):
        class Meta(AbstractLabel.Meta):
            abstract = False

        def get_main_content(self):
            pass

## templates:

Обратите внимание! здесь используется определенный {% formfied %} он задан в spicy.core
Если произвоится подключение для spicy.document код добавляется в следующий шаблон:
webapp/templates/spicy.document/admin/parts/edit_document_form.html

    {% load spicy_admin %}{% load url from future %}

    <div class="span6">
	    <ul class="padded separate-sections">
            {% url "labels:admin:autocomplete" as autocomplete_url %}
            {% url "labels:admin:get-data" as data_url %}
            {% formfield "" form "labels" "li-select2" ajax_url=autocomplete_url data_url=data_url %}
        </ul>
    </div>
