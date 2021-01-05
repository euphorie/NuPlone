from zope.dottedname.resolve import resolve

import six


# I am not going to document this. This is a essentially workaround
# http://code.google.com/p/dexterity/issues/detail?id=123


def FieldWidgetFactory(factory, **kw):
    if isinstance(factory, six.string_types):
        factory = resolve(factory)

    def wrapper(field, request):
        widget = factory(field, request)
        for (key, value) in kw.items():
            setattr(widget, key, value)
        return widget

    return wrapper
