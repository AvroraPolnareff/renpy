from __future__ import print_function, unicode_literals, division, absolute_import

str = unicode # @ReservedAssignment

import collections
import os
import io

# The path to the directory containing this file.
BASE = os.path.dirname(os.path.abspath(__file__))

################################################################################
# Prefixes
################################################################################

# A map from prefix name to Prefix object.
prefixes = { }

class Prefix(object):
    def __init__(self, index, name, priority, alts):

        # The index of where this prefix is stored in memory, or -1 if this
        # prefix isn't stored in memory.
        self.index = index

        # The name of this prefix.
        self.name = name

        # The priority of this prefix. When added at the same time, higher
        # priority prefixes take precendence over lower priority prefixes.
        self.priority = priority

        # A list of prefix indexes that should be updated when this prefix is
        # updated, including this prefix.
        if index >= 0:
            self.alts = [ self.index ]
            self.alt_names = [ self.name ]
        else:
            self.alts = [ ]
            self.alt_names = [ ]

        for i in alts:
            self.alts.append(prefixes[i].index)
            self.alt_names.append(i)

        prefixes[name] = self

# The number of priority levels we have.
PRIORITY_LEVELS = 4

# The number of prefixes we have.
PREFIX_COUNT = 6

Prefix(5, 'selected_hover_', 3, [ ])
Prefix(4, 'selected_idle_', 3, [ ])
Prefix(3, 'selected_insensitive_', 3, [ ])
Prefix(-3, 'selected_', 2, [ "selected_hover_", "selected_idle_", "selected_insensitive_" ])
Prefix(2, 'hover_', 1, [ "selected_hover_" ])
Prefix(1, 'idle_', 1, [ "selected_idle_" ] )
Prefix(0, 'insensitive_', 1, [ "selected_insensitive_" ])
Prefix(-4, '', 0, [ "selected_hover_", "selected_idle_", "selected_insensitive_", "idle_", "hover_", "insensitive_" ] )

Prefix(-2, 'activate_', 0, [ ])
Prefix(-1, 'selected_activate_', 0, [ ])


################################################################################
# Style Properties
################################################################################

# All the style properties we know about. This is a dict, that maps each style
# to a function that is called when it is set, or None if no such function
# is needed.
style_properties = collections.OrderedDict(
    activate_sound = None,
    aft_bar = 'none_is_null',
    aft_gutter = None,
    antialias = None,
    vertical = None,
    background = 'renpy.easy.displayable_or_none',
    bar_invert = None,
    bar_resizing = None,
    unscrollable = None,
    bar_vertical = None,
    black_color = 'renpy.easy.color',
    bold = None,
    bottom_margin = None,
    bottom_padding = None,
    box_layout = None,
    box_reverse = None,
    box_wrap = None,
    caret = 'renpy.easy.displayable_or_none',
    child = 'renpy.easy.displayable_or_none',
    clipping = None,
    color = 'renpy.easy.color',
    drop_shadow = None,
    drop_shadow_color = 'renpy.easy.color',
    first_indent = None,
    first_spacing = None,
    fit_first = None,
    focus_mask = None,
    focus_rect = None,
    font = None,
    fore_bar = 'none_is_null',
    fore_gutter = None,
    foreground = 'renpy.easy.displayable_or_none',
    hover_sound = None,
    hyperlink_functions=None,
    italic = None,
    justify = None,
    kerning = None,
    language = None,
    layout = None,
    line_leading = None,
    left_margin = None,
    line_overlap_split=None,
    left_padding = None,
    line_spacing = None,
    mouse = None,
    min_width = None,
    newline_indent = None,
    order_reverse = None,
    outlines = 'expand_outlines',
    rest_indent = None,
    right_margin = None,
    right_padding = None,
    ruby_style = None,
    size = None,
    size_group = None,
    slow_abortable = None,
    slow_cps = None,
    slow_cps_multiplier = None,
    spacing = None,
    strikethrough = None,
    subtitle_width = None,
    subpixel = None,
    text_y_fudge = None,
    text_align = None,
    thumb = 'none_is_null',
    thumb_offset = None,
    thumb_shadow = 'none_is_null',
    time_policy = None,
    top_margin = None,
    top_padding = None,
    underline = None,
    xanchor = 'expand_anchor',
    xfill = None,
    xmaximum = None,
    xminimum = None,
    xoffset = None,
    xpos = None,
    yanchor = 'expand_anchor',
    yfill = None,
    ymaximum = None,
    yminimum = None,
    yoffset = None,
    ypos = None,
    )

