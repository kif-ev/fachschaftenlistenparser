import mwparserfromhell
import requests

list_url = 'https://wiki.kif.rocks/w/index.php?action=raw&title=Liste_unserer_Fachschaften'

r = requests.get(list_url)
r.raise_for_status()

wikitext = mwparserfromhell.parse(r.text, skip_style_tags=True)

zeilen_matcher = (lambda n: n.name.matches('FSListe Zeile\n'))
for t in wikitext.filter_templates(matches=zeilen_matcher):
    for param in t.params:
        if param.name.matches('fon'):
            val = param.value.strip()
            if not val: continue
            print(val)
