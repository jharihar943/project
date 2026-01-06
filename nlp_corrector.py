"""
NLP-Based Error Correction and Language Detection
Uses Natural Language Processing for intelligent code analysis
"""

import re
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher

class NLPErrorCorrector:
    """NLP-based error correction and suggestions"""
    
    # Language patterns for auto-detection
    LANGUAGE_SIGNATURES = {
        'python': {
            'keywords': ['def', 'print', 'import', 'from', 'class', 'elif', 'pass'],
            'patterns': [r'def\s+\w+\(', r'print\(', r':\s*$', r'import\s+\w+'],
            'syntax': [':', 'def', 'import']
        },
        'javascript': {
            'keywords': ['function', 'var', 'let', 'const', 'console', 'return'],
            'patterns': [r'function\s+\w+\(', r'console\.log\(', r'=>', r'{\s*$'],
            'syntax': ['{', '}', 'function', 'var', 'const']
        },
        'cpp': {
            'keywords': ['include', 'cout', 'cin', 'endl', 'namespace', 'using'],
            'patterns': [r'#include', r'cout\s*<<', r'int\s+main\(', r'std::'],
            'syntax': ['#include', '::', 'cout', 'cin', 'endl']
        },
        'java': {
            'keywords': ['public', 'class', 'static', 'void', 'System'],
            'patterns': [r'public\s+class', r'System\.out\.println', r'public\s+static\s+void\s+main'],
            'syntax': ['public', 'class', 'System.out']
        }
    }
    
    # Common error patterns across languages
    ERROR_PATTERNS = [
        {
            'pattern': r'(\w+)\s*=\s*=\s*(\w+)',  # = = instead of ==
            'correction': r'\1 == \2',
            'message': 'Use == for comparison, not = ='
        },
        {
            'pattern': r'if\s+(\w+)\s*=\s*(\w+)',  # = in if condition
            'correction': r'if \1 == \2',
            'message': 'Use == for comparison in conditions, not ='
        },
        {
            'pattern': r'(\w+)\s*===\s*(\w+)',  # === in Python
            'correction': r'\1 == \2',
            'message': 'Python uses == not ==='
        },
    ]
    
    def __init__(self):
        self.detected_language = None
        self.confidence = 0.0
    
    def detect_language(self, code: str) -> Tuple[str, float]:
        """
        Automatically detect programming language using NLP
        Returns: (language_name, confidence_score)
        """
        scores = {}
        
        for lang, signatures in self.LANGUAGE_SIGNATURES.items():
            score = 0.0
            
            # Check keywords
            for keyword in signatures['keywords']:
                if re.search(r'\b' + keyword + r'\b', code):
                    score += 1.5
            
            # Check patterns
            for pattern in signatures['patterns']:
                if re.search(pattern, code, re.MULTILINE):
                    score += 2.0
            
            # Check syntax elements
            for syntax in signatures['syntax']:
                count = code.count(syntax)
                score += count * 0.5
            
            scores[lang] = score
        
        if not scores or max(scores.values()) == 0:
            return 'unknown', 0.0
        
        detected = max(scores.items(), key=lambda x: x[1])
        total_score = sum(scores.values())
        confidence = detected[1] / total_score if total_score > 0 else 0.0
        
        self.detected_language = detected[0]
        self.confidence = confidence
        
        return detected[0], confidence
    
    def correct_syntax_errors(self, code: str, language: str) -> Dict:
        """
        Correct common syntax errors using NLP patterns
        Returns: Dictionary with corrected code and applied fixes
        """
        corrected_code = code
        fixes_applied = []
        
        # Apply error patterns
        for error_pattern in self.ERROR_PATTERNS:
            pattern = error_pattern['pattern']
            correction = error_pattern['correction']
            message = error_pattern['message']
            
            matches = list(re.finditer(pattern, corrected_code))
            if matches:
                corrected_code = re.sub(pattern, correction, corrected_code)
                fixes_applied.append({
                    'type': 'pattern_correction',
                    'message': message,
                    'count': len(matches)
                })
        
        # Language-specific corrections
        if language == 'python':
            corrected_code, python_fixes = self._correct_python_syntax(corrected_code)
            fixes_applied.extend(python_fixes)
        elif language == 'javascript':
            corrected_code, js_fixes = self._correct_javascript_syntax(corrected_code)
            fixes_applied.extend(js_fixes)
        
        return {
            'corrected_code': corrected_code,
            'fixes_applied': fixes_applied,
            'original_code': code
        }
    
    def _correct_python_syntax(self, code: str) -> Tuple[str, List[Dict]]:
        """Python-specific syntax corrections"""
        fixes = []
        corrected = code
        
        # Convert C-style variable declarations (int a=5; float x=3.14; etc.)
        c_style_patterns = [
            (r'\b(int|float|double|long|short|char|bool|string|var)\s+(\w+)\s*=\s*([^;]+);', r'\2 = \3'),
            (r'\b(int|float|double|long|short|char|bool|string|var)\s+(\w+)\s*;', r'\2 = None'),
        ]
        
        for pattern, replacement in c_style_patterns:
            matches = list(re.finditer(pattern, corrected, re.MULTILINE))
            if matches:
                corrected = re.sub(pattern, replacement, corrected, flags=re.MULTILINE)
                fixes.append({
                    'type': 'c_style_declaration',
                    'message': f'Converted {len(matches)} C-style declaration(s) to Python syntax',
                    'count': len(matches)
                })
        
        # Remove trailing semicolons from statements
        lines = corrected.split('\n')
        semicolon_removed = 0
        for i, line in enumerate(lines):
            stripped = line.rstrip()
            if stripped.endswith(';') and not stripped.strip().startswith('#'):
                lines[i] = line.rstrip()[:-1]
                semicolon_removed += 1
        
        if semicolon_removed > 0:
            corrected = '\n'.join(lines)
            fixes.append({
                'type': 'semicolon_removal',
                'message': f'Removed {semicolon_removed} unnecessary semicolon(s)',
                'count': semicolon_removed
            })
        else:
            corrected = '\n'.join(lines)
        
        # Fix missing colons
        lines = corrected.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('if ', 'elif ', 'else', 'for ', 'while ', 'def ', 'class ')):
                if stripped and not stripped.endswith(':'):
                    lines[i] = line + ':'
                    fixes.append({
                        'type': 'missing_colon',
                        'line': i + 1,
                        'message': 'Added missing colon'
                    })
        
        corrected = '\n'.join(lines)
        
        # Fix "then" keyword (doesn't exist in Python)
        if 'then:' in corrected or 'then :' in corrected:
            corrected = re.sub(r'\s+then\s*:', ':', corrected)
            fixes.append({
                'type': 'keyword_correction',
                'message': 'Removed "then" keyword (not used in Python)'
            })
        
        return corrected, fixes
    
    def _correct_javascript_syntax(self, code: str) -> Tuple[str, List[Dict]]:
        """JavaScript-specific syntax corrections"""
        fixes = []
        corrected = code
        
        # No major automated corrections for JS yet
        # Could add semicolon insertion, etc.
        
        return corrected, fixes
    
    def analyze_semantic_similarity(self, code1: str, code2: str) -> float:
        """
        Calculate semantic similarity between two code snippets
        Uses sequence matching algorithm
        """
        return SequenceMatcher(None, code1, code2).ratio()
    
    def suggest_variable_names(self, context: str, current_name: str) -> List[str]:
        """
        Suggest better variable names based on context
        Uses NLP to understand code context
        """
        suggestions = []
        
        # Simple heuristics (could be enhanced with ML models)
        context_lower = context.lower()
        
        if 'count' in context_lower or 'number' in context_lower:
            suggestions.extend(['count', 'num', 'total', 'index'])
        
        if 'name' in context_lower:
            suggestions.extend(['name', 'user_name', 'full_name'])
        
        if 'list' in context_lower or 'array' in context_lower:
            suggestions.extend(['items', 'list_data', 'values', 'elements'])
        
        if 'result' in context_lower:
            suggestions.extend(['result', 'output', 'answer', 'value'])
        
        # Remove duplicates and current name
        suggestions = [s for s in suggestions if s != current_name]
        return list(dict.fromkeys(suggestions))[:5]  # Top 5 unique suggestions
    
    def explain_error(self, error_message: str, code_context: str) -> str:
        """
        Provide human-friendly explanation of error messages
        Uses NLP to make error messages more understandable
        """
        explanations = {
            'syntax error': 'There\'s a mistake in how you wrote the code. Check for missing colons, parentheses, or quotes.',
            'name error': 'You\'re trying to use a variable or function that hasn\'t been defined yet.',
            'type error': 'You\'re trying to perform an operation on the wrong type of data (like adding a number to text).',
            'indentation error': 'Your code indentation is incorrect. Make sure blocks of code are properly indented.',
            'index error': 'You\'re trying to access a position in a list that doesn\'t exist.',
            'key error': 'You\'re trying to access a dictionary key that doesn\'t exist.',
            'value error': 'The value you provided is not valid for this operation.',
            'attribute error': 'The object doesn\'t have the property or method you\'re trying to access.',
        }
        
        error_lower = error_message.lower()
        
        for error_type, explanation in explanations.items():
            if error_type in error_lower:
                return f"💡 {explanation}\n\nOriginal error: {error_message}"
        
        return f"Error: {error_message}"
    
    def generate_code_documentation(self, code: str, language: str) -> Dict:
        """
        Auto-generate documentation for code using NLP
        Analyzes code structure and generates descriptions
        """
        doc = {
            'summary': '',
            'functions': [],
            'variables': [],
            'complexity': 'simple'
        }
        
        lines = code.split('\n')
        
        # Detect functions
        if language == 'python':
            for line in lines:
                if line.strip().startswith('def '):
                    match = re.search(r'def\s+(\w+)\s*\((.*?)\)', line)
                    if match:
                        func_name = match.group(1)
                        params = match.group(2)
                        doc['functions'].append({
                            'name': func_name,
                            'parameters': params,
                            'description': f'Function: {func_name}'
                        })
        
        # Estimate complexity
        if len(lines) < 10:
            doc['complexity'] = 'simple'
        elif len(lines) < 50:
            doc['complexity'] = 'moderate'
        else:
            doc['complexity'] = 'complex'
        
        doc['summary'] = f"{language.title()} code with {len(doc['functions'])} functions"
        
        return doc
