# 🚨 Springfield Disaster Review: Week {{ metadata.week }}
## 🔬 Post-Mortem Report: {{ metadata.episode_title }}

---

## ⏱️ Incident Timeline
{{ incident_timeline }}

---

## 🔍 Root Cause Analysis
{{ root_cause }}

---

## 💸 Financial & Brand Damage
{{ financial_damage }}

---

## 🧠 Lessons Learned & Remediation Actions
{{ lessons_learned }}

---

## 🔄 Spaced Repetition Drill (Reviewing Prior Lore)
*Try to answer these questions based on our past episodes before moving forward:*
{% for question in review_drills %}
**Question {{ loop.index }}:** {{ question }}
{% endfor %}

---

## 🔮 Next Week Teaser: Season Arc Preview
{{ next_week_teaser }}