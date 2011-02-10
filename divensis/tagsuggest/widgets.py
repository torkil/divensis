from django.forms.widgets import Input
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

class TaggingSuggestWidget(Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        search_url = reverse('tagsuggest_search')
        html = super(TaggingSuggestWidget, self).render(name, value, attrs)
        # TODO: Add jQuery(document).ready()-stuff. Just need to find
        # an ok jQuery script first...
        js = u'''
            <script type="text/javascript">
            $(document).ready(function() {
                var autocomplete = new $.TextboxList(
                    '#%s',
                    {
                        unique: true,
                        plugins: {
                            autocomplete: {
                                minLength: 1,
                                queryRemote: true,
                                remote: {url: '%s'}
                            }
                        }
                    }
                );
            });
            </script>
            ''' % (attrs['id'], search_url)
        return mark_safe("\n".join([html, js]))

    class Media:
        # TODO: Make setting for path
        base_url = '%stagsuggest' % settings.MEDIA_URL
        css = {
            'all': ('%s/TextboxList.css' % base_url,
                    '%s/TextboxList.Autocomplete.css' % base_url),
        }
        js = (
            '%s/GrowingInput.js' % base_url,
            '%s/TextboxList.js' % base_url,
            '%s/TextboxList.Autocomplete.js' % base_url,
        )
