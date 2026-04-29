import streamlit as st
import subprocess
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(page_title="Savage Local Squad", layout="wide")
st.title("🩸 Savage Local Squad")

# ====================== PATHS ======================
HOME = "/Users/lenaaoyama"   # ← Change if your username is different
CODER_MODEL = f"{HOME}/qwen-coder-32b"
CRITIC_MODEL = f"{HOME}/qwen2.5-72b-q4"
DOCS_FOLDER = f"{HOME}/docs"   # Put your files here

MEMORY_FILE = "coding_memory.json"

def load_memory():
    if Path(MEMORY_FILE).exists():
        return json.loads(Path(MEMORY_FILE).read_text(encoding="utf-8"))
    return {"history": []}

def save_memory(data):
    Path(MEMORY_FILE).write_text(json.dumps(data, indent=2, ensure_ascii=False))

def run_mlx(model_path, prompt, max_tokens=3800, temp=0.88):
    temp_file = Path("temp_task.txt")
    temp_file.write_text(prompt, encoding="utf-8")
    
    cmd = f'source ~/mlx_env/bin/activate && mlx_lm.generate --model {model_path} --prompt "$(cat temp_task.txt)" --max-tokens {max_tokens} --temp {temp}'
    
    with st.spinner(f"Running {Path(model_path).name}..."):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)
    
    temp_file.unlink(missing_ok=True)
    return result.stdout.strip() or "No output"

# ====================== LIGHTWEIGHT RAG ======================
def load_docs():
    docs_text = ""
    if Path(DOCS_FOLDER).exists():
        for file in Path(DOCS_FOLDER).glob("**/*.*"):
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                docs_text += f"\n--- {file.name} ---\n{content[:1500]}\n"
            except:
                pass
    return docs_text[:8000]  # Limit context size

# ====================== UI ======================
mode = st.radio("Select Mode", 
                ["🔨 Brutal Code Factory (32B Coder + 72B Critic)", 
                 "🧠 Mad Researcher (72B + Light RAG)"], horizontal=True)

task = st.text_area("Your task:", height=160)

if st.button("Unleash the Beast", type="primary"):
    if not task.strip():
        st.error("Give me a task.")
        st.stop()

    mem = load_memory()

    if "Code Factory" in mode:
        # Brutal Code Factory
        context = "\n\n".join([h.get("output", "")[:400] for h in mem["history"][-3:]])

        coder_prompt = f"""Previous context:\n{context}\n\nYou are a code-raping machine.
STAY ON TASK. ALWAYS start directly with ```python
Output ONLY the complete production-ready code. No explanations.

Task: {task}"""

        code_output = run_mlx(CODER_MODEL, coder_prompt, 3800, 0.9)

        critic_prompt = f"""You are PsychoCritic — psychotic savage warlord.
Roast this code brutally. Point out every weakness. Then give a much meaner, tighter version.

Code:
{code_output}"""

        critique = run_mlx(CRITIC_MODEL, critic_prompt, 2800, 0.85)

        st.subheader("🛠️ Coder (32B)")
        st.code(code_output, language="python", line_numbers=True)
        
        st.subheader("🔥 Critic (72B)")
        st.code(critique, language="python", line_numbers=True)

        final_output = critique

    else:
        # Mad Researcher with Light RAG
        docs = load_docs()
        researcher_prompt = f"""You are Mad Researcher — psychotic savage analyst.
Use the following documents if relevant:

{docs}

Task: {task}

Be extremely thorough, brutal, and insightful."""

        final_output = run_mlx(CRITIC_MODEL, researcher_prompt, 3200, 0.85)

        st.subheader("🧠 Mad Researcher (72B + RAG)")
        st.code(final_output, language="python", line_numbers=True)

    # Save
    mem["history"].append({
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "task": task[:300],
        "output": final_output
    })
    if len(mem["history"]) > 10:
        mem["history"] = mem["history"][-8:]
    save_memory(mem)

# History
with st.sidebar:
    st.header("History")
    mem = load_memory()
    for entry in reversed(mem["history"]):
        with st.expander(f"{entry['timestamp'][:16]}"):
            st.caption(entry["task"])
            st.code(entry.get("output", "No output")[:1200] + "...", language="python")