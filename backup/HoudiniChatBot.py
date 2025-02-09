import hou
from PySide2 import QtWidgets, QtCore, QtGui, QtSvg
import requests
import json
import re

# --- Embedded Bootstrap Icons (SVG in white color) ---
# The SVGs use "currentColor" as fill. Here, we replace it with white ("#ffffff").
SVG_CLEAR = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" viewBox="0 0 24 28">
  <path d="M19 4.5L17.5 3L7 13.5C7 13.5 6 14.5 4.5 16C3 17.5 3 18.5 3 18.5C3 18.5 3.5 21 6 21C6.5 21 7.5 21 9 19.5C10.5 18 11.5 17 11.5 17L21 6.5L19.5 5L19 4.5ZM8.5 15L9.5 14C9.8 14.3 10.2 14.7 10.5 15C10.8 15.3 11.2 15.7 11.5 16L10.5 17C10.2 16.7 9.8 16.3 9.5 16C9.2 15.7 8.8 15.3 8.5 15Z"
  />
</svg>
"""

SVG_EXPORT = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" class="bi bi-download" viewBox="0 0 16 16">
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.6a.5.5 0 0 0 .5.5h13a.5.5 0 0 0 .5-.5V10.4a.5.5 0 0 1 1 0v2.6A1.5 1.5 0 0 1 15.5 14.5h-13A1.5 1.5 0 0 1 1 13V10.4a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V10.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
</svg>
"""

SVG_SETTINGS = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" class="bi bi-gear" viewBox="0 0 16 16">
  <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
  <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.893-3.433.826-2.54 2.466l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.893 1.64.826 3.433 2.466 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.433-.826 2.54-2.466l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.826-3.433-2.466-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.416 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.318.094a1.873 1.873 0 0 0-1.116 2.692l.159.292c.416.764-.42 1.6-1.184 1.184l-.291-.16a1.873 1.873 0 0 0-2.693 1.115l-.094.319c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.116l-.292.159c-.764.416-1.6-.42-1.184-1.184l.16-.292a1.873 1.873 0 0 0-1.115-2.693l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094a1.873 1.873 0 0 0 1.115-2.692l-.16-.292c-.416-.764.42-1.6 1.184-1.184l.292.16a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
</svg>
"""

SVG_SEND = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" class="bi bi-send" viewBox="0 0 16 16">
  <path d="M15.964.686a.5.5 0 0 0-.644-.164L.678 7.055a.5.5 0 0 0 .005.91l4.85 2.42 2.42 4.85a.5.5 0 0 0 .91.005l6.533-14.642a.5.5 0 0 0-.164-.644zM6.636 10.15L4.133 8.647l7.295-3.64L6.636 10.15z"/>
</svg>
"""

