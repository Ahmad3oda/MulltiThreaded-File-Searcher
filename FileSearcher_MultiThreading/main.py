import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from typing import Callable


class FileHandler:
    def __init__(self):
        self.files = []
        self.threads = []
        self.pause_toggle = False
        self.keyword = ""

    def set_files(self, files):
        self.files = files

    def toggle_pause(self):
        self.pause_toggle = not self.pause_toggle

    def start_search(self, keyword, progress_callback):
        self.keyword = keyword
        self.threads.clear()

        for i, file in enumerate(self.files):
            thread = threading.Thread(
                target=self.search_file,
                args=(i, file, progress_callback)
            )
            self.threads.append(thread)
            thread.start()

    def search_file(self, index, file, progress_callback):
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                total_lines = len(lines)

            found = False
            highlighted_lines = []

            for line_num, line in enumerate(lines, start=1):
                while self.pause_toggle:
                    time.sleep(0.1)

                progress = f"{int((line_num / total_lines) * 100)}%"
                progress_callback(index, "Searching...", progress, "", "searching")
                time.sleep(.2)

                if self.keyword.lower() in line.lower():
                    found = True

                    highlighted_line = line.replace(
                        self.keyword,
                        f'<span style="background-color: yellow; color: black;">{self.keyword}</span>'
                    )
                    highlighted_lines.append(highlighted_line)
                else:
                    highlighted_lines.append(line)

            if found:
                print(os.path.splitext(file))
                highlighted_file = f"{os.path.splitext(file)[0]}_highlighted.html"
                with open(highlighted_file, "w", encoding="utf-8") as fw:
                    fw.write("<html><body><pre>\n")
                    fw.writelines(highlighted_lines)
                    fw.write("\n</pre></body></html>")

                details = f"Keyword found and saved in {highlighted_file}"
                progress_callback(index, "Found", "100%", details, "found")
            else:
                progress_callback(index, "Not Found", "100%", "", "not_found")

        except Exception as e:
            progress_callback(index, "Error", "0%", str(e), "not_found")




    def open_selected_file(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            file_path = tree.item(selected_item[0], "values")[0]
            try:
                os.startfile(file_path)
            except Exception as e:
                print(f"Error opening file: {e}")


class FileSearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-threaded File Searcher")
        self.root.config(bg="white")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.window_width = 800
        self.window_height = 600

        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        self.root.resizable(False, False)

        self.file_handler = FileHandler()
        self.files = []

        self.init_components()

    def init_components(self):

        self.frame1 = tk.Frame(self.root, bg = "black", width = self.window_width, height = 70)
        self.frame1.place(x=0, y=0)

        self.frame2 = tk.Frame(self.root, bg = "black", width = self.window_width, height = 100)
        self.frame2.place(x=0, y=70)

        self.frame3 = tk.Frame(self.root, bg = "white", width=self.window_width, height=440)
        self.frame3.place(x=0, y=150)

        # elements in frame 1
        self.keyword_label = tk.Label(self.frame1, width = 15, text = "Enter Keyword:", bg = "white")
        self.keyword_label.place(x=200, y=40)

        self.keyword_entry = tk.Entry(self.frame1, width = 46)
        self.keyword_entry.place(x=320, y=40)

        # elements in frame 2
        self.select_files_button = tk.Button(
            self.frame2,
            text="Select Files",
            width=56,
            command=self.select_files,
            bg="white"
        )
        self.select_files_button.place(x = 200, y = 0)

        self.start_button = tk.Button(
            self.frame2,
            text="Search",
            width=25,
            command=self.start_search,
            bg="lightgreen"
        )
        self.start_button.place(x = 200, y = 40)

        self.pause_resume_button = tk.Button(
            self.frame2,
            text="Pause",
            width=25,
            command=self.pause_resume,
            bg="red"
        )
        self.pause_resume_button.place(x = 418, y = 40)

        # elements in frame 3
        self.tree = ttk.Treeview(
            self.frame3,
            columns=("File", "Status", "Progress", "Details"),
            show="headings",
            height=100
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.tree.tag_configure("found", background="lightgreen")
        self.tree.tag_configure("not_found", background="lightcoral")
        self.tree.tag_configure("searching", background="orange")

        self.tree.bind("<Double-1>", self.file_handler.open_selected_file)
        self.tree.pack(fill=tk.BOTH, expand = True)

        self.start = False


    def select_files(self):

        files = filedialog.askopenfilenames(title = "Select Files")
        self.file_handler.set_files(files)
        self.tree.delete(*self.tree.get_children())

        self.start = False
        for file in files:
            self.tree.insert("", "end", values=(file, "Pending", "0%", ""))

    def start_search(self):
        keyword = self.keyword_entry.get()
        if not keyword:
            messagebox.showerror("Error", "Please enter a keyword.")
            return
        if self.start:
            return

        self.start = True
        self.file_handler.start_search(keyword, self.update_progress)

    def pause_resume(self):
        self.file_handler.toggle_pause()
        if self.file_handler.pause_toggle:
            self.pause_resume_button.config(text = "Resume")
        else:
            self.pause_resume_button.config(text = "Pause")

    def update_progress(self, index, status, progress, details, color = None):
        if not self.tree.get_children():
            return

        item = self.tree.get_children()[index]
        self.tree.item(
            item,
            values=(self.file_handler.files[index], status, progress, details)
        )

        if color:
            self.tree.item(item, tags = (color,))

        self.tree.see(item)
        self.tree.update_idletasks()


def run_gui():
    root = tk.Tk()
    app = FileSearcherApp(root)
    root.mainloop()


if __name__ == "__main__":
    gui_thread = threading.Thread(target=run_gui, daemon = True)
    gui_thread.start()

    try:
        while gui_thread.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting application...")
        os._exit(0)
