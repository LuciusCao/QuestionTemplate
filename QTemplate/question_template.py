import re
import random


class QuestionTemplate:
    def __init__(self, params):
        self.template = params['模板']
        self.knowledge = params['知识点']
        self.__body_raw = params['题干']
        self.__hint_raw = params['思路']
        self.__key_raw = params['答案']
        self.__explanation_raw = params['解析']
        self.__variables_raw = params['变量']

        self.variables = self._generate_variables()

    def roll(self):
        var = self._generate_variables()
        self.variables = var

    def generate(self):
        self.body = self._inject_data_to_template(self.__body_raw)
        self.hint = self._inject_data_to_template(self.__hint_raw)
        self.key = self._inject_data_to_template(self.__key_raw)
        self.explanation = self._inject_data_to_template(self.__explanation_raw)
        print(self.body)
        print(self.hint)
        print(self.key)
        print(self.explanation)

    def _generate_variables(self):
        variables = self.__variables_raw.copy()
        for var_name, rule in variables.items():
            variables[var_name] = self._parse_rule(rule)
        return variables

    def _parse_rule(self, rule, random_state=None):
        if random_state is not None:
            random.seed(random_state)

        tokens = rule.split()
        d_type = 'int'
        if 'float' in tokens:
            d_type = 'float'

        use_random = 'random'
        if use_random:
            assert 'from' in tokens and 'to' in tokens
            floor = int(re.findall(r'(?<=from).(\d+)', rule)[0])
            ceil = int(re.findall(r'(?<=to).(\d+)', rule)[0])
            if d_type == 'int':
                return random.randint(floor, ceil)
            else:
                return random.random * (ceil - floor) + floor

        else:
            number = re.findall(r'\d+', rule)[0]
            return eval('{}({})'.format(d_type, number))

    def _inject_data_to_template(self, content):
        expressions = self._parse_expressions(content)
        template_wo_data = self._parse_template(content)
        calced_expressions = self._eval_expressions(expressions)
        template_with_data = template_wo_data.format(*calced_expressions)
        return template_with_data

    @staticmethod
    def _parse_expressions(content):
        pattern = r'(?<=<)[^<]+?(?=>)'
        return re.findall(pattern, content)

    @staticmethod
    def _parse_template(content):
        pattern = r'<[^<]+?>'
        replacement = '{}'
        return re.sub(pattern, replacement, content)

    def _eval_expressions(self, exprs):
        var_name = list(self.__variables_raw.keys())
        for v in var_name:
            exprs = [re.sub(v, str(self.variables[v]), e) for e in exprs]
        result = [eval(e) for e in exprs]
        return result