# A map from a style property to its index in the order of style_properties.
style_property_index = { }
for i, name in enumerate(style_properties):
    style_property_index[name] = i

style_property_count = len(style_properties)

# print("{} properties * {} prefixes = {} cache entries".format(
#     style_property_count, PREFIX_COUNT, style_property_count * PREFIX_COUNT))

# A list of synthetic style properties, where each property is expanded into
# multiple style properties. Each property are mapped into a list of tuples,
# with each consisting of:
#
# * The name of the style to assign.
# * A string giving the name of a functon to call to get the value to assign, a constant
#   numeric value, or None to not change the argument.
synthetic_properties = collections.OrderedDict(
    xmargin = [
        ('left_margin', None),
        ('right_margin', None)
        ],

    ymargin = [
        ('top_margin', None),
        ('bottom_margin', None),
        ],

    xalign = [
        ('xpos', None),
        ('xanchor', None),
        ],

    yalign = [
        ('ypos', None),
        ('yanchor', None),
        ],

    xpadding = [
        ('left_padding', None),
        ('right_padding', None),
        ],

    ypadding = [
        ('top_padding', None),
        ('bottom_padding', None),
        ],

    minwidth = [ ('min_width', None) ],
    textalign = [ ('text_align', None) ],
    slow_speed = [ ('slow_cps', None) ],
    enable_hover = [ ],
    left_gutter = [ ('fore_gutter', None) ],
    right_gutter = [ ('aft_gutter', None) ],
    top_gutter = [ ('fore_gutter', None) ],
    bottom_gutter = [ ('aft_gutter', None) ],
    left_bar = [ ('fore_bar', None) ],
    right_bar = [ ('aft_bar', None) ],
    top_bar = [ ('fore_bar', None) ],
    bottom_bar = [ ('aft_bar', None) ],
    box_spacing = [ ( 'spacing', None ) ],
    box_first_spacing = [ ( 'first_spacing', None) ],

    pos = [
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ],

    anchor = [
        ('xanchor', 'index_0'),
        ('yanchor', 'index_1'),
        ],

    # Conflicts w/ a variable used in the Style implementation.
    # offset = [
    #     ('xoffset', index_0),
    #     ('yoffset', index_1),
    #     ],

    align = [
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ('xanchor', 'index_0'),
        ('yanchor', 'index_1'),
        ],

    maximum = [
        ('xmaximum', 'index_0'),
        ('ymaximum', 'index_1'),
        ],

    minimum = [
        ('xminimum', 'index_0'),
        ('yminimum', 'index_1'),
        ],

    area = [
        ('xpos', 'index_0'),
        ('ypos', 'index_1'),
        ('xanchor', 0),
        ('yanchor', 0),
        ('xfill', True),
        ('yfill', True),
        ('xmaximum', 'index_2'),
        ('ymaximum', 'index_3'),
        ('xminimum', 'index_2'),
        ('yminimum', 'index_3'),
        ],

    xcenter = [
        ('xpos', None),
        ('xanchor', 0.5),
        ],

    ycenter = [
        ('ypos', None),
        ('yanchor', 0.5),
        ],

    )

all_properties = collections.OrderedDict()

for k, v in style_properties.items():
    all_properties[k] = [ (k, None) ]

all_properties.update(synthetic_properties)

################################################################################
# Code Generation
################################################################################

