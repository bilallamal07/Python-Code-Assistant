import gradio as gr
from io import StringIO
import sys
import httpx
import asyncio
import socket
import tempfile
import os

# Configuration for Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"

# Check for Matplotlib availability
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def find_available_port(start_port=7860, end_port=8000):
    """Find an available port within the specified range"""
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                continue
    return start_port  # Fallback to start port if none available

def query_ollama(prompt: str, model_name: str = "devstral:24b") -> str:
    """Query the local Ollama LLM API and return the response"""
    try:
        async def fetch_ollama_response():
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    OLLAMA_URL,
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                return response
        response = asyncio.run(fetch_ollama_response())
        if response.status_code == 200: 
            return response.json()['response']
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error querying Ollama: {str(e)}"

def execute_code(code: str) -> str:
    """
    Execute Python code and return the output or error message.
    Args:
        code (str): The Python code to execute.
    Returns:
        str: The output of the executed code or the error message if an exception occurs.
    """
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    try:
        # Create a new namespace to prevent 'factorial' not defined errors
        namespace = {}
        exec(code, namespace)
        return redirected_output.getvalue()
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = old_stdout

def generate_plot(code: str) -> str:
    """
    Execute Python code and save the resulting plot to a temporary file.
    Args:
        code (str): The Python code to execute.
    Returns:
        str: Path to the generated plot image or error message.
    """
    if not MATPLOTLIB_AVAILABLE:
        return "Matplotlib is not installed. Please install with: pip install matplotlib"
    
    try:
        # Create a new namespace
        namespace = {}
        exec(code, namespace)
        
        # Save the plot to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plt.savefig(tmpfile.name)
            plt.close()  # Close the figure to free memory
            return tmpfile.name
    except Exception as e:
        return f"Error generating plot: {str(e)}"

def handle_request(code_input: str, action: str, model_name: str) -> (str, str):
    """Handle different types of code processing requests"""
    text_output = ""
    plot_path = None
    
    if action == "execute":
        text_output = execute_code(code_input)
    elif action == "plot":
        plot_path = generate_plot(code_input)
        if not plot_path.startswith("Error"):
            text_output = "Plot generated successfully!"
        else:
            text_output = plot_path
            plot_path = None
    else:
        prompt = ""
        if action == "explain":
            prompt = f"Explain this Python code in detail:\n\n{code_input}\n\nFocus on the algorithm, functions, and control flow."
        elif action == "rewrite":
            prompt = f"Rewrite this Python code to improve readability and maintainability:\n\n{code_input}\n\nOnly return the refactored code with no additional text."
        elif action == "optimize":
            prompt = f"Optimize this Python code for performance:\n\n{code_input}\n\nFirst briefly explain the optimizations, then provide the optimized code."
        elif action == "suggest":
            prompt = f"Suggest improvements for this Python code:\n\n{code_input}\n\nInclude potential bug fixes, style improvements, and best practices."
        
        text_output = query_ollama(prompt, model_name)
    
    return text_output, plot_path

def clear_output():
    """Clear the output textbox and plot"""
    return "", None

def clear_code():
    """Clear the code input"""
    return ""

# Recommended plotting libraries
plotting_libraries = """
Recommended Python Plotting Libraries:
1. Matplotlib - Most common, flexible, and well-documented
   Install: pip install matplotlib

2. Seaborn - Built on Matplotlib, better for statistical plots
   Install: pip install seaborn

3. Plotly - Interactive plots, good for web applications
   Install: pip install plotly

4. Bokeh - Interactive visualization for modern web browsers
   Install: pip install bokeh

5. Altair - Declarative statistical visualization
   Install: pip install altair vega_datasets
"""

# Custom CSS for colorful buttons
custom_css = """
/* Colorful action buttons */
.action-button {
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin: 4px !important;
    font-weight: bold !important;
}

#execute { background: linear-gradient(145deg, #FF6B6B, #FF8E53) !important; color: white !important; }
#plot { background: linear-gradient(145deg, #4ECDC4, #00C9FF) !important; color: white !important; }
#explain { background: linear-gradient(145deg, #7CEC9F, #00D2AA) !important; color: white !important; }
#rewrite { background: linear-gradient(145deg, #FFD166, #FFB74D) !important; color: white !important; }
#optimize { background: linear-gradient(145deg, #9D50BB, #6E48AA) !important; color: white !important; }
#suggest { background: linear-gradient(145deg, #FF9A8B, #FF6B6B) !important; color: white !important; }

/* Clear buttons */
#clear-code { background: linear-gradient(145deg, #FFA500, #FF8C00) !important; color: white !important; }
#clear-output { background: linear-gradient(145deg, #FFA500, #FF8C00) !important; color: white !important; }
"""

