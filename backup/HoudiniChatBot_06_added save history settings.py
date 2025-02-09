import hou
from PySide2 import QtWidgets, QtCore, QtGui, QtSvg
import requests
import json
import re
import socket
import os

# Try importing voice libraries.
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

# --- Automatic API URL/Port Check Functions ---
def is_port_open(port, host="localhost", timeout=0.5):
    """Return True if the given port is open on the host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def find_api_url(default_path="/api/generate", candidate_ports=[11434, 11435, 11433, 5000, 8000]):
    """Return a full API URL for the first open candidate port on localhost.
       If none are found, returns None."""
    for port in candidate_ports:
        if is_port_open(port):
            return f"http://localhost:{port}{default_path}"
    return None

# --- Embedded SVG Icons ---
SVG_CLEAR = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 24 28">
  <path d="M19 4.5L17.5 3L7 13.5C7 13.5 6 14.5 4.5 16C3 17.5 3 18.5 3 18.5C3 18.5 3.5 21 6 21C6.5 21 7.5 21 9 19.5C10.5 18 11.5 17 11.5 17L21 6.5L19.5 5L19 4.5Z"/>
</svg>
"""

SVG_EXPORT = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 16 16">
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.6a.5.5 0 0 0 .5.5h13a.5.5 0 0 0 .5-.5V10.4a.5.5 0 0 1 1 0v2.6A1.5 1.5 0 0 1 15.5 14.5h-13A1.5 1.5 0 0 1 1 13V10.4a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V10.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
</svg>
"""

SVG_SETTINGS = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 16 16">
  <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
  <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.893-3.433.826-2.54 2.466l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.893 1.64.826 3.433 2.466 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.433-.826 2.54-2.466l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.826-3.433-2.466-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.416 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.318.094a1.873 1.873 0 0 0-1.116 2.692l.159.292c.416.764-.42 1.6-1.184 1.184l-.291-.16a1.873 1.873 0 0 0-2.693 1.115l-.094.319c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.116l-.292.159c-.764.416-1.6-.42-1.184-1.184l.16-.292a1.873 1.873 0 0 0-1.115-2.693l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094a1.873 1.873 0 0 0 1.115-2.692l-.16-.292c-.416-.764.42-1.6 1.184-1.184l.292.16a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
</svg>
"""

SVG_SEND = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 16 16">
  <path d="M15.964.686a.5.5 0 0 0-.644-.164L.678 7.055a.5.5 0 0 0 .005.91l4.85 2.42 2.42 4.85a.5.5 0 0 0 .91.005l6.533-14.642a.5.5 0 0 0-.164-.644zM6.636 10.15L4.133 8.647l7.295-3.64L6.636 10.15z"/>
</svg>
"""

SVG_RUN = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="#4CAF50" d="M5 4v16l14-8L5 4z"/>
</svg>
"""

# --- Microphone Icons ---
SVG_MIC_DEFAULT = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#ffffff" viewBox="0 0 16 16">
  <path d="M8 11a3 3 0 0 0 3-3V4a3 3 0 0 0-6 0v4a3 3 0 0 0 3 3z"/>
  <path d="M5 8a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5A.5.5 0 0 1 5 8z"/>
  <path d="M8 0a2 2 0 0 1 2 2v4a2 2 0 0 1-4 0V2a2 2 0 0 1 2-2z"/>
  <path d="M3.5 9A.5.5 0 0 1 4 9.5v.5h8v-.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5V10a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5v-.5a.5.5 0 0 1 .5-.5h1z"/>
</svg>
"""

SVG_MIC_ACTIVE = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#0000FF" viewBox="0 0 16 16">
  <path d="M8 11a3 3 0 0 0 3-3V4a3 3 0 0 0-6 0v4a3 3 0 0 0 3 3z"/>
  <path d="M5 8a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5A.5.5 0 0 1 5 8z"/>
  <path d="M8 0a2 2 0 0 1 2 2v4a2 2 0 0 1-4 0V2a2 2 0 0 1 2-2z"/>
  <path d="M3.5 9A.5.5 0 0 1 4 9.5v.5h8v-.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5V10a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5v-.5a.5.5 0 0 1 .5-.5h1z"/>
</svg>
"""

