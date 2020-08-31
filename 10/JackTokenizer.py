class JackTokenizer:
    def __init__(self, entry):
        self.__keywords = ['class', 'constructor', 'function', 'method', 'field', 'static',
                           'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                           'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.__symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
                          '&', '|', '<', '>', '=', '~']
        self.__file = entry
        self.tokens = []
        self.__current_token_position = 0

    def tokenize(self):
        something = ''
        can_be_string_constant = False
        for key_char, char in enumerate(self.__file):
            if can_be_string_constant is False and (char == ' ' or char in self.__symbols):
                if something in self.__keywords:
                    self.tokens.append(Token(something, 'keyword'))
                elif something in self.__symbols:
                    self.tokens.append(Token(something, 'symbol'))
                elif something.isnumeric():
                    self.tokens.append(Token(something, 'integerConstant'))
                elif something != '':
                    self.tokens.append(Token(something, 'identifier'))
                if char in self.__symbols:
                    self.tokens.append(Token(char, 'symbol'))

                something = ''
            elif can_be_string_constant is True:
                if char == '"':  # Only on the ending
                    can_be_string_constant = False
                    self.tokens.append(Token(something, 'stringConstant'))
                    something = ''
                else:
                    something = f'{something}{char}'
            elif char == '"':  # Only on the opening
                can_be_string_constant = True
            else:
                something = f'{something}{char}'

    def has_more_tokens(self):
        return bool(self.__current_token_position+1 >= len(self.tokens))

    def advance(self):
        self.__current_token_position += 1

    def get_token(self):
        return self.tokens[self.__current_token_position]


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.__presentation_symbols = {'<': '&lt', '>': '&gt', '"': '&quot', '&': '&amp'}

    def __repr__(self):
        return f'Typo: {self.type} | Value: {self.get_presentation_value()}'

    def get_presentation_value(self):
        if self.value in self.__presentation_symbols:
            return self.__presentation_symbols[self.value]
        else:
            return self.value

    def get_xml_style(self):
        return f'<{self.type}> {self.get_presentation_value()} </{self.type}>'
