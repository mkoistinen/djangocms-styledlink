# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import StyledLinkStyle


class StyledLinkStyleAdmin(admin.ModelAdmin):
	pass

admin.site.register(StyledLinkStyle, StyledLinkStyleAdmin)