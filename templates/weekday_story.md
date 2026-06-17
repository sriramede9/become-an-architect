# 🎬 {{ metadata.season_name }}: Season 1
## 📂 Arc: {{ metadata.season_arc }}
### 📺 Episode {{ metadata.episode_number }}: {{ metadata.episode_title }}

**Timeline Context:**
* ◀️ Previous Week: *{{ metadata.previous_episode }}*
* ▶️ Coming Next: *{{ metadata.next_episode }}*

---

## 💡 The Technical Fact Sheet
* 🧠 **The Surprising Fact:** {{ technical_core.surprising_fact }}
* ❌ **The Common Misconception:** {{ technical_core.misconception }}

---

## 🏰 The Springfield Chronicles
{{ story_narrative }}

---

## 💰 Mr. Burns' Cost-Cutting Proposal
> **The Strategy:** "{{ narrative_hooks.burns_proposal }}"

### 📋 Architectural Analysis:
{{ burns_evaluation }}

---

## 🛹 Bart's Security Incident
> **The Breach:** "{{ narrative_hooks.barts_incident }}"

### 🔧 The Exploit Root Cause:
{{ barts_evaluation }}

---

## 🧠 Architect Brain Upgrade
* 🟢 **Beginner Thinks:** *{{ brain_upgrade.beginner }}*
* 🟡 **Intermediate Thinks:** *{{ brain_upgrade.intermediate }}*
* 🔵 **Architect Thinks:** **{{ brain_upgrade.architect }}**

---

## 🤔 What Would You Choose?
### The Architectural Dilemma:
{{ decision_tree.scenario }}

### Your Options:
{% for option, desc in decision_tree.options.items() %}
**{{ option }})** {{ desc }}
{% endfor %}

### The Architectural Instinct:
> **The Verdict:** **Option {{ decision_tree.correct_option }}**. {{ decision_tree.rationale }}

---

## ⚠️ Exam Trap Radar
* 🎯 **The Trigger Phrase:** "{{ exam_radar.trigger }}"
* 🪤 **The Distractor Trap:** {{ exam_radar.distractor }}
* 🔮 **The Architectural Truth:** {{ exam_radar.truth }}

---

## 🎤 You Are The Architect
> **The Stakeholder Challenge:** "{{ interview.challenge }}"

*Try to articulate your solution aloud before reading the blueprint answer below!*

### The Defense Blueprint:
{{ interview.answer }}

---

## 🏗️ Weekend Micro-Project Blueprint: {{ project.title }}
### The Goal:
{{ project.objective }}

### The Steps:
{% for step in project.steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

---

## 🌪️ The Architect's Cliffhanger
{{ cliffhanger }}