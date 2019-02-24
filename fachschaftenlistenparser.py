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

# put more formatter functions here (yes really)

# keep the formatters dict outside of the formatter function, if it's in the
# function it will be re-built on each call, which isn't the most efficient
formatters = {
        'anschrift': format_anschrift,
        'besucheradresse': format_anschrift,
        'email': format_email,
}
def formatter(key):
    return formatters.get(key, lambda n: n)

r = requests.get(
        'https://wiki.kif.rocks/w/index.php?action=raw&title=Liste_unserer_Fachschaften'
)

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
        hs[key] = formatter(key)(val)
    res.append(hs)

print(json.dumps(res))
