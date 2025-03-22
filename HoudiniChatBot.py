"""
Houdini Chatbot
Author: Anshul Vashist
Role: FX TD | Python & Automation Enthusiast
GitHub: [https://github.com/waveWhirlVfx]
LinkedIn: [https://www.linkedin.com/in/av-0001/]
Email: [vashistanshul.7@gmail.com]
Youtube: https://www.youtube.com/@waveWhirlVfx
Description:
    This Houdini Python Panel integrates AI assistance for generating Houdini Python & VEX code,
    automating workflows, and improving efficiency.
"""

import hou
from PySide2 import QtWidgets, QtCore, QtGui, QtSvg
import requests
import json
import re
import socket
import os
import subprocess
import shutil
from typing import Tuple

def check_windows_ollama() -> Tuple[bool, str]:
    if shutil.which('ollama') is not None:
        return True, "Ollama is installed and available in PATH"
    paths_to_check = [
        os.path.expandvars(r'%ProgramFiles%\Ollama\ollama.exe'),
        os.path.expandvars(r'%ProgramFiles(x86)%\Ollama\ollama.exe'),
        os.path.expandvars(r'%LocalAppData%\Programs\Ollama\ollama.exe')
    ]
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Ollama') as key:
            install_path = winreg.QueryValueEx(key, 'InstallLocation')[0]
            return True, f"Ollama found in registry at: {install_path}"
    except ImportError:
        pass
    except WindowsError:
        pass
    for path in paths_to_check:
        if os.path.exists(path):
            return True, f"Ollama found at: {path}"
    return False, "Ollama not found on the system"

