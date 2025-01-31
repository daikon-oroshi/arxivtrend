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
        "plotColorPalette":"{%- for c in colors -%}
        {{c}}{% if not loop.last %},{% endif %}
        {%- endfor -%}"
      }
    }
  }
}%%
xychart-beta;
  x-axis [
    {%- for p in period -%}
      {{p.period_from}}{% if not loop.last %},{% endif %}
    {%- endfor -%}
  ];
  y-axis 0 --> {{max_of_count}};
  {%- for t in top10_tokens %}
  line "{{t.word}}-{{t.pos}}" [
    {%- for p in period -%}
      {{p.get_count_by_word(t)}}{% if not loop.last %},{% endif %}
    {%- endfor -%}
  ];
  {%- endfor %}
....

.色対応表
|===
| 色 |単語 |品詞
{%- for t in top10_tokens %}

|[{{colors[loop.index-1]}}]#a#
|{{t.word}}
|{{t.pos}}
{%- endfor %}
|===