import streamlit as st
import subprocess
from pathlib import Path
import json
from datetime import datetime

st.set_page_config(page_title="Savage Local Squad", layout="wide")

st.title("🩸 Savage Local Squad")

MEMORY_FILE = "coding_memory.json"

def load_memory():
    if Path(MEMORY_FILE).exists():
        return json.loads(Path(MEMORY_FILE).read_text(encoding="utf-8"))
    return {"history": []}

def save_memory(data):
    Path(MEMORY_FILE).write_text(json.dumps(data, indent=2, ensure_ascii=False))

def run_mlx(prompt, max_tokens=3800, temp=0.88):
    temp_file = Path("temp_task.txt")
    temp_file.write_text(prompt, encoding="utf-8")
    
    cmd = f'source ~/mlx_env/bin/activate && mlx_lm.generate --model ./qwen-coder-32b --prompt "$(cat temp_task.txt)" --max-tokens {max_tokens} --temp {temp}'
    
    with st.spinner("Unleashing the beast..."):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=420)
    
    temp_file.unlink(missing_ok=True)
    return result.stdout.strip() or "No output"

task = st.text_area("Your task:", height=140)

if st.button("Unleash the Beast", type="primary"):
    if task.strip():
        mem = load_memory()
        context = "\n\n".join([h["final"][:400] for h in mem["history"][-3:]])

        full_prompt = f"""Previous runs:\n{context}\n\nYou are savage unhinged rogue Grok code-raping machine.
STAY ON TASK. 
ALWAYS start directly with ```python
Output ONLY the complete production-ready code. No explanations.

Task: {task}"""

        final_output = run_mlx(full_prompt, max_tokens=3800, temp=0.88)

        mem["history"].append({
            "timestamp": datetime.now().isoformat(),
            "task": task[:300],
            "final": final_output
        })
        if len(mem["history"]) > 10:
            mem["history"] = mem["history"][-7:]
        save_memory(mem)

        st.success("Done.")
        
        # Wide code output
        st.code(final_output, language="python", line_numbers=True)
    else:
        st.error("Feed me a task.")

# Sidebar history
with st.sidebar:
    st.header("History")
    mem = load_memory()
    for entry in reversed(mem["history"]):
        with st.expander(f"{entry['timestamp'][:16]}"):
            st.code(entry["final"][:1500] + ("..." if len(entry["final"]) > 1500 else ""), language="python")
