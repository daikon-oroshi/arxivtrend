|===
|単語 |数 | 品詞
{% for tc in token_counts %}
|{{ tc.token.word }}
|{{tc.count}}回
|{{tc.token.pos}}
{% endfor %}
|===