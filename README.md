## **Multi-threaded File Searcher**

### **Project Overview**
**Multi-threaded File Searcher** is a Python application that allows users to search for a specific keyword across multiple files efficiently. By applying multi-threading, the application ensures faster performance while maintaining a **responsive GUI** using Tkinter that trackes the progress for each thread.

The usage of MultiThreading, unlike sequential Searching, can **speed up the process up to n times** in best-case senario, where **n** is the number of files being processed simultaneouslty.

---

### **Features**
- **Multi-threaded Search:** Files are processed concurrently, improving search speed.
- **Responsive GUI:** The graphical user interface (Tkinter) runs on a separate thread to avoid UI hanging.
- **Real-time Progress Tracking:** Updates on file progress and search status.
- **Pause/Resume Search:** Users can pause and resume the search operation.
- **Keyword Highlighting:** Generates an HTML file with the keyword highlighted (if found).
- **File Access:** Double-click any file in the results to open it directly.
---
### **How It Works**

1. **Select Files:** Use the "Select Files" button to choose files for processing.
2. **Enter Keyword:** Provide the keyword to be searched.
3. **Start Search:** Click "Start Search" to initiate the search.
4. **Pause/Resume:** Use the "Pause" button to toggle between paused and active states.
5. **View Results:** 
   - Real-time progress is displayed in the GUI.
   - Generated HTML files highlight the found keyword.
     
### **Screenshots**

#### **1. Main GUI**
![image](https://github.com/user-attachments/assets/6a26213d-0424-4251-b135-7f3a39357b3a)

#### **2. Progress Tracking**
![image](https://github.com/user-attachments/assets/4db9a470-db80-477a-836f-520bc906b086)

#### **3. Keyword Highlighting **
![image](https://github.com/user-attachments/assets/2f91d7f1-cd9a-4fb5-86a4-fdb2d352a866)

---

### **Technologies Used**
- **Python Standard Libraries:**
  - `threading` for multi-threaded processing.
  - `tkinter` for GUI development.
  - `os` and `time` for file operations.
- **No external dependencies** are required.

---

### **Usage Instructions**

1. Clone the repository:
   ```bash
   git clone https://github.com/Ahmad3oda/MulltiThreaded-File-Searcher.git
   cd MulltiThreaded-File-Searcher
   ```

2. Run the program:
   ```bash
   python main.py
   ```

3. Follow the GUI steps:
   - Select files.
   - Enter a keyword.
   - Start the search and monitor progress.