def get_ollama_version() -> str:
    try:
        result = subprocess.run(['ollama', 'version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
        return "Could not determine version"
    except:
        return "Could not determine version"

def main():
    print("Checking Ollama Installation on Windows...")
    print("-" * 40)
    is_installed, message = check_windows_ollama()
    print(f"Installation Status: {'Installed' if is_installed else 'Not Installed'}")
    print(f"Details: {message}")
    if is_installed:
        version = get_ollama_version()
        print(f"Version: {version}")

try:
    import speech_recognition as sr
except ImportError:
    sr = None
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

def is_port_open(port, host="localhost", timeout=0.5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def find_api_url(default_path="/api/generate", candidate_ports=[11434, 11435, 11433, 5000, 8000]):
    for port in candidate_ports:
        if is_port_open(port):
            return f"http://localhost:{port}{default_path}"
    return None

SVG_CLEAR = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M19 4.5L17.5 3L7 13.5C7 13.5 6 14.5 4.5 16C3 17.5 3 18.5 3 18.5C3 18.5 3.5 21 6 21C6.5 21 7.5 21 9 19.5C10.5 18 11.5 17 11.5 17L21 6.5L19.5 5L19 4.5Z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Clear</text>
    </g>
</svg>
"""

SVG_EXPORT = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M12 3L8 7h3v8h2V7h3L12 3zM4 14v4h16v-4h-2v2H6v-2H4z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Export</text>
    </g>
</svg>
"""

SVG_SETTINGS = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Settings</text>
    </g>
</svg>
"""

SVG_SEND = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Send</text>
    </g>
</svg>
"""

SVG_MIC_DEFAULT = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Voice</text>
    </g>
</svg>
"""

SVG_MIC_ACTIVE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#0000FF">
        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Voice</text>
        <circle cx="12" cy="12" r="11" fill="none" stroke="#0000FF" stroke-width="2" opacity="0.3"/>
    </g>
</svg>
"""

SVG_RUN = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g>
        <path fill="#4CAF50" d="M8 5v14l11-7z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" fill="#4CAF50" text-anchor="middle">Run</text>
    </g>
</svg>
"""

SVG_COPY = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Copy</text>
    </g>
</svg>
"""

SVG_EDIT = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <g fill="#ffffff">
        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
        <text x="12" y="23" font-family="Arial" font-size="4" text-anchor="middle">Edit</text>
    </g>
</svg>
"""

def create_svg_icon(svg_data, size):
    svg_bytes = svg_data.encode('utf-8')
    renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_bytes))
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QtGui.QIcon(pixmap)

class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal(str, bool, str)
    error = QtCore.Signal(str)
    partial = QtCore.Signal(str)

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
                "You are a Houdini automation assistant chat bot. "
                "If the user request is related to Houdini, Python, or VEX, provide the complete and precise, correct and executable code accordingly, enclosed within the appropriate code fences.Answer only what is asked, precisely and concisely, without extra details.  "
                "If the user request is not related to Houdini (for example, casual greetings or general questions), respond conversationally without any code, but still provide a helpful answer."
            )
            full_prompt = houdini_context + "\nUser request:\n" + self.user_message
            data = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": True
            }
            with requests.post(self.api_url, json=data, stream=True) as r:
                if r.status_code != 200:
                    error_msg = f"Bad response: {r.status_code}"
                    try:
                        error_msg += f" - {r.json()}"
                    except:
                        error_msg += f" - {r.text}"
                    raise Exception(error_msg)
    
                partial_text = ""
                for line in r.iter_lines(decode_unicode=True):
                    if self._cancelled:
                        self.signals.error.emit("Request cancelled by user.")
                        return
                    if line:
                        try:
                            chunk = json.loads(line)
                            token = chunk.get('response', '')
                            partial_text += token
                            self.signals.partial.emit(partial_text)
                        except:
                            pass
    
            if not partial_text.strip():
                raise Exception("Empty response from API")
    
            code_match = re.search(r'```python(.*?)```', partial_text, re.DOTALL)
            if code_match:
                extracted_code = code_match.group(1).strip()
            else:
                vex_match = re.search(r'```vex(.*?)```', partial_text, re.DOTALL)
                if vex_match:
                    extracted_code = vex_match.group(1).strip()
                else:
                    extracted_code = ""
    
            if extracted_code:
                hou.session.ai_execution_code = extracted_code
                self.signals.finished.emit(partial_text, True, extracted_code)
            else:
                self.signals.finished.emit(partial_text, False, "")
    
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
        api_group = QtWidgets.QGroupBox("API Settings")
        api_layout = QtWidgets.QFormLayout(api_group)
        self.api_url_edit = QtWidgets.QLineEdit(api_url)
        self.model_name_edit = QtWidgets.QLineEdit(model_name)
        api_layout.addRow("API URL:", self.api_url_edit)
        api_layout.addRow("Model Name:", self.model_name_edit)
        layout.addWidget(api_group)
        history_group = QtWidgets.QGroupBox("Chat History Settings")
        history_layout = QtWidgets.QVBoxLayout(history_group)
        self.storage_type = QtWidgets.QComboBox()
        self.storage_type.addItems(["Session Storage", "Disk Storage"])
        self.storage_type.setCurrentIndex(1 if use_disk_storage else 0)
        self.storage_type.currentIndexChanged.connect(self.toggle_path_widgets)
        history_layout.addWidget(QtWidgets.QLabel("Storage Type:"))
        history_layout.addWidget(self.storage_type)
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
        self.toggle_path_widgets(self.storage_type.currentIndex())
        layout.addStretch(1)
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("Save")
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def toggle_path_widgets(self, index):
        use_disk = index == 1
        self.path_edit.setEnabled(use_disk)
        self.browse_button.setEnabled(use_disk)

    def browse_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory for Chat History", self.path_edit.text(), QtWidgets.QFileDialog.ShowDirsOnly)
        if path:
            self.path_edit.setText(path)

    def get_settings(self):
        return (
            self.api_url_edit.text().strip(),
            self.model_name_edit.text().strip(),
            self.path_edit.text().strip(),
            self.storage_type.currentIndex() == 1
        )

class ChatbotPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.thread_pool = QtCore.QThreadPool()
        found_url = find_api_url(candidate_ports=[11434, 11435, 11433, 5000, 8000])
        self.api_url = found_url if found_url else "http://localhost:11434/api/generate"
        self.model_name = "qwen2.5-coder:32b"
        self.history_path = ""
        self.use_disk_storage = False
        self.load_settings()
        self.load_chat_history()
        self.current_conversation = []
        if hasattr(hou.session, "ai_chat_history"):
            self.conversations = hou.session.ai_chat_history
        else:
            self.conversations = []
        self.thinking_label = None
        self.thinking_timer = None
        self.thinking_state = 0
        self.current_worker = None
        self.request_in_progress = False
        self.cancel_requested = False
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

        chat_area_widget = QtWidgets.QWidget()
        chat_area_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        chat_area_layout = QtWidgets.QVBoxLayout(chat_area_widget)
        chat_area_layout.setContentsMargins(20,20,20,20)
        chat_area_layout.setSpacing(15)
        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0,0,0,0)
        title_label = QtWidgets.QLabel("Houdini AI Assistant")
        title_label.setObjectName("titleLabel")
        is_installed, _ = check_windows_ollama()
        status_color = "#00ff00" if is_installed else "#ff0000"
        status_icon = QtWidgets.QLabel()
        status_icon.setFixedSize(12, 12)
        status_icon.setStyleSheet(f"border-radius: 6px; background-color: {status_color};")
        title_container = QtWidgets.QWidget()
        title_layout2 = QtWidgets.QHBoxLayout(title_container)
        title_layout2.setContentsMargins(0, 0, 0, 0)
        title_layout2.setSpacing(8)
        title_layout2.addWidget(title_label)
        title_layout2.addWidget(status_icon)
        header_layout.addWidget(title_container)
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
        self.chat_container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.chat_layout = QtWidgets.QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0,0,0,0)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_container)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        chat_area_layout.addWidget(self.scroll_area, 1)

        self.error_display = QtWidgets.QLabel("")
        self.error_display.setStyleSheet("color: #e0e0e0; font-size: 11px; padding: 2px;")
        self.error_display.setAlignment(QtCore.Qt.AlignLeft)
        self.error_display.setWordWrap(True)
        chat_area_layout.addWidget(self.error_display)

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
            #titleLabel {
                font-size: 18px;
                font-weight: 500;
                color: #ffffff;
            }
            QLabel.message {
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
                font-size: 13px;
                line-height: 1.4;
                background-color: #2d2d2d;
                word-wrap: break-word;
                max-width: 700px;
            }
            QLabel.user, QLabel.assistant {
                margin: 0;
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
            QScrollArea {
                border: none;
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
        code_widget.setReadOnly(False)
        code_widget.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard)
        code_widget.setPlainText(code)
        code_widget.setObjectName("codeBlock")
        code_widget.setProperty("class", "codeBlock")
        PythonHighlighter(code_widget.document())
        layout.addWidget(code_widget)

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

        vex_indicators = [
            '@', 'v@', 'f@', 'i@', 'p@',
            'point()', 'prim()', 'vertex()', 'detail()',
            'volumesample()', 'chramp()', 'primintrinsic()'
        ]
        is_vex = any(indicator in code_to_run for indicator in vex_indicators)

        try:
            if is_vex:
                selected_nodes = hou.selectedNodes()
                parent_node = None
                if selected_nodes:
                    parent_node = selected_nodes[0].parent()
                    insert_position = selected_nodes[0].position()
                    insert_position = hou.Vector2(insert_position[0] + 1, insert_position[1] - 1)
                else:
                    editor = [pane for pane in hou.ui.paneTabs() if isinstance(pane, hou.NetworkEditor)]
                    if editor:
                        parent_node = editor[0].pwd()
                        insert_position = editor[0].cursorPosition()
                    else:
                        parent_node = hou.node("/obj")
                        insert_position = hou.Vector2(0, 0)

                if parent_node:
                    wrangle = parent_node.createNode("attribwrangle")
                    wrangle.setPosition(insert_position)
                    wrangle.parm("snippet").set(code_to_run)
                    wrangle.setSelected(True)
                    self.error_display.setText("Created attribute wrangle node with VEX code")
                else:
                    raise Exception("Could not determine where to create the wrangle node")
            else:
                exec(code_to_run, {'hou': hou})
                self.error_display.setText("Python code executed successfully")

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
    
        self.start_thinking()  # show "thinking" immediately
    
        self.send_button.setEnabled(False)
        self.cancel_button.show()
        self.request_in_progress = True
        self.cancel_requested = False
    
        worker = AIWorker(message, self.api_url, self.model_name)
        worker.signals.partial.connect(self.handle_partial_response)
        worker.signals.finished.connect(self.handle_ai_response)
        worker.signals.error.connect(self.handle_error)
        self.current_worker = worker
        self.thread_pool.start(worker)

    def handle_partial_response(self, partial_text):
        if self.cancel_requested:
            return
    
        # As soon as AI starts sending any text, stop thinking
        if self.thinking_label:
            self.stop_thinking()
    
        # Display partial text in a dedicated label
        if not hasattr(self, 'partial_label') or self.partial_label is None:
            self.partial_label = QtWidgets.QLabel()
            self.partial_label.setProperty("class", "message assistant")
            self.partial_label.setTextFormat(QtCore.Qt.RichText)
            self.partial_label.setWordWrap(True)
            self.add_message(self.partial_label)
    
        self.partial_label.setText(partial_text)


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
        if hasattr(self, 'partial_label') and self.partial_label:
            self.partial_label.setText(ai_response)
            self.partial_label = None
    
        vex_match = re.search(r'```vex(.*?)```', ai_response, re.DOTALL)
        if vex_match:
            code_found = True
            python_code = vex_match.group(1).strip()
    
        entry = {"role": "assistant", "message": ai_response}
        if code_found and python_code:
            entry["code"] = python_code
            entry["is_vex"] = bool(vex_match)
    
        self.current_conversation.append(entry)
    
        if code_found and python_code:
            self.add_code_block(python_code)
    
        self.cleanup_after_request()


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
        settings_path = os.path.join(os.path.expanduser("~"), ".houdini_ai_settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    self.api_url = settings.get('api_url', self.api_url)
                    self.model_name = settings.get('model_name', self.model_name)
                    self.history_path = settings.get('history_path', '')
                    self.use_disk_storage = settings.get('use_disk_storage', False)
            except:
                pass

    def save_settings(self):
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
        except:
            pass

    def load_chat_history(self):
        if self.use_disk_storage and self.history_path:
            history_file = os.path.join(self.history_path, "houdini_ai_chat_history.json")
            try:
                if os.path.exists(history_file):
                    with open(history_file, 'r') as f:
                        self.conversations = json.load(f)
                else:
                    self.conversations = []
            except:
                self.conversations = []
        else:
            if hasattr(hou.session, "ai_chat_history"):
                self.conversations = hou.session.ai_chat_history
            else:
                self.conversations = []

    def save_chat_history(self):
        if self.use_disk_storage and self.history_path:
            try:
                if not os.path.exists(self.history_path):
                    os.makedirs(self.history_path)
                history_file = os.path.join(self.history_path, "houdini_ai_chat_history.json")
                with open(history_file, 'w') as f:
                    json.dump(self.conversations, f)
            except:
                pass
        else:
            hou.session.ai_chat_history = self.conversations

    def open_settings(self):
        dialog = SettingsDialog(self, self.api_url, self.model_name, self.history_path, self.use_disk_storage)
        if dialog.exec_():
            self.api_url, self.model_name, self.history_path, self.use_disk_storage = dialog.get_settings()
            self.save_settings()
            self.load_chat_history()
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
