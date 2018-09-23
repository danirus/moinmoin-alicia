var _ = undefined;
var _header_added = false;

var shiftWindow = function() { scrollBy(0, -60) };
window.addEventListener("hashchange", shiftWindow);

var getParam = function(href, name) {
    var qs_starts = href.indexOf("?");
    var qs = href.substring(qs_starts+1);
    var args = qs.split('&');
    for (var i = 0; i < args.length; i++) {
        var param = args[i].split('=');
        if (param[0] == name) {
            return param[1];
        }
    }
    return null;
}

var getQueryStringParam = function(name) {
    var href = window.location.search;
    return getParam(href, name);
}

$(document).ready(function() {
    $('.sidebar-collapse').slimScroll({
        height: '100%',
        railOpacity: 0.9
    });
    var toc = $('div.table-of-contents');
    if(toc.length) {
        $('#toc').append(toc[0]);
        $('#toc').append('<hr/>');
        $('#toc').removeClass("invisible");
    }

    //----------------------------------------------------------------------
    // In case the location URL points to an anchor within the page.
    if (window.location.hash) shiftWindow();
    
    // Moin-to-Bootstrap substitutions.
    $('DIV.red.solid').removeClass('red solid').addClass('alert alert-danger');

    //----------------------------------------------------------------------
    // Tables.
    $('table').each(function() {
        $(this).addClass("table");
        // $(this).prepend('<thead></thead>')
        // $(this).find('thead').append($(this).find("tr:eq(0)").addClass("col"));
        // Check if 
    })

    //----------------------------------------------------------------------
    // Remove '&quot;' and '&quot' from style attribute content.
    var elems = $("[style*='&quot']");
    elems.each(function() {
        var style = $(this).attr('style');
        style = style.replace(/&quot;/i, '').replace(/&quot/i, '');
        $(this).attr('style', style);
    });

    //----------------------------------------------------------------------
    // Form fields.
    _ = $('#content FORM');
    if(_.length) {
        _.find('LABEL').addClass("form-check-label");
        _.find('SELECT').removeAttr('size').addClass("form-control");
        _.find('TEXTAREA').addClass("form-control");
        _.find('INPUT[type=checkbox]').addClass("form-check-input");
        _.find('INPUT[type=text]').addClass("form-control");
        _.find('INPUT[type=submit][name=cancel]').addClass("btn btn-secondary");
        _.find('INPUT[type=submit][name!=cancel]').addClass("btn btn-primary");
        _.find("TABLE TR>TD:nth-child(1)").each(function() {
            $(this).find('B').replaceWith('<label>'+$(this).text()+'</label>');
        });
    }
    
    //----------------------------------------------------------------------
    // Make admonitions look like alert-warning.
    $('DIV.caution').each(function() {
        var header = $(this).find('P:first');
        header.replaceWith('<h5 class="alert-heading">'+header.html()+'</h5>');
        $(this).removeClass("caution").addClass("alert alert-warning");
    });

    //----------------------------------------------------------------------
    // Add alert-link class to all anchors inside a div.alert element.
    $('DIV.alert').each(function() {
        $(this).find('a').addClass("alert-link");
    });

    //----------------------------------------------------------------------
    // Transform messages shown as div.dialog within div.alert at the top.
    // Like the MoinMoin/action/RenamePage.py form.
    _ = $('DIV.dialog > FORM');
    if(_.length) {
        _.find('br').remove();  // Remove useless <br>'s.
        var strong = _.find('STRONG');
        if(strong) {
            strong.replaceWith('<legend class="alert-heading pb-3">'+strong.text()+'</legend>');
        }
        _.find('input[type="text"]').addClass('form-control');
        var buttons = _.find('input[type="submit"]');
        if(buttons.length==2) {
            $(buttons[0]).addClass('btn btn-primary mr-2');
            $(buttons[1]).addClass('btn btn-secondary');
        };
    }

    //----------------------------------------------------------------------
    // User preferences page.
    /*
     * The only way to detect that the page is being displayed is by finding
     * that the three links the user preferences menu contains are actually
     * being displayed in the <div id="content">
     */
    _ = $('#content UL:eq(0)');
    if(_.length && _.find('A').length > 0) {
        var is_an_action_userpref_anchor = true;
        _.find('A').each(function() {
            if(is_an_action_userpref_anchor) {
                var action = getParam($(this).attr('href'), 'action');
                if(action!='userprefs') {
                    is_an_action_userpref_anchor = false;
                }
            }
        });
        if(is_an_action_userpref_anchor) {
            if(!_header_added) {
                _header_added = true;
                $('#content').prepend('<h1>User preferences</h1>');
            }
        }
    }
    
    if(getQueryStringParam('action') == 'userprefs') {
        if(!_header_added) {
            _header_added = true;
            $('#content').prepend('<h1>User preferences</h1>');
        }
    }

    //----------------------------------------------------------------------
    // Edit page.
    _ = $('FORM#editor');
    if(_.length) {
        var ids = ['chktrivialtop', 'chktrivial', 'chkrstrip'];
        for(var i=0; i<ids.length; i++) {
            _.find('#'+ids[i]).before('<div id="'+ids[i]+'_div" class="form-check ml-1 mt-1">');
            var label = $('LABEL[for='+ids[i]+']').text();
            $('LABEL[for='+ids[i]+']').text('');
            _.find('#'+ids[i]+'_div').append($('LABEL[for='+ids[i]+']'));
            _.find('LABEL[for='+ids[i]+']').append($('#'+ids[i]));
            _.find('LABEL[for='+ids[i]+']').append(label);
            _.find('TEXTAREA').addClass("my-3");
        }
    }
    
    //----------------------------------------------------------------------
    // Login action page.
    _ = $('FORM#loginform');
    if(_ && _.length && getQueryStringParam('action') == 'login') {
        _.addClass("offset-sm-1 col-sm-8");
        if(!_header_added) {
            _header_added = true;
            $('#content').prepend('<h1>Login</h1>');
        }
        _.find('input[type=text]').addClass('form-control');
        _.find('input[type=password]').addClass('form-control');
        _.find('input[type=submit]').addClass('btn btn-primary');
    }

    //----------------------------------------------------------------------
    // Signup action page.
    _ = $('input[value=newaccount]');
    if(_ && _.length && getQueryStringParam('action') == 'newaccount') {
        _ = _.parent("FORM");
        _.addClass("offset-sm-1 col-sm-9");
        if(!_header_added) {
            _header_added = true;
            $('#content').prepend('<h1>Create Account</h1>');
        }
        _.find('input[type=text]').addClass('form-control');
        _.find('input[type=password]').addClass('form-control');
        _.find('input[type=submit]').addClass('btn btn-primary');
        
    }

    //----------------------------------------------------------------------
    // Info action page.
    if(getQueryStringParam('action') == 'info') {
        var has_param_general = false || getQueryStringParam('general') == 1,
            has_param_hitscount = false || getQueryStringParam('hitcounts') == 1;
        var has_only_action = (!has_param_general && !has_param_hitscount);
        // Convert top 3 links into tabs.
        var tabsArr = new Array();
        $('#content>P:first-child>A').each(function() {
            var href = $(this).attr('href'),
                rel  = $(this).attr('rel'),
                text = $(this).text(),
                css  = "";
            if((href.indexOf('general=1')>-1 && has_param_general) ||
               (href.indexOf('hitcounts=1')>-1 && has_param_hitscount) ||
               (href.indexOf('general=1')==-1 && href.indexOf('hitcounts=1')==-1 && has_only_action))
            { css = "active" } 
            else { css = "" }
            tabsArr.push('<a class="nav-link '+css+'" href="'+href+'">'+text+'</a>');
        });
        var tabs = '<ul class="nav nav-tabs" role="tablist">';
        for(var i=0; i<tabsArr.length; i++)
            tabs += '<li class="nav-item">'+tabsArr[i]+'</li>';
        tabs += '</ul>';
        $('#content>P:first-child').remove();
        $('#content').prepend(tabs);
        // Set title.
        var pagename = $('DIV.page').data('pagename');
        if(!_header_added) {
            _header_added = true;
            $('#content').prepend('<h1>Info <small class="text-muted">'+pagename+'</small></h1>');
        }
        $('TBODY>TR:first-child>TD').addClass("align-middle");
        $('TD>input[type=radio]').addClass("mr-2");
        $('input[type=submit]').addClass("btn btn-secondary");
        // Fix second title (after tabs).
        if(has_only_action) {
            var _t = $('#content H2:first');
            _t.replaceWith('<h3>'+_t.text()+'</h3>');
        } else if(has_param_general) {
            var _t = $('#content H1:eq(1)');
            _t.replaceWith('<h3>'+_t.text()+'</h3>');
        } else if(has_param_hitscount) {
            $('<h3>Page hits and edits</h3>').insertAfter('#content UL.nav');
        }
    }

    //----------------------------------------------------------------------
    // Diff action page.
    if(getQueryStringParam('action') == 'diff') {
        _ = $('#content SPAN.diff-header');
        _.replaceWith('<H3>'+_.text()+'</h3>');
        _ = $('#content TABLE.diff.table').addClass("table-striped");
        _.find('input[type=submit]').addClass('btn btn-secondary');
        $('#content-below-diff').before('<hr/>');
    }
    
    //----------------------------------------------------------------------
    // Search action page.
    var has_search_stats = ($('P.searchstats').length > 0);
    if(has_search_stats && getQueryStringParam('action') == 'fullsearch') {
        if(!_header_added) {
            _header_added = true;
            $('#content').prepend('<h1>'+$('#searchinput').attr('placeholder')+'</h1>');
        }
    }

    //----------------------------------------------------------------------
    // FindPage.
    if($('div.page').data('pagename') == 'FindPage') {
        if(!_header_added) {
            _header_added = true;
            $("#content").prepend('<H1>Find page</H1>');
        }
        $('#content FORM').eq(1).addClass("form-inline");
    }
    
    //----------------------------------------------------------------------
    // Make the p.searchhint look like an alert-info.
    $('P.searchhint').each(function() {
        $(this).removeClass('searchhint').addClass('alert alert-info text-center');
    });

    //----------------------------------------------------------------------
    // Make close button visible only when URL contains hash (like in #preview)
    if(window.location.href.indexOf('#') > -1) {
        $('A.close.invisible').removeClass('invisible');
    }
});
