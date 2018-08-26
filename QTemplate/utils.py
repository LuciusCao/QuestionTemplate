import re
import logging


def extract_var_expressions(content):
    pattern = r'(?<=<)[^<]+?(?=>)'
    return re.findall(pattern, content)


def parse_template(content):
    pattern = r'<[^<]+?>'
    replacement = '{}'
    return re.sub(pattern, replacement, content)


def get_expressions_to_eval(var_dict, exprs):
    var_name = set(var_dict.keys())
    for v in var_name:
        exprs = [re.sub(v, str(var_dict[v]), e) for e in exprs]

    return exprs


def evaluate_expressions(exprs):
    try:
        data = [eval(e) for e in exprs]
    except Exception:
        logging.error('Errors in exprs!')
        data = [-1 for e in exprs]

    return data


def inject_data_to_template(template, data):
    num_placeholders = template.count('{}')
    if num_placeholders == len(data):
        return template.format(*data)
    elif num_placeholders < len(data):
        logging.warning('More data than placeholders')
        return template.format(*data)
    else:
        logging.error('Error occurred! Insufficient data!')
        return template.format(*[-1 for i in range(num_placeholders)])
