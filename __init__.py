# Replace default Markdown-filter
from django_markup.markup import formatter
from divensis.util.markdown_filter import MarkdownMarkupFilter
formatter.update('markdown', MarkdownMarkupFilter)