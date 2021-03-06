# -*- coding: utf-8 -*-

"""
Copyright (c) 2009 Barry Schwartz

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

import fontforge
from sortsmill import font_db
from sortsmill.spacing_by_anchors import *
from sortsmill.glyphbuild import *

def build_glyphs(bitbucket, f):

    from sortsmill import cap_spacing

    figures = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    lining_figures = [s + '.lining' for s in figures]

    caps = [
        'A', 'Agrave', 'Aacute', 'Acircumflex', 'Atilde', 'Adieresis', 'Aring', 'Amacron', 'Abreve', 'Aogonek',
        'B',
        'C', 'Ccedilla', 'Cacute', 'Ccircumflex', 'Cdotaccent', 'Ccaron',
        'D', 'Dcaron', 'Dcroat',
        'E', 'Egrave', 'Eacute', 'Ecircumflex', 'Edieresis', 'Emacron', 'Ebreve', 'Edotaccent', 'Eogonek', 'Ecaron',
        'F',
        'G', 'Gcircumflex', 'Gbreve', 'Gdotaccent', 'Gcommaaccent',
        'H', 'Hcircumflex', 'Hbar',
        'I', 'Igrave', 'Iacute', 'Icircumflex', 'Idieresis', 'Itilde', 'Imacron', 'Ibreve', 'Iogonek',
        'J', 'Jcircumflex',
        'K', 'Kcommaaccent',
        'L', 'Lacute', 'Lcommaaccent', 'Lcaron', 'Ldot', 'Lslash',
        'M',
        'N', 'Ntilde', 'Nacute', 'Ncommaaccent', 'Ncaron',
        'O', 'Ograve', 'Oacute', 'Ocircumflex', 'Otilde', 'Odieresis', 'Oslash', 'Omacron', 'Obreve', 'Ohungarumlaut',
        'P',
        'Q',
        'R', 'Racute', 'Rcommaaccent', 'Rcaron',
        'S', 'Sacute', 'Scircumflex', 'Scedilla', 'uni0218', 'Scaron',
        'T', 'uni0162', 'uni021A', 'Tcaron', 'Tbar',
        'U', 'Ugrave', 'Uacute', 'Ucircumflex', 'Udieresis', 'Utilde', 'Umacron', 'Ubreve', 'Uring', 'Uhungarumlaut', 'Uogonek',
        'V',
        'W', 'Wcircumflex',
        'X',
        'Y', 'Yacute', 'Ydieresis', 'Ycircumflex',
        'Z', 'Zacute', 'Zdotaccent', 'Zcaron',
        'IJ', 'AE', 'OE', 'Eth', 'Thorn',
        'question', 'questiondown',
        'exclam', 'exclamdown',
        'ampersand'
        ]

    def base(letter):
        if letter == 'i':
            base = 'dotlessi'
        elif letter == 'j':
            base = 'uni0237'
        else:
            base = letter
        return base    

    db = font_db.db_create(f)

    db['spacing_anchor_heights'] = { 'hi' : 732, # caps and ascenders
                                     't'  : 562, # top diacritics
                                     'x'  : 415,  # ex-height
                                     'o'  : 220,  # like the letter o
                                     'bl' : 20,   # baseline
                                     'lo' : -205 } # descenders

    build_several_space_glyphs(f, emsize = 1000, spacesize = 213,
                               thinspacesize = 1000 / 6,
                               hairspacesize = 1000 / 10,
                               tabwidth = f['zero.lining'].width)
    propagate_hyphens(f)
    propagate_hyphens(f, '.uppercase')
    build_spacing_marks(f, width = 439)

    make_glyph_reference('quotesingle', f['quoteright'])
    make_glyph_reference('quotedbl', f['quotedblright'])
    make_glyph_reference('i.TRK', f['i'])
    make_glyph_reference('Dcroat', f['Eth'])
    make_glyph_reference('dcroat.sc', f['eth.sc'])

    make_glyph_reference('uni00B9', f['one.lining.sup'])
    make_glyph_reference('uni00B2', f['two.lining.sup'])
    make_glyph_reference('uni00B3', f['three.lining.sup'])
    for g in f:
        if g[-4:] == '.sup':
            make_glyph_reference(g[:-4] + '.sub', f[g], (1, 0, 0, 1, 0, -707))
    for g in lining_figures + ['comma', 'period']:
        make_glyph_reference(g + '.numer', f[g + '.sup'], (1, 0, 0, 1, 0, -177))
    for g in lining_figures + ['comma', 'period']:
        make_glyph_reference(g + '.denom', f[g + '.sup'], (1, 0, 0, 1, 0, -386))
    build_multigraph('onequarter', [f['one.lining.numer'], f['fraction'], f['four.lining.denom']])
    build_multigraph('onehalf', [f['one.lining.numer'], f['fraction'], f['two.lining.denom']])
    build_multigraph('threequarters', [f['three.lining.numer'], f['fraction'], f['four.lining.denom']])

    for g in f:
        if g[-3:] == '.sc':
            if g == 'periodcentered.sc':
                make_glyph_reference(g[:-3] + '.c2', f[g])
            elif g == 'uni0163.sc':
                make_glyph_reference('uni0162.c2', f[g])
            elif g == 'uni0219.sc':
                make_glyph_reference('uni0218.c2', f[g])
            elif g == 'uni021B.sc':
                make_glyph_reference('uni021A.c2', f[g])
            elif g in ('ae.sc', 'oe.sc'):
                make_glyph_reference(g[:-3].upper() + '.c2', f[g])
            else:
                make_glyph_reference(g[:-3].capitalize() + '.c2', f[g])

    #--------------------------------------------------------------------------

    for letter in 'GKkLlNnRr':
                build_accented_glyph(letter + 'commaaccent', f[base(letter)], f['uni0326'])
    build_accented_glyph('gcommaaccent', f['g'], f['uni0312'])
    build_accented_glyph('uni0218', f['S'], f['uni0326'])
    build_accented_glyph('uni0219', f['s'], f['uni0326'])
    build_accented_glyph('uni021A', f['T'], f['uni0326'])
    build_accented_glyph('uni021B', f['t'], f['uni0326'])

    for letter in 'gklnr':
                build_accented_glyph(letter + 'commaaccent.sc', f[letter + '.sc'], f['uni0326'])
    build_accented_glyph('uni0219.sc', f['s.sc'], f['uni0326'])
    build_accented_glyph('uni021B.sc', f['t.sc'], f['uni0326'])

    #--------------------------------------------------------------------------

    for letter in 'CcSs':
                build_accented_glyph(letter + 'cedilla', f[base(letter)], f['uni0327'])
    build_accented_glyph('uni0162', f['T'], f['uni0327'])
    build_accented_glyph('uni0163', f['t'], f['uni0327'])

    for letter in 'cs':
                build_accented_glyph(letter + 'cedilla.sc', f[letter + '.sc'], f['uni0327'])
    build_accented_glyph('uni0163.sc', f['t.sc'], f['uni0327'])

    #--------------------------------------------------------------------------

    for letter in 'AaEeIiOoUu':
                build_accented_glyph(letter + 'grave', f[base(letter)], f['gravecomb'])

    for letter in 'aeiou':
                build_accented_glyph(letter + 'grave.sc', f[letter + '.sc'], f['gravecomb'])

    #--------------------------------------------------------------------------

    for letter in 'AaCcEeIiLlNnOoRrSsUuYyZz':
                build_accented_glyph(letter + 'acute', f[base(letter)], f['acutecomb'])

    for letter in 'aceilnorsuyz':
                build_accented_glyph(letter + 'acute.sc', f[letter + '.sc'], f['acutecomb'])

    #--------------------------------------------------------------------------

    for letter in 'AaIiNnOoUu':
                build_accented_glyph(letter + 'tilde', f[base(letter)], f['tildecomb'])

    for letter in 'ainou':
                build_accented_glyph(letter + 'tilde.sc', f[letter + '.sc'], f['tildecomb'])

    #--------------------------------------------------------------------------

    for letter in 'AaEeIiOoUuYy':
                build_accented_glyph(letter + 'dieresis', f[base(letter)], f['uni0308'])

    for letter in 'aeiouy':
                build_accented_glyph(letter + 'dieresis.sc', f[letter + '.sc'], f['uni0308'])

    #--------------------------------------------------------------------------

    for letter in 'AaUu':
                build_accented_glyph(letter + 'ring', f[base(letter)], f['uni030A'])

    for letter in 'au':
                build_accented_glyph(letter + 'ring.sc', f[letter + '.sc'], f['uni030A'])

    #--------------------------------------------------------------------------

    for letter in 'AaCcEeGgHhIiJjOoSsUuWwYy':
        build_accented_glyph(letter + 'circumflex', f[base(letter)], f['uni0302'])

    for letter in 'aceghijosuwy':
        build_accented_glyph(letter + 'circumflex.sc', f[letter + '.sc'], f['uni0302'])

    #--------------------------------------------------------------------------

    for letter in 'AaEeGgIiOoUu':
                build_accented_glyph(letter + 'breve', f[base(letter)], f['uni0306'])

    for letter in 'aegiou':
                build_accented_glyph(letter + 'breve.sc', f[letter + '.sc'], f['uni0306'])

    #--------------------------------------------------------------------------

    for letter in 'CcEeGgIZz':
                build_accented_glyph(letter + 'dotaccent', f[base(letter)], f['uni0307'])

    for letter in 'cegz':
                build_accented_glyph(letter + 'dotaccent.sc', f[letter + '.sc'], f['uni0307'])
    build_accented_glyph('i.TRK.sc', f['i.sc'], f['uni0307'])

    #--------------------------------------------------------------------------

    for letter in 'CcDEeNnRrTSsZz':
                build_accented_glyph(letter + 'caron', f[base(letter)], f['uni030C'])
    for letter in 'dLlt':
                build_accented_glyph(letter + 'caron', f[base(letter)], f['uni0315'])

    for letter in 'cdenrstz':
                build_accented_glyph(letter + 'caron.sc', f[letter + '.sc'], f['uni030C'])
    build_accented_glyph('lcaron.sc', f['l.sc'], f['uni0315'])

    #--------------------------------------------------------------------------

    for letter in 'AaEeIiOoUu':
                build_accented_glyph(letter + 'macron', f[base(letter)], f['uni0304'])

    for letter in 'aeiou':
                build_accented_glyph(letter + 'macron.sc', f[letter + '.sc'], f['uni0304'])

    #--------------------------------------------------------------------------

    for letter in 'OoUu':
                build_accented_glyph(letter + 'hungarumlaut', f[base(letter)], f['uni030B'])

    for letter in 'ou':
                build_accented_glyph(letter + 'hungarumlaut.sc', f[letter + '.sc'], f['uni030B'])

    #--------------------------------------------------------------------------

    build_multigraph('ellipsis', [f['period'], f['period'], f['period']])
    build_multigraph('napostrophe', [f['quoteright'], f['n']])
    build_multigraph('IJ', [f['I'], f['J']])
    build_multigraph('ij', [f['i'], f['j']])
    build_multigraph('Ldot', [f['L'], f['periodcentered']])
    build_multigraph('ldot', [f['l'], f['periodcentered']])
    build_multigraph('ldot.sc', [f['l.sc'], f['periodcentered.sc']])

    #--------------------------------------------------------------------------

    f.selection.all()
    spacing_by_anchors.space_selected_by_anchors(f)
    f.selection.none()

    generate_kerning_and_read_features(None, f)

    #--------------------------------------------------------------------------

    font_db.db_close(f)

    #--------------------------------------------------------------------------
