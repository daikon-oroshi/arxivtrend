= arXivトレンドレポート

以下の条件でarXivの論文概要を検索し、その中で多く現れた単語 (名詞、動詞、形容詞) の数を年次、月次、週次でグラフ化します。

.検索クエリー
|===
|名前 |値

|検索ワード
|{{query.search_q}}

|期間 (開始)
|{{query.submitted_begin}}

|期間 (終了)
|{{query.submitted_end}}

|カテゴリー
|{{query.category}}
|===


== 全期間


.全期間TOP10
[mermaid]
....
xychart-beta;
  x-axis [
    {%- for tc in report.whole.top10|reverse -%}
      {{ tc.token.word }}{% if not loop.last %},{% endif %}
    {%- endfor -%}
  ];
  y-axis 0 --> {{ report.whole.max_of_count }};
  bar [
    {%- for tc in report.whole.top10|reverse -%}
      {{tc.count}}{% if not loop.last %},{% endif %}
    {%- endfor -%}
  ];
....


.全期間TOP20
{% with token_counts = report.whole.top20 %}
{% include 'rank-table.tpl' %}
{% endwith %}


=== 名詞集計


.全期間名詞TOP20
{% with token_counts = report.whole.noun %}
{% include 'rank-table.tpl' %}
{% endwith %}


=== 動詞集計


.全期間動詞TOP20
{% with token_counts = report.whole.verb %}
{% include 'rank-table.tpl' %}
{% endwith %}


=== 形容詞集計


.全期間形容詞TOP20
{% with token_counts = report.whole.adj %}
{% include 'rank-table.tpl' %}
{% endwith %}


{% if report.annual|length > 1 %}

== 年次

全期間でTOP10に入った単語を年次でグラフ化します。

{% with
  period = report.annual,
  top10_tokens = report.whole.top10_tokens,
  max_of_count=report.annual_max_of_count
%}
{% include 'period-aggregate.tpl' %}
{% endwith %}

{% endif %}


{% if report.monthly|length %}
== 月次

全期間でTOP10に入った単語を月次でグラフ化します。

{% with
  period = report.monthly,
  top10_tokens = report.whole.top10_tokens,
  max_of_count=report.monthly_max_of_count
%}
{% include 'period-aggregate.tpl' %}
{% endwith %}

{% endif %}


{% if report.weekly|length > 1 %}
== 週次

全期間でTOP10に入った単語を週次でグラフ化します。

{% with
  period = report.weekly,
  top10_tokens = report.whole.top10_tokens,
  max_of_count=report.weekly_max_of_count
%}
{% include 'period-aggregate.tpl' %}
{% endwith %}

{% endif %}