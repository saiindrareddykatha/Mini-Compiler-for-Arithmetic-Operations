import tkinter as tk
from tkinter import ttk
import ply.lex as lex
import ply.yacc as yacc

# Token list
tokens = (
    'PRINT',
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Token rules
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'

# Ignored characters
t_ignore = ' \t'

# Additional rule for the 'print' token
def t_PRINT(t):
    r'print'
    return t

# Newline rule
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_statement_print(p):
    'statement : PRINT expression'
    print(p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = int(p[1])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_id(p):
    'expression : ID'
    # For simplicity, assume variables are 0 by default
    p[0] = 0

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {find_column(p.lexer.lexdata, p)}: Unexpected token '{p.value}'")
    exit()

# Helper function to find the column of a token
def find_column(lexer_input, token):
    last_cr = lexer_input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    return token.lexpos - last_cr + 1

# Build the parser
parser = yacc.yacc()

# GUI Class
class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Compiler GUI")

        self.code_text = tk.Text(self.root, wrap=tk.WORD, height=10, width=40)
        self.code_text.pack(pady=10)

        self.compile_button = ttk.Button(self.root, text="Compile", command=self.compile_code)
        self.compile_button.pack(pady=5)

        self.result_label = ttk.Label(self.root, text="Result:")
        self.result_label.pack(pady=5)

    def compile_code(self):
        code = self.code_text.get("1.0", tk.END).strip()

        try:
            result = parser.parse(code, lexer=lexer)
            self.result_label.config(text=f"Result: {result}")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}")

def main():
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
