# 🌐 Advanced SpeechToTxt Translator
![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Python](https://img.shields.io/badge/Python-0078D4?logo=python&logoColor=white)
![streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?&logo=streamlit&logoColor=white)
![terminal](https://img.shields.io/badge/Windows%20Terminal-4D4D4D?&logo=Windows%20terminal&logoColor=white)
![vscode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?&logo=visual%20studio%20code&logoColor=white)

A powerful language translation tool built with Streamlit, featuring real-time translation, audio output, and language detection.

## ✨ Features

- Real-time language detection
- Support for 100+ languages
- Text-to-speech output
- Bulk text translation
- Translation history
- Copy-to-clipboard functionality
- Dark/Light mode support
- Mobile-responsive design

## 🛠️ Technologies Used

- Python 3.8+
- Streamlit
- googletrans 3.1.0a0
- gTTS (Google Text-to-Speech)
- playsound
- clipboard
- language_detector

## 🚀 Quick Installation

```bash
# Clone repository
git clone https://github.com/yourusername/advanced-streamlit-translator.git

# Navigate to directory
cd advanced-streamlit-translator

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## 📦 Requirements
```txt
streamlit==1.24.0
googletrans==3.1.0a0
gTTS==2.3.2
playsound==1.3.0
clipboard==0.0.4
language_detector==1.1.0
```

## 💡 Usage

1. Select source language (or use auto-detect)
2. Choose target language
3. Enter or paste your text
4. Click "Translate" or enable auto-translation
5. Use the audio button to hear pronunciation
6. Copy translated text with one click

## 🎯 Key Functions

```python
# Language detection
def detect_language(text):
    try:
        return translator.detect(text).lang
    except:
        return "en"

# Text translation
def translate_text(text, target_lang):
    try:
        return translator.translate(text, dest=target_lang).text
    except:
        return "Translation error. Please try again."

# Text to speech
def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("temp.mp3")
        return True
    except:
        return False
```

## 🎨 UI Features

- Clean, modern interface
- Language selection dropdowns
- Auto-detection toggle
- Character count display
- Translation history sidebar
- Audio playback controls
- Copy/paste buttons
- Progress indicators

## 🔧 Configuration

```python
# config.py
STREAMLIT_CONFIG = {
    "theme": {
        "primaryColor": "#FF4B4B",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif",
    },
    "server": {
        "port": 8501,
        "address": "localhost"
    }
}
```

## 📝 Future Enhancements

- OCR integration for image translation
- API endpoint for programmatic access
- Offline translation support
- Custom voice selection
- Translation memory for frequent phrases
- Batch file translation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 📞 Support

- GitHub Issues
- Email: piyushaundhekar@gmail.com

