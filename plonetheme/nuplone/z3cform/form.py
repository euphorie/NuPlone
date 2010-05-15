from zope.dottedname.resolve import resolve

def FieldWidgetFactory(factory, **kw):
    if isinstance(factory, basestring):
        factory=resolve(factory)
    def wrapper(field, request):
        widget=factory(field, request)
        for (key,value) in kw.items():
            setattr(widget, key, value)
        return widget
    return wrapper



