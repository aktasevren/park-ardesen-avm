#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yuvarlak bayrak simgeleri — satır içi SVG (dış istek yok)."""

# Hepsi 24x24 daire içine kırpılmış.
_TR = ('<svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="bk-tr">'
       '<circle cx="12" cy="12" r="12"/></clipPath></defs><g clip-path="url(#bk-tr)">'
       '<rect width="24" height="24" fill="#E30A17"/>'
       '<circle cx="10.4" cy="12" r="5" fill="#fff"/>'
       '<circle cx="11.8" cy="12" r="4" fill="#E30A17"/>'
       '<path fill="#fff" d="M15.6 12l3.2-1.05-1.98 2.72V10.3l1.98 2.72z"/>'
       '</g></svg>')

_EN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="bk-en">'
       '<circle cx="12" cy="12" r="12"/></clipPath></defs><g clip-path="url(#bk-en)">'
       '<rect width="24" height="24" fill="#012169"/>'
       '<path d="M0 0l24 24M24 0L0 24" stroke="#fff" stroke-width="5"/>'
       '<path d="M0 0l24 24M24 0L0 24" stroke="#C8102E" stroke-width="3"/>'
       '<path d="M12 0v24M0 12h24" stroke="#fff" stroke-width="8"/>'
       '<path d="M12 0v24M0 12h24" stroke="#C8102E" stroke-width="4.6"/>'
       '</g></svg>')

_KA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="bk-ka">'
       '<circle cx="12" cy="12" r="12"/></clipPath></defs><g clip-path="url(#bk-ka)">'
       '<rect width="24" height="24" fill="#fff"/>'
       '<path d="M10 0h4v24h-4zM0 10h24v4H0z" fill="#FF0000"/>'
       '<g fill="#FF0000">'
       '<path d="M4.1 4.1h1.5v1.3h1.3v1.5H5.6v1.3H4.1V6.9H2.8V5.4h1.3z"/>'
       '<path d="M18.4 4.1h1.5v1.3h1.3v1.5h-1.3v1.3h-1.5V6.9h-1.3V5.4h1.3z"/>'
       '<path d="M4.1 16.9h1.5v1.3h1.3v1.5H5.6V21H4.1v-1.3H2.8v-1.5h1.3z"/>'
       '<path d="M18.4 16.9h1.5v1.3h1.3v1.5h-1.3V21h-1.5v-1.3h-1.3v-1.5h1.3z"/>'
       '</g></g></svg>')

# Arapça için BAE bayrağı: net, tanınır ve doğru çizilebilir.
_AR = ('<svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="bk-ar">'
       '<circle cx="12" cy="12" r="12"/></clipPath></defs><g clip-path="url(#bk-ar)">'
       '<rect width="24" height="8" y="0" fill="#00732F"/>'
       '<rect width="24" height="8" y="8" fill="#fff"/>'
       '<rect width="24" height="8" y="16" fill="#000"/>'
       '<rect width="7" height="24" fill="#FF0000"/>'
       '</g></svg>')

BAYRAK = {"tr": _TR, "en": _EN, "ka": _KA, "ar": _AR}
