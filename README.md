# 🩸 Savage Local Squad

A brutal, fast, local AI coding assistant running on Apple Silicon (M5 Max) using MLX + Qwen2.5-Coder-32B.

### Features
- Savage unhinged coding style
- Persistent memory across sessions
- Beautiful dark Streamlit UI
- Full production-ready code output
- No cloud, no censorship, no bullshit

### Tech Stack
- **Model**: Qwen2.5-Coder-32B (MLX 4-bit)
- **Inference**: MLX
- **UI**: Streamlit
- **Memory**: JSON + context

### Project Structure
```bash 
SavageLocalSquad/
├── squad_ui.py                 # Main UI
├── coding_memory.json          # Conversation memory
├── README.md
└── .gitignore
```

### Installation
```bash 
1. Activate your MLX environment
source ~/mlx_env/bin/activate

2. Install UI dependencies
pip install streamlit

3. Run the squad
streamlit run squad_ui.py

Access at: http://localhost:8501
```
### Usage

- Type your task in the box
- Click Unleash the Beast
- Get raw, complete, production-ready code

### Tips

- Best for coding / scripting / data tasks
- For very long outputs, it may take 3-6 minutes
- History is saved automatically
- You can continue previous tasks naturally

### Future Plans

- File upload support (CSV, PDF, etc.)
- One-click "Improve this code" button
