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

**This website is in progress and all content is subject to change.**

[Zoom links](https://campuswire.com/c/GF82D3B2E/feed/1){: .btn .btn-purple } [Lecture recordings](#){: .btn .btn-blue }

{% for module in site.modules %}
{{ module }}
{% endfor %}
