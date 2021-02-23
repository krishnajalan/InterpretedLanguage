from lib.lexer import Lexer
from lib.parser_ import Parser
from lib.interpreter import Interpreter, Context, Number
from lib.symbols import SymbolTable

##################################
# RUN
##################################

globalSymbolTable = SymbolTable()
globalSymbolTable.set('null', Number(0))


def run(filename, text):

    lexer = Lexer(text, filename)
    tokens, error = lexer.make_token()
    # make token segregate the input symbols
    # according to tokens defined and return
    # list of tokens and error (if any/None)
    if error: return None, error
    parser = Parser(tokens) 
    # Abstract syntax tree
    ast = parser.parse()
    if ast.error: return None, ast.error


    # Run Program
    interpreter = Interpreter()
    context = Context('<progrom>')
    context.symbolTable = globalSymbolTable
    result = interpreter.visit(ast.node, context)
    return result.value , result.error
