import nuke
import subprocess
import sys
import os



# Add the custom comfiUI menu
def add_comfi_menu():
    import nuke
    # Check if 'comfy_tools' menu already exists, if not, create it
    menu = nuke.menu('Nuke')
    comfy_tools = menu.findItem('comfy_tools')
    if comfy_tools is None:
        comfy_tools = menu.addMenu('comfy_tools')

    # Add 'comfy_nuke_prompt' to 'comfy_tools'
    comfy_tools.addCommand('comfy_nuke_prompt', comfy_nuke_prompt_main.show_nuke_ui)

# Add the menu when Nuke starts
add_comfi_menu()

def launch_browser():
    # Path to your PySide6 script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir,Pyside_browser.py)
    
    # Path to the Python executable in the PySide6 environment
    python_env_path = r'C:\Users\vishr\Documents\comfy_test\env\Scripts\python.exe'
    
    # Check if the script exists
    if not os.path.exists(script_path):
        nuke.message(f"Script not found: {script_path}")
        return

    # Check if the Python executable exists
    if not os.path.exists(python_env_path):
        nuke.message(f"Python executable not found: {python_env_path}")
        return

    try:
        # Launch the external script using subprocess
        subprocess.Popen([python_env_path, script_path], shell=False)
    except Exception as e:
        nuke.message(f"Failed to launch browser: {str(e)}")

# Add the command to Nuke's menu
nuke.menu('Nuke').addCommand('Custom/Launch PySide6 Browser', launch_browser)

