from django.template import Library, Node, TemplateSyntaxError, Variable
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache

from divensis.util.decorators import basictag, blocktag

# many of the following tags are from
# from http://svn.navi.cx/misc/trunk/djblets/

register = Library()

@register.filter
def realname(user):
    """
    Returns the real name of a user, if available, or the username.

    If the user has a full name set, this will return the full name.
    Otherwise, this returns the username.
    
    Usage::
        {{ object.user|realname }}    
    """
    full_name = user.get_full_name()
    if full_name == '':
        return user.username
    else:
        return full_name


@register.tag
@blocktag
def definevar(context, nodelist, varname):
    """
    Defines a variable in the context based on the contents of the block.
    This is useful when you need to reuse the results of some tag logic
    multiple times in a template or in a blocktrans tag.
    
    Usage::
        {% definevar %}{{ some_output }}{% enddefinevar %}
    
    """
    context[varname] = nodelist.render(context)
    return ""


@register.filter
def humanize_list(value):
    """
    Humanizes a list of values, inserting commands and "and" where appropriate.

      ========================= ======================
      Example List              Resulting string
      ========================= ======================
      ``["a"]``                 ``"a"``
      ``["a", "b"]``            ``"a and b"``
      ``["a", "b", "c"]``       ``"a, b and c"``
      ``["a", "b", "c", "d"]``  ``"a, b, c, and d"``
      ========================= ======================
    
    Usage::
        {{ some_list|humanize_list }}
    
    """
    if len(value) == 0:
        return ""
    elif len(value) == 1:
        return value[0]

    s = ", ".join(value[:-1])

    if len(value) > 3:
        s += ","

    #return "%s and %s" % (s, value[-1])
    # added translation string
    return "%s %s %s" % (s, _('and'), value[-1])


class TwitterStatusNode(Node):
    def __init__(self, tweet):
        self.tweet = tweet

    def render(self, context):
        import twitter
        try:
            cache_key = 'twitter_status_%s'%settings.TWITTER_USERNAME
            most_recent_status = cache.get(cache_key)
            if most_recent_status is None:
                api = twitter.Api()
                most_recent_status = api.GetUserTimeline(settings.TWITTER_USERNAME)[0]
                cache.set(cache_key, most_recent_status)
            context[self.tweet] = {
                "status": "%s" % most_recent_status.text,
                "username": "%s" % settings.TWITTER_USERNAME,
                "url": "http://twitter.com/%s/statuses/%s" % (settings.TWITTER_USERNAME, most_recent_status.id),
                "url_user": "http://twitter.com/%s" % (settings.TWITTER_USERNAME),
                "time": "%s" % most_recent_status.relative_created_at,
            }
        except:
            context[self.tweet] = {
                "status": "Ack! Looks like Twitter's codes are broken!",
                "username": "",
                "url": "",
                "url_user": "",
                "time": "",
            }
        return ''

@register.tag(name='get_twitter_status')
def twitter_status(parser, token):
    """
    Gets twitter status and assigns it to a given template context variable.
        
    Usage::
        {% get_twitter_status as tweet %}
    """
    bits = token.split_contents()
    if len(bits) != 3:
            raise TemplateSyntaxError, "%s takes 2 arguments" % bits[0]
    if bits[1] != "as":
        raise TemplateSyntaxError, "First argument for %s should be 'as'" % bits[0]
    return TwitterStatusNode(bits[2])


class EncryptEmail(Node):
    def __init__(self, context_var):
        self.context_var = Variable(context_var)# context_var
    def render(self, context):
        import random
        email_address = self.context_var.resolve(context)
        character_set = '+-.0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
        char_list = list(character_set)
        random.shuffle(char_list)
        
        key = ''.join(char_list)
        
        cipher_text = ''
        id = 'e' + str(random.randrange(1,999999999))
        
        for a in email_address:
            cipher_text += key[ character_set.find(a) ]
            
        script = 'var a="'+key+'";var b=a.split("").sort().join("");var c="'+cipher_text+'";var d="";'
        script += 'for(var e=0;e<c.length;e++)d+=b.charAt(a.indexOf(c.charAt(e)));'
        script += 'document.getElementById("'+id+'").innerHTML="<a href=\\"mailto:"+d+"\\">"+d+"</a>"'
        script = "eval(\""+ script.replace("\\","\\\\").replace('"','\\"') + "\")"
        script = '<script type="text/javascript">/*<![CDATA[*/'+script+'/*]]>*/</script>'
        return '<span id="'+ id + '">[javascript protected email address]</span>'+ script
 
 
@register.tag
def encrypt_email(parser, token):
    """
        This template tag encrypts the email address and generates a equivalent Javascript code that
        can decrypt it. This Javascript produce an email link when it runs on browser. As most bots
        and spider don't executes Javascript they wouldn't be able to extract mail addresses. While
        a visitor of your web page will not notice that you used this script as long as he/she has
        javascript enabled.
        
        A normal visitor with a javascript enabled browser will find no difference. The visitor with
        non-javascript browser will see "[javascript protected email address]" in stead of the
        e-mail address.
        
        Usage::
            {% encrypt_email user.email %}
    """
 
    tokens = token.contents.split()
    if len(tokens)!=2:
        raise TemplateSyntaxError("%r tag accept two argument" % tokens[0])
    return EncryptEmail(tokens[1])
#register.tag('encrypt_email', encrypt_email)