class CodeGen(object):
    """
    Utility class for code generation.

    `filename`
        The name of the file we code-generate into.
    `spew`
        If true, spew the generated code to stdout.
    """

    def __init__(self, filename, spew=False):
        self.filename = os.path.join(BASE, "gen", filename)
        self.f = io.StringIO()
        self.depth = 0
        self.spew = spew

    def close(self):

        text = self.f.getvalue()

        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                old = f.read()

            if old == text:
                return

        with open(self.filename, "wb") as f:
            f.write(text)

    def write(self, s, *args, **kwargs):
        out = "    " * self.depth
        out += s.format(*args, **kwargs)
        out = out.rstrip()

        if self.spew:
            print(out)

        out += "\n"
        self.f.write(out)

    def indent(self):
        self.depth += 1

    def dedent(self):
        self.depth -= 1


def generate_constants():
    """
    This generates code that defines the property functions.
    """

    g = CodeGen("styleconstants.pxi")

    g.write("DEF PRIORITY_LEVELS = {}", PRIORITY_LEVELS)
    g.write("DEF PREFIX_COUNT = {}", PREFIX_COUNT)
    g.write("DEF STYLE_PROPERTY_COUNT = {}", style_property_count)

    for p in prefixes.values():
        if p.index < 0:
            continue

        g.write("DEF {}PREFIX = {}", p.name.upper(), p.index * style_property_count)

    for k in style_properties:
        g.write("DEF {}_INDEX = {}", k.upper(), style_property_index[k])

    g.close()

def generate_property_function(g, prefix, propname, properties):
    name = prefix.name + propname

    g.write("cdef int {name}_property(PyObject **cache, int *cache_priorities, int priority, object value) except -1:", name=name)
    g.indent()

    g.write("priority += {}", prefix.priority)

    for stylepropname, func in properties:
        value = "value"

        g.write("")

        if isinstance(func, str):
            g.write("v = {func}({value})", func=func, value=value)
            value = "v"
        elif func is not None:
            g.write("v = {}", func)
            value = "v"

        propfunc = style_properties[stylepropname]

        if propfunc is not None:
            g.write("v = {propfunc}({value})", propfunc=propfunc, value=value)
            value = "v"

        for alt, alt_name in zip(prefix.alts, prefix.alt_names):
            g.write("assign({}, cache, cache_priorities, priority, <PyObject *> {}) # {}{}",
                alt * len(style_properties) + style_property_index[stylepropname],
                value, alt_name, stylepropname)

    g.write("return 0")
    g.dedent()

    g.write("")
    g.write('register_property_function("{}", {}_property)', name, name)
    g.write("")

    pass

def generate_property_functions():
    """
    This generates code that defines the property functions.
    """

    g = CodeGen("stylepropertyfunctions.pxi")

    for propname, proplist in all_properties.items():
        for prefix in sorted(prefixes.values(), key=lambda p : p.index):
            generate_property_function(g, prefix, propname, proplist)

    g.close()

def generate_property(g, propname, prefix):
    """
    This generates the code for a single property on the style object.
    """

    name = prefix.name + propname

    g.write("property {}:", name)
    g.indent()

    if name in style_properties:
        # __get__
        g.write("def __get__(self):")
        g.indent()
        g.write("return self._get({})", style_property_index[propname])
        g.dedent()

    # __set__
    g.write("def __set__(self, value):")
    g.indent()
    g.write("self.properties.append({{ '{}' : value }})", name)
    g.dedent()

    # __del__
    g.write("def __del__(self):")
    g.indent()
    g.write("self.delattr('{}')", name)
    g.dedent()

    g.dedent()
    g.write("")

def generate_properties():

    g = CodeGen("styleproperties.pxi")

    g.write("cdef class Style(StyleCore):")
    g.write("")

    g.indent()

    for propname in all_properties:
        for prefix in sorted(prefixes.values(), key=lambda p : p.index):
            generate_property(g, propname, prefix)

    g.dedent()
    g.close()

def generate():
    generate_constants()
    generate_property_functions()
    generate_properties()

if __name__ == "__main__":
    generate()
