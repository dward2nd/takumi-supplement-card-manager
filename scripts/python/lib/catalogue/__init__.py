"""Promotion Catalogues: a Thai reading page per merchant per month (every promotion + a spending plan).

deterministic + idempotent — see each module.

Modules:
  markdown   Markdown → Notion blocks (headings, lists, callouts, tables, inline marks)
  cover      the cover image: the merchant's logo on a white plate, month, issuer cards
  store      Notion I/O for the Promotion Catalogues DB (find/create a page, dates, icon, cover, body)
  status     the Promotion Bureau's usage for a month, for the plan's "already used" lines

/write-catalogue (scripts/python/write-catalogue/cli.py) drives them.
"""
