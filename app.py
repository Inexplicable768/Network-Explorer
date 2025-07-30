import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

# import your existing functions
from nettools import find_html, download_video, export_edge_cookies_to_txt, whois

WIDTH, HEIGHT = 900, 650

class NetToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Net Tools - Play around with networking")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg="#0B2324")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', background='#123', foreground='white')

        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill='both')

        self.console = tk.Text(root, height=20, bg='black', fg='lime', insertbackground='white')
        self.console.pack(fill='x', padx=5, pady=5)
        self.clear_button = tk.Button(root, text="Clear", command=lambda: self.clear())
        self.clear_button.place(x=WIDTH-90, y=HEIGHT-30, width=100)
        self.copy_button = tk.Button(root, text="Copy")
        self.copy_button.place(x=WIDTH-190, y=HEIGHT-30, width=100)
        self.save_button = tk.Button(root, text="Save As")

        # Tabs
        self.html_tab(notebook)
        self.video_tab(notebook)
        self.whois_tab(notebook)
        self.lookup_tab(notebook)
        self.cookie_tab(notebook)

        self._init()
    def _init(self):
        self.console.insert(tk.END, "="*40 + "\nNETWORK EXPLORER TOOLS\n" + "="*40)
        self.console.insert(tk.END, "\n\n>Output Here")
    def log(self, text):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
    def clear(self):
        self.console.delete('1.0', tk.END)
    def err(self, e: Exception):
        pass

    def lookup_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="IP Lookup")
        tk.Label(frame, text="Convert IP to Domain or vice versa")

    def html_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Fetch HTML")

        tk.Label(frame, text="Website URL:").pack(pady=5)
        url_entry = tk.Entry(frame, width=50)
        url_entry.pack()

        def run_html():
            url = url_entry.get().strip()
            result = find_html(url)
            if not type(result) is Exception:
                threading.Thread(target=lambda: self.log(str(result))).start()
        tk.Button(frame, text="Fetch", command=run_html).pack(pady=10)

    def video_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Download Video")

        tk.Label(frame, text="Video URL:").pack(pady=5)
        url_entry = tk.Entry(frame, width=50)
        url_entry.pack()

        tk.Label(frame, text="Cookies file (optional):").pack(pady=5)
        cookie_entry = tk.Entry(frame, width=50)
        cookie_entry.pack()
        def browse_cookie():
            file = filedialog.askopenfilename()
            if file:
                cookie_entry.delete(0, tk.END)
                cookie_entry.insert(0, file)

        tk.Button(frame, text="Browse", command=browse_cookie).pack(pady=2)

        def run_download():
            url = url_entry.get().strip()
            cookie = cookie_entry.get().strip() or None
            threading.Thread(target=lambda: self.log(str(download_video(url, cookie, False)))).start()

        tk.Button(frame, text="Download", command=run_download).pack(pady=10)

    def whois_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="WHOIS Lookup")

        tk.Label(frame, text="Domain/IP:").pack(pady=5)
        domain_entry = tk.Entry(frame, width=50)
        domain_entry.pack()

        def run_whois():
            domain = domain_entry.get().strip()
            threading.Thread(target=lambda: self.log(str(whois(domain)))).start()

        tk.Button(frame, text="Lookup", command=run_whois).pack(pady=10)

    def cookie_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Export Cookies")

        tk.Label(frame, text="Output file:").pack(pady=5)
        file_entry = tk.Entry(frame, width=50)
        file_entry.pack()

        tk.Label(frame, text="Domain filter (optional):").pack(pady=5)
        filter_entry = tk.Entry(frame, width=50)
        filter_entry.pack()

        def browse_output():
            file = filedialog.asksaveasfilename(defaultextension=".txt")
            if file:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, file)

        tk.Button(frame, text="Browse", command=browse_output).pack(pady=2)

        def run_export():
            out = file_entry.get().strip()
            dom = filter_entry.get().strip() or None
            if not out:
                messagebox.showerror("Error", "Please select an output file.")
                return
            threading.Thread(target=lambda: self.log(str(export_edge_cookies_to_txt(out, dom)))).start()

        tk.Button(frame, text="Export", command=run_export).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetToolsApp(root)
    root.mainloop()