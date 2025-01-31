{%- set colors = [
    "gray",
    "black",
    "red",
    "maroon",
    "yellow",
    "lime",
    "green",
    "aqua",
    "blue",
    "purple"
] -%}
[mermaid]
....
%%{
  init:{
    "themeVariables":{
      "xyChart":{
        "plotColorPalette":"{%- for c in colors %}
        {{c}}{% if not loop.last %},{% endif %}
        {%- endfor %}"
      }
    }
  }
}%%
xychart-beta;
  x-axis [
    {%- for p in period %}
      {{p.period_from}}{% if not loop.last %},{% endif %}
    {%- endfor %}
  ];
  y-axis 0 --> {{max_of_count}};
  {%- for t in top10_tokens %}
  line "{{t.word}},{{t.pos}}" [
    {%- for p in period %}
      {{p.get_count_by_word(t)}}{{^-last}},{{/-last}}
    {%- endfor %}
  ];
  {%- endfor %}
....

.色対応表
|===
|単語 |品詞 | 色
{%- for _ in top10_tokens %}
|a
|動詞
|{{colors[loop.index]}}#◼︎#
{%- endfor %}
|===