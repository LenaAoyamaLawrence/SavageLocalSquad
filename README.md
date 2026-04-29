# 🩸 Savage Local Squad

A brutal local AI assistant running on M5 Max (MLX + Qwen models).

### Modes + Models
- **Brutal Code Factory** → 32B Coder + 72B Critic (stable, strong for coding)
- **Mad Researcher** → 72B solo + lightweight RAG (reads files from `./docs/`)

### Tech Stack
- **Inference**: MLX
- **UI**: Streamlit
- **Memory**: JSON + context

### Project Structure
```bash 
SavageLocalSquad/
├── squad_ui.py
├── coding_memory.json          # Auto-created
├── README.md
├── .gitignore
├── docs/                       # ← Drop CSVs, PDFs, txt files here for RAG
├── qwen-coder-32b/             # Install via mlx_lm.convert, e.g., 
└── qwen2.5-72b-q4/             # mlx_lm.convert --hf-path Qwen/Qwen2.5-72B-Instruct --mlx-path ./qwen2.5-72b-q4 --quantize --q-bits 4 --q-group-size 64
```

### Installation
```bash 
1. Activate your MLX environment
source ~/mlx_env/bin/activate

2. Install UI dependencies
pip install streamlit

3. Redirection
cd ~/Savage-Local-Squad

4. Run the squad
streamlit run squad_ui.py

Access at: http://localhost:8501
```

### Tips
- Use absolute paths for stability
- Mad Researcher mode will read everything in ./docs/
- Code Factory is currently the most reliable
- History is saved automatically
- You can continue previous tasks naturally
