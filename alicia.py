# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Alicia theme

    @copyright: 2017 Daniel Rus Morales.
    @license: GNU GPL, see COPYING for details.
"""
from cStringIO import StringIO

import bs4
from jinja2 import Environment, Markup, FileSystemLoader, select_autoescape

from MoinMoin import wikiutil, config
from MoinMoin.wikiutil import getLocalizedPage
from MoinMoin.action import get_available_actions
from MoinMoin.Page import Page
from MoinMoin.theme import ThemeBase


class Theme(ThemeBase):

    name = "alicia"

    stylesheets = (
        # media         basename
        ('all',         'bootstrap'),
        ('all',         'pygments'),
        # ('screen',      'screen'),
        ('print',       'print'),
        ('projection',  'projection'),
    )

    # Used in print mode
    stylesheets_print = (
        # media         basename
        ('all',         'bootstrap'),
        ('all',         'print'),
    )

    # Used in slide show mode
    stylesheets_projection = (
        # media         basename
        ('all',         'bootstrap'),
        ('all',         'projection'),
    )

    fa_icons = {
        'help': 'fa fa-lg fa-question-circle',
        'find': 'fa fa-lg fa-search',
        'diff': 'fa fa-lg fa-clone',
        'info': 'fa fa-lg fa-info-circle',
        'edit': 'fa fa-lg fa-pencil',
        'unsubscribe': 'fa fa-lg fa-envelope-o',
        'subscribe': 'fa fa-lg fa-envelope',
        'raw': 'fa fa-lg fa-file-o',
        'xml': 'fa fa-lg fa-file-text-o',
        'print': 'fa fa-lg fa-print',
        'view': 'fa fa-lg fa-eye',
        'home': 'fa fa-lg fa-home',
        'up': 'fa fa-lg fa-arrow-up',
        # FileAttach
        'attach': 'fa fa-lg fa-paperclip',
        'attachimg': 'fa fa-lg fa-file-image-o',
        # RecentChanges
        'rss': 'fa fa-lg fa-rss-square',
        'deleted': 'fa fa-lg fa-trash-o',
        'updated': 'fa fa-lg fa-refresh',
        'renamed': 'fa fa-lg fa-files-o',
        'conflict': 'fa fa-lg fa-times-rectangle',
        'new': 'fa fa-lg fa-plus-square',
        'diffrc': 'fa fa-lg fa-clone',
        # General
        'bottom': 'fa fa-lg fa-arrow-down',
        'top': 'fa fa-lg fa-arrow-up',
        'www': 'fa fa-lg fa-globe',
        'mailto': 'fa fa-lg fa-share',
        'news': 'fa fa-lg fa-newspaper',
        'telnet': 'fa fa-lg fa-phone-square',
        'ftp': 'fa fa-lg fa-exchange',
        'file': 'fa fa-lg fa-file',
        # search forms
        'searchbutton': 'fa fa-lg fa-search',
        'interwiki': 'fa fa-lg fa-users',

        # Emojis.
        'X-(': 'twa twa-lg twa-angry',
        ':D': 'twa twa-lg twa-grin',
        '<:(': 'twa twa-lg twa-frowning',
        ':o': 'twa twa-lg twa-flushed',
        ':(': 'twa twa-lg twa-disappointed',
        ':)': 'twa twa-lg twa-smiley',
        'B)': 'twa twa-lg twa-sunglasses',
        ':))': 'twa twa-lg twa-smile',
        ';)': 'twa twa-lg twa-wink',
        '/!\\': 'fa fa-lg fa-exclamation',
        '<!>': 'fa fa-lg fa-exclamation-triangle',
        '(!)': 'twa twa-lg twa-bulb',

        ':-?': 'twa twa-lg twa-stuck-out-tongue',
        ':\\': 'twa twa-lg twa-confused',
        '>:>': 'twa twa-lg twa-smiling-imp',
        '|)': 'twa twa-lg twa-sweat',

        # some folks use noses in their emoticons
        ':-(': 'twa twa-lg twa-worried',
        ':-)': 'twa twa-lg twa-smiley',
        'B-)': 'twa twa-lg twa-sunglasses',
        ':-))': 'twa twa-lg twa-laughing',
        ';-)': 'twa twa-lg twa-wink',
        '|-)': 'twa twa-lg twa-grinning',

        # version 1.0
        '(./)': 'fa fa-lg fa-check',
        '{OK}': 'twa twa-lg twa-thumbsup',
        '{X}': 'twa twa-lg twa-no-entry-sign',
        '{i}': 'twa twa-lg twa-information-source',
        '{1}': 'twa twa-lg twa-one',
        '{2}': 'twa twa-lg twa-two',
        '{3}': 'twa twa-lg twa-three',

        '{*}': 'fa fa-lg fa-star',
        '{o}': 'fa fa-lg fa-star-o',
    }

    _menu = [
        {
            'label': 'Navigation',
            'entries': [
                'RecentChanges', 'FindPage', 'LocalSiteMap',
                'HelpContents', 'HelpOnMoinWikiSyntax',
            ],
        }, {
            'label': 'Display',
            'entries': [
                'AttachFile', 'info', 'raw', 'print',
            ]
        }, {
            'label': 'Edit',
            'entries': [
                'RenamePage', 'DeletePage', 'revert', 'CopyPage',
                'Load', 'Save', 'Despam', 'editSideBar',
            ]
        }, {
            'label': 'User',
            'entries': [
                'quicklink', 'subscribe',
            ]
        }   
    ]

    def __init__(self, *args, **kwargs):
        ThemeBase.__init__(self, *args, **kwargs)
        self.j2env = Environment(loader=FileSystemLoader(self.cfg.templates_path),
                                 autoescape=select_autoescape(['html', 'xml']))
        
    def make_icon(self, icon, vars=None, **kwargs):
        if icon in self.fa_icons:
            return '<i class="%s" aria-hidden="true"></i>' % self.fa_icons[icon]
        return ThemeBase.make_icon(self, icon, vars=vars, **kwargs) 
    
    def guiEditorScript(self, dic):
        page = dic['page']
        if not (page.isWritable() and
                self.request.user.may.write(page.page_name) and
                self.showBothEditLinks() and
                self.guiworks(page)):
            return None, None
        return (page.url(self.request, querystr={'action': 'edit',
                                                 'editor': 'gui'}),
                self.request.getText('Edit (GUI)'))

    def rsslink(self, dic):
        """Returns a tuple with the title and the href for a link element."""
        page = dic['page']
        if self.shouldUseRSS(page):
            return (wikiutil.escape(self.cfg.sitename, True),   # title
                    wikiutil.escape(self.rsshref(page), True))  # href
        elif self.cfg.rss_show_page_history_link:
            return ("%s: %s" % (wikiutil.escape(self.cfg.sitename, True),
                                wikiutil.escape(page.page_name, True)),  # title
                    wikiutil.escape(page.url(self.request, querystr={
                        'action': 'rss_rc', 'ddiffs': '1', 'unique': '0',
                        'diffs': '1', 'show_att': '1',
                        'page': page.page_name }, escape=0), True))  # href
        else:
            return None, None

    def universal_edit_button(self, dic, **kwargs):
        """Returns a tuple with the title and the href for a link element."""
        page = dic['page']
        if 'edit' in self.request.cfg.actions_excluded:
            return None, None
        if not (page.isWritable() and
                self.request.user.may.write(page.page_name)):
            return None, None
        text = self.request.getText(u'Edit')
        url = page.url(self.request, querystr={'action': 'edit'}, escape=0)
        return text, url        

    def _stylesheet_link(self, theme, media, href, title=None):
        """
        Same as parent class, but returns dictionary with <link> attributes.
        """
        attrs = []
        if theme:
            href= '%s/%s/css/%s.css' % (self.cfg.url_prefix_static,
                                        self.name, href)
        attrs.append({'name': 'type', 'value': "text/css"})
        attrs.append({'name': 'charset', 'value': self.stylesheetsCharset})
        attrs.append({'name': 'media', 'value': media})
        attrs.append({'name': 'href', 'value': wikiutil.escape(href, True)})
        if title:
            attrs.append({'name': 'rel', 'value': "alternate stylesheet"})
            attrs.append({'name': 'title', 'value': title})
        else:
            attrs.append({'name': 'rel', 'value': "stylesheet"})
        return attrs

    def html_stylesheets(self, dic):
        items = []
        request = self.request
        if dic.get('print_mode'):
            media = dic.get('media', 'print')
            stylesheets = getattr(self, 'stylesheets_' + media)
        else:
            stylesheets = self.stylesheets
        items.extend([self._stylesheet_link(True, *stylesheet) for stylesheet in stylesheets])
        items.extend([self._stylesheet_link(False, *stylesheet) for stylesheet in request.cfg.stylesheets])
        # Add user css url (assuming that user css uses same charset)
        href = request.user.valid and request.user.css_url
        if href and href.lower() != "none":
            items.extend(self._stylesheet_link(False, 'all', href))
        return items
    
    def send_title(self, text, **keywords):
        """
        An almost verbatim copy of MoinMoin.theme.__init__.ThemeBase.send_title, 
        that replaces hard coded HTML string template with Jinja2. 
        """
        req = self.request
        _ = req.getText
        rev = req.rev

        if keywords.has_key('page'):
            page = keywords['page']
            pagename = page.page_name
        else:
            pagename = keywords.get('pagename', '')
            page = Page(req, pagename)
        if keywords.get('msg', ''):
            raise DeprecationWarning("Using send_page(msg=) is deprecated! "
                                     "Use theme.add_msg() instead!")
        scriptname = req.script_root

        # get name of system pages
        page_front_page = wikiutil.getFrontPage(req).page_name
        page_help_contents = getLocalizedPage(req, 'HelpContents').page_name
        page_title_index = getLocalizedPage(req, 'TitleIndex').page_name
        page_site_navigation = getLocalizedPage(req, 'SiteNavigation').page_name
        page_word_index = getLocalizedPage(req, 'WordIndex').page_name
        page_help_formatting = getLocalizedPage(req, 'HelpOnFormatting').page_name
        page_find_page = getLocalizedPage(req, 'FindPage').page_name
        home_page = wikiutil.getInterwikiHomePage(req)
        page_parent_page = getattr(page.getParentPage(), 'page_name', None)

        # set content_type, including charset, so web server doesn't touch it:
        req.content_type = "text/html; charset=%s" % config.charset

        meta_keywords = req.getPragma('keywords') or ""
        meta_description = req.getPragma('description') or ""

        rss_link = self.rsslink({'page': page})
        universal_edit_button = self.universal_edit_button({'page': page})
        stylesheets = self.html_stylesheets({'print_media': keywords.get('print_mode', False),
                                             'media': keywords.get('media', 'screen')})
        gui_edit_link = self.guiEditorScript({'page': page})

        context = {
            'title': Markup(wikiutil.escape(text)),
            'sitename': wikiutil.escape(req.cfg.html_pagetitle or req.cfg.sitename),
            'charset': page.output_charset,
            'meta_keywords': wikiutil.escape(meta_keywords, 1),
            'meta_description': wikiutil.escape(meta_description, 1),
            'robots': None,  # might be "index", "noindex", or None
            'refresh_seconds': None,
            'refresh_url': None,
            'static_base': "%s/%s/" % (self.cfg.url_prefix_static, self.name),
            'stylesheets': stylesheets,
            'rss_link_title': rss_link[0],
            'rss_link_href': rss_link[1],
            'universal_edit_button_title': universal_edit_button[0],
            'universal_edit_button_href': universal_edit_button[1],
            'common_js': '%s/common/js/%s.js' % (req.cfg.url_prefix_static, 'common'),
            'search_hint': req.getText('Search'),
            'gui_editor_link_href': gui_edit_link[0],
            'gui_editor_link_text': gui_edit_link[1],
            'extra_html_head': Markup(keywords.get('html_head', '')),
            'page_start_href': req.href(page_front_page),
            'page_alternate_title': None,
            'page_alternate_href': '',
            'print_alternate_title': None,
            'print_alternate_href': '',
            'page_up_href': None,
        }

        # search engine precautions / optimization:
        # if it is an action or edit/search, send query headers (noindex,nofollow):
        if req.query_string or req.method == 'POST':
            context['robots'] = "noindex"
        # we don't want to have BadContent stuff indexed:
        elif pagename in ['BadContent', 'LocalBadContent', ]:
            context['robots'] = "noindex"
        # if it is a special page, index it and follow the links - we do it
        # for the original, English pages as well as for (the possibly
        # modified) frontpage:
        elif pagename in [page_front_page, req.cfg.page_front_page,
                          page_title_index, 'TitleIndex',
                          page_find_page, 'FindPage',
                          page_site_navigation, 'SiteNavigation',
                          'RecentChanges', ]:
            context['robots'] = "index"

        if 'pi_refresh' in keywords and keywords['pi_refresh']:
            context.update({'refresh_seconds': keywords['pi_refresh'][0],
                            'refresh_url': keywords['pi_refresh'][1]})
        
        # Links
        if pagename:
            context.update({'page_alternate_title': _('Wiki Markup'),
                            'page_alternate_href': page.url(req, querystr=dict(action='raw'))})
            context.update({'print_alternate_title': _('Print View'),
                            'print_alternate_href': page.url(req, querystr=dict(action='print'))})
            if page_parent_page:
                context['page_up'] = req.href(page_parent_page)
        
        output = StringIO()
        write_f_onhold = req.write
        req.write = lambda s: output.write(s.encode('utf-8'))
        
        if pagename and req.user.may.read(pagename):
            from MoinMoin.action import AttachFile
            AttachFile.send_link_rel(req, pagename)

        context['attached_links'] = Markup(output.getvalue())
        req.write = write_f_onhold

        context['extra_links'] = [
            {'rel': "Search", 'href': "%s" % req.href(page_find_page)},
            {'rel': "Index", 'href': "%s" % req.href(page_title_index)},
            {'rel': "Glossary", 'href': "%s" % req.href(page_word_index)},
            {'rel': "Help", 'href': "%s" % req.href(page_help_formatting)},
        ]

        template = self.j2env.get_template('bits/head.html')
        output = template.render(context)
        req.write(output)
        
        output = []

        # start the <body>
        bodyattr = []
        if keywords.has_key('body_attr'):
            bodyattr.append(' ')
            bodyattr.append(keywords['body_attr'])

        # Set body to the user interface language and direction
        bodyattr.append(' %s' % self.ui_lang_attr())

        body_onload = keywords.get('body_onload', '')
        if body_onload:
            bodyattr.append(''' onload="%s"''' % body_onload)
        output.append('\n<body%s>\n' % ''.join(bodyattr))

        # Output -----------------------------------------------------------

        # If in print mode, start page div and emit the title
        if keywords.get('print_mode', 0):
            d = {
                'title_text': text,
                'page': page,
                'page_name': pagename or '',
                'rev': rev,
            }
            req.themedict = d
            output.append(self.startPage())
            output.append(self.interwiki(d))
            output.append(self.title(d))

        # In standard mode, emit theme.header
        else:
            exists = pagename and page.exists(includeDeleted=False)
            # prepare dict for theme code:
            d = {
                'theme': self.name,
                'script_name': scriptname,
                'title_text': text,
                'logo_string': req.cfg.logo_string,
                'site_name': req.cfg.sitename,
                'page': page,
                'rev': rev,
                'pagesize': pagename and page.size() or 0,
                # exists checked to avoid creation of empty edit-log for non-existing pages
                'last_edit_info': exists and page.lastEditInfo() or '',
                'page_name': pagename or '',
                'page_find_page': page_find_page,
                'page_front_page': page_front_page,
                'home_page': home_page,
                'page_help_contents': page_help_contents,
                'page_help_formatting': page_help_formatting,
                'page_parent_page': page_parent_page,
                'page_title_index': page_title_index,
                'page_word_index': page_word_index,
                'user_name': req.user.name,
                'user_valid': req.user.valid,
                'msg': self._status,
                'trail': keywords.get('trail', None),
                # Discontinued keys, keep for a while for 3rd party theme developers
                'titlesearch': 'use self.searchform(d)',
                'textsearch': 'use self.searchform(d)',
                'navibar': ['use self.navibar(d)'],
                'available_actions': ['use self.request.availableActions(page)'],
            }

            # add quoted versions of pagenames
            newdict = {}
            for key in d:
                if key.startswith('page_'):
                    if not d[key] is None:
                        newdict['q_'+key] = wikiutil.quoteWikinameURL(d[key])
                    else:
                        newdict['q_'+key] = None
            d.update(newdict)
            req.themedict = d

            # now call the theming code to do the rendering
            if keywords.get('editor_mode', 0):
                output.append(self.editorheader(d))
            else:
                output.append(self.header(d))

        # emit it
        req.write(''.join(output))
        output = []
        self._send_title_called = True

    def get_navigation_items(self, dic):
        """
        Returns a list of dict with the elements of the navigation block.

        Each dictionary item of the returned list contains three attributes.
        A 'name' with the name of the page, an 'href' and an active boolean
        value to indicate whether the page being displayed is the current page.
        """
        found = {}  # Pages found, to prevent duplicates.
        items = []  # Navigation block items.
        curr_page = dic['page_name']

        # Process config navi_bar.
        if self.request.cfg.navi_bar:
            for text in self.request.cfg.navi_bar:
                page_name, page_href = self.splitNavilink(text)
                soup = bs4.BeautifulSoup(page_href, 'html.parser')
                item = {'name': page_name,
                        'href': soup.find('a')['href'],
                        'active': page_name == curr_page}
                found[page_name] = 1
                items.append(item)

        # Add user links to wiki links, eliminating duplicates.
        userlinks = self.request.user.getQuickLinks()
        for text in userlinks:
            # Split text without localization, user knows what she wants.
            page_name, page_href = self.splitNavilink(text, localize=0)
            soup = bs4.BeautifulSoup(page_href, 'html.parser')
            if not page_name in found:
                item = {'name': page_name,
                        'href': soup.find('a')['href'],
                        'active': page_name == curr_page}
                found[page_name] = 1
                items.append(item)

        # Add current page at end of local pages.
        trail = []
        if self.request.user.show_page_trail:
            trail = self.request.user.getTrail()
        if not curr_page in found and not curr_page in trail:
            title = dic['page'].split_title()
            title = self.shortenPagename(title)
            href = dic['page'].url(self.request)
            items.append({'name': title, 'href': href, 'active': True})

        return items

    def get_trail_items(self, dic, exclude=[]):
        """
        Returns a list of dict with the elements of the navigation block.

        Each dictionary item of the return list contains three attributes.
        A 'name' with the name of the page, an 'href' and an active boolean
        value to indicate whether the page being displayed is the current page.
        """
        items = []
        curr_page = dic['page_name']
        if not self.request.user.valid or self.request.user.show_page_trail:
            trail = self.request.user.getTrail()
            if trail:
                for page_name in trail:
                    page = Page(self.request, page_name)
                    if page.page_name in exclude:
                        continue
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    items.append({'name': title,
                                  'href': self.request.href(page.page_name)})
        return items

    def get_user_items(self, dic):
        items = {'user': None, 'settings': None, 'logout': None, 'login': None}
        if self.request.user.valid and self.request.user.name:
            items['user'] = {'title': self.request.user.name,
                             'url': self.request.href(self.request.user.name),
                             'icon': 'fa fa-user-circle'}
            settings_url = dic['page'].url(self.request,
                                           querystr={'action': 'userprefs'})
            items['settings'] = {'title': self.request.getText('Settings'),
                                 'url': settings_url,
                                 'icon': 'fa fa-sliders'}
            logout_url = dic['page'].url(self.request,
                                         querystr={'action': 'logout',
                                                   'logout': 'logout'})
            items['logout'] = {'title': self.request.getText('Logout'),
                               'url': logout_url,
                               'icon': 'fa fa-sign-out'}
        else:
            login_url = dic['page'].url(self.request,
                                        querystr={'action': 'login'})
            items['login'] = {'title': self.request.getText('Login'),
                              'url': login_url,
                              'icon': 'fa fa-sign-in'}
        return items

    def get_edit_button(self, dic):
        edit_mode = dic.get('edit_mode', False)
        if 'edit' in self.request.cfg.actions_excluded:
            return {'visible': False}
        if not (
                dic['page'].isWritable() and
                self.request.user.may.write(dic['page'].page_name)
        ):
            return {
                'visible': True,
                'label': self.request.getText('Immutable Page'),
                'href': self.request.href(dic['page'].page_name),
                'class': 'disabled'
            }
        else:
            url = self.request.href(dic['page'].page_name)
            if edit_mode:
                css = 'active'
            else:
                css = ''
            return {
                'visible': True,
                'label': self.request.getText('Edit Page'),
                'href': "%s?action=edit" % url,
                'class': css
            }
    
    def get_pageinfo(self, page):
        if self.shouldShowPageinfo(page):
            info = page.lastEditInfo()
            if len(info):
                if info['editor']:
                    msg = "last edited %(time)s by %(editor)s"
                else:
                    msg = "last modified %(time)s"
                info = self.request.getText(msg) % info
                return Markup(info)
        return ""

    def _is_available_action(self, page, action):
        """
        Return if action is available or not.
        If action starts with lowercase, return True without actually check if action exists.
        """
        req = self.request
        excluded = req.cfg.actions_excluded
        available = get_available_actions(req.cfg, page, req.user)
        return not (action in excluded or (action[0].isupper() and not action in available))

    def _is_editable_page(self, page):
        """
        Return True if page is editable for current user, False if not.

        @param page: page object
        """
        return page.isWritable() and self.request.user.may.write(page.page_name)
    
    def _menu_quick_link(self, page):
        """
        Returns quicklink action name and text according to page's status.

        @param page: page object
        @rtype: unicode
        @return (action, text)
        """
        if not self.request.user.valid:
            return (u'', u'')

        _ = self.request.getText
        if self.request.user.isQuickLinkedTo([page.page_name]):
            action, text = u'quickunlink', _("Remove Link")
        else:
            action, text = u'quicklink', _("Add Link")
        if action in self.request.cfg.actions_excluded:
            return (u'', u'')
        return (action, text)

    def _menu_subscribe(self, page):
        """
        Return subscribe action name and text according to page's status.

        @rtype: unicode
        @return (action, text)
        """
        if not (
                (self.cfg.mail_enabled or self.cfg.jabber_enabled) and
                self.request.user.valid
        ):
            return (u'', u'')

        _ = self.request.getText
        if self.request.user.isSubscribedTo([page.page_name]):
            action, text = 'unsubscribe', _("Unsubscribe")
        else:
            action, text = 'subscribe', _("Subscribe")
        if action in self.request.cfg.actions_excluded:
            return (u'', u'')
        return (action, text)

    def _get_query_string(self, args):
        """
        Return a URL query string generated from arguments dictionary.
        {'q1': 'v1', 'q2': 'v2'} will turn into u'?q1=val&q2=val'
        """
        parts = []
        for key, value in args.iteritems():
            if value:
                parts.append(u'%s=%s' % (key, value))
        output = u'&'.join(parts)
        if output:
            output = u'?' + output
        return output
    
    def get_menu(self, dic, user_items=None):
        req = self.request
        rev = req.rev
        _ = req.getText
        page = dic['page']

        page_recent_changes = getLocalizedPage(req, u'RecentChanges')
        page_find_page = getLocalizedPage(req, u'FindPage')
        page_help_contents = getLocalizedPage(req, u'HelpContents')
        page_help_formatting = getLocalizedPage(req, u'HelpOnFormatting')
        page_help_wikisyntax = getLocalizedPage(req, u'HelpOnMoinWikiSyntax')
        page_title_index = getLocalizedPage(req, u'TitleIndex')
        page_word_index = getLocalizedPage(req, u'WordIndex')
        page_front_page = wikiutil.getFrontPage(req)
        page_sidebar = Page(req, req.getPragma('sidebar', u'SideBar'))
        quicklink = self._menu_quick_link(page)
        subscribe = self._menu_subscribe(page)
        
        menu_cfg = {
            'raw': {
                # Title for this menu entry
                'title': _('Raw Text'),
                # href and args are for normal entries ('special': False),
                # otherwise ignored.
                # 'href': Nonexistent or empty for current page
                'href': '',
                # 'args': {'query1': 'value1', 'query2': 'value2', }
                # Optionally specify this for:
                #  <a href="href?query1=value1&query2=value2">
                # If href and args are both nonexistent or empty, key is
                # automatically interpreted to be an action name and href
                # and args are automatically set.
                'args': '',
                # 'special' can be:
                #   'disabled', 'removed', 'separator' or 'header' for
                #   whatever they say, False, None or nonexistent for
                #   normal menu display.
                # 'separator' and 'header' are automatically removed when
                # there are no entries to show among them.
                'special': False,
                'icon': 'fa fa-file-o'
            },
            'print': {'title': _('Print View'), 'icon': 'fa fa-print'},
            'refresh': {
                'title': _('Delete Cache'),
                'special': not (
                    self._is_available_action(page, 'refresh') and
                    page.canUseCache()
                ) and 'removed',
                'icon': 'fa fa-refresh'
            },
            'SpellCheck': {'title': _('Check Spelling'),
                           'icon': 'fa fa-check-square-o'},
            'RenamePage': {'title': _('Rename Page'),
                           'icon': 'fa fa-repeat'},
            'CopyPage':   {'title': _('Copy Page'),
                           'icon': 'fa fa-clone'},
            'DeletePage': {'title': _('Delete Page'),
                           'icon': 'fa fa-trash'},
            'LikePages':  {'title': _('Like Pages'),
                           'icon': 'fa fa-thumbs-o-up'},
            'LocalSiteMap': {'title': _('Local Site Map'),
                             'icon': 'fa fa-sitemap'},
            'MyPages':    {'title': _('My Pages'),
                           'icon': 'fa fa-newspaper-o'},
            'SubscribeUser': {
                'title': _('Subscribe User'),
                'special': not (
                    self._is_available_action(page, 'SubscribeUser') and
                    req.user.may.admin(page.page_name)
                ) and 'removed',
                'icon': 'fa fa-envelope-o'
            },
            'Despam': {
                'title': _('Remove Spam'),
                'special': not (
                    self._is_available_action(page, 'Despam') and
                    req.user.isSuperUser()
                ) and 'removed',
                'icon': 'fa fa-fire'
            },
            'revert': {
                'title': _('Revert to this revision'),
                'special': not (
                    self._is_available_action(page, 'revert') and rev and
                    req.user.may.revert(page.page_name)
                ) and 'removed',
                'icon': 'fa fa-undo'
            },
            'PackagePages': {'title': _('Package Pages'),
                             'icon': 'fa fa-suitcase'},
            'RenderAsDocbook': {'title': _('Render as Docbook'),
                                'icon': 'fa fa-book'},
            'SyncPages': {'title': _('Sync Pages'),
                          'icon': 'fa fa-refresh'},
            'AttachFile': {'title': _('Attachments'),
                           'icon': 'fa fa-paperclip'},
            'quicklink': {
                'title': quicklink[1] or _('Quick Link'),
                'args': dict(action=quicklink[0], rev=rev),
                'special': not quicklink[0] and 'removed',
                'icon': 'fa fa-share'
            },
            'subscribe': {
                'title': subscribe[1] or _('Subscribe'),
                'args': dict(action=subscribe[0], rev=rev),
                'special': not subscribe[0] and 'removed',
                'icon': 'fa fa-envelope'
            },
            'info': {'title': _('Info'), 'icon': 'fa fa-info-circle'},
            'Load': {'title': _('Load'), 'icon': 'fa fa-upload'},
            'Save': {'title': _('Save'), 'icon': 'fa fa-download'},
            # useful pages
            'RecentChanges': {'title': page_recent_changes.page_name,
                              'href': page_recent_changes.url(req),
                              'icon': 'fa fa-clock-o'},
            'FindPage': {'title': page_find_page.page_name,
                         'href': page_find_page.url(req),
                         'icon': 'fa fa-search'},
            'HelpContents': {'title': page_help_contents.page_name,
                             'href': page_help_contents.url(req),
                             'icon': 'fa fa-question-circle'},
            'HelpOnFormatting': {'title': page_help_formatting.page_name,
                                 'href': page_help_formatting.url(req),
                                 'icon': 'fa fa-question-circle'},
            'HelpOnMoinWikiSyntax': {'title': page_help_wikisyntax.page_name,
                                     'href': page_help_wikisyntax.url(req),
                                     'icon': 'fa fa-question-circle'},
            'TitleIndex': {'title': page_title_index.page_name,
                           'href': page_title_index.url(req),
                           'icon': 'fa fa-list'},
            'WordIndex': {'title': page_word_index.page_name,
                          'href': page_word_index.url(req),
                          'icon': 'fa fa-list'},
            'FrontPage': {'title': page_front_page.page_name,
                          'href': page_front_page.url(req),
                          'icon': 'fa fa-home'},
            'SideBar': {'title': page_sidebar.page_name,
                        'href': page_sidebar.url(req),
                        'icon': 'fa fa-columns'},
            'editSideBar': {
                'title': _('Edit SideBar'),
                'href': page_sidebar.url(req),
                'args': dict(action='edit'),
                'special': (
                    not self._is_editable_page(page_sidebar) and
                    'removed'
                ),
                'icon': 'fa fa-columns'
            },
        }

        output = []
        
        for group in self._menu:
            _group = {
                'label': _(group['label']),
                'entries': []
            }
            for entry in group['entries']:
                data = menu_cfg.get(entry)
                if data:
                    if data.get('special'):
                       _group['entries'].append(data)
                    else:
                        if not (data.get('href') or data.get('args')):
                            # It's an Action.
                            if self._is_available_action(page, entry):
                                query = self._get_query_string(
                                    {'action': entry, 'rev': rev})
                                _entry = {
                                    'title': data.get('title', _(entry)),
                                    'href': u'%s%s' % (page.url(req), query),
                                    'icon': data['icon'],
                                }
                                _group['entries'].append(_entry)
                            else:
                                continue
                        else:
                            # A normal menu entry.
                            if not data.get('href'):
                                data['href'] = page.url(req)
                            if data.get('args'):
                                data['href'] = u'%s%s' % (
                                    data['href'],
                                    self._get_query_string(data['args'])
                                )
                            _group['entries'].append({
                                'title': data.get('title', _(entry)),
                                'href': data['href'],
                                'icon': data['icon'],
                            })
            if _group['label'] == 'User':
                for k in user_items.keys():
                    if user_items[k]:
                        _group['entries'].append({
                            'title': _(user_items[k]['title']),
                            'href': user_items[k]['url'],
                            'icon': user_items[k]['icon']})
            output.append(_group)
        return output

    def get_msgs(self, dic):
        msgs = []
        msg_type = {'dialog': 'alert-success',
                    'hint': 'alert-success',
                    'info': 'alert-info',
                    'warning': 'alert-warning',
                    'error': 'alert-danger'}
        for msg, msg_class in dic['msg']:
            try:
                text = msg.render()
            except AttributeError as exc:
                text = msg
            if text:
                msgs.append({'text': Markup(text),
                             'type': 'alert' if msg_class in msg_type.keys() else 'card',
                             'style': msg_type.get(msg_class, 'text-black bg-light')})
        return msgs

    def editorheader(self, dic, **kwargs):
        dic['edit_mode'] = 1
        return self.header(dic, **kwargs)
    
    def header(self, dic, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        # html = [
        #     # Pre header custom html
        #     self.emit_custom_html(self.cfg.page_header1),

        #     # Header
        #     u'<div id="header">',
        #     self.logo(),
        #     self.searchform(dic),
        #     self.username(dic),
        #     u'<div id="locationline">',
        #     self.interwiki(dic),
        #     self.title(dic),
        #     u'</div>',
        #     self.trail(dic),
        #     self.navibar(dic),
        #     #u'<hr id="pageline">',
        #     u'<div id="pageline"><hr style="display:none;"></div>',
        #     self.msg(dic),
        #     self.editbar(dic),
        #     u'</div>',

        #     # Post header custom html (not recommended)
        #     self.emit_custom_html(self.cfg.page_header2),

        #     # Start of page
        #     self.startPage(),
        # ]

        frontpage = wikiutil.getFrontPage(self.request)
        findpage = getLocalizedPage(self.request, 'FindPage')
        helpcontents = getLocalizedPage(self.request, 'HelpContents')

        navigation_items = self.get_navigation_items(dic)
        trail_items = self.get_trail_items(
            dic, exclude=[i['name'] for i in navigation_items])

        form = self.request.values

        if self.cfg.logo_markup:
            logo_markup = Markup(self.cfg.logo_markup)
        else:
            logo_markup = Markup(self.cfg.logo_string)

        user_items = self.get_user_items(dic)
        context = {
            'page_name': dic['page'].page_name,
            'logo_markup': logo_markup,
            'logo_string': Markup(self.cfg.logo_string),
            'user_items': user_items,
            'homepage_url': self.request.href(frontpage.page_name),
            'findpage_url': self.request.href(findpage.page_name),
            'edit_button': self.get_edit_button(dic),
            'menu_label': self.request.getText('Menu'),
            'menu': self.get_menu(dic, user_items=user_items),
            'helpcontents_url': self.request.href(helpcontents.page_name),
            'navigation_items': navigation_items,
            'trail_items': trail_items,
            'search_form_action': self.request.href(dic['page'].page_name),
            'search_form_label': self.request.getText('Search'),
            'search_form_value': wikiutil.escape(form.get('value', ''), 1),
            'msgs': self.get_msgs(dic),
        }
        
        template = self.j2env.get_template('bits/body_header.html')
        output = template.render(context)
        return output

    def footer(self, dic, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = dic['page']
        html = [
            # End of page
            self.pageinfo(page),
            self.endPage(),

            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            # Footer
            u'<div id="footer">',
            self.editbar(dic),
            self.credits(dic),
            self.showversion(dic, **keywords),
            u'</div>',

            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
            ]
        # return u'\n'.join(html)

        context = {
            'edit_mode': dic.get('edit_mode', False),
            'static_base': "%s/%s/" % (self.cfg.url_prefix_static, self.name),
            'pageinfo': self.get_pageinfo(dic['page']),            
        }
        template = self.j2env.get_template('bits/body_footer.html')
        output = template.render(context)
        return output
    

def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

