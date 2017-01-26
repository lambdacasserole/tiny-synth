import os.path
import sys


compiled_function_names = []  # Store the names of compiled functions here to prevent duplicate compilations.
compiled_functions = []  # Store the C source code of compiled functions here.


def is_list(obj):
    """Gets whether or not a given object is a list.

    Args:
        obj (object): The object to check.

    """
    return type(obj) is list


def read_file(path):
    """Gets the text from the file at the specified path.

    Args:
        path (str): The path of the file to read.

    """
    with open(path, 'r') as file:
        return file.read()


def primitive_path(name):
    """Gets the relative path to the primitive file with the specified name.

    Args:
        name (str): The name of the primitive.

    """
    return 'primitives/' + name + '.pc'


def is_primitive(name):
    """Gets whether or not a primitive exists with the given name.

    Args:
        name (str): The name of the primitive.

    """
    return os.path.isfile(primitive_path(name))


def get_primitive(name):
    """Loads and returns the text of the primitive with the given name.

    Args:
        name (str): The name of the primitive.

    """
    return read_file(primitive_path(name))


def function_path(name):
    """Gets the relative path to the function file with the specified name.

    Args:
        name (str): The name of the function.

    """
    return 'functions/' + name + '.spec'


def is_function(name):
    """Gets whether or not a function exists with the given name.

    Args:
        name (str): The name of the function.

    """
    return os.path.isfile(function_path(name))


def get_function(name):
    """Loads and returns the text of the function with the given name.

    Args:
        name (str): The name of the function.

    """
    return read_file(function_path(name))


def tokenize(source):
    """Transforms a string of source code into a list of tokens.

    Args:
        source (str): The source code to transform.

    """
    return source.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    """Converts the given source code into a abstract syntax tree.

    Args:
        program (str): The source code to convert.

    """
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    """Converts the given set of tokens into an abstract syntax tree.

    Args:
        tokens (list): The tokens to convert.

    """
    if len(tokens) == 0:
        raise SyntaxError('Unexpected end of input.')
    token = tokens.pop(0)
    if '(' == token:
        children = []
        while tokens[0] != ')':
            children.append(read_from_tokens(tokens))
        tokens.pop(0)
        return children
    elif ')' == token:
        raise SyntaxError('Unexpected closing parenthesis.')
    else:
        return token


def compile_tree(tree, in_function=''):
    """Compiles an abstract syntax tree into C code.

    Args:
        tree (list): The abstract syntax tree to compile.
        in_function (str): The name of the function currently being compiled.

    """
    if is_list(tree):
        function_name = tree[0]
        args = tree[1:]
        if is_primitive(function_name):
            primitive = get_primitive(function_name)
            for i, arg in enumerate(args):
                primitive = primitive.replace('%' + str(i + 1), compile_tree(arg, in_function))
            return primitive
        elif is_function(function_name):
            if function_name not in compiled_function_names and in_function != function_name:
                compile_function(function_name)
            compiled_args = []
            for arg in args:
                compiled_args.append(compile_tree(arg, in_function))
            return function_name + '(' + ', '.join(compiled_args) + ')'
    else:
        return tree


def compile_function(name):
    """Loads and compiles the function with the given name.

    Args:
        name (str): The name of the function to compile.

    """
    source_code = get_function(name)
    metadata_source = source_code.split(';')
    metadata = metadata_source[0]
    metadata_fields = metadata.split(',')
    return_type = metadata_fields[0]
    code = return_type + ' ' + name + '('
    for field in metadata_fields[1:]:
        if not code.endswith('('):
            code += ', '
        parameter_type = field.split(':')
        code += parameter_type[1] + ' ' + parameter_type[0]
    code += ') {'
    code += 'return '
    code += compile_tree(parse(metadata_source[1]), name)
    code += ';'
    code += '}'
    compiled_functions.append(code)
    compiled_function_names.append(name)


def beautify(functions):
    """Pretty prints an array of compiled functions as one string.

    Args:
        functions (list): The functions to pretty print.

    """
    output = '\n\n'.join(functions)
    output = output.replace('{', '{\n')  # Sort out braces.
    output = output.replace('}', '\n}')
    lines = output.split('\n')
    indentation_level = 0
    output = []
    for line in lines:
        new_indentation_level = line.count('{') - line.count('}')
        if new_indentation_level < 0:
            indentation_level = new_indentation_level  # Un-indents need to happen on this line, not the next.
        formatted_line = ''
        for i in range(0, indentation_level):
            formatted_line += '    '
        formatted_line += line
        output.append(formatted_line)
        indentation_level = new_indentation_level
    return '\n'.join(output)


# Compile and print specified function.
compile_function(sys.argv[1])
print(beautify(compiled_functions))
