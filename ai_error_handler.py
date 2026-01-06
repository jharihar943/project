"""
AI/ML Error Handler and Suggestion Engine
Provides intelligent error detection, correction, and suggestions
"""

import difflib
from typing import List, Dict, Optional
import re

class AIErrorHandler:
    """AI-powered error detection and suggestion system"""
    
    # Common programming mistakes and their fixes
    COMMON_ERRORS = {
        'python': {
            'sintax error': 'syntax error',
            'prit': 'print',
            'retrun': 'return',
            'dif': 'def',
            'calss': 'class',
            'improt': 'import',
            'form': 'from',
            'elseif': 'elif',
            'whlie': 'while',
            'braek': 'break',
            'contineu': 'continue',
        },
        'javascript': {
            'functino': 'function',
            'vra': 'var',
            'cosnt': 'const',
            'consol': 'console',
            'retrn': 'return',
            'tru': 'true',
            'flase': 'false',
        },
        'cpp': {
            'inclde': 'include',
            'inlcude': 'include',
            'cot': 'cout',
            'cint': 'cin',
            'enld': 'endl',
            'reutrn': 'return',
            'voiad': 'void',
        }
    }
    
    # Syntax pattern corrections
    SYNTAX_PATTERNS = {
        'python': [
            {
                'pattern': r'if\s+(.+)\s+then:',
                'correction': r'if \1:',
                'message': 'Python uses "if condition:" without "then"'
            },
            {
                'pattern': r'function\s+(\w+)\s*\(',
                'correction': r'def \1(',
                'message': 'Python uses "def" instead of "function"'
            },
            {
                'pattern': r'(\w+)\s*{\s*$',
                'correction': r'\1:',
                'message': 'Python uses colons (:) not braces ({})'
            },
        ],
        'javascript': [
            {
                'pattern': r'def\s+(\w+)\s*\(',
                'correction': r'function \1(',
                'message': 'JavaScript uses "function" instead of "def"'
            },
        ]
    }
    
    def __init__(self, language: str = 'python'):
        self.language = language.lower()
        self.error_history: List[Dict] = []
    
    def analyze_errors(self, code: str, tokens: List, lexer_errors: List[dict]) -> Dict:
        """
        Comprehensive error analysis with AI-enhanced suggestions
        Returns: Dictionary with errors, warnings, and suggestions
        """
        result = {
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'fixed_code': code
        }
        
        # Analyze lexer errors
        for error in lexer_errors:
            enhanced_error = self._enhance_error(error, code)
            if enhanced_error['severity'] == 'error':
                result['errors'].append(enhanced_error)
            else:
                result['warnings'].append(enhanced_error)
        
        # Check for common syntax patterns
        syntax_fixes = self._check_syntax_patterns(code)
        if syntax_fixes:
            result['suggestions'].extend(syntax_fixes['suggestions'])
            result['fixed_code'] = syntax_fixes['fixed_code']
        
        # Check for common typos
        typo_fixes = self._check_common_typos(code)
        if typo_fixes:
            result['suggestions'].extend(typo_fixes)
        
        # Analyze structural issues
        structural_issues = self._analyze_structure(code)
        result['warnings'].extend(structural_issues)
        
        return result
    
    def _enhance_error(self, error: dict, code: str) -> dict:
        """Enhance error message with AI suggestions"""
        enhanced = error.copy()
        
        # Add context from code
        lines = code.split('\n')
        if 0 <= error['line'] - 1 < len(lines):
            enhanced['code_line'] = lines[error['line'] - 1]
        
        # Use ML-based similarity to find better suggestions
        if 'suggestion' not in enhanced or not enhanced['suggestion']:
            enhanced['suggestion'] = self._generate_smart_suggestion(error, code)
        
        # Add fix action if possible
        enhanced['fix_action'] = self._get_fix_action(enhanced)
        
        return enhanced
    
    def _generate_smart_suggestion(self, error: dict, code: str) -> str:
        """Generate intelligent suggestions using pattern matching and ML"""
        message = error.get('message', '').lower()
        
        # Common error patterns and suggestions
        if 'unexpected character' in message:
            return self._suggest_character_fix(error)
        elif 'unterminated string' in message:
            return 'Add a closing quote to complete the string'
        elif 'typo' in message:
            return error.get('suggestion', 'Check spelling')
        elif 'undefined' in message or 'not defined' in message:
            return 'Variable or function not defined. Check spelling or declare it first'
        
        return 'Review syntax and try running again'
    
    def _suggest_character_fix(self, error: dict) -> str:
        """Suggest fixes for unexpected characters"""
        char = error.get('message', '').split("'")
        if len(char) >= 2:
            problem_char = char[1]
            
            suggestions_map = {
                '@': 'Remove @ or use it for decorators in Python',
                '$': 'Remove $ (not used in Python variable names)',
                '`': 'Use " or \' for strings instead of `',
                '^': 'Use ** for exponentiation in Python',
                '&': 'Use "and" for logical operations in Python',
                '|': 'Use "or" for logical operations in Python',
            }
            
            return suggestions_map.get(problem_char, 'Remove or replace this character')
        
        return 'Check for invalid characters'
    
    def _check_syntax_patterns(self, code: str) -> Optional[Dict]:
        """Check for language-specific syntax patterns"""
        patterns = self.SYNTAX_PATTERNS.get(self.language, [])
        suggestions = []
        fixed_code = code
        
        for pattern_info in patterns:
            pattern = pattern_info['pattern']
            correction = pattern_info['correction']
            message = pattern_info['message']
            
            if re.search(pattern, code):
                suggestions.append({
                    'type': 'syntax_pattern',
                    'message': message,
                    'fix': f'Change pattern to: {correction}'
                })
                fixed_code = re.sub(pattern, correction, fixed_code)
        
        if suggestions:
            return {
                'suggestions': suggestions,
                'fixed_code': fixed_code
            }
        
        return None
    
    def _check_common_typos(self, code: str) -> List[Dict]:
        """Check for common typos in keywords"""
        typos = self.COMMON_ERRORS.get(self.language, {})
        suggestions = []
        
        for typo, correct in typos.items():
            if re.search(r'\b' + typo + r'\b', code):
                suggestions.append({
                    'type': 'typo',
                    'message': f"Possible typo: '{typo}' should be '{correct}'",
                    'fix': f'Replace "{typo}" with "{correct}"'
                })
        
        return suggestions
    
    def _analyze_structure(self, code: str) -> List[Dict]:
        """Analyze code structure for potential issues"""
        warnings = []
        lines = code.split('\n')
        
        # Check for common structural issues
        if self.language == 'python':
            # Check indentation
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.startswith((' ', '\t')):
                    if i > 1 and lines[i-2].rstrip().endswith(':'):
                        warnings.append({
                            'line': i,
                            'type': 'indentation',
                            'message': 'Expected indentation after colon',
                            'severity': 'warning'
                        })
            
            # Check for missing colons
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith(('if ', 'elif ', 'else', 'for ', 'while ', 'def ', 'class ')):
                    if not stripped.endswith(':'):
                        warnings.append({
                            'line': i,
                            'type': 'missing_colon',
                            'message': 'Missing colon at end of statement',
                            'severity': 'error'
                        })
        
        return warnings
    
    def _get_fix_action(self, error: dict) -> Optional[str]:
        """Get automated fix action for error"""
        if error.get('type') == 'typo':
            return 'auto_correct'
        elif error.get('type') == 'missing_colon':
            return 'add_colon'
        elif error.get('type') == 'indentation':
            return 'fix_indentation'
        
        return None
    
    def apply_auto_fix(self, code: str, error: dict) -> str:
        """Apply automatic fix to code"""
        fix_action = error.get('fix_action')
        
        if fix_action == 'auto_correct' and 'typo' in error.get('type', ''):
            # Extract typo and correction from message
            message = error.get('message', '')
            # Apply correction
            # This is a simplified version
            return code
        
        elif fix_action == 'add_colon':
            lines = code.split('\n')
            line_num = error.get('line', 0) - 1
            if 0 <= line_num < len(lines):
                lines[line_num] = lines[line_num].rstrip() + ':'
                return '\n'.join(lines)
        
        return code
    
    def get_learning_insights(self) -> Dict:
        """Provide learning insights based on error history"""
        if not self.error_history:
            return {'message': 'No errors yet. Keep coding!'}
        
        # Analyze common error types
        error_types = {}
        for error in self.error_history:
            error_type = error.get('type', 'unknown')
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        most_common = max(error_types.items(), key=lambda x: x[1])
        
        return {
            'total_errors': len(self.error_history),
            'most_common_error': most_common[0],
            'suggestion': f'Focus on improving: {most_common[0]}',
            'error_breakdown': error_types
        }
