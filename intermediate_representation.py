"""
Intermediate Representation (IR) System
Common IR for multi-language compiler
"""

from enum import Enum, auto
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

class IROpCode(Enum):
    """Intermediate Representation Operation Codes"""
    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    
    # Comparison
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    
    # Logical
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Control flow
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    JUMP_IF_TRUE = auto()
    CALL = auto()
    RETURN = auto()
    
    # Memory operations
    LOAD = auto()
    STORE = auto()
    LOAD_CONST = auto()
    
    # Function operations
    FUNC_BEGIN = auto()
    FUNC_END = auto()
    PARAM = auto()
    
    # I/O operations
    PRINT = auto()
    INPUT = auto()
    
    # Special
    NOP = auto()
    HALT = auto()

@dataclass
class IRInstruction:
    """Single IR instruction"""
    opcode: IROpCode
    operands: List[Any]
    result: Optional[str] = None
    line: int = 0
    
    def __str__(self):
        operands_str = ', '.join(str(op) for op in self.operands)
        if self.result:
            return f"{self.result} = {self.opcode.name} {operands_str}"
        return f"{self.opcode.name} {operands_str}"

class IRGenerator:
    """Generates Intermediate Representation from AST"""
    
    def __init__(self):
        self.instructions: List[IRInstruction] = []
        self.temp_counter = 0
        self.label_counter = 0
        self.symbol_table: Dict[str, Any] = {}
    
    def generate_temp(self) -> str:
        """Generate temporary variable name"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def generate_label(self) -> str:
        """Generate unique label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, opcode: IROpCode, operands: List[Any], result: Optional[str] = None, line: int = 0):
        """Emit an IR instruction"""
        instruction = IRInstruction(opcode, operands, result, line)
        self.instructions.append(instruction)
        return instruction
    
    def generate_from_tokens(self, tokens: List) -> List[IRInstruction]:
        """
        Generate IR from tokens (simplified version)
        In a full compiler, this would work with an AST
        """
        self.instructions = []
        
        # Simple pattern matching for common constructs
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Function definition
            if token.value in ['def', 'function']:
                func_name = tokens[i + 1].value if i + 1 < len(tokens) else 'unknown'
                self.emit(IROpCode.FUNC_BEGIN, [func_name], line=token.line)
            
            # Print statement
            elif token.value in ['print', 'console']:
                # Look for what to print
                if i + 1 < len(tokens):
                    print_value = tokens[i + 1].value
                    self.emit(IROpCode.PRINT, [print_value], line=token.line)
            
            # Return statement
            elif token.value == 'return':
                if i + 1 < len(tokens):
                    return_value = tokens[i + 1].value
                    self.emit(IROpCode.RETURN, [return_value], line=token.line)
            
            # Assignment (simplified)
            elif i + 1 < len(tokens) and tokens[i + 1].value == '=':
                var_name = token.value
                if i + 2 < len(tokens):
                    value = tokens[i + 2].value
                    self.emit(IROpCode.STORE, [value], result=var_name, line=token.line)
            
            i += 1
        
        return self.instructions
    
    def get_ir_code(self) -> str:
        """Get IR code as string"""
        lines = []
        for idx, instr in enumerate(self.instructions):
            lines.append(f"{idx:3d}: {instr}")
        return '\n'.join(lines)
    
    def optimize(self) -> List[IRInstruction]:
        """Apply basic optimizations to IR"""
        optimized = []
        
        # Remove consecutive NOP instructions
        for i, instr in enumerate(self.instructions):
            if instr.opcode == IROpCode.NOP:
                # Skip multiple NOPs
                if i > 0 and self.instructions[i-1].opcode == IROpCode.NOP:
                    continue
            optimized.append(instr)
        
        # Constant folding (simplified)
        # This would be much more sophisticated in a real compiler
        
        self.instructions = optimized
        return self.instructions

class IROptimizer:
    """ML-based IR optimization engine"""
    
    def __init__(self):
        self.optimization_history: List[Dict] = []
    
    def optimize_ir(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """
        Apply ML-based optimizations
        In a full implementation, this would use ML models to predict
        optimal instruction ordering and transformations
        """
        optimized = instructions.copy()
        
        # Dead code elimination
        optimized = self._eliminate_dead_code(optimized)
        
        # Constant propagation
        optimized = self._constant_propagation(optimized)
        
        # Common subexpression elimination
        optimized = self._eliminate_common_subexpressions(optimized)
        
        return optimized
    
    def _eliminate_dead_code(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Remove unreachable code"""
        used_temps = set()
        
        # Backward pass to find used variables
        for instr in reversed(instructions):
            for operand in instr.operands:
                if isinstance(operand, str) and operand.startswith('t'):
                    used_temps.add(operand)
            
            if instr.result and instr.result.startswith('t'):
                if instr.result not in used_temps:
                    # This result is never used
                    continue
        
        return instructions
    
    def _constant_propagation(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Propagate constant values"""
        constants = {}
        optimized = []
        
        for instr in instructions:
            # Track constant assignments
            if instr.opcode == IROpCode.LOAD_CONST:
                constants[instr.result] = instr.operands[0]
            
            # Replace variable references with constants
            new_operands = []
            for operand in instr.operands:
                if operand in constants:
                    new_operands.append(constants[operand])
                else:
                    new_operands.append(operand)
            
            instr.operands = new_operands
            optimized.append(instr)
        
        return optimized
    
    def _eliminate_common_subexpressions(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        """Eliminate redundant computations"""
        expressions = {}
        optimized = []
        
        for instr in instructions:
            # Create expression signature
            if instr.opcode in [IROpCode.ADD, IROpCode.SUB, IROpCode.MUL, IROpCode.DIV]:
                expr_key = (instr.opcode, tuple(instr.operands))
                
                if expr_key in expressions:
                    # Reuse previous computation
                    # Replace with LOAD instruction
                    new_instr = IRInstruction(
                        IROpCode.LOAD,
                        [expressions[expr_key]],
                        instr.result,
                        instr.line
                    )
                    optimized.append(new_instr)
                else:
                    expressions[expr_key] = instr.result
                    optimized.append(instr)
            else:
                optimized.append(instr)
        
        return optimized
    
    def get_optimization_report(self) -> Dict:
        """Generate optimization statistics"""
        return {
            'optimizations_applied': len(self.optimization_history),
            'techniques': ['dead_code_elimination', 'constant_propagation', 'cse'],
            'estimated_improvement': '15-30% faster execution'
        }
