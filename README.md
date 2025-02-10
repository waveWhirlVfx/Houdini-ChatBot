# Houdini AI Assistant ChatBot

A powerful AI-powered chat interface for Houdini that helps users generate and execute Python and VEX code. This tool integrates with Ollama to provide intelligent code generation and automation capabilities within Houdini.
![Screenshot 2025-02-09 021532](https://github.com/user-attachments/assets/e2382ea6-de81-47f2-b672-781e52793eb6)



## Features

- 🤖 AI-powered code generation for both Python and VEX
- 💻 Built-in code editor with syntax highlighting
- 🔄 Real-time code execution within Houdini
- 🎙️ Voice input support (optional)
- 🔊 Text-to-speech output (optional)
- 💾 Persistent chat history with both session and disk storage options
- 📤 Export chat conversations
- ⚙️ Configurable settings for API endpoint and model selection
- 🎨 Modern, dark-themed UI with responsive design

## Prerequisites

- Houdini (Recent version)
- [Ollama](https://ollama.ai/) installed and running
- Python 3.x
- PySide2

### Optional Dependencies
- `speech_recognition` (for voice input)
- `pyttsx3` (for text-to-speech)

## Installation

1. Clone this repository into your Houdini Python scripts directory:
```bash
git clone https://github.com/waveWhirlVfx/Houdini-ChatBot.git
```
2. For voice features (optional):
```bash
pip install SpeechRecognition pyttsx3
```

3. Ensure Ollama is installed and running on your system:
   - The tool automatically checks for Ollama installation
   - Default API endpoint is `http://localhost:11434/api/generate`

## Usage

1. Launch Houdini

2. Create a new Python Panel and add this code:
```python
import HoudiniChatBot
def onCreateInterface():
    return HoudiniChatBot.createInterface()
```

3. The chat interface will appear with the following features:
   - Input field for typing queries
   - Send button to submit requests
   - Voice input button (if speech recognition is installed)
   - Code execution button for running generated code
   - Copy and Edit buttons for code manipulation
   - Clear chat and Export options
   - Settings configuration

## Configuration

Click the Settings icon to configure:
- API URL for Ollama
- Model name (default: "qwen2.5-coder:32b")
- Chat history storage location
- Storage type (Session or Disk)

## Code Execution

The tool supports two types of code execution:

### Python Code
- Generated Python code can be executed directly within Houdini
- Supports selection-based execution
- Full access to Houdini Python API (hou)

### VEX Code
- Automatically detects VEX code snippets
- Creates attribute wrangle nodes
- Places nodes in current network context
- Maintains proper node connections

## Chat History

- Conversations are automatically saved
- Choose between session storage or disk storage
- Export conversations to text files
- Sidebar displays previous conversations
- Quick access to past code snippets

## UI Features

- Modern dark theme
- Syntax highlighting for code
- Real-time typing animation for responses
- Status indicators for Ollama connection
- Progress indicators during code generation
- Responsive layout with adjustable panels

## Error Handling

- Comprehensive error messages
- Connection status monitoring
- Safe code execution environment
- Graceful fallback for missing dependencies

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for Houdini's Python Panel system
- Powered by Ollama's AI models
- Uses PySide2 for the user interface
- Inspired by modern AI assistants

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
