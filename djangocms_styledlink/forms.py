# -*- coding: utf-8 -*-

import re
from importlib import import_module

# from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms import CharField, ChoiceField, Textarea
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import StyledLink, STYLEDLINK_MODELS


class StyledLinkForm(ModelForm):
    """Form for creating a link to many of the types of CMS or Application Objects."""

    class Meta:
        model = StyledLink
        fields = (
            'label',
            'title',
            'page_destination',
            'int_destination',
            'ext_destination', 'target', 'ext_follow',
            'styles',
        )

    # We have a special set of widget parameters for long URL fields
    ext_destination = CharField(
        required=False,
        widget=Textarea(attrs={'rows': 2, 'cols': 80, }),
        help_text=_('Link to an external destination. Specify full absolute URL e.g. "http://blah.com/page.html".')
    )


    #
    # GenericForeignKey form field, will hold combined object_type and
    # object_id. Also we attempt to use a easy-select2 widget, if it is
    # available, if not, just use a regular ChoiceField and whatever widget
    # Django uses for that (Select).
    #
    try:
        from easy_select2.widgets import Select2
        int_destination = ChoiceField(
            required=False,
            help_text=_('Link to an internal destination.'),
            widget=Select2(select2attrs={'width': '262px'}),
        )
    except:
        int_destination = ChoiceField(
            required=False,
            help_text=_('Link to an internal destination.'),
        )

    def __init__(self, *args, **kwargs):
        super(StyledLinkForm, self).__init__(*args, **kwargs)

        #
        # Combine object_type and object_id into a single 'int_destination'
        # field Get all the objects that we want the user to be able to choose
        # from.
        #
        # For the objects, if its not convenient to sort in the queryset, (I'm
        # looking at you django-cms), then just set 'sorted=False' and we'll
        # do it below, based on the sort values.
        #
        available_objects = []

        for item in STYLEDLINK_MODELS:
            if 'type' in item:
                model = item['type']
            else:
                model = item['_cls_name']

            parts = item['class_path'].rsplit('.', 1)
            cls = getattr(import_module(parts[0]), parts[1])
            queryset = cls.objects

            if 'manager_method' in item:
                queryset = getattr(queryset, item['manager_method'])()

            if 'filter' in item:
                for (k, v) in item['filter'].items():
                    try:
                        # Attempt to execute any callables in the filter dict.
                        item['filter'][k] = v()
                    except TypeError:
                        # OK, it wasn't a callable, so, leave it be
                        pass
                queryset = queryset.filter(**item['filter'])
            else:
                if not 'manager_method' in item:
                    queryset = queryset.all()

            if 'order_by' in item:
                queryset = queryset.order_by(item['order_by'])

            available_objects.append({
                'model': model,
                'objects': list(queryset),
            })

        # Now create our list of choices for the <select> field
        object_choices = []
        object_choices.append(("", "--", ))

        for group in sorted(available_objects):

            obj_list = []
            for obj in group['objects']:

                type_class = ContentType.objects.get_for_model(obj.__class__)
                type_id = type_class.id
                obj_id = obj.id
                form_value = "type:%s-id:%s" % (type_id, obj_id)
                display_text = str(obj)

                obj_list.append((form_value, display_text))

            object_choices.append(( group['model'], obj_list, ))

        self.fields['int_destination'].choices = object_choices

        # If there is an existing value, pre-select it
        if self.instance.int_destination:
            type_class = ContentType.objects.get_for_model(self.instance.int_destination.__class__)
            type_id = type_class.id
            obj_id = self.instance.int_destination.id
            current_value = "type:%s-id:%s" % (type_id, obj_id)
            self.fields['int_destination'].initial = current_value

    def save(self, *args, **kwargs):
        try:
            # get object_type and object_id values from combined int_destination field
            object_string = self.cleaned_data['int_destination']
            matches = re.match("type:(\d+)-id:(\d+)", object_string).groups()
            object_type_id = matches[0]  # get 45 from "type:45-id:38"
            object_id = matches[1]       # get 38 from "type:45-id:38"
            object_type = ContentType.objects.get(id=object_type_id)
            self.cleaned_data['int_destination_type'] = object_type_id
            self.cleaned_data['int_destination_id'] = object_id
            self.instance.int_destination_id = object_id
            self.instance.int_destination_type = object_type
        except:
            self.cleaned_data['int_destination_type'] = None
            self.cleaned_data['int_destination_id'] = None
            self.instance.int_destination_id = None
            self.instance.int_destination_type = None

        return super(StyledLinkForm, self).save(*args, **kwargs)
