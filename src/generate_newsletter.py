import os
import json
import yaml
from google import genai
from google.genai import types

STATE_FILE = "data/state.json"
OUTPUT_DIR = "newsletters"
DAYS = ["mon", "wed", "fri", "sun"]

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"week": 1, "day_index": 0}

def save_state(current_week, current_day_index):
    next_day_index = current_day_index + 1
    next_week = current_week

    if next_day_index >= 4:
        next_day_index = 0
        next_week += 1

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"week": next_week, "day_index": next_day_index}, f, indent=4)

def main():
    state = load_state()
    week = state["week"]
    day_index = state["day_index"]
    current_day = DAYS[day_index]

    yaml_path = f"curriculum/week-{week:02d}-{current_day}.yaml"
    if not os.path.exists(yaml_path):
        print(f"File target not found, terminating gracefully: {yaml_path}")
        return

    with open(yaml_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Critical Failure: Missing required GEMINI_API_KEY environment variable.")

    # Instantiate the modern, stateless SDK client mapping explicitly
    client = genai.Client(api_key=api_key)

    is_review = meta.get("is_review", False)
    
    if is_review:
        system_instruction = (
            "You are an expert AWS Solutions Architect specializing in operational forensics. "
            "Your objective is to generate an interactive AWS Sunday Incident Review newsletter. "
            "Maintain an advanced, professional engineering architecture tone while using the provided "
            "Simpsons scenario context to anchor the diagnostic challenge. Do not output conversational filler. "
            "Start directly with the Markdown title '# 🚨 Incident Report: Topic Name'."
        )
        prompt_structure = f"""
        Generate a comprehensive, scenario-based AWS Sunday Incident Review newsletter.
        Week Counter: {meta['week']}
        Forensic Case Focus: {meta['topic']}
        Target Infrastructure Layer: {meta['target_services']}
        Simpsons Narrative Hook: {meta['simpsons_angle']}
        Worst Architectural Move: {meta['worst_solution']}
        Best Cloud-Native Fix Strategy: {meta['best_solution']}
        
        The layout MUST contain these precise Markdown headers:
        1. # 🚨 Incident Report: [Topic Name]
        2. ## 📈 Analytical Breakdown of the Failure
        3. ## 🔬 SAA-Style Interactive Review Question (Provide a highly realistic scenario multiple choice question with 4 custom options)
        4. ## 🔑 Comprehensive Evaluation and Explanation of Options (Explain why the correct answer is pristine and deep dive into why every single distractor option fails structurally)
        5. ## 📊 Quantitative Calculations (Elaborate on this specific LaTeX math metric: {meta['technical_math']})
        """
    else:
        system_instruction = (
            "You are an elite AWS Solutions Architect and cloud infrastructure educator. "
            "Your objective is to generate a comprehensive, highly technical weekday AWS Solutions Architect "
            "Associate certification preparation newsletter. Use the provided Simpsons analogy to simplify "
            "the core intuition without diluting professional engineering terminology. Avoid conversational greetings. "
            "Start directly with the Markdown title '# ⚡ Week X, Drop Y: Topic Name'."
        )
        prompt_structure = f"""
        Generate a comprehensive technical AWS preparation newsletter.
        Week Counter: {meta['week']}
        Technical Topic Focus: {meta['topic']}
        Target Core Cloud Services: {meta['target_services']}
        Simpsons Narrative Hook: {meta['simpsons_angle']}
        The Monorail Anti-Pattern (Worst Design): {meta['worst_solution']}
        The Industrial Patch (Moderate Design): {meta['moderate_solution']}
        The Well-Architected Masterpiece (Best Design): {meta['best_solution']}
        
        The layout MUST include these exact Markdown headings:
        1. # ⚡ Week {meta['week']}: [Topic Name]
        2. ## 🎯 Curiosity Trigger
        3. ## 🏰 The Springfield Chronicles (Weave a deep, multi-paragraph conceptual analogy based on the hook)
        4. ## 🛠️ Technical Concept Deep-Dive (Explain the underlying service configurations, parameters, and flags deeply)
        5. ## 🧬 Architectural Design Evolution (Detail Worst vs Moderate vs Best architectures cleanly)
        6. ## 🚧 Architectural Guardrails: Do's and Don'ts
        7. ## 🔍 Similar Problems to Study
        8. ## 🏗️ Weekend Micro-Project Blueprint (Step-by-step hands-on challenge instructions)
        9. ## 📐 Technical Calculations & Logic (Expand on this required formula context using LaTeX notation: {meta['technical_math']})
        10. ## 🌪️ The Architect's Cliffhanger (End with a single, high-stakes unresolved problem or trade-off question to leave them thinking)
        """

    # Define your free-tier fallback hierarchy (from highest capability to fastest workhorse)
    FALLBACK_MODELS = [
        "gemini-3.5-flash",       # Tier 1: Best available free reasoning & instruction-following
        "gemini-2.5-flash",       # Tier 2: Highly stable, deeply reliable baseline
        "gemini-3.1-flash-lite"   # Tier 3: Ultra-fast backup meant for high-volume processing
    ]

    content = None
    
    # Iterate sequentially through the fallback models
    for model_name in FALLBACK_MODELS:
        try:
            print(f"Attempting generation using model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_structure,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.6,
                )
            )
            content = response.text
            print(f"✨ Success! Content compiled beautifully using {model_name}.")
            break  # Break out of the loop completely because we got our text
            
        except Exception as e:
            print(f"⚠️ Warning: {model_name} was bypassed, exhausted, or rate-limited.")
            print(f"Reason: {e}")
            print("Shifting down to the next tier in the fallback array...\n")
            continue

    # Final protection step if all free models fail to respond
    if not content:
        raise RuntimeError("❌ Catastrophic Error: All available free-tier models have exhausted their quotas.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = f"{OUTPUT_DIR}/week_{week:02d}_{current_day}.md"
    with open(output_filename, "w", encoding="utf-8") as out:
        out.write(response.text)

    print(f"Success: Newsletter file archived at {output_filename}")
    save_state(week, day_index)

if __name__ == "__main__":
    main()