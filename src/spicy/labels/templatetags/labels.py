from django import template
from django.db.models import Count
from spicy.labels import models
import datetime
from spicy.utils import get_custom_model_class
from spicy.labels import defaults
from django.core.paginator import Paginator

Doc = get_custom_model_class(defaults.LABELS_CONSUMER)

register = template.Library()


@register.filter
def top_labels(num):
    now = datetime.datetime.now()
    return models.Label.objects.filter(
            document__is_public=True, document__pub_date__lte=now,
        ).values('text').annotate(Count('text')).order_by('-text__count')[:num]


@register.simple_tag(takes_context=True)
def all_labels(context, num=None):
    context['labels'] = models.Label.objects.annotate(
        Count('consumers')).select_related().order_by('-consumers__count')[:num]
    return ""


class LabelNode(template.Node):
    def __init__(
            self, nodelist, slug, num_per_page=None,
            paginate=False, object_name='doc', 
            filter_query=None, show_all=False):
        self.nodelist = nodelist
        self.slug = template.Variable(slug)
        self.num_per_page = template.Variable(
            num_per_page if num_per_page else '10')
        self.paginate = paginate
        self.show_all = show_all
        self.object_name = object_name
        self.filter_query = [
            q.split('=') for q in (filter_query or '').split(',') if q]

    def render(self, context):
        for var in (True, False, None):
            # Not needed in Django 1.5?
            context[unicode(var)] = var

        try:
            slug = self.slug.resolve(context)
        except:
            slug = None

        label = models.Label.objects.get(slug=slug)
        objects = Doc.objects.filter(label=label)

        def get_vars((k, v)):
            try:
                return k, template.Variable(v).resolve(context)
            except template.VariableDoesNotExist:
                return ()

        if self.filter_query:
            objects = objects.filter(
                **dict(filter(
                    None, (get_vars(item) for item in self.filter_query))))

        if self.paginate:
            request = context.get('request')
            if request:
                try:
                    page_num = int(request.GET.get('page', 1))
                except ValueError:
                    page_num = 1

            paginator = Paginator(objects, self.num_per_page.resolve(context))
            context['paginator'] = paginator
            page = paginator.page(page_num)
            context['pages'] = page
            paginator.current_page = page
            objs = page.object_list
        else:
            objs = objects[:self.num_per_page.resolve(context)]

        results = []
        last_obj = len(objs) - 1
        for i, obj in enumerate(objs):
            context[self.object_name] = obj
            context['label_counter'] = i
            context['last_label'] = i == last_obj
            try:
                result = self.nodelist.render(context)
                results.append(result)
            except Exception:
                pass
        return ''.join(results)
        


@register.tag
def label(parser, token):
    bits = token.split_contents()
    remaining_bits = bits[1:]

    options = {'show_all': False}

    try:
        options['slug'] = remaining_bits.pop(0)
    except IndexError:
        raise template.TemplateSyntaxError('Invalid category block syntax')

    try:
        num_per_page = remaining_bits.pop(0)
    except IndexError:
        num_per_page = 10

    if num_per_page == u'all':
        num_per_page = None
    else:
        options['num_per_page'] = num_per_page

    while remaining_bits:
        option = remaining_bits.pop(0)
        if option == 'paginate':
            options['paginate'] = True
            continue
        elif option == 'all':
            options['show_all'] = True
            continue
        elif option in ('as', 'where'):
            obj_name = remaining_bits.pop(0)
            if option == 'as':
                options['object_name'] = obj_name
            else:
                options['filter_query'] = obj_name
        else:
            raise template.TemplateSyntaxError('Invalid category block syntax')

    nodelist = parser.parse(('endlabel',))
    parser.delete_first_token()
    return LabelNode(nodelist, **options)
