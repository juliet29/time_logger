import ast


class InputParser(ast.NodeVisitor):
    def __init__(self):
        self.values = []

    def visit_Constant(self, node: ast.AST):
        try:
            self.values.append(node.value)  # type: ignore
        except:
            pass
        self.generic_visit(node)


def extract_constant_values_from_string(code):
    # code must be valid python, like "12,34,45"
    node = ast.parse(code)
    parser = InputParser()
    parser.visit_Constant(node)
    return parser.values
