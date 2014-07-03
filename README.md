# djangocms-styledlink

A universal, styled link plugin for django-cms.

Why would you use this instead of the djangocms-link Plugin? Well, imagine
that you have a number of CMS pages, but you've also defined an app-hook which
has a list-view and a detail view that displays any number of model objects?
At best, your operator would have to type in the url to that object which is
both annoying for the operator and brittle for the system. If the object's
absolute_url changes, the link will probably 404 until it is updated.

This plugin also provides more comprehensive support for different link types
(intra-page, intra-site and external) and better search-engine support.

The plugin can be used in any placeholder and is "text-enabled" for use in
text plugins such as djangocms-text-ckeditor.

This code is tested to work with Python 2.7, Django 1.6 and django-cms 3.0,
but should work fine with older versions of each (within reason). One thing to
note is that users of Python < 2.7 may need to install `importlib` from
https://pypi.python.org/pypi/importlib/.

```` python
# This is NOT needed for Django 2.7+
pip install importlib
````

### Optional but Recommended

If [`django-easy-select2`](https://github.com/asyncee/django-easy-select2) is
available, its Select2 widget will be used in the plugin. This not only
provides a much more attractive select box (the venerable
[Select2](http://ivaynberg.github.io/select2/)), but also provides enhanced
useability by allow the operator to narrow the available choices by typing in
string. Note the screenshot below does **not** use select2, but standard
Django ChoiceField's widget (a normal select element).


## Operator Configuration

Operators can configure the link to go to:

*   A hash (works by itself for linking to an anchor on the current page, or
    on an internal object page);
*   An internal object (more below);
*   An external URL;

In addition to being very flexible with the link destination, the operator can
also affect:

*   The linked text;
*   The link’s title attribute for browser implemented tooltips;
*   The target attribute to open the link in one of `same window` (default),
    `new window`, `parent window`, `top-most frame`;
*   Whether search engines should follow this link when indexing via the
    rel="nofollow" attribute.
*   Zero or more styles as defined by the developer (see below);


#### Other Features

*   This plugin is also 'allow_children' enabled, so, it can "wrap" other
    content plugins like images, by accepting them as children plugins;
*   Destination model objects URLs are updated as they change, preventing
    broken links in most cases.
*   If the destination model object is deleted, this plugin will "decay" from
    a link to normal text, so that broken links are not left all over
    your project.

#### Features coming soon!

*   A management tool to assist in finding plugins whose destination objects
    no longer exist.


## Developer Configuration

### Available Internal Destination Choices

The developer can easily configure which internal objects may be link
destinations as follows:

In the projects settings.py, define the setting `DJANGOCMS_STYLEDLINK_MODELS`.

By default, this is set to:

```` python
DJANGOCMS_STYLEDLINK_MODELS = [
    {
        'type': 'CMS Pages',
        'class_path': 'cms.models.Page',
        'manager_method': 'public',
        'filter': { 'publisher_is_draft': False },
    }
]
````

which will allow the user to select any published CMS Page as an internal
destination.

The developer may update this setting to include other models as well. Each
model is specified within its own dict.  The resulting drop-down list will
contain objects grouped by their `type`.  The order of the `type`s in the list
is defined by the order of their definition in this setting.

The only required attribute for each model is `class_path`, which must be the
full path to the model.

Additional attributes are:

* `type`: This is the name that will appear in the grouped dropdown menu. If
not specified, the name of the class will be used E.g., "Page".

* `filter`: You can specify additional filtering rules here. This must be
specified as a dict but is converted directly into kwargs internally, so,
`{'published': True}` becomes `filter(published=True)` for example.

* `order_by`: Specify the ordering of any found objects exactly as you would
in a queryset. If this is not provided, the objects will be ordered in the
natural order of your model, if any.


NOTE: Each of the defined models **must** define a get_absolute_url() method
on its objects or the configuration will be rejected.

NOTE: At this time, all choices are rendered as a grouped drop-down list. If
your project will present a very large number of choices for the configured
models, you should consider another solution until we can find another
solution for this project.


#### An example of multiple types.

```` python
DJANGOCMS_STYLEDLINK_MODELS = [
    {
        'type': 'Clients',
        'class_path': 'myapp.Client',
        'manager_method': 'published',
        'order_by': 'title'
    },
    {
        'type': 'Projects',
        'class_path': 'myapp.Project',
        'filter': { 'approved': True },
        'order_by': 'title',
    },
    {
        'type': 'Solutions',
        'class_path': 'myapp.Solution',
        'filter': { 'published': True },
        'order_by': 'name',
    }
]

````


### Link Styles

The developer can also define a number of link styles. These are "defined" by
creating the appropriate CSS class and rules and adding this class to the
StyledLinkStyle objects in the appropriate Administration panel.

The template for the resulting link is carefully crafted using only `<span>`'s
so that the link will work as a inline element and, with appropriate styling,
as an inline-block or even block-level element.

```` html
<span class="plugin_styledlink [Selected StyledLink Style classnames]">
    <span class="inner">
        [ link and link content ]
    </span>
</span>
````

We've found this to be extremely flexible and allows for a wide variety of
styles, but if you find this is too limiting, you may override the template in
the normal Django manner.

Note that the operator can choose **multiple** styles at the same time, so the
CSS rules should allow for this, carefully considering how combinations of
styles should render.


## Preview of plugin

This is an animated GIF preview of the plugin UI for a ficticious set of data.
It alternates between the plain form and with the drop-menu menu invoked.

![](repo_images/djangocms_styledlink-preview.gif?raw=true)
