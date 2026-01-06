# AI/ML-Powered Multi-Language Compiler

An intelligent compiler design that combines traditional compilation phases with **AI/ML enhancements** for error detection, syntax correction, and code optimization.

![InvitiQ Compiler](https://img.shields.io/badge/InvitiQ-Compiler-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![AI/ML](https://img.shields.io/badge/AI%2FML-Powered-orange)
![Languages](https://img.shields.io/badge/Languages-10-brightgreen)

## 🎯 Overview

This project implements a **multi-language compiler** supporting **10 programming languages** with AI/ML enhancements:

### Supported Languages
- **Python** - Dynamic scripting with comprehensive standard library
- **Java** - Object-oriented with strong type system
- **C** - Low-level systems programming with GCC
- **C++** - Object-oriented systems programming with G++
- **JavaScript** - Dynamic web scripting (client-side execution)
- **Go** - Modern systems programming with concurrency
- **PHP** - Server-side scripting for web development
- **TypeScript** - JavaScript with static typing
- **SQL** - Database query language
- **R** - Statistical computing and graphics

### Key Features
- **Intelligent error detection and suggestions**
- **NLP-based syntax correction**
- **Interactive input support** for all languages
- **Real-time syntax highlighting** with keyword recognition
- **ML-driven code optimization**
- **Common intermediate representation (IR)**
- **Human-friendly error explanations**
- **Web-based IDE** with InvitiQ branding

## 🏗️ Architecture

### Traditional Compiler Phases Enhanced with AI/ML

```
┌─────────────────────────────────────────────────────┐
│           MULTI-LANGUAGE FRONTEND                   │
│  Python | JavaScript | C++ | Java (Extensible)     │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────▼─────────┐
        │  NLP Corrector   │ ← AI: Language Detection
        │  Auto-fix Syntax │ ← AI: Pattern Matching
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  Lexer (Tokens)  │ ← AI: Typo Detection
        │  + Error Handler │ ← AI: Smart Suggestions
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Intermediate Rep │ ← Common IR for all languages
        │   (IR Generator) │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  IR Optimizer    │ ← ML: Optimization Strategies
        │  (AI/ML Based)   │ ← ML: Instruction Ordering
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  Code Generator  │
        │  (Backend)       │
        └──────────────────┘
```

## 🚀 Features

### 1. **AI-Powered Error Detection**
- Detects syntax errors with context-aware suggestions
- Identifies common typos in keywords
- Provides human-friendly error explanations

### 2. **NLP-Based Corrections**
- Automatic language detection (Python, JavaScript, C++, Java)
- Pattern-based syntax fixing
- Intelligent code completion suggestions

### 3. **Intermediate Representation**
- Language-agnostic IR
- Easy to add new languages
- Optimized for analysis

### 4. **ML-Driven Optimization**
- Dead code elimination
- Constant propagation
- Common subexpression elimination
- Instruction reordering

### 5. **Multi-Language Support**
- Python
- JavaScript
- C++
- Easily extensible for more languages

## 📁 Project Structure

```
COMPILER DESIGN/
├── api_server.py              # Flask REST API backend
├── compiler.py                # Main compiler engine
├── lexer.py                   # Lexical analyzer with AI
├── ai_error_handler.py        # AI/ML error detection
├── nlp_corrector.py           # NLP-based corrections
├── intermediate_representation.py  # IR generator & optimizer
├── index.html                 # Web interface
├── style.css                  # UI styling
├── script.js                  # Frontend logic
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Modern web browser

### Setup Steps

1. **Clone or download the project**

2. **Install Python dependencies**
```bash
cd "COMPILER DESIGN"
pip install -r requirements.txt
```

3. **Start the backend server**
```bash
python api_server.py
```
The API server will start at `http://localhost:5000`

4. **Open the web interface**
   - Open `index.html` in your web browser
   - Or use a local server:
```bash
# Using Python
python -m http.server 8000
# Then open http://localhost:8000
```

## 📖 Usage

### Web Interface

1. **Select Language**: Click "Language" button to choose Python, JavaScript, or C++
2. **Write Code**: Enter your code in the editor
3. **Run**: Click "Run ▶" button or press `Ctrl+Enter`
4. **View Results**: See compilation results with:
   - Error detection and suggestions
   - Auto-applied fixes
   - Optimization reports
   - AI recommendations

### API Usage

```python
import requests

# Compile code
response = requests.post('http://localhost:5000/api/compile', json={
    'code': 'print("Hello World")',
    'language': 'python',
    'auto_detect': True
})

result = response.json()
print(result['explanation'])
```

### Python Library Usage

```python
from compiler import AIMLCompiler

# Create compiler instance
compiler = AIMLCompiler('python')

# Compile code
source_code = """
def greet(name):
    print(f"Hello {name}")

greet("InvitiQ")
"""

result = compiler.compile(source_code)

# Get explanation
print(compiler.explain_compilation(result))

# Check success
if result['success']:
    print("✓ Compilation successful!")
    print("\nOptimized IR:")
    print(result['optimized_ir'])
```

## 🔬 AI/ML Techniques Used

### 1. **Natural Language Processing (NLP)**
- Language pattern recognition
- Similarity matching for typo detection
- Context-aware error messages

### 2. **Machine Learning Concepts**
- Classification for language detection
- Pattern matching for error prediction
- Heuristic-based optimization

### 3. **Rule-Based AI**
- Expert system for error suggestions
- Pattern recognition for syntax fixing
- Knowledge base for common mistakes

## 📊 Example Output

```
=== AI/ML Compiler Analysis ===

✓ Detected language: PYTHON (confidence: 95.3%)

✓ Applied 2 automatic fixes:
  • Added missing colon
  • Removed "then" keyword (not used in Python)

💡 AI Suggestions (1):
  • Use more descriptive variable names

🚀 Optimizations: 3 applied
   Estimated improvement: 15-30% faster execution

✓ Compilation successful! Code is ready to execute.
```

## 🎓 Educational Value

This project demonstrates:

1. **Compiler Design Phases**
   - Lexical Analysis
   - Syntax Analysis (simplified)
   - Semantic Analysis
   - IR Generation
   - Optimization
   - Code Generation

2. **AI/ML Integration**
   - Error prediction
   - Pattern recognition
   - Intelligent suggestions
   - Auto-correction

3. **Software Engineering**
   - Modular architecture
   - REST API design
   - Frontend-backend integration
   - Error handling

## 🚧 Future Enhancements

- [ ] Support for more languages (Java, Go, Rust)
- [ ] Advanced ML-based optimization using trained models
- [ ] Natural language to code conversion
- [ ] Real-time collaborative editing
- [ ] Code quality metrics
- [ ] Performance profiling
- [ ] Self-learning from user corrections

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| AI/ML | scikit-learn, NLTK, difflib |
| Frontend | HTML5, CSS3, JavaScript |
| API | REST (JSON) |
| Compiler | Custom lexer, IR generator |

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/compile` | POST | Compile code with AI enhancements |
| `/api/detect-language` | POST | Auto-detect programming language |
| `/api/correct-syntax` | POST | Auto-correct syntax errors |
| `/api/explain-error` | POST | Get human-friendly error explanation |
| `/api/analyze` | POST | Comprehensive code analysis |
| `/api/health` | GET | Health check |

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Implement more ML-based optimizations
- Enhance error detection accuracy
- Improve UI/UX with themes
- Add unit tests and CI/CD
- Add code completion and IntelliSense
- Implement code formatting and linting

## 🌟 Language-Specific Features

### Go
- **Interactive Input**: `fmt.Scan()`, `fmt.Scanf()`, `fmt.Scanln()`
- **Syntax Highlighting**: Keywords, types, functions, built-ins
- **Error Detection**: Compile-time errors with line numbers
- **Features**: Goroutines, channels, defer statements
- **Standard Library**: Full fmt package support

### PHP
- **Interactive Input**: `fgets(STDIN)`, `readline()`, `trim()`
- **Syntax Highlighting**: Keywords, variables ($), functions, built-ins
- **Comment Support**: //, /* */, and # comments
- **Features**: OOP, namespaces, traits
- **Functions**: echo, print, include, require support

### TypeScript
- **Type System**: Interfaces, types, enums, generics
- **Syntax Highlighting**: TypeScript-specific keywords
- **Compilation**: Transpiles to JavaScript via tsc
- **Execution**: Runs compiled JS with Node.js
- **Features**: Abstract classes, decorators, type guards
- **Modern JS**: Full ES6+ support with type safety

## 📊 Input Detection Matrix

| Language | Input Methods | Format | Example |
|----------|--------------|--------|---------|
| Python | `input()` | String | `name = input("Enter name: ")` |
| Java | Scanner methods | Typed | `int n = sc.nextInt();` |
| C | `scanf()` | Format specifiers | `scanf("%d %f", &a, &b);` |
| C++ | `cin >>`, `getline()` | Stream | `cin >> x; getline(cin, s);` |
| JavaScript | `prompt()` | String | `let name = prompt("Name:");` |
| Go | `fmt.Scan()` | Pointers | `fmt.Scan(&a, &b)` |
| PHP | `fgets(STDIN)` | String | `$name = trim(fgets(STDIN));` |
| TypeScript | readlineSync | String | `const x = readlineSync.question("Enter:");` |

## 📄 License

This project is created for educational purposes.

## 👥 Authors

**InvitiQ Team**
- *"Where Users Meet, You Learn"*

## 🙏 Acknowledgments

- Traditional compiler design principles
- Modern AI/ML techniques
- Open-source community

## 📞 Support

For questions or issues:
1. Check the documentation
2. Review error messages carefully
3. Use the AI suggestions provided

---

**Made with ❤️ by InvitiQ**

*Combining Traditional Compiler Design with Modern AI/ML*
#   p r o j e c t  
 #   p r o j e c t  
 #   p r o j e c t  
 