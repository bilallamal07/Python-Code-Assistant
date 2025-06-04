# Python-Code-Assistant

Python Code Executor with Ollama Integration
A powerful Python code execution and analysis tool built with Gradio that integrates with Ollama for AI-powered code analysis. 
This application allows you to execute Python code, generate plots, and get AI-powered code analysis in real-time.

## Features

- 🚀 Execute Python code in real-time
- 📊 Generate and display plots
- 🤖 AI-powered code analysis using Ollama
- ♻️ Code optimization suggestions
- 📝 Code explanation and rewriting
- 🎨 Beautiful and intuitive user interface

## Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows
- [Ollama](https://ollama.ai/) installed locally if is not alreay done so

## Installation

1. **First, install Ollama** (if not already installed):
   ```bash
   # For macOS
   curl -fsSL https://ollama.ai/install.sh | sh

   # For Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # For Windows
   # Download from https://ollama.ai/download
   ```

2. **Pull required Ollama models:** you can add your models 
   ```bash
   ollama pull devstral:24b
   ollama pull qwen2.5-coder:32b-instruct-q4_K_M
   ```

3. **Clone the repository** (if using version control):
   ```bash
   git clone <repository-url>
   cd Agents_LLM
   ```

4. **Install dependencies using uv** (faster than pip):
   ```bash
   # Install uv if you haven't already
   curl -fsSL https://raw.githubusercontent.com/astral-sh/uv/main/install.sh | sh

   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   uv pip install gradio httpx matplotlib numpy
   ```

## Running the Application

1. **Start Ollama server** (if not already running):
   ```bash
   ollama serve
   ```

2. **Run the application:**
   ```bash
   python Python-Code-Executor.py
   ```

3. **Access the interface:**
   - Open your web browser
   - Navigate to `http://localhost:<port>` (the port will be displayed in the terminal)

## Usage Guide

### Code Execution
- Enter your Python code in the left panel
- Click "Execute" to run the code
- Results will appear in the right panel

### Plot Generation
- Write matplotlib/plotting code
- Click "Plot" to generate and display the visualization
- The plot will appear in the right panel

### AI Analysis Features
- **Explain**: Get detailed explanation of your code
- **Rewrite**: Get suggestions for code improvement
- **Optimize**: Receive performance optimization tips
- **Suggest**: Get general improvement suggestions

### Available Models
- devstral:24b (default)
- qwen2.5-coder:32b-instruct-q4_K_M
- qwen2.5-Coder-14B-Instruct-abliterated
- deepseek-r1:14b

## Uninstallation

1. **Remove Ollama:**
   ```bash
   # For macOS/Linux
   sudo rm -rf /usr/local/bin/ollama
   sudo rm -rf ~/.ollama

   # For Windows
   # Use Windows Control Panel to uninstall Ollama
   ```

2. **Remove the Python environment:**
   ```bash
   # Deactivate the virtual environment
   deactivate

   # Remove the virtual environment directory
   rm -rf venv
   ```

## Recommended Plotting Libraries
The application supports various Python plotting libraries:
- Matplotlib
- Seaborn
- Plotly
- Bokeh
- Altair

To install any of these libraries:
```bash
uv pip install <library-name>
```

## Troubleshooting

1. **Port Already in Use**
   - The application will automatically find an available port
   - Default port range: 7860-8000

2. **Ollama Connection Issues**
   - Ensure Ollama is running: `ollama serve`
   - Check if models are properly installed: `ollama list`

3. **Plotting Issues**
   - Ensure matplotlib is installed
   - Check if the code includes `plt.show()`

## Notes

- The application runs locally and doesn't require internet connection once models are downloaded
- Code execution is done in a safe environment
- All plots are saved temporarily and cleaned up automatically
