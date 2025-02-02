[mermaid]
....
xychart-beta;
  x-axis [
    {%- for p in period -%}
      {{p.period_from}}{% if not loop.last %},{% endif %}
    {%- endfor -%}
  ];
  y-axis 0 --> {{ max_count }}
  bar [
    {%- for p in period -%}
      {{p.paper_count}}{% if not loop.last %},{% endif %}
    {%- endfor -%}
  ];
....
