
class ParseError(Exception):
    pass

class BaseCmd:
    def __init__(self, clazz, signifiers):
        self.clazz = clazz
        self.signifiers = tuple(signifiers)

    def match(self, words):
        n = len(self.signifiers)
        return len(words) >= n and tuple(words[0:n]) == self.signifiers

    def parse(self, words):
        if not self.match(words):
            raise ParseError('Does not match %s: %s' % (self, words))
        return clazz(words[len(self.signifiers):])

    def __str__(self):
        return ' '.join(self.signifiers)

class RequireCommandCmd(BaseCmd):
    def __init__(self):
        BaseCmd.__init__(self, RequireCommandCmd1, ['require','command'])

class RequireCommandCmd1:
    def __init__(self, words):
        if len(words) != 1:
            raise ParseError('require command: expected <cmd-name>')

class RequireCommandsCmd(BaseCmd):
    def __init__(self):
        BaseCmd.__init__(self, RequireCommandsCmd1, ['require','commands'])

class RequireCommandsCmd1:
    def __init__(self, words):
        if len(words) != 1:
            raise ParseError('require commands: expected <major-cmd-name>')

class EmptyCmd:
    def match(self, words):
        return len(words) == 0
    def parse(self, words):
        return EmptyCmd1()

class EmptyCmd1:
    pass

class CommandSet:
    def __init__(self):
        self.commands = [EmptyCmd(), RequireCommandCmd(), RequireCommandsCmd()]

    def parse(self, words):
        for command in self.commands:
            if command.match(words):
                return command
        raise ParseError('Command %s does not match any in %s' % (words, self.commands))

class Script:
    def __init__(self, text):
        commands = CommandSet()
        for line in text.split('\n'):
            words = line.split()
            commands.parse(words)

text = open('script').read()
Script(text)

