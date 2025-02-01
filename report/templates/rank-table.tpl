[cols="^1,4,4", options="header"]
|===
|数 |単語 | 品詞
{% for tc in token_counts %}
|{{tc.count}}回
| {{ tc.token.word }}
| {{tc.token.pos}}
{% endfor %}
|===