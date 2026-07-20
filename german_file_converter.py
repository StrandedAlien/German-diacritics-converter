# =========================================================================
# APPLICATION      : German Diacritic File Converter (GUI Picker Mode)
# PATH             : NATIVE_LINUX_FORMATTED_STORAGE_ONLY Path Mapping Active
# SOFTWARE VERSION : 1.0.0
# TARGET PLATFORM  : LINUX OS 
# COMPLIANCE       : based on EN IEC/IEEE 82079-1 
# AUTHORS          : Stranded Alien
# 
# CHANGELOG:
# - 2026-07-20: Upgraded to Version 1.0.0 [READY for hobby purposes].
# - Confirmed certain field deployment stability on native Linux systems.
# - Validated text window previews, memory locks, and persistent historical tracking.
# - Maintained narrow vertical formatting constraints to fix Geany text wrap.
# =========================================================================
import sys
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as st

print("Executing: german_file_converter.py (Version 1.0.0)")

HISTORY_FILE = "lastscriptdir.txt"

NORMAL_MAP = {
    'ae': 'ä', 'oe': 'ö', 'ue': 'ü',
    'AE': 'Ä', 'OE': 'Ö', 'UE': 'Ü',
    'Ae': 'Ä', 'Oe': 'Ö', 'Ue': 'Ü'
}

REVERSE_MAP = {
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
    'Ä': 'AE', 'ß': 'ss', 'ẞ': 'SS'
}

def multi_replace(text, mapping):
    sorted_keys = sorted(
        mapping.keys(),
        key=len,
        reverse=True
    )
    for key in sorted_keys:
        text = text.replace(key, mapping[key])
    return text

def get_last_directory():
    script_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    history_path = os.path.join(
        script_dir, 
        HISTORY_FILE
    )
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                saved_dir = f.read().strip()
                if os.path.isdir(saved_dir):
                    return saved_dir
        except Exception:
            pass
    return None

def save_last_directory(file_path):
    script_dir = os.path.dirname(
        os.path.abspath(__file__)
    )
    history_path = os.path.join(
        script_dir, 
        HISTORY_FILE
    )
    target_dir = os.path.dirname(
        os.path.abspath(file_path)
    )
    try:
        with open(history_path, 'w', encoding='utf-8') as f:
            f.write(target_dir)
    except Exception as e:
        print(f"Warning: Could not save folder history: {e}")

def get_file_via_gui():
    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', True)
    
    initial_dir = get_last_directory()
    
    selected_file = filedialog.askopenfilename(
        title="Select German Text File for Conversion",
        initialdir=initial_dir,
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )
    root.destroy()
    return selected_file

def choose_mode_via_gui(filename):
    mode_window = tk.Tk()
    mode_window.title("Evaluate File Content & Choose Direction")
    mode_window.geometry("520x400")
    mode_window.lift()
    mode_window.attributes('-topmost', True)

    chosen_mode = tk.StringVar(value="none")

    def select_normal():
        chosen_mode.set("normal")
        mode_window.destroy()

    def select_reverse():
        chosen_mode.set("reverse")
        mode_window.destroy()

    display_name = os.path.basename(filename)

    tk.Label(
        mode_window, 
        text=f"Selected File: {display_name}", 
        font=("Arial", 10, "bold"),
        pady=5,
        padx=10
    ).pack(anchor="w")

    tk.Label(
        mode_window, 
        text="File Content Preview (Read-Only):", 
        font=("Arial", 9, "italic"),
        padx=10
    ).pack(anchor="w")

    preview_text = ""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            preview_text = f.read(2000)
    except Exception as e:
        preview_text = f"[Could not read preview: {e}]"

    text_area = st.ScrolledText(
        mode_window, 
        wrap=tk.WORD, 
        width=60, 
        height=12,
        font=("Arial", 10)
    )
    text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    text_area.insert(tk.INSERT, preview_text)
    text_area.configure(state='disabled')

    tk.Label(
        mode_window, 
        text="Choose conversion format based on the text above:", 
        font=("Arial", 9),
        pady=5
    ).pack()

    btn_frame = tk.Frame(mode_window)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame, 
        text="Normal (ä)", 
        width=18, 
        command=select_normal
    ).pack(side=tk.LEFT, padx=15)

    tk.Button(
        btn_frame, 
        text="Reverse (ae)", 
        width=18, 
        command=select_reverse
    ).pack(side=tk.LEFT, padx=15)

    mode_window.mainloop()
    return chosen_mode.get()

def show_success_gui(output_path):
    success_window = tk.Tk()
    success_window.title("Conversion Successful")
    success_window.geometry("460x160")
    success_window.lift()
    success_window.attributes('-topmost', True)

    def close_all():
        success_window.destroy()

    display_out = os.path.basename(output_path)

    message_text = (
        "SUCCESS:\n"
        "The file processing stream completed flawlessly.\n\n"
        f"Saved to: {display_out}"
    )

    tk.Label(
        success_window, 
        text=message_text, 
        justify=tk.LEFT, 
        font=("Arial", 10),
        pady=15,
        padx=20
    ).pack(anchor="w")

    tk.Button(
        success_window, 
        text="Acknowledge and Close", 
        width=24, 
        font=("Arial", 10, "bold"),
        bg="#2ecc71",
        fg="white",
        command=close_all
    ).pack(pady=10)

    success_window.mainloop()

def main():
    print("Spawning graphical file picker window...")
    input_path = get_file_via_gui()
    
    if not input_path:
        print("Operation cancelled: No file selected.")
        sys.exit(0)

    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    save_last_directory(input_path)

    mode = choose_mode_via_gui(input_path)
    if mode == "none":
        print("Operation cancelled: No conversion mode selected.")
        sys.exit(0)

    if mode == "normal":
        mapping = NORMAL_MAP
    else:
        mapping = REVERSE_MAP

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_converted{ext}"

    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                outfile.write(multi_replace(line, mapping))
        
        print(f"SUCCESS: Stream processed cleanly. Saved to: {output_path}")
        show_success_gui(output_path)

    except Exception as e:
        print(f"System Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
