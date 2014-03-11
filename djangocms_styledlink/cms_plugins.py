# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import StyledLink
from .forms import StyledLinkForm


class StyledLinkPlugin(CMSPluginBase):
    model = StyledLink
    form = StyledLinkForm
    name = _("Styled Link")
    render_template = "djangocms_styledlink/styled_link.html"
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder,
        })
        return context

    def get_form(self, request, obj=None, **kwargs):
        Form = super(StyledLinkPlugin, self).get_form(request, obj, **kwargs)

        class FakeForm(object):
            def __init__(self, Form, site):
                self.Form = Form
                self.site = site
                self.base_fields = Form.base_fields

            def __call__(self, *args, **kwargs):
                # instanciate the form on call
                form = self.Form(*args, **kwargs)
                return form

        if self.cms_plugin_instance.page and self.cms_plugin_instance.page.site:
            site = self.cms_plugin_instance.page.site
        elif self.page and self.page.site:
            site = self.page.site
        else:
            site = Site.objects.get_current()

        return FakeForm(Form, site)


    def icon_src(self, instance):
        return settings.STATIC_URL + u"cms/img/icons/plugins/link.png"


plugin_pool.register_plugin(StyledLinkPlugin)
