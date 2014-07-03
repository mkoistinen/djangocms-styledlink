# -*- coding: utf-8 -*-

import warnings
from importlib import import_module
from django.conf import settings
from django.db import models
from django.utils.encoding import force_unicode
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from cms.models import CMSPlugin


if hasattr(settings, 'DJANGOCMS_STYLEDLINK_MODELS'):
    DJANGOCMS_STYLEDLINK_MODELS = settings.DJANGOCMS_STYLEDLINK_MODELS
else:
    DJANGOCMS_STYLEDLINK_MODELS = [{
        'type': 'CMS Pages',
        'class_path': 'cms.models.Page',
        'manager_method': 'public',
        'filter': { 'publisher_is_draft': False },
    }]

#
# Let's make sure that we can load the given configuration...
#
STYLEDLINK_MODELS = []
for model in DJANGOCMS_STYLEDLINK_MODELS:
    parts = model['class_path'].rsplit('.', 1)

    try:
        # Ensure we can resolve this class
        cls = getattr(import_module(parts[0]), parts[1])
    except:
        warnings.warn('djangocms_styledlink: Unable to resolve model: %s. Skipping...' % model['class_path'], SyntaxWarning)
        continue

    # Check that the class defines a get_absolute_url() method on its objects.
    if 'get_absolute_url' not in cls.__dict__:
        warnings.warn('djangocms_styledlink: Model %s does not appear to define get_absolute_url() for its object. Skipping...' % model['class_path'], SyntaxWarning)
        continue

    # Check that any manager method defined is legit
    if 'manager_method' in model and not getattr(cls.objects, model['manager_method']):
        warnings.warn('djangocms_styledlink: Specified manager_method %s for model %s does not appear to exist. Skipping...' %(model['manager_method'], model['class_path'], ), SyntaxWarning)
        continue

    ok = True
    if 'filter' in model:
        for field in model['filter'].iterkeys():
            try:
                cls._meta.get_field_by_name(field.split('__')[0])
            except models.FieldDoesNotExist:
                warnings.warn('StyledLink: Defined filter expression refers to a field (%s) in model %s that do not appear to exist. Skipping...' % (field, model['class_path'], ), SyntaxWarning)
                ok = False
                break
    if not ok:
        continue

    if 'order_by' in model:
        fields = model['order_by'].split(',')
        # Strip any leading -/+ chars
        fields = [ f.translate(None, '-+') for f in fields ]
        for field in fields:
            try:
                cls._meta.get_field_by_name(field)
            except models.FieldDoesNotExist:
                warnings.warn('StyledLink: Defined order_by expression refers to a field (%s) in model %s that do not appear to exist. Skipping...' % (field, model['class_path'], ), SyntaxWarning)
                ok = False
                break;
    if not ok:
        continue

    #
    # Still here? Awesome...
    # Store the class name for our use.
    #
    model.update({
        '_cls_name': parts[1]
    })

    # Add this configuration
    STYLEDLINK_MODELS.append(model)


class StyledLinkStyle(models.Model):

    label = models.CharField(_('label'),
        max_length=32,
        default='',
        help_text=_('The internal name of this link style.'),
    )

    link_class = models.CharField(
        _('link class'),
        max_length=32,
        default='',
        help_text=('The class to add to this link (do NOT preceed with a ".").'),
    )

    def __unicode__(self):
        return self.label


class StyledLink(CMSPlugin):

    """
    A link to an other page or to an external website
    """

    label = models.CharField(_('link text'),
        blank=True,
        default='',
        help_text=_("Required. The text that is linked."),
        max_length=255,
    )

    title = models.CharField(_('title'),
        blank=True,
        default='',
        help_text=_("Optional. If provided, will provide a tooltip for the link."),
        max_length=255,
    )

    int_destination_type = models.ForeignKey(ContentType,
        null=True,
        blank=True,
        limit_choices_to={"model__in": [ model['_cls_name'] for model in STYLEDLINK_MODELS ]},
    )

    int_destination_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    int_destination = generic.GenericForeignKey(
        'int_destination_type',
        'int_destination_id',
    )

    #
    # Hash, for current page or internal page destination
    #
    page_destination = models.CharField(_('intra-page destination'),
        blank=True,
        help_text=_(u'Use this to specify an intra-page link. Can be used for the <em>current page</em> or with a specific internal destination. Do <strong>not</strong> include a leading “#”.'),
        max_length=64,
    )

    #
    # See note in save()
    #
    int_hash = models.BooleanField(default=False)

    #
    # External links
    #
    ext_destination = models.TextField(_('external destination'),
        blank=True,
        default='',
    )

    ext_follow = models.BooleanField(_('follow external link?'),
        default=True,
        help_text=_('Let search engines follow this hyperlink?'),
    )

    mailto = models.EmailField(
        _("email address"),
        blank=True,
        null=True,
        help_text=_("An email address. This will override an external url."),
    )

    target = models.CharField(_("target"),
        blank=True,
        choices=((
            ("", _("same window")),
            ("_blank", _("new window")),
            ("_parent", _("parent window")),
            ("_top", _("topmost frame")),
        )),
        default='',
        help_text=_('Optional. Specify if this link should open in a new tab or window.'),
        max_length=100,
    )

    styles = models.ManyToManyField(StyledLinkStyle,
        blank=True,
        default=None,
        null=True,
        help_text=_('Optional. Choose one or more styles for this link.'),
        related_name='styled_link_style',
        verbose_name=_("link style"),
    )


    @property
    def link(self):
        """Returns the specified destination url"""

        if self.int_destination:
            # This is an intra-site link and the destination object is still
            # here, nice.
            url = self.int_destination.get_absolute_url()
            if self.page_destination:
                # Oooh, look, it also has a hash component
                return u'%s#%s' % (url, self.page_destination, )
            return url
        elif self.page_destination and not self.int_hash:
            # OK, this was just an intra-page hash
            return u'#%s' % (self.page_destination, )
        elif self.ext_destination:
            # External link
            return self.ext_destination
        elif self.mailto:
            # Mailto: link
            return u'mailto:%s' % (self.mailto, )
        else:
            return ''


    def save(self, **kwargs):
        #
        # We always need to remember if `page_destination` (hash) was set in
        # the context of `int_destination` (internal cms page/model view)
        # because if it was, and the `int_destination` object was subsequently
        # deleted, then the page_destination by itself would mistakenly be
        # applied to the *current* page.
        #
        self.int_hash = bool(self.int_destination and self.page_destination)

        #
        # As a convenience, if the operator omits the label, extract one from
        # the linked model object.
        #
        if not self.label and self.int_destination:
            self.label = force_unicode(self.int_destination)

        super(StyledLink, self).save(**kwargs)


    def copy_relations(self, oldinstance):
        self.styles = oldinstance.styles.all()


    def __unicode__(self):
        return self.label
