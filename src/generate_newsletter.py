import os
import json
import yaml
from jinja2 import Template
from google import genai
from google.genai import types

STATE_FILE = "data/state.json"
OUTPUT_DIR = "newsletters"
DAYS = ["monday", "wednesday", "friday", "sunday"]

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"season_folder": "season-01-secure-foundations", "week": 1, "day_index": 0}

def save_state(season_folder, current_week, current_day_index):
    next_day_index = current_day_index + 1
    next_week = current_week
    
    if next_day_index >= 4:
        next_day_index = 0
        next_week += 1
        
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "season_folder": season_folder,
            "week": next_week,
            "day_index": next_day_index
        }, f, indent=4)

def get_valid_model(client):
    """Queries live models from the user API profile to guarantee 404 elimination."""
    try:
        available_models = [m.name for m in client.models.list()]
        for model in ["models/gemini-2.5-flash", "models/gemini-1.5-flash"]:
            if model in available_models:
                return model
    except Exception:
        pass
    return "gemini-2.5-flash"

def main():
    state = load_state()
    season = state["season_folder"]
    week = state["week"]
    day_index = state["day_index"]
    current_day = DAYS[day_index]

    yaml_path = f"curriculum/{season}/week-{week:02d}/{current_day}.yaml"
    if not os.path.exists(yaml_path):
        print(f"Target configuration card file missing: {yaml_path}")
        return

    with open(yaml_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)

    is_review = meta["metadata"].get("is_review", False)
    template_path = "templates/sunday_disaster.md" if is_review else "templates/weekday_story.md"

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model_target = get_valid_model(client)
    print(f"Routing generation pipeline through active execution node: {model_target}")

    system_instruction = (
        "You are an expert AWS Solutions Architect. Your role is to return pure data string "
        "attributes matching the requested JSON output blueprint framework layout completely. "
        "Do not wrap JSON properties inside markdown backticks or conversational filler text lines. "
        "Maintain an advanced engineering narrative style mixed with dry, witty Simpsons character choices."
    )

    if is_review:
        prompt = f"""
        Compile an advanced AWS Forensic Incident Post-Mortem.
        Topic: {meta['technical_core']['topic']}
        Services: {meta['technical_core']['target_services']}
        Simpsons Narrative Anchor: {meta['technical_core']['simpsons_angle']}
        
        Generate values for this structural schema layout:
        {{
          "episode_title": "{meta['metadata']['episode_title']}",
          "incident_timeline": "Detailed step-by-step technical log of the crash based on: {meta['forensic_prompts']['timeline_prompt']}",
          "root_cause": "Advanced systemic failure review answering: {meta['forensic_prompts']['root_cause_prompt']}",
          "financial_damage": "Calculation breakdown processing business losses based on: {meta['forensic_prompts']['financial_prompt']}",
          "lessons_learned": "Production recovery engineering guidelines answering: {meta['forensic_prompts']['lessons_prompt']}",
          "next_week_teaser": "High-yield forward-looking teaser text preparing for the next season arc topic step."
        }}
        """
    else:
        prompt = f"""
        Compile an elite technical cloud architecture newsletter lesson module data layout.
        Topic: {meta['technical_core']['topic']}
        Services: {meta['technical_core']['target_services']}
        Simpsons Narrative Setup: {meta['narrative_hooks']['simpsons_angle']}
        
        Generate values for this structural schema layout:
        {{
          "episode_title": "{meta['metadata']['episode_title']}",
          "curiosity": "Generate one highly unexpected, paradox-style question analyzing the surprising fact: {meta['technical_core']['surprising_fact']} and debunking the misconception: {meta['technical_core']['misconception']}",
          "story_narrative": "Multi-paragraph rich narrative expansion tracking the story elements. Lisa is the Well-Architected standard, Homer causes cost issues, Bart causes security gaps.",
          "burns_evaluation": "A deep analysis tearing down this specific proposal suggestion: {meta['narrative_hooks']['burns_proposal']}",
          "barts_evaluation": "A forensic breakdown of exactly why this security failure happened: {meta['narrative_hooks']['barts_incident']}",
          "decision_tree": {{
             "scenario": "{meta['decision_tree']['scenario']}",
             "options": {json.dumps(meta['decision_tree']['options'])},
             "correct_option": "{meta['decision_tree']['correct_option']}",
             "rationale": "{meta['decision_tree']['rationale']}"
          }},
          "exam_radar": {{
             "trigger": "{meta['exam_radar']['trigger']}",
             "distractor": "{meta['exam_radar']['distractor']}",
             "truth": "{meta['exam_radar']['truth']}"
          }},
          "interview": {{
             "challenge": "{meta['interview']['challenge']}",
             "answer": "{meta['interview']['answer']}"
          }},
          "guardrails": {{
             "dos": ["Concrete DO implementation tip 1", "Concrete DO implementation tip 2"],
             "donts": ["Dangerous DON'T anti-pattern 1", "Dangerous DON'T anti-pattern 2"]
          }},
          "project": {{
             "title": "{meta['project']['title']}",
             "objective": "{meta['project']['objective']}",
             "steps": {json.dumps(meta['project']['steps'])}
          }},
          "technical_math": "Write out the performance metrics or math equations clearly using plain-text code blocks based on: {meta['technical_math_prompt']}",
          "cliffhanger": "{meta['cliffhanger_prompt']}"
        }}
        """

    response = client.models.generate_content(
        model=model_target,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.5
        )
    )

    # Process and build JSON payload
    raw_json = json.loads(response.text)
    raw_json["metadata"] = meta["metadata"]
    raw_json["technical_core"] = meta["technical_core"]
    raw_json["narrative_hooks"] = meta.get("narrative_hooks", {})
    raw_json["brain_upgrade"] = meta.get("brain_upgrade", {})
    
    if is_review:
        raw_json["review_drills"] = meta["review_drills"]

    # Read specific presentation layout template target
    with open(template_path, "r", encoding="utf-8") as t_file:
        template = Template(t_file.read())

    final_markdown = template.render(raw_json)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = f"{OUTPUT_DIR}/week_{week:02d}_{current_day}.md"
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(final_markdown)

    print(f"Successfully generated decoupled issue output: {out_path}")
    save_state(season, week, day_index)

if __name__ == "__main__":
    main()