# Create the Gradio interface
with gr.Blocks(title="Python Code Assistant", css=custom_css) as demo:
    gr.Markdown("# 🐍 Python Code Assistant")
    gr.Markdown("Execute Python code, generate plots, or get AI-powered analysis using local LLMs")
    
    with gr.Row():
        with gr.Column():
            code_input = gr.Code(
                label="Python Code", 
                language="python",
                value="""# Basic plot example (requires matplotlib)
import matplotlib.pyplot as plt
import numpy as np

# Create data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
plt.figure(figsize=(8, 4))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Sine Wave')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()""",
                lines=20
            )
            
            # Colorful action buttons
            with gr.Row():
                execute_btn = gr.Button("Execute", elem_id="execute", variant="primary", size="sm", elem_classes="action-button")
                plot_btn = gr.Button("Plot", elem_id="plot", variant="primary", size="sm", elem_classes="action-button")
                explain_btn = gr.Button("Explain", elem_id="explain", variant="primary", size="sm", elem_classes="action-button")
                rewrite_btn = gr.Button("Rewrite", elem_id="rewrite", variant="primary", size="sm", elem_classes="action-button")
                optimize_btn = gr.Button("Optimize", elem_id="optimize", variant="primary", size="sm", elem_classes="action-button")
                suggest_btn = gr.Button("Suggest", elem_id="suggest", variant="primary", size="sm", elem_classes="action-button")
            
            # Hidden action selector
            action = gr.Radio(
                label="Action",
                choices=["execute", "plot", "explain", "rewrite", "optimize", "suggest"],
                value="execute",
                visible=False
            )
            
            model_name = gr.Dropdown(
                label="LLM Model",
                choices=["devstral:24b", "qwen2.5-coder:32b-instruct-q4_K_M"],
                value="devstral:24b"
            )
            
            # Run button
            submit_btn = gr.Button("Run Analysis", variant="primary")
        
        with gr.Column():
            output = gr.Textbox(
                label="Result", 
                interactive=False,
                lines=10,
                autoscroll=True
            )
            plot_output = gr.Image(
                label="Generated Plot",
                interactive=False
            )
            
            # Clear buttons
            with gr.Row():
                clear_code_btn = gr.Button("Clear Python Code", elem_id="clear-code", variant="secondary")
                clear_output_btn = gr.Button("Clear Output", elem_id="clear-output", variant="secondary")
    
    # Add library recommendations
    gr.Markdown("### 📊 Plotting in Python")
    gr.Markdown(plotting_libraries)
    
    # Connect action buttons to set the action
    execute_btn.click(lambda: "execute", outputs=action)
    plot_btn.click(lambda: "plot", outputs=action)
    explain_btn.click(lambda: "explain", outputs=action)
    rewrite_btn.click(lambda: "rewrite", outputs=action)
    optimize_btn.click(lambda: "optimize", outputs=action)
    suggest_btn.click(lambda: "suggest", outputs=action)
    
    # Set button styles
    for btn in [execute_btn, plot_btn, explain_btn, rewrite_btn, optimize_btn, suggest_btn]:
        btn.click(lambda: None)
    
    # Main processing
    submit_btn.click(
        fn=handle_request,
        inputs=[code_input, action, model_name],
        outputs=[output, plot_output]
    )
    
    # Clear functions
    clear_output_btn.click(
        fn=clear_output,
        inputs=[],
        outputs=[output, plot_output]
    )
    
    clear_code_btn.click(
        fn=clear_code,
        inputs=[],
        outputs=code_input
    )

if __name__ == "__main__":
    # Find an available port dynamically
    available_port = find_available_port()
    print(f"🚀 Launching application on port {available_port}")
    
    demo.launch(
        server_name="localhost",
        server_port=available_port,
        show_api=False,
        share=False
    )
