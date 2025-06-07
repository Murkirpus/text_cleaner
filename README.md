# 📝 Text Cleaner - Non-Standard Character Highlighter

**A simple yet powerful text editor for detecting and replacing non-standard characters in text.**

This program is especially useful when working with text copied from ChatGPT, web pages, and other sources that often contain invisible or problematic characters.

## 🎯 Key Features

- 🔍 **Non-standard character highlighting** - 4 types of color highlighting
- 🔧 **Automatic replacement** of suspicious characters with standard equivalents
- 📊 **Text analysis** with detailed statistics
- 💾 **File operations** - open and save in various formats
- 🖱️ **Context menu** with full set of functions
- ⌨️ **Hotkeys** for quick operations
- 🎨 **User-friendly interface** with toolbar

## 🚀 Quick Start

### Requirements
- Python 3.7+
- tkinter (usually included with Python)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Murkirpus/text-cleaner.git
cd text-cleaner
```

2. **Run the program:**
```bash
python text_cleaner.py
```

### Alternative Installation (exe file)

Download the ready-to-use exe file from [releases](https://github.com/Murkirpus/text-cleaner/releases) and run without installing Python.

## 📋 What the program can fix

### 🔴 Invisible characters
- Zero-width spaces
- Text direction control characters
- Combining characters
- Line and paragraph separators

### 🟡 Similar characters  
- Cyrillic letters that look like Latin (а→a, е→e, о→o)
- Special quotes (" " → " ")
- Various types of dashes (— – → -)

### 🔵 Special spaces
- Non-breaking spaces
- Narrow spaces  
- Em/En spaces
- Ideographic spaces

### 🟣 Other characters
- Mathematical symbols (≤ → <=, ∞ → inf)
- Greek letters (π → pi, α → alpha)  
- Fractions (½ → 1/2, ¾ → 3/4)
- Arrows (→ → ->, ← → <-)
- Currency symbols (€ → EUR, £ → GBP)

## 🎮 How to Use

### Basic Functions

1. **Paste text** into the editor window
2. **Non-standard characters** will be automatically highlighted in different colors
3. **Click "Fix ALL"** to replace all problematic characters
4. **Use context menu** (right-click) for additional functions

### Hotkeys

| Combination | Action |
|-------------|--------|
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `Ctrl+X` | Cut |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select all |

### Toolbar

- **Highlight** - find and highlight all non-standard characters
- **Clear** - remove highlighting
- **Replace spaces** - replace only non-standard spaces
- **Fix ALL** - replace all suspicious characters
- **Auto-highlight** - automatically highlight when text changes

## 🛠️ Building exe file

To create a standalone exe file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build exe file
pyinstaller --onefile --windowed --name="TextCleaner" text_cleaner.py
```

The ready file will appear in the `dist/` folder

## 🤝 Contributing

I welcome any improvements! To contribute:

1. Fork the repository
2. Create a branch for your changes (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## 📝 Changelog

### v1.0.0 (2025-01-XX)
- ✨ First release
- 🔍 Highlighting of 4 types of non-standard characters
- 🔧 Automatic replacement of 200+ characters
- 📊 Selected text analysis
- 🖱️ Context menu
- 💾 File operations

## 🐛 Report a Bug

If you found a bug or have a suggestion:

1. Check [existing issues](https://github.com/Murkirpus/text-cleaner/issues)
2. Create a [new issue](https://github.com/Murkirpus/text-cleaner/issues/new) with detailed description

## 📄 License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Vitaliy Litvinov**
- Email: murkir@gmail.com
- GitHub: [@Murkirpus](https://github.com/Murkirpus)

## 🙏 Acknowledgments

- Python community for excellent libraries
- Everyone who tested the program and provided feedback

---

⭐ **Like the project? Give it a star!** ⭐
