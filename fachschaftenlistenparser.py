import mwparserfromhell
import requests
import json
import re

def format_anschrift(val):
    return re.sub(r"<br>\n?", "\n", val)

def format_email(val):
    res = re.sub(r"\s*", "", val)
    res = re.sub(r"\(.t\)", "@", res)
    res = re.sub(r"\(punkt\)", ".", res)
    res = re.sub(r"\((strich|minus)\)", "-", res)
    return res


list_url = 'https://wiki.kif.rocks/w/index.php?action=raw&title=Liste_unserer_Fachschaften'

r = requests.get(list_url)
r.raise_for_status()

wikitext = mwparserfromhell.parse(r.text, skip_style_tags=True)

res = []

zeilen_matcher = (lambda n: n.name.matches('FSListe Zeile\n'))
for t in wikitext.filter_templates(matches=zeilen_matcher):
    hs = {}
    for param in t.params:
        val = param.value.strip()
        if not val: continue
        key = param.name.strip()
        if key == 'anschrift': val = format_anschrift(val)
        if key == 'besucheradresse': val = format_anschrift(val)
        if key == 'email': val = format_email(val)
        hs[key] = val
    res.append(hs)

print(json.dumps(res))
