# std:
# n/a

# pip-ext:
import bleach;

# pip-int:
# n/a

# loc:
import utils;

# Allowed Tags: ::::::::::::::::::::::::::::::::::::::::::::

DEFAULT_ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote',
    'code', 'em', 'i', 'li', 'ol', 'strong', 'ul',
];
assert DEFAULT_ALLOWED_TAGS == bleach.sanitizer.ALLOWED_TAGS;

ALLOWED_TAGS = DEFAULT_ALLOWED_TAGS + [
    "p", "pre", "br", "label",
    "table", "thead", "tbody", "tr", "th", "td",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "div", "span", "section",
    "img", "figure",
    "font", # WYSIWYGs use this for setting font.
    "u",    # Commonly used in WYSIWYG editing.
    "hr",
];

# Allowed Attributes: ::::::::::::::::::::::::::::::::::::::

DEFAULT_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'], # TODO: Allow target="_blank";
    'abbr': ['title'],
    'acronym': ['title'],
};
assert DEFAULT_ALLOWED_ATTRIBUTES == bleach.sanitizer.ALLOWED_ATTRIBUTES;

ALLOWED_ATTRIBUTES = utils.deepCopy(DEFAULT_ALLOWED_ATTRIBUTES);
ALLOWED_ATTRIBUTES.update({
    "img": ["src", "height", "width"],
    "*": ["class", "style"],                                            # 'style' req'd in ALLOWED_ATTRIBUTES, and ALLOWED_STYLES too.
    "font": ["color"],
    #TODO: "iframe": ["src", "class", "width", "height", "frameborder"],
});

# Allowed Styles: ::::::::::::::::::::::::::::::::::::::::::

assert bleach.sanitizer.ALLOWED_STYLES == [];

ALLOWED_STYLES = [
    "background-color", # WYSIWYGs use for text-highlight
];

# Bleaching: :::::::::::::::::::::::::::::::::::::::::::::::

def sanitizeHtml (s):   # AKA bleachHtml                    # Externally: `import bleachUp; bleachUp.bleachHtml(html);`
    cleaned_s = bleach.clean(s,
        tags = ALLOWED_TAGS,
        attributes = ALLOWED_ATTRIBUTES,
        styles = ALLOWED_STYLES,
        strip_comments = False,
    );
    ## TODO: Consider below, and using LinkifyFilter.       # Docs: https://bleach.readthedocs.io/en/latest/linkify.html
    #linkified_s = bleach.linkify(cleaned_s);               # <- Adds rel="nofollow" to links. TODO?: Add noopener via param `callbacks`
    #return linkified_s;
    return cleaned_s;
bleachHtml = sanitizeHtml;  # Alias, thematic nomenclature.
