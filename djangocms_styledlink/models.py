# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from cms.models import CMSPlugin


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

    #
    # These are the supported types of things we can link to internally. Soon,
    # this will be moved to settings.STYLED_LINK_MODELS for more universal
    # usability.
    #
    SUPPORTED_MODELS = (
        "Page",
    )

    label = models.CharField(_('link text'),
        blank=False,
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
        limit_choices_to={"model__in": SUPPORTED_MODELS},
    )

    int_destination_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    int_destination = generic.GenericForeignKey('int_destination_type', 'int_destination_id')

    #
    # Hash, for current page or internal page destination
    #
    page_destination = models.CharField(_('intra-page destination'),
        blank=True,
        help_text=_(u'Use this to specify an intra-page link. Can be used for the <em>current page</em> or with a specific internal destination. Do <strong>not</strong> include a leading “#”.'),
        max_length=64,
    )

    # External links
    ext_destination = models.TextField(_('external destination'), default='', blank=True)
    ext_follow = models.BooleanField(_('follow external link?'), default=True, help_text=_('Let search engines follow this hyperlink?'))

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
        help_text=_('Optional. Specify if this link should open in a new tab or window.'),
        max_length=100,
    )

    styles = models.ManyToManyField(StyledLinkStyle,
        blank=True,
        default=1,
        null=True,
        help_text=_('Optional. Choose one or more styles for this link.'),
        related_name='styled_link_style',
        verbose_name=_("link style"),
    )


    def copy_relations(self, oldinstance):
        self.styles = oldinstance.styles.all()


    @property
    def link(self):

        """Returns the specified destination url"""

        if self.int_destination:
            url = self.int_destination.get_absolute_url()
            if self.page_destination:
                return u'%s#%s' % (url, self.page_destination, )
            return url
        elif self.page_destination:
            return u'#%s' % (self.page_destination, )
        elif self.ext_destination:
            return self.ext_destination
        elif self.mailto:
            return u'mailto:%s' % (self.mailto, )
        else:
            # Sane default?
            return '#'


    def __unicode__(self):
        return self.label
