DigiPage Scanner Pro
====================

**DigiPage Scanner Pro** is a specialized desktop application designed for high-volume document digitization workflows. It streamlines the process of scanning, inspecting, correcting, and organizing book pages in real-time.

Built with **Python** and **PySide6 (Qt)**, the application is engineered for operators who need speed and reliability. It decouples the user interface from heavy image processing tasks to ensure a responsive experience even when handling high-resolution scans.

🚀 Key Features
---------------

### 1\. Specialized Scanning Modes

*   **Dual Scan Mode:** The standard workflow for scanners that produce separate image files for left and right pages. Displays two large canvases for simultaneous inspection.
    
*   **Single-Shot Split Mode:** Designed for overhead scanners that capture a full book spread in a single wide image. The application automatically splits the image into two pages based on a smart, persistent crop layout.
    

### 2\. Real-Time Image Processing

*   **Non-Destructive Editing:** Crop, rotate, and split operations save changes to new files or backups, preserving the original scan data where possible.
    
*   **Auto-Correction:** Optional automatic adjustment of lighting (autocontrast) and color cast removal using NumPy-accelerated algorithms.
    
*   **Smart Caching:** An optimized background worker manages an LRU cache of QPixmaps to ensure instant page navigation without UI freezes.
    

### 3\. Automated Workflow

*   **File Watcher:** Automatically detects new scans arriving in the configured folder and updates the UI instantly.
    
*   **Book Assembly:** One-click creation of book folders from the day's scanned pages.
    
*   **Archive Transfer:** Intelligent routing of completed books to network destinations based on city codes parsed from the book name (e.g., -297-).
    

🛠️ Architecture
----------------

The project follows a modular, layered architecture to separate concerns and improve maintainability.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   digipage/  ├── main.py                 # Application Entry Point  ├── core/                   # Logic-only Configuration & Styling  │   ├── config.py           # Typed ConfigManager & Dataclasses  │   └── theme.py            # Dynamic Stylesheet Generation  ├── data/                   # Data Persistence Layer  │   └── io.py               # JSON Log handling & Stats calculation  ├── workers/                # Background Threads (Heavy Lifting)  │   ├── scanner_worker.py   # File I/O, Image Manipulation (PIL), Archiving  │   ├── image_worker.py     # UI Image Loading & Caching  │   └── watcher.py          # Watchdog File System Monitoring  ├── ui/                     # Presentation Layer  │   ├── main_window.py      # Central Controller  │   ├── modes/              # Scan Logic Strategies (Strategy Pattern)  │   │   ├── dual.py         # Logic for 2-page view  │   │   └── single.py       # Logic for 1-page splitter view  │   ├── viewer/             # Custom Image Widget  │   │   ├── canvas.py       # Painting & Coordinate Mapping  │   │   └── handlers.py     # Mouse Interaction State Machine  │   ├── panels/             # Sidebars & Toolbars  │   └── dialogs/            # Settings & Logs  └── utils/                  # Shared Utilities   `

### Design Patterns Used

*   **State Pattern:** Used in ui/viewer/handlers.py to manage complex mouse interactions (Cropping vs. Rotating vs. Panning) without massive if-else chains.
    
*   **Strategy Pattern:** Used in ui/modes/ to switch the entire UI logic and layout between "Dual Scan" and "Single Split" modes seamlessly.
    
*   **Observer Pattern:** Heavy use of Qt Signals/Slots to decouple Workers from the UI.
    

📦 Installation
---------------

### Prerequisites

*   Python 3.10+
    
*   Virtual Environment (Recommended)
    

### Dependencies

Install the required packages:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install PySide6 Pillow watchdog numpy   `

### Running the Application

1.  Navigate to the project root directory.
    
2.  Run the main module:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python digipage/main.py   `

_Note: On the first run, the application will prompt you to open the Settings Dialog to configure your scan folders._

⚙️ Configuration
----------------

The application uses a config.json file located in the root directory. While this can be edited manually, it is recommended to use the built-in **Settings Dialog**.

### Key Settings

*   **Scan Folder:** The directory where your scanner saves images. The app watches this folder.
    
*   **Today's Books Folder:** The staging area where processed pages are assembled into book folders.
    
*   **City Paths:** A mapping of 3-digit codes (e.g., 001) to network paths. Used for the "Transfer to Data" feature.
    
*   **Scanner Mode:** Switches between dual\_scan and single\_split.
    

📖 User Guide
-------------

### General Navigation

*   **Next/Prev:** Use the buttons on the bottom toolbar or the **Mouse Wheel**.
    
*   **Zoom:** Double-click an image or use **Ctrl + Scroll**.
    
*   **Pan:** Click and drag when zoomed in.
    

### Dual Scan Workflow

1.  Scan a spread (2 images appear).
    
2.  **Crop:** Click "Crop" and drag the box handles.
    
3.  **Rotate:** Click "Rotate" and drag the slider at the bottom of the image.
    
4.  **Delete/Replace:** Use the toolbar buttons to manage bad scans.
    

### Single-Shot Split Workflow

1.  Scan a spread (1 wide image appears).
    
2.  The app automatically attempts to split the page based on the _previous_ layout.
    
3.  **Adjust Split:** If the book moved, drag the green (left) or red (right) boxes to correct the crop area.
    
4.  **Toggle Pages:** Click "Left Page" or "Right Page" on the toolbar to disable a page if it's blank.
    
5.  **Update:** Click "Update Layout" to re-process the split files immediately.
    

👨‍💻 Development
-----------------

### Adding a New Interaction Mode

To add a new tool to the image viewer (e.g., a "Despeckle" brush):

1.  Create a new class in ui/viewer/handlers.py inheriting from InteractionHandler.
    
2.  Implement on\_mouse\_press, move, release, and paint.
    
3.  Register the handler in ui/viewer/canvas.py.
    

### Adding a New Worker Task

To add a heavy task (e.g., OCR):

1.  Add a method to workers/scanner\_worker.py decorated with @Slot.
    
2.  Emit a signal when finished.
    
3.  Connect the signal in ui/main\_window.py.
