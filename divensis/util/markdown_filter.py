from django_markup.filter import MarkupFilter
 
class MarkdownMarkupFilter(MarkupFilter):
    """
    Applies Markdown conversion to a string, and returns the HTML. If the
    pygments library is installed, it highlights code blocks with it.
    """
    title = 'Markdown'
    use_pygments = False
 
    def __init__(self):
        try:
            # Check if pygments is installed and highlight code blocks.
            import pygments
            self.use_pygments = True
        except ImportError:
            pass
 
    def render(self, text, **kwargs):
        from markdown import markdown
        #text = markdown(text, **kwargs)
        if self.use_pygments:
            text = markdown(text, ['codehilite'], **kwargs)
        else:
            text = markdown(text, **kwargs)
        return text