---
layout: Post
permalink: /publications/
title: Publications & Press
content-type: eg
---


### Publications 
<ol>
{% for item in site.data.publications %}
    {% if item.link == "/" %}
        <li>
            {{ item.date }} - {{ item.name }}
        </li>
    {% else %}
        <li>
            <a href="{{ item.link }}">
            {{ item.date }} - {{ item.name }}
            </a>
        </li>
    {% endif %}
{% endfor %}
</ol>

### Press clipping
<ol>
{% for item in site.data.press %}
    {% if item.link == "/" %}
        <li>
            {{ item.date }} - {{ item.name }}
        </li>
    {% else %}
        <li>
            <a href="{{ item.link }}">
            {{ item.date }} - {{ item.name }}
            </a>
        </li>
    {% endif %}
{% endfor %}
</ol>

### Awards
<ol>
{% for item in site.data.awards %}
    {% if item.link == "/" %}
        <li>
            {{ item.date }} - {{ item.name }}
        </li>
    {% else %}
        <li>
            <a href="{{ item.link }}">
            {{ item.date }} - {{ item.name }}
            </a>
        </li>
    {% endif %}
{% endfor %}
</ol>


