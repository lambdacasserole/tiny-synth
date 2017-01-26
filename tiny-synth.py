import os.path


compiled_function_names = []
compiled_functions = []


def is_list(obj):
    return type(obj) is list


def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def primitive_path(name):
    return 'primitives/' + name + '.pc'


def is_primitive(name):
    return os.path.isfile(primitive_path(name))


def get_primitive(name):
    return read_file(primitive_path(name))


def function_path(name):
    return 'functions/' + name + '.spec'


def is_function(name):
    return os.path.isfile(function_path(name))


def get_function(name):
    return read_file(function_path(name))


def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('Unexpected end of input.')
    token = tokens.pop(0)
    if '(' == token:
        list = []
        while tokens[0] != ')':
            list.append(read_from_tokens(tokens))
        tokens.pop(0)
        return list
    elif ')' == token:
        raise SyntaxError('Unexpected closing parenthesis.')
    else:
        return token


def compile(tree, in_function=''):
    if is_list(tree):
        function_name = tree[0]
        args = tree[1:]
        if is_primitive(function_name):
            primitive = get_primitive(function_name)
            for i, arg in enumerate(args):
                primitive = primitive.replace('%' + str(i + 1), compile(arg, in_function))
            return primitive
        elif is_function(function_name):
            if function_name not in compiled_function_names and in_function != function_name:
                compile_function(function_name)
            compiled_args = []
            for arg in args:
                compiled_args.append(compile(arg, in_function))
            return function_name + '(' + ', '.join(compiled_args) + ')'
    else:
        return tree


def compile_function(name):
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
    code += compile(parse(metadata_source[1]), name)
    code += ';'
    code += '}'
    compiled_functions.append(code)
    compiled_function_names.append(name)


compile_function('bsd')
print(compiled_functions)
