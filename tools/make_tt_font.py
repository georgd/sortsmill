#!/usr/bin/python

"""
Copyright (c) 2009, 2010 Barry Schwartz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

#--------------------------------------------------------------------------

import fontforge
import os
import psMat
import re
import subprocess
import sys
import tempfile

font_extension = '.ttf'
name_modifier = 'TT'
generation_flags = ['opentype']

#--------------------------------------------------------------------------

def modify_names(f, modifier):
    f.fontname = modify_postscript_name(f.fontname, modifier)
    f.familyname = f.familyname + ' ' + modifier
    f.fullname = f.fullname + ' ' + modifier
    sfnt_names = f.sfnt_names
    for (lang, name_id, name) in sfnt_names:
        if (name_id in ['Family', 'Preferred Family', 'WWS Family'] and
            name[- (len(modifier) + 1):] != ' ' + modifier):
            f.appendSFNTName(lang, name_id, name + ' ' + modifier)

def modify_postscript_name(ps_name, modifier):
    m = re.match('^(.*)(-[^-]*)$', ps_name)
    if m:
        new_name = m.group(1) + modifier + m.group(2)
    else:
        new_name = ps_name + modifier
    return new_name

def compile_graphite(gdl_file, input_file, output_file):
    # Ignore warning 3521: 'Vertical overlap between glyphs in items 1
    # and 2; attachment may be needed'
    subprocess.call(['grcompiler', '-q', '-w3521', gdl_file, input_file, output_file])

# follow_references() assumes there are no mixtures of contours and
# references; thus, font.correctReferences() should have been run
# before follow_references() is called.
def follow_references(glyph):
    f = glyph.font
    leaves = []
    for ref in glyph.references:
        if len(f[ref[0]].references) != 0:
            subrefs = follow_references(f[ref[0]])
            leaves += [(r[0], psMat.compose(r[1], ref[1])) for r in subrefs]
        else:
            leaves.append(ref)
    return leaves

def generate_tt_font(f, unadorned_font_name, modifier,
                     output_dir = None,
                     emsize = None,
                     graphite_enabled = False):

    modify_names(f, modifier)

    if emsize != None:
        f.em = emsize
    f.layers['Fore'].is_quadratic = True
    f.selection.all()
    f.autoInstr()
    f.selection.none()

    if output_dir:
        ttf_file = os.path.join(output_dir, f.fontname + font_extension)
    else:
        ttf_file = f.fontname + font_extension

    gdl_file = unadorned_font_name + '.gdl'
    if graphite_enabled and os.path.exists(gdl_file):
        temp_ttf = tempfile.NamedTemporaryFile(suffix = '.ttf')
        print('Generating ' + temp_ttf.name)

        # grcompiler (version 2.4) seems not to like nested
        # references; it claims it can't compute the bounding box.  So
        # we resolve nested references.
        for g in f.glyphs():
            if len(g.references) != 0:
                g.references = follow_references(g)

        f.generate(temp_ttf.name, flags = generation_flags)
        print('Compiling Graphite: ' + gdl_file + ' ' + temp_ttf.name + ' -> ' + ttf_file)
        compile_graphite(gdl_file, temp_ttf.name, ttf_file)
        temp_ttf.close()
    else:
        print('Generating ' + ttf_file)
        f.generate(ttf_file, flags = generation_flags)

    print('Validating ' + ttf_file)
    subprocess.call(['fontlint', ttf_file])
    

#--------------------------------------------------------------------------

# If someone runs some script by using "fontforge -script", then name
# may be "__main__" and fontforge won't have a user interface, but
# also the |sys| module will not yet have an |argv| attribute. Weed
# out that case.  Perhaps fontforge should handle the situation
# better. (5 Nov 2009)
if __name__ == '__main__' and not fontforge.hasUserInterface() and hasattr(sys, 'argv'):

    for font_file in sys.argv[1:]:
        f = fontforge.open(font_file)
        generate_tt_font(f, name_modifier)
        f.close()

#--------------------------------------------------------------------------
