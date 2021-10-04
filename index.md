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

[Lecture Recordings](https://podcast.ucsd.edu/watch/fa21/dsc40a_a00){: .btn .btn-blue } [Assignment Solutions](https://campuswire.com/c/GF82D3B2E/feed/73){: .btn .btn-purple }

{% for module in site.modules %}
{{ module }}
{% endfor %}