# --- New Icons for Copy and Edit ---
SVG_COPY = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 16 16">
  <path d="M10 1H2a1 1 0 0 0-1 1v11h1V2h8V1z"/>
  <path d="M14 4H6a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1zm-1 9H7V6h6v7z"/>
</svg>
"""

SVG_EDIT = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 16 16">
  <path d="M15.502 1.94a.5.5 0 0 1 0 .706l-1.793 1.793-2.121-2.121 1.793-1.793a.5.5 0 0 1 .707 0l1.414 1.414z"/>
  <path d="M14.207 3.207l-2.121-2.121L3 10.171V13h2.829l8.378-8.378z"/>
</svg>
"""

def create_svg_icon(svg_data, size):
    """
    Create a QIcon from an SVG string.
    """
    svg_bytes = svg_data.encode('utf-8')
    renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_bytes))
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QtGui.QIcon(pixmap)

# --- End Embedded Icons ---

class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal(str, bool, str)
    error = QtCore.Signal(str)

class AIWorker(QtCore.QRunnable):
    def __init__(self, user_message, api_url, model_name):
        super().__init__()
        self.signals = WorkerSignals()
        self.user_message = user_message
        self.api_url = api_url
        self.model_name = model_name
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            houdini_context = (
                "You are a Houdini automation assistant chat bot. You are an expert in Houdini, Python, and VEX. "
                "Your task is to generate only the Houdini code (either Python or VEX) that the user requests, with no extra commentary or explanations. "
                "If the request is for Python, output a brief message indicating that the code follows, then provide the complete, correct, and executable Houdini Python code enclosed between ```python and ```.\n"
                "If the request is for VEX, output a brief message indicating that the code follows, then provide the complete, correct VEX code enclosed between ```vex and ```."
            )
            full_prompt = houdini_context + "\nUser request:\n" + self.user_message
            data = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False
            }
            response = requests.post(self.api_url, json=data)
            if self._cancelled:
                self.signals.error.emit("Request cancelled by user.")
                return
            if response.status_code != 200:
                error_msg = f"Bad response: {response.status_code}"
                try:
                    error_msg += f" - {response.json()}"
                except Exception:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)
            ai_response = response.json().get('response', '')
            if not ai_response:
                raise Exception("Empty response from API")
            code_match = re.search(r'```python(.*?)```', ai_response, re.DOTALL)
            if code_match:
                extracted_code = code_match.group(1).strip()
            else:
                vex_match = re.search(r'```vex(.*?)```', ai_response, re.DOTALL)
                if vex_match:
                    extracted_code = vex_match.group(1).strip()
                else:
                    extracted_code = ""
            if extracted_code:
                hou.session.ai_execution_code = extracted_code
                self.signals.finished.emit(ai_response, True, extracted_code)
            else:
                self.signals.finished.emit(ai_response, False, "")
        except requests.exceptions.Timeout:
            self.signals.error.emit("Request timed out.")
        except requests.exceptions.ConnectionError:
            self.signals.error.emit(f"Failed to connect to {self.api_url}. Check if the server is running.")
        except Exception as e:
            error_msg = f"Model request error: {str(e)}\nAPI URL: {self.api_url}\nModel: {self.model_name}"
            self.signals.error.emit(error_msg)

class PythonHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("#666666"))
        keyword_format.setFontWeight(QtGui.QFont.Bold)
        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QColor("#444444"))
        comment_format = QtGui.QTextCharFormat()
        comment_format.setForeground(QtGui.QColor("#999999"))
        self.highlighting_rules = []
        keywords = [
            "def", "class", "import", "from", "as", "if", "elif", "else", "try",
            "except", "finally", "for", "while", "with", "return", "in", "is", "not",
            "and", "or", "pass", "break", "continue", "yield", "lambda"
        ]
        for keyword in keywords:
            pattern = QtCore.QRegExp(r"\b" + keyword + r"\b")
            self.highlighting_rules.append((pattern, keyword_format))
        self.highlighting_rules.extend([
            (QtCore.QRegExp(r"\".*\""), string_format),
            (QtCore.QRegExp(r"\'.*\'"), string_format),
        ])
        self.highlighting_rules.append((QtCore.QRegExp(r"#.*"), comment_format))
        self.code_block_regex = QtCore.QRegExp(r"```python.*?```")
        self.code_block_regex.setMinimal(True)

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, api_url="http://localhost:11434/api/generate", model_name="deepseek-coder-v2", history_path="", use_disk_storage=False):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(500, 350)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                padding: 4px;
            }
            QLineEdit, QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                padding: 8px;
                border-radius: 4px;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #505050;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QCheckBox {
                color: #e0e0e0;
            }
            QGroupBox {
                border: 1px solid #404040;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 1em;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # API Settings Group
        api_group = QtWidgets.QGroupBox("API Settings")
        api_layout = QtWidgets.QFormLayout(api_group)
        
        self.api_url_edit = QtWidgets.QLineEdit(api_url)
        self.model_name_edit = QtWidgets.QLineEdit(model_name)
        api_layout.addRow("API URL:", self.api_url_edit)
        api_layout.addRow("Model Name:", self.model_name_edit)
        layout.addWidget(api_group)
        
        # History Settings Group
        history_group = QtWidgets.QGroupBox("Chat History Settings")
        history_layout = QtWidgets.QVBoxLayout(history_group)
        
        # Storage Type Selection
        self.storage_type = QtWidgets.QComboBox()
        self.storage_type.addItems(["Session Storage", "Disk Storage"])
        self.storage_type.setCurrentIndex(1 if use_disk_storage else 0)
        self.storage_type.currentIndexChanged.connect(self.toggle_path_widgets)
        history_layout.addWidget(QtWidgets.QLabel("Storage Type:"))
        history_layout.addWidget(self.storage_type)
        
        # Path Selection Widgets
        path_widget = QtWidgets.QWidget()
        path_layout = QtWidgets.QHBoxLayout(path_widget)
        self.path_edit = QtWidgets.QLineEdit(history_path)
        self.path_edit.setPlaceholderText("Select path to store chat history...")
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_button)
        history_layout.addWidget(QtWidgets.QLabel("Storage Path:"))
        history_layout.addWidget(path_widget)
        
        layout.addWidget(history_group)
        
        # Toggle path widgets based on initial selection
        self.toggle_path_widgets(self.storage_type.currentIndex())
        
        layout.addStretch(1)
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("Save")
        layout.addWidget(button_box)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
    
    def toggle_path_widgets(self, index):
        """Enable/disable path selection widgets based on storage type."""
        use_disk = index == 1
        self.path_edit.setEnabled(use_disk)
        self.browse_button.setEnabled(use_disk)
    
    def browse_path(self):
        """Open file dialog to select history storage path."""
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Directory for Chat History",
            self.path_edit.text(),
            QtWidgets.QFileDialog.ShowDirsOnly
        )
        if path:
            self.path_edit.setText(path)
    
    def get_settings(self):
        """Return tuple of all settings."""
        return (
            self.api_url_edit.text().strip(),
            self.model_name_edit.text().strip(),
            self.path_edit.text().strip(),
            self.storage_type.currentIndex() == 1  # True if Disk Storage
        )

class ChatbotPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.thread_pool = QtCore.QThreadPool()
        found_url = find_api_url(candidate_ports=[11434, 11435, 11433, 5000, 8000])
        self.api_url = found_url if found_url else "http://localhost:11434/api/generate"
        self.model_name = "qwen2.5-coder:32b"
        # Add new persistence settings
        self.history_path = ""
        self.use_disk_storage = False
        self.load_settings()
        
        # Load chat history based on storage type
        self.load_chat_history()
        
        self.current_conversation = []
        if hasattr(hou.session, "ai_chat_history"):
            self.conversations = hou.session.ai_chat_history
        else:
            self.conversations = []
        self.current_conversation = []
        self.thinking_timer = None
        self.thinking_label = None
        self.thinking_state = 0
        self.current_worker = None
        self.request_in_progress = False
        self.cancel_requested = False

        # Cache icons
        self.icon_clear = create_svg_icon(SVG_CLEAR, 24)
        self.icon_export = create_svg_icon(SVG_EXPORT, 24)
        self.icon_settings = create_svg_icon(SVG_SETTINGS, 24)
        self.icon_send = create_svg_icon(SVG_SEND, 24)
        self.icon_run = create_svg_icon(SVG_RUN, 24)
        self.icon_mic_default = create_svg_icon(SVG_MIC_DEFAULT, 24)
        self.icon_mic_active = create_svg_icon(SVG_MIC_ACTIVE, 24)
        self.icon_copy = create_svg_icon(SVG_COPY, 16)
        self.icon_edit = create_svg_icon(SVG_EDIT, 16)

        self.init_ui()
        self.apply_modern_styles()

    def init_ui(self):
        main_hlayout = QtWidgets.QHBoxLayout(self)
        main_hlayout.setContentsMargins(0,0,0,0)
        main_hlayout.setSpacing(0)

        # Sidebar
        sidebar_widget = QtWidgets.QWidget()
        sidebar_layout = QtWidgets.QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10,10,10,10)
        sidebar_layout.setSpacing(10)
        self.new_chat_button = QtWidgets.QPushButton("New Chat")
        self.new_chat_button.clicked.connect(self.new_chat)
        sidebar_layout.addWidget(self.new_chat_button)
        self.sidebar = QtWidgets.QListWidget()
        self.sidebar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sidebar.customContextMenuRequested.connect(self.show_context_menu)
        self.sidebar.itemClicked.connect(self.load_conversation)
        sidebar_layout.addWidget(self.sidebar,1)
        for conv in self.conversations:
            self.sidebar.addItem(conv["title"])

        # Main Chat Area
        chat_area_widget = QtWidgets.QWidget()
        chat_area_layout = QtWidgets.QVBoxLayout(chat_area_widget)
        chat_area_layout.setContentsMargins(20,20,20,20)
        chat_area_layout.setSpacing(15)
        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0,0,0,0)
        title_label = QtWidgets.QLabel("Houdini AI Assistant")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.clear_button = QtWidgets.QPushButton()
        self.clear_button.setIcon(self.icon_clear)
        self.clear_button.setToolTip("Clear Chat")
        self.clear_button.setIconSize(QtCore.QSize(24,24))
        self.clear_button.clicked.connect(self.clear_chat)
        header_layout.addWidget(self.clear_button)
        self.export_button = QtWidgets.QPushButton()
        self.export_button.setIcon(self.icon_export)
        self.export_button.setToolTip("Export Chat")
        self.export_button.setIconSize(QtCore.QSize(24,24))
        self.export_button.clicked.connect(self.export_chat)
        header_layout.addWidget(self.export_button)
        self.settings_button = QtWidgets.QPushButton()
        self.settings_button.setIcon(self.icon_settings)
        self.settings_button.setToolTip("Settings")
        self.settings_button.setIconSize(QtCore.QSize(24,24))
        self.settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_button)
        chat_area_layout.addWidget(header_widget)

        self.chat_container = QtWidgets.QWidget()
        self.chat_layout = QtWidgets.QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0,0,0,0)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_container)
        chat_area_layout.addWidget(self.scroll_area, 1)
        self.error_display = QtWidgets.QLabel("")
        self.error_display.setStyleSheet("color: #e0e0e0; font-size: 11px; padding: 2px;")
        self.error_display.setAlignment(QtCore.Qt.AlignLeft)
        self.error_display.setWordWrap(True)
        chat_area_layout.addWidget(self.error_display)

        # Input area with text, Send, Mic, Cancel buttons.
        input_container = QtWidgets.QWidget()
        input_layout = QtWidgets.QHBoxLayout(input_container)
        input_layout.setSpacing(8)
        self.input_field = QtWidgets.QTextEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setMaximumHeight(36)
        self.input_field.setObjectName("inputField")
        input_layout.addWidget(self.input_field)
        self.send_button = QtWidgets.QPushButton()
        self.send_button.setIcon(self.icon_send)
        self.send_button.setToolTip("Send Message")
        self.send_button.setIconSize(QtCore.QSize(24,24))
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        self.mic_button = QtWidgets.QPushButton()
        self.mic_button.setIcon(self.icon_mic_default)
        self.mic_button.setToolTip("Voice Input")
        self.mic_button.setIconSize(QtCore.QSize(24,24))
        self.mic_button.clicked.connect(self.voice_input)
        input_layout.addWidget(self.mic_button)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setToolTip("Cancel Request")
        self.cancel_button.clicked.connect(self.cancel_request)
        self.cancel_button.hide()
        input_layout.addWidget(self.cancel_button)
        chat_area_layout.addWidget(input_container)
        main_hlayout.addWidget(sidebar_widget,0)
        main_hlayout.addWidget(chat_area_widget,1)

    def show_context_menu(self, pos):
        item = self.sidebar.itemAt(pos)
        if item is None:
            return
        menu = QtWidgets.QMenu()
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.sidebar.mapToGlobal(pos))
        if action == delete_action:
            self.delete_conversation(item)

    def delete_conversation(self, item):
        index = self.sidebar.row(item)
        if index < 0 or index >= len(self.conversations):
            return
        self.conversations.pop(index)
        self.sidebar.takeItem(index)
        hou.session.ai_chat_history = self.conversations

    def apply_modern_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            }
            #titleLabel { font-size: 18px; font-weight: 500; color: #ffffff; }
            QLabel.message {
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
                line-height: 1.4;
            }
            QLabel.user {
                background-color: #2d2d2d;
                max-width: 80%;
                margin-left: auto;
            }
            QLabel.assistant {
                background-color: #2d2d2d;
                margin-right: auto;
            }
            QPlainTextEdit.codeBlock {
                background-color: #1E1E1E;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
                font-family: Consolas, Monaco, "Courier New", monospace;
                font-size: 13px;
                line-height: 1.45;
            }
            #inputField {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
                min-height: 36px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(80,80,80,0.3);
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                border-radius: 4px;
            }
            QListWidget {
                background-color: #2d2d2d;
                border: none;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #404040;
            }
        """)

    def add_message(self, widget):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(10,5,10,5)
        role = widget.property("class")
        if role == "message user":
            layout.addStretch()
            layout.addWidget(widget)
        elif role == "message assistant":
            layout.addWidget(widget)
            layout.addStretch()
        else:
            layout.addStretch()
            layout.addWidget(widget)
            layout.addStretch()
        self.chat_layout.insertWidget(self.chat_layout.count()-1, container)
        QtCore.QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()))

    def add_code_block(self, code):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(10,5,10,5)
        code_widget = QtWidgets.QPlainTextEdit()
        code_widget.setReadOnly(True)
        code_widget.setPlainText(code)
        code_widget.setObjectName("codeBlock")
        code_widget.setProperty("class", "codeBlock")
        PythonHighlighter(code_widget.document())
        layout.addWidget(code_widget)

        # Button container for Run, Copy, and Edit
        buttons_container = QtWidgets.QWidget()
        buttons_layout = QtWidgets.QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0,0,0,0)
        buttons_layout.setSpacing(10)
        
        run_button = QtWidgets.QPushButton()
        run_button.setIcon(self.icon_run)
        run_button.setToolTip("Execute Code")
        run_button.setIconSize(QtCore.QSize(24,24))
        run_button.clicked.connect(lambda: self.execute_code(code_widget))
        buttons_layout.addWidget(run_button)
        
        copy_button = QtWidgets.QPushButton("Copy")
        copy_button.setIcon(self.icon_copy)
        copy_button.setToolTip("Copy Code")
        copy_button.clicked.connect(lambda: self.copy_code(code_widget, copy_button))
        buttons_layout.addWidget(copy_button)
        
        edit_button = QtWidgets.QPushButton("Edit")
        edit_button.setIcon(self.icon_edit)
        edit_button.setToolTip("Toggle Editable Code")
        edit_button.clicked.connect(lambda: self.toggle_edit_code(code_widget, edit_button))
        buttons_layout.addWidget(edit_button)
        
        layout.addWidget(buttons_container)
        self.chat_layout.insertWidget(self.chat_layout.count()-1, container)
        QtCore.QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()))

    def toggle_edit_code(self, code_widget, edit_button):
        if code_widget.isReadOnly():
            code_widget.setReadOnly(False)
            edit_button.setText("Lock")
        else:
            code_widget.setReadOnly(True)
            edit_button.setText("Edit")

    def copy_code(self, code_widget, copy_button):
        code_text = code_widget.toPlainText()
        QtWidgets.QApplication.clipboard().setText(code_text)
        original_text = copy_button.text()
        copy_button.setText("✓ Copied")
        QtCore.QTimer.singleShot(2000, lambda: copy_button.setText(original_text))

    def execute_code(self, code_widget):
        cursor = code_widget.textCursor()
        selected_text = cursor.selectedText()
        code_to_run = selected_text if selected_text.strip() else code_widget.toPlainText()
        try:
            exec(code_to_run, {'hou': hou})
        except Exception as e:
            self.error_display.setText(f"Execution error: {e}")

    def voice_input(self):
        if sr is None:
            self.error_display.setText("Speech recognition module not available.")
            return
        self.mic_button.setIcon(self.icon_mic_active)
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.error_display.setText("Listening...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            self.input_field.setPlainText(text)
            self.error_display.setText("")
        except Exception as e:
            self.error_display.setText("Voice recognition error: " + str(e))
        finally:
            self.mic_button.setIcon(self.icon_mic_default)

    def voice_output(self, text):
        if pyttsx3 is None:
            self.error_display.setText("Text-to-speech module not available.")
            return
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def start_thinking(self):
        if self.thinking_label is None:
            self.thinking_label = QtWidgets.QLabel("thinking.")
            self.thinking_label.setProperty("class", "message assistant")
            self.thinking_label.setTextFormat(QtCore.Qt.RichText)
            self.thinking_label.setWordWrap(True)
            self.add_message(self.thinking_label)
        self.thinking_state = 0
        self.thinking_timer = QtCore.QTimer()
        self.thinking_timer.timeout.connect(self.update_thinking)
        self.thinking_timer.start(500)

    def update_thinking(self):
        dots = "." * ((self.thinking_state % 3) + 1)
        self.thinking_label.setText(f"thinking{dots}")
        self.thinking_state += 1

    def stop_thinking(self):
        if self.thinking_timer:
            self.thinking_timer.stop()
            self.thinking_timer = None
        if self.thinking_label:
            self.thinking_label.setParent(None)
            self.thinking_label = None

    def cleanup_after_request(self):
        self.request_in_progress = False
        self.cancel_requested = False
        self.current_worker = None
        self.cancel_button.hide()
        self.send_button.setEnabled(True)

    def send_message(self):
        self.error_display.setText("")
        message = self.input_field.toPlainText().strip()
        if not message:
            return
        timestamp = QtCore.QDateTime.currentDateTime().toString("hh:mm")
        user_label = QtWidgets.QLabel(f"{message}   <span style='font-size:11px; color:#666666;'>{timestamp}</span>")
        user_label.setObjectName("userMessage")
        user_label.setProperty("class", "message user")
        user_label.setTextFormat(QtCore.Qt.RichText)
        user_label.setWordWrap(True)
        self.add_message(user_label)
        self.current_conversation.append({"role": "user", "message": message})
        self.input_field.clear()
        self.start_thinking()
        self.send_button.setEnabled(False)
        self.cancel_button.show()
        self.request_in_progress = True
        self.cancel_requested = False
        worker = AIWorker(message, self.api_url, self.model_name)
        self.current_worker = worker
        worker.signals.finished.connect(self.handle_ai_response)
        worker.signals.error.connect(self.handle_error)
        self.thread_pool.start(worker)

    def cancel_request(self):
        if self.request_in_progress and self.current_worker:
            self.cancel_requested = True
            self.current_worker.cancel()
            self.stop_thinking()
            self.error_display.setText("Request cancelled by user.")
            self.cleanup_after_request()

    def handle_ai_response(self, ai_response, code_found, python_code):
        if self.cancel_requested:
            return
        self.stop_thinking()
        timestamp = QtCore.QDateTime.currentDateTime().toString("hh:mm")
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(10,5,10,5)
        assistant_label = QtWidgets.QLabel()
        assistant_label.setProperty("class", "message assistant")
        assistant_label.setTextFormat(QtCore.Qt.RichText)
        assistant_label.setWordWrap(True)
        layout.addWidget(assistant_label)
        if pyttsx3 is not None:
            speak_button = QtWidgets.QPushButton("Speak")
            speak_button.setToolTip("Speak Response")
            speak_button.clicked.connect(lambda: self.voice_output(ai_response))
            layout.addWidget(speak_button)
        layout.addStretch()
        self.chat_layout.insertWidget(self.chat_layout.count()-1, container)
        full_text = ai_response
        current_text = ""
        typing_timer = QtCore.QTimer()
        def update_text():
            nonlocal current_text
            if len(current_text) < len(full_text):
                current_text += full_text[len(current_text)]
                assistant_label.setText(f"{current_text}   <span style='font-size:11px; color:#909090;'>{timestamp}</span>")
            else:
                typing_timer.stop()
                entry = {"role": "assistant", "message": ai_response}
                if code_found and python_code:
                    entry["code"] = python_code
                self.current_conversation.append(entry)
                if code_found and python_code:
                    self.add_code_block(python_code)
                self.cleanup_after_request()
        typing_timer.timeout.connect(update_text)
        typing_timer.start(30)

    def handle_error(self, error_message):
        if self.cancel_requested:
            return
        self.stop_thinking()
        self.error_display.setText(error_message)
        self.cleanup_after_request()

    def clear_chat(self):
        for i in reversed(range(self.chat_layout.count()-1)):
            widget = self.chat_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.error_display.setText("")

    def export_chat(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Chat", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                for entry in self.current_conversation:
                    role = entry.get("role", "")
                    message = entry.get("message", "")
                    f.write(f"{role.capitalize()}: {message}\n")
                    if entry.get("code", ""):
                        f.write("Code:\n" + entry["code"] + "\n")
                    f.write("\n")

    def load_conversation(self, item):
        index = self.sidebar.row(item)
        if index < 0 or index >= len(self.conversations):
            return
        conversation = self.conversations[index]["messages"]
        self.clear_chat()
        self.current_conversation = conversation.copy()
        for entry in conversation:
            timestamp = ""
            if entry.get("role") == "user":
                label = QtWidgets.QLabel(f"{entry.get('message')}   <span style='font-size:11px; color:#666666;'>{timestamp}</span>")
                label.setProperty("class", "message user")
                label.setTextFormat(QtCore.Qt.RichText)
                label.setWordWrap(True)
                self.add_message(label)
            elif entry.get("role") == "assistant":
                label = QtWidgets.QLabel(f"{entry.get('message')}   <span style='font-size:11px; color:#909090;'>{timestamp}</span>")
                label.setProperty("class", "message assistant")
                label.setTextFormat(QtCore.Qt.RichText)
                label.setWordWrap(True)
                self.add_message(label)
                if entry.get("code", ""):
                    self.add_code_block(entry.get("code"))
                    
    def keyPressEvent(self, event):
        if (event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]) and not (event.modifiers() & QtCore.Qt.ShiftModifier):
            if self.input_field.hasFocus():
                self.send_message()
                event.accept()
                return
        super().keyPressEvent(event)

    def load_settings(self):
        """Load settings from disk if they exist."""
        settings_path = os.path.join(os.path.expanduser("~"), ".houdini_ai_settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    self.api_url = settings.get('api_url', self.api_url)
                    self.model_name = settings.get('model_name', self.model_name)
                    self.history_path = settings.get('history_path', '')
                    self.use_disk_storage = settings.get('use_disk_storage', False)
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save current settings to disk."""
        settings_path = os.path.join(os.path.expanduser("~"), ".houdini_ai_settings.json")
        try:
            settings = {
                'api_url': self.api_url,
                'model_name': self.model_name,
                'history_path': self.history_path,
                'use_disk_storage': self.use_disk_storage
            }
            with open(settings_path, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_chat_history(self):
        """Load chat history based on storage type."""
        if self.use_disk_storage and self.history_path:
            history_file = os.path.join(self.history_path, "houdini_ai_chat_history.json")
            try:
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        self.conversations = json.load(f)
                else:
                    self.conversations = []
            except Exception as e:
                print(f"Error loading chat history: {e}")
                self.conversations = []
        else:
            # Use session storage
            if hasattr(hou.session, "ai_chat_history"):
                self.conversations = hou.session.ai_chat_history
            else:
                self.conversations = []

    def save_chat_history(self):
        """Save chat history based on storage type."""
        if self.use_disk_storage and self.history_path:
            try:
                if not os.path.exists(self.history_path):
                    os.makedirs(self.history_path)
                history_file = os.path.join(self.history_path, "houdini_ai_chat_history.json")
                with open(history_file, 'w') as f:
                    json.dump(self.conversations, f)
            except Exception as e:
                print(f"Error saving chat history: {e}")
        else:
            # Use session storage
            hou.session.ai_chat_history = self.conversations

    def open_settings(self):
        dialog = SettingsDialog(
            self, 
            self.api_url, 
            self.model_name,
            self.history_path,
            self.use_disk_storage
        )
        if dialog.exec_():
            self.api_url, self.model_name, self.history_path, self.use_disk_storage = dialog.get_settings()
            self.save_settings()
            # Reload chat history with new settings
            self.load_chat_history()
            # Refresh sidebar
            self.sidebar.clear()
            for conv in self.conversations:
                self.sidebar.addItem(conv["title"])
            info_label = QtWidgets.QLabel("Settings updated.")
            info_label.setStyleSheet("background-color: #2d2d2d; color: #e0e0e0; padding: 8px 12px; border: 1px solid #404040; border-radius: 4px; text-align: center;")
            info_label.setAlignment(QtCore.Qt.AlignCenter)
            self.add_message(info_label)

    def new_chat(self):
        if self.current_conversation:
            first_msg = ""
            for entry in self.current_conversation:
                if entry.get("role") == "user":
                    first_msg = entry.get("message")
                    break
            title = (first_msg[:20] + "...") if first_msg else "New Chat"
            self.conversations.append({"title": title, "messages": self.current_conversation})
            self.sidebar.addItem(title)
            self.save_chat_history()
        self.clear_chat()
        self.current_conversation = []

    def closeEvent(self, event):
        if self.current_conversation:
            first_msg = ""
            for entry in self.current_conversation:
                if entry.get("role") == "user":
                    first_msg = entry.get("message")
                    break
            title = (first_msg[:20] + "...") if first_msg else "New Chat"
            self.conversations.append({"title": title, "messages": self.current_conversation})
            self.sidebar.addItem(title)
            self.save_chat_history()
        event.accept()

def createInterface():
    return ChatbotPanel()