SVG_RUN = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path 
    fill="#4CAF50" 
    d="M5 4v16l14-8L5 4z"
  />
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

    def run(self):
        try:
            # Updated context: the assistant is now a Houdini chat bot that knows both Python and VEX.
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
            response = requests.post(self.api_url, json=data, timeout=150)
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
            # First, try to extract Python code
            code_match = re.search(r'```python(.*?)```', ai_response, re.DOTALL)
            # If no Python code is found, try to extract VEX code
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
            self.signals.error.emit("Request timed out after 30 seconds")
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
    def __init__(self, parent=None, api_url="http://localhost:11434/api/generate", model_name="deepseek-coder-v2"):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        # Increase the size for a more comfortable view
        self.resize(500, 300)
        self.setModal(True)
        # Updated stylesheet for a modern, clean look
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
            QLineEdit {
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
        """)
        layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout()
        self.api_url_edit = QtWidgets.QLineEdit(api_url)
        self.model_name_edit = QtWidgets.QLineEdit(model_name)
        form_layout.addRow("API URL:", self.api_url_edit)
        form_layout.addRow("Model Name:", self.model_name_edit)
        layout.addLayout(form_layout)
        
        # Add a stretch to push the button box to the bottom
        layout.addStretch(1)
        
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("Save")
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
    def get_settings(self):
        return self.api_url_edit.text().strip(), self.model_name_edit.text().strip()

class ChatbotPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.thread_pool = QtCore.QThreadPool()
        self.api_url = "http://localhost:11434/api/generate"
        self.model_name = "deepseek-coder-v2"
        self.history = []
        self.thinking_timer = None
        self.thinking_label = None
        self.thinking_state = 0

        # Cache Bootstrap icons (rendered from embedded SVG data) at 24x24 size.
        self.icon_clear = create_svg_icon(SVG_CLEAR, 24)
        self.icon_export = create_svg_icon(SVG_EXPORT, 24)
        self.icon_settings = create_svg_icon(SVG_SETTINGS, 24)
        self.icon_send = create_svg_icon(SVG_SEND, 24)
        self.icon_run = create_svg_icon(SVG_RUN, 24)

        self.init_ui()
        self.apply_modern_styles()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QtWidgets.QLabel("Houdini AI Assistant")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Use cached Bootstrap icons for header buttons.
        self.clear_button = QtWidgets.QPushButton()
        self.clear_button.setIcon(self.icon_clear)
        self.clear_button.setToolTip("Clear Chat")
        self.clear_button.setIconSize(QtCore.QSize(24, 24))
        self.clear_button.clicked.connect(self.clear_chat)
        header_layout.addWidget(self.clear_button)

        self.export_button = QtWidgets.QPushButton()
        self.export_button.setIcon(self.icon_export)
        self.export_button.setToolTip("Export Chat")
        self.export_button.setIconSize(QtCore.QSize(24, 24))
        self.export_button.clicked.connect(self.export_chat)
        header_layout.addWidget(self.export_button)

        self.settings_button = QtWidgets.QPushButton()
        self.settings_button.setIcon(self.icon_settings)
        self.settings_button.setToolTip("Settings")
        self.settings_button.setIconSize(QtCore.QSize(24, 24))
        self.settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(self.settings_button)

        main_layout.addWidget(header_widget)

        self.chat_container = QtWidgets.QWidget()
        self.chat_layout = QtWidgets.QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll_area, 1)

        self.error_display = QtWidgets.QLabel("")
        self.error_display.setStyleSheet("color: #e0e0e0; font-size: 11px; padding: 2px;")
        self.error_display.setAlignment(QtCore.Qt.AlignLeft)
        self.error_display.setWordWrap(True)
        main_layout.addWidget(self.error_display)

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
        self.send_button.setIconSize(QtCore.QSize(24, 24))
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(input_container)

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
                background-color: rgba(80, 80, 80, 0.3);
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
        """)

    def add_message(self, widget):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)
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
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, container)
        QtCore.QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()))

    def add_code_block(self, code):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)
        code_widget = QtWidgets.QPlainTextEdit()
        code_widget.setReadOnly(True)
        code_widget.setPlainText(code)
        code_widget.setObjectName("codeBlock")
        code_widget.setProperty("class", "codeBlock")
        PythonHighlighter(code_widget.document())
        layout.addWidget(code_widget)

        # Use cached Bootstrap icon for execute code button.
        run_button = QtWidgets.QPushButton()
        run_button.setIcon(self.icon_run)
        run_button.setToolTip("Execute Code")
        run_button.setIconSize(QtCore.QSize(24, 24))
        run_button.clicked.connect(lambda: self.execute_code(code_widget))
        layout.addWidget(run_button)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, container)
        QtCore.QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()))

    def execute_code(self, code_widget):
        cursor = code_widget.textCursor()
        selected_text = cursor.selectedText()
        code_to_run = selected_text if selected_text.strip() else code_widget.toPlainText()
        try:
            exec(code_to_run, {'hou': hou})
        except Exception as e:
            self.error_display.setText(f"Execution error: {e}")

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
        self.history.append({"role": "user", "message": message})
        self.input_field.clear()
        self.start_thinking()
        worker = AIWorker(message, self.api_url, self.model_name)
        worker.signals.finished.connect(self.handle_ai_response)
        worker.signals.error.connect(self.handle_error)
        self.thread_pool.start(worker)

    def handle_ai_response(self, ai_response, code_found, python_code):
        self.stop_thinking()
        timestamp = QtCore.QDateTime.currentDateTime().toString("hh:mm")
        
        # Create a label for real-time typing
        assistant_label = QtWidgets.QLabel()
        assistant_label.setObjectName("assistantMessage")
        assistant_label.setProperty("class", "message assistant")
        assistant_label.setTextFormat(QtCore.Qt.RichText)
        assistant_label.setWordWrap(True)
        self.add_message(assistant_label)
        
        # Real-time typing animation
        full_text = ai_response  # or text_part if you want to separate code
        current_text = ""
        typing_timer = QtCore.QTimer()
        
        def update_text():
            nonlocal current_text
            if len(current_text) < len(full_text):
                current_text += full_text[len(current_text)]
                assistant_label.setText(f"{current_text}   <span style='font-size:11px; color:#909090;'>{timestamp}</span>")
            else:
                typing_timer.stop()
                # Optional: Add code block if code is found
                if code_found and python_code:
                    self.add_code_block(python_code)
        
        typing_timer.timeout.connect(update_text)
        typing_timer.start(30)  # Adjust speed as needed

    def handle_error(self, error_message):
        self.stop_thinking()
        self.error_display.setText(error_message)

    def clear_chat(self):
        for i in reversed(range(self.chat_layout.count() - 1)):
            widget = self.chat_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.history.clear()
        self.error_display.setText("")

    def export_chat(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Chat", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                for entry in self.history:
                    role = entry.get("role", "")
                    message = entry.get("message", "")
                    f.write(f"{role.capitalize()}: {message}\n")
                    if entry.get("code", ""):
                        f.write("Code:\n" + entry["code"] + "\n")
                    f.write("\n")

    def open_settings(self):
        dialog = SettingsDialog(self, self.api_url, self.model_name)
        if dialog.exec_():
            self.api_url, self.model_name = dialog.get_settings()
            info_label = QtWidgets.QLabel("Settings updated.")
            info_label.setStyleSheet("background-color: #f5f5f5; color: #666666; padding: 8px 12px; border: 1px solid #e0e0e0; border-radius: 4px; text-align: center;")
            info_label.setAlignment(QtCore.Qt.AlignCenter)
            self.add_message(info_label)

    def keyPressEvent(self, event):
        if (event.key() in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]) and not (event.modifiers() & QtCore.Qt.ShiftModifier):
            if self.input_field.hasFocus():
                self.send_message()
                event.accept()
                return
        super().keyPressEvent(event)

def createInterface():
    return ChatbotPanel()
