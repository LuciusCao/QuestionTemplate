import re


from QTemplate.parser import run_command
from QTemplate.utils import (
    parse_template,
    extract_var_expressions,
    get_expressions_to_eval,
    evaluate_expressions,
    inject_data_to_template,
)


class QuestionTemplate:
    def __init__(self, params):
        self.template = params['模板']
        self.knowledge = params['知识点']
        self.__body_raw = params['题干']
        self.__hint_raw = params['思路']
        self.__key_raw = params['答案']
        self.__explanation_raw = params['解析']
        self.__variables_raw = params['变量']

        if self.template == '选择题':
            self.__choices_raw = params['选项']

        self.variables = self._generate_variables()

    def roll(self):
        var = self._generate_variables()
        self.variables = var

    def generate(self):
        self.body = self.generate_piece(self.__body_raw)
        self.hint = self.generate_piece(self.__hint_raw)
        self.key = self.generate_piece(self.__key_raw)
        self.explanation = self.generate_piece(self.__explanation_raw)

        if self.template == '选择题':
            self.choices = self.__choices_raw.copy()
            for k, v in self.choices.items():
                self.choices[k] = self.generate_piece(v)

        print(self.body)
        print(self.hint)
        print(self.key)
        print(self.explanation)

        if self.template == '选择题':
            print(self.choices)

    def _generate_variables(self):
        variables = self.__variables_raw.copy()
        for var_name, rule in variables.items():
            variables[var_name] = run_command(rule)
        return variables

    def generate_piece(self, content):
        var_expressions = extract_var_expression(content)
        template = parse_template(content)
        expressions = get_expressions_to_eval(self.variables)
        data = evaluate_expressions(expressions)
        result = template.format(*calced_expressions)
        return template_with_data
