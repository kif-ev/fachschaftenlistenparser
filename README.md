# Fachschaftenlistenparser

Gibt die Einträge der [Liste der KIF
Fachschaften](https://wiki.kif.rocks/wiki/Liste_unserer_Fachschaften) im
json-Format aus. Das resultierende json kann man dann auf der Kommandozeile
direkt mit z.B. [jq](https://stedolan.github.io/jq/) weiter bearbeiten:

```shell
python3 fachschaftenlistenparser.py | jq '.[]|.email // empty'
```
