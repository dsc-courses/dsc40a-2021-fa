---
layout: home
title: Home
nav_exclude: false
nav_order: 1
seo:
  type: Course
  name: Just the Class
---

# {{ site.tagline }} 🧠
{: .mb-2 }
{{ site.description }}
{: .fs-6 .fw-300 }

{{ site.staffersnobio }}

[Lecture recordings](https://podcast.ucsd.edu/watch/fa21/dsc40a_a00){: .btn .btn-blue }

{% for module in site.modules %}
{{ module }}
{% endfor %}
