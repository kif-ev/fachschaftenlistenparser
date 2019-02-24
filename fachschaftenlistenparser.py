"""
Returns a json formatted list of the KIF Fachschaften
"""

import json
import re
import mwparserfromhell
import requests

def format_anschrift(address):
    """
    Returns a correctly formatted postal address
    """
    return re.sub(r"<br>\n?", "\n", address)

def format_email(address):
    """
    Returns a correctly formatted and de-obfuscated email address
    """
    address = re.sub(r"\s*", "", address)
    address = re.sub(r"\(.t\)", "@", address)
    address = re.sub(r"\(punkt\)", ".", address)
    address = re.sub(r"\((strich|minus)\)", "-", address)
    return address

# put more formatter functions here (yes really)

# keep the FORMATTERS dict outside of the formatter function, if it's in the
# function it will be re-built on each call, which isn't the most efficient
FORMATTERS = {
    'anschrift': format_anschrift,
    'besucheradresse': format_anschrift,
    'email': format_email,
}
def formatter(key):
    """
    Returns the formatter function for the current key or identity
    """
    return FORMATTERS.get(key, lambda n: n)

def main():
    """
    Grabs the "Liste unserer Fachschaften" page and returns its contents as json
    """
    req = requests.get(
        'https://wiki.kif.rocks/w/index.php?action=raw&title=Liste_unserer_Fachschaften'
    )

    req.raise_for_status()

    wikitext = mwparserfromhell.parse(req.text, skip_style_tags=True)

    res = []

    zeilen_matcher = (lambda n: n.name.matches('FSListe Zeile\n'))
    for template in wikitext.filter_templates(matches=zeilen_matcher):
        hochschule = {}
        for param in template.params:
            val = param.value.strip()
            if not val:
                continue
            key = param.name.strip()
            hochschule[key] = formatter(key)(val)
        res.append(hochschule)

    print(json.dumps(res))

main()
