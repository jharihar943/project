"""
Main Compiler Engine
Integrates all components: Lexer, Parser, IR Generator, AI/ML Error Handler
"""

from lexer import Lexer, Token
from ai_error_handler import AIErrorHandler
from nlp_corrector import NLPErrorCorrector
from intermediate_representation import IRGenerator, IROptimizer
from typing import Dict, List
import json

class AIMLCompiler:
    """
    AI/ML-Powered Multi-Language Compiler
    Combines traditional compiler phases with AI/ML enhancements
    """
    
    def __init__(self, language: str = 'python'):
        self.language = language
        self.lexer = None
        self.error_handler = AIErrorHandler(language)
        self.nlp_corrector = NLPErrorCorrector()
        self.ir_generator = IRGenerator()
        self.ir_optimizer = IROptimizer()
        self.compilation_stats = {}
    
    def compile(self, source_code: str, auto_detect_language: bool = True) -> Dict:
        """
        Main compilation pipeline with AI/ML enhancements
        
        Returns comprehensive compilation result with:
        - Tokens
        - Errors and warnings
        - AI suggestions
        - Intermediate representation
        - Optimizations applied
        - Execution ready code
        """
        result = {
            'success': False,
            'language': self.language,
            'tokens': [],
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'ir_code': '',
            'optimized_ir': '',
            'corrected_code': source_code,
            'stats': {}
        }
        
        try:
            # Phase 1: Language Detection (AI-powered)
            if auto_detect_language:
                detected_lang, confidence = self.nlp_corrector.detect_language(source_code)
                if confidence > 0.5:
                    self.language = detected_lang
                    result['language'] = detected_lang
                    result['language_confidence'] = f"{confidence * 100:.1f}%"
            
            # Phase 2: NLP-based syntax correction
            correction_result = self.nlp_corrector.correct_syntax_errors(
                source_code, 
                self.language
            )
            
            if correction_result['fixes_applied']:
                result['corrected_code'] = correction_result['corrected_code']
                result['auto_fixes'] = correction_result['fixes_applied']
                source_code = correction_result['corrected_code']  # Use corrected code
            
            # Phase 3: Lexical Analysis
            self.lexer = Lexer(source_code, self.language)
            tokens, lexer_errors = self.lexer.tokenize()
            result['tokens'] = [self._token_to_dict(t) for t in tokens]
            
            # Phase 4: AI-Enhanced Error Analysis
            error_analysis = self.error_handler.analyze_errors(
                source_code, 
                tokens, 
                lexer_errors
            )
            
            result['errors'] = error_analysis['errors']
            result['warnings'] = error_analysis['warnings']
            result['suggestions'] = error_analysis['suggestions']
            
            if error_analysis['fixed_code'] != source_code:
                result['ai_suggested_code'] = error_analysis['fixed_code']
            
            # Phase 5: Intermediate Representation Generation
            ir_instructions = self.ir_generator.generate_from_tokens(tokens)
            result['ir_code'] = self.ir_generator.get_ir_code()
            
            # Phase 6: ML-Based Optimization
            optimized_ir = self.ir_optimizer.optimize_ir(ir_instructions)
            self.ir_generator.instructions = optimized_ir
            result['optimized_ir'] = self.ir_generator.get_ir_code()
            result['optimization_report'] = self.ir_optimizer.get_optimization_report()
            
            # Phase 7: Generate execution code (simplified)
            if not result['errors'] or all(e.get('severity') != 'error' for e in result['errors']):
                result['success'] = True
                result['executable_code'] = self._generate_executable(optimized_ir)
            
            # Compilation Statistics
            result['stats'] = {
                'tokens_count': len(tokens),
                'errors_count': len([e for e in result['errors'] if e.get('severity') == 'error']),
                'warnings_count': len(result['warnings']),
                'suggestions_count': len(result['suggestions']),
                'ir_instructions': len(ir_instructions),
                'optimized_instructions': len(optimized_ir)
            }
            
        except Exception as e:
            result['errors'].append({
                'type': 'compiler_error',
                'message': f'Compiler internal error: {str(e)}',
                'severity': 'critical'
            })
        
        return result
    
    def _token_to_dict(self, token: Token) -> Dict:
        """Convert Token object to dictionary"""
        return {
            'type': token.type.name,
            'value': token.value,
            'line': token.line,
            'column': token.column
        }
    
    def _generate_executable(self, ir_instructions: List) -> str:
        """
        Generate executable code from optimized IR
        This is a simplified version - full implementation would
        generate actual machine code or bytecode
        """
        lines = []
        lines.append("# Generated executable code")
        lines.append("# Optimized by AI/ML Compiler")
        lines.append("")
        
        for instr in ir_instructions:
            if instr.opcode.name == 'PRINT':
                lines.append(f"print({instr.operands[0]})")
            elif instr.opcode.name == 'STORE':
                lines.append(f"{instr.result} = {instr.operands[0]}")
            elif instr.opcode.name == 'FUNC_BEGIN':
                lines.append(f"def {instr.operands[0]}():")
            elif instr.opcode.name == 'RETURN':
                lines.append(f"    return {instr.operands[0]}")
        
        return '\n'.join(lines)
    
    def explain_compilation(self, result: Dict) -> str:
        """
        Generate human-friendly explanation of compilation process
        Uses NLP to create understandable descriptions
        """
        explanation = []
        
        explanation.append("=== AI/ML Compiler Analysis ===\n")
        
        # Language detection
        if 'language_confidence' in result:
            explanation.append(f"✓ Detected language: {result['language'].upper()} "
                             f"(confidence: {result['language_confidence']})")
        
        # Auto-fixes
        if 'auto_fixes' in result and result['auto_fixes']:
            explanation.append(f"\n✓ Applied {len(result['auto_fixes'])} automatic fixes:")
            for fix in result['auto_fixes']:
                explanation.append(f"  • {fix['message']}")
        
        # Errors
        if result['errors']:
            explanation.append(f"\n✗ Found {len(result['errors'])} errors:")
            for error in result['errors'][:3]:  # Show first 3
                msg = error.get('message', 'Unknown error')
                suggestion = error.get('suggestion', '')
                explanation.append(f"  • {msg}")
                if suggestion:
                    explanation.append(f"    💡 {suggestion}")
        
        # Warnings
        if result['warnings']:
            explanation.append(f"\n⚠ {len(result['warnings'])} warnings:")
            for warning in result['warnings'][:3]:
                explanation.append(f"  • {warning.get('message', 'Unknown warning')}")
        
        # Suggestions
        if result['suggestions']:
            explanation.append(f"\n💡 AI Suggestions ({len(result['suggestions'])}):")
            for suggestion in result['suggestions'][:3]:
                explanation.append(f"  • {suggestion.get('message', suggestion)}")
        
        # Optimization
        if 'optimization_report' in result:
            opt_report = result['optimization_report']
            explanation.append(f"\n🚀 Optimizations: {opt_report.get('optimizations_applied', 0)} applied")
            explanation.append(f"   Estimated improvement: {opt_report.get('estimated_improvement', 'N/A')}")
        
        # Success
        if result['success']:
            explanation.append("\n✓ Compilation successful! Code is ready to execute.")
        else:
            explanation.append("\n✗ Compilation failed. Please fix errors above.")
        
        return '\n'.join(explanation)
    
    def get_learning_insights(self) -> Dict:
        """Provide learning insights based on compilation history"""
        return self.error_handler.get_learning_insights()

# Convenience function
def compile_code(source_code: str, language: str = 'python') -> Dict:
    """
    Quick compilation function
    
    Usage:
        result = compile_code("print('Hello')", "python")
        print(result['success'])
    """
    compiler = AIMLCompiler(language)
    return compiler.compile(source_code)

# Example usage
if __name__ == "__main__":
    # Test code
    test_code = """
def greet(name):
    print("Hello " + name)
    return True

greet("InvitiQ")
    """
    
    compiler = AIMLCompiler('python')
    result = compiler.compile(test_code)
    
    print(compiler.explain_compilation(result))
    print("\n" + "="*50)
    print("\nIntermediate Representation:")
    print(result['ir_code'])
    
    if result['success']:
        print("\n" + "="*50)
        print("\nOptimized IR:")
        print(result['optimized_ir'])
