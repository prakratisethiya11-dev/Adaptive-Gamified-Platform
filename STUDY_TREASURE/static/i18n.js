/*
 * Study Treasure - shared language engine (works on EVERY page)
 *
 * How to use on any page (put these 2 lines at the end of <body>):
 *   <script src="/static/translations.js"></script>
 *   <script src="/static/i18n.js"></script>
 *
 * HTML attributes:
 *   data-i18n="key"              -> element text
 *   data-i18n-html="key"         -> element innerHTML (for text containing <b> etc.)
 *   data-i18n-placeholder="key"  -> input placeholder
 *   data-i18n-title="key"        -> title attribute (tooltip / validation hint)
 *   data-i18n-vars='{"n": 5}'    -> values for {n} placeholders inside the text
 *
 * JavaScript:
 *   t('key', {name: 'x'})            -> translated string in current language
 *   i18n.set(el, 'key', vars, html)  -> put translated text in element AND keep it
 *                                       translated if the language changes later
 *   Values in vars starting with "@" are treated as another key, e.g. {name: '@sol_lemon'}
 *
 * The chosen language is saved in localStorage ("selected_lang"), so it is the same
 * on all pages. Changing it on one page updates it everywhere.
 */
(function () {
    'use strict';

    var STORAGE_KEY = 'selected_lang';
    var DEFAULT_LANG = 'en';
    var LANGUAGES = [
        { code: 'en',  label: 'English',           htmlLang: 'en' },
        { code: 'hi',  label: 'हिन्दी (Hindi)',     htmlLang: 'hi' },
        { code: 'nim', label: 'निमाड़ी (Nimadi)',    htmlLang: 'hi' },
        { code: 'mr',  label: 'मराठी (Marathi)',     htmlLang: 'mr' }
    ];

    // Messages that come from the Flask backend in English -> translation key
    var SERVER_MESSAGES = {
        'Welcome back, You Successfully Logged in': 'msg_login_student',
        'Welcome back, Faculty Login Successful': 'msg_login_faculty',
        'Incorrect password': 'msg_incorrect_password',
        'Email not found!': 'msg_email_not_found',
        'Invalid credentials': 'msg_invalid_credentials',
        'Unauthorized': 'err_unauthorized',
        'Invalid Session': 'err_invalid_session'
    };

    function getLang() {
        var lang = DEFAULT_LANG;
        try { lang = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG; } catch (e) { /* storage blocked */ }
        return (typeof translations !== 'undefined' && translations[lang]) ? lang : DEFAULT_LANG;
    }

    function t(key, vars) {
        var lang = getLang();
        var text = (translations[lang] && translations[lang][key]);
        if (text === undefined) text = translations[DEFAULT_LANG][key];
        if (text === undefined) return key;
        if (vars) {
            text = text.replace(/\{(\w+)\}/g, function (match, name) {
                if (!(name in vars)) return match;
                var v = vars[name];
                if (typeof v === 'string' && v.charAt(0) === '@') return t(v.slice(1));
                return v;
            });
        }
        return text;
    }

    function tServer(message) {
        var key = SERVER_MESSAGES[message];
        if (key) return t(key);
        // "Database Error: <details>" -> translate only the first part
        var dbPrefix = 'Database Error: ';
        if (typeof message === 'string' && message.indexOf(dbPrefix) === 0) {
            return t('msg_db_error') + ' ' + message.slice(dbPrefix.length);
        }
        return message;
    }

    function readVars(el) {
        var raw = el.getAttribute('data-i18n-vars');
        if (!raw) return null;
        try { return JSON.parse(raw); } catch (e) { return null; }
    }

    function applyToElement(el) {
        var vars = readVars(el);
        var key;
        if ((key = el.getAttribute('data-i18n')) !== null) el.textContent = t(key, vars);
        if ((key = el.getAttribute('data-i18n-html')) !== null) el.innerHTML = t(key, vars);
        if ((key = el.getAttribute('data-i18n-placeholder')) !== null) el.setAttribute('placeholder', t(key, vars));
        if ((key = el.getAttribute('data-i18n-title')) !== null) el.setAttribute('title', t(key, vars));
    }

    function apply(root) {
        root = root || document;
        var nodes = root.querySelectorAll('[data-i18n],[data-i18n-html],[data-i18n-placeholder],[data-i18n-title]');
        for (var i = 0; i < nodes.length; i++) applyToElement(nodes[i]);
    }

    // Put a translated text in an element and remember it, so it re-translates on language change.
    // key = null/'' clears the element.
    function set(el, key, vars, asHtml) {
        if (!el) return;
        el.removeAttribute('data-i18n');
        el.removeAttribute('data-i18n-html');
        el.removeAttribute('data-i18n-vars');
        if (!key) { el.textContent = ''; return; }
        el.setAttribute(asHtml ? 'data-i18n-html' : 'data-i18n', key);
        if (vars) el.setAttribute('data-i18n-vars', JSON.stringify(vars));
        applyToElement(el);
    }

    function syncSwitchers(lang) {
        var selects = document.querySelectorAll('select[data-lang-select]');
        for (var i = 0; i < selects.length; i++) selects[i].value = lang;
    }

    function setLang(lang) {
        if (!translations[lang]) lang = DEFAULT_LANG;
        try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* storage blocked */ }
        refresh();
        document.dispatchEvent(new CustomEvent('languagechange', { detail: { lang: lang } }));
    }

    function refresh() {
        var lang = getLang();
        for (var i = 0; i < LANGUAGES.length; i++) {
            if (LANGUAGES[i].code === lang) document.documentElement.setAttribute('lang', LANGUAGES[i].htmlLang);
        }
        apply(document);
        syncSwitchers(lang);
    }

    // Floating language picker, added automatically on pages that have no switcher of their own
    function injectFloatingSwitcher() {
        if (document.querySelector('[data-lang-switcher]') || !document.body) return;

        var box = document.createElement('div');
        box.setAttribute('data-lang-switcher', 'floating');
        box.style.cssText = 'position:fixed;right:14px;bottom:14px;z-index:100000;display:flex;align-items:center;' +
            'gap:6px;background:#ffffff;border:1px solid #cbd5e1;border-radius:999px;padding:6px 12px;' +
            'box-shadow:0 4px 14px rgba(0,0,0,0.2);font-family:Arial,sans-serif;';

        var icon = document.createElement('span');
        icon.textContent = '🌐';
        icon.style.cssText = 'font-size:16px;line-height:1;';

        var select = document.createElement('select');
        select.setAttribute('data-lang-select', '');
        select.setAttribute('data-i18n-title', 'lang_label');
        select.style.cssText = 'border:none;background:transparent;color:#0f172a;font-size:14px;cursor:pointer;outline:none;';
        LANGUAGES.forEach(function (l) {
            var opt = document.createElement('option');
            opt.value = l.code;
            opt.textContent = l.label;
            select.appendChild(opt);
        });
        select.addEventListener('change', function () { setLang(select.value); });

        box.appendChild(icon);
        box.appendChild(select);
        document.body.appendChild(box);
    }

    // Keep several open tabs/pages in sync
    window.addEventListener('storage', function (e) {
        if (e.key === STORAGE_KEY) {
            refresh();
            document.dispatchEvent(new CustomEvent('languagechange', { detail: { lang: getLang() } }));
        }
    });

    function init() {
        injectFloatingSwitcher();
        refresh();
    }

    window.i18n = { t: t, tServer: tServer, apply: apply, set: set, setLang: setLang, getLang: getLang, languages: LANGUAGES };
    window.t = t;
    window.changeLanguage = setLang; // used by the language dropdown on the home page

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
