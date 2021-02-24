##################################
# ERROR
##################################

class Error:
    def __init__(self, startPos, endPos, errorName, details):
        self.errorName = errorName
        self.details = details
        self.startPos = startPos
        self.endPos = endPos

    def as_string(self):
        err = f'{self.errorName}: {self.details}'
        err += f' File {self.startPos.fn}, line {self.startPos.ln+1}'
        err += f' \n\n{stringWithArrows(self.startPos.ftxt, self.startPos, self.endPos)}'
        return err


class IllegalCharacterError(Error):
    def __init__(self, startPos, endPos, details):
        super().__init__(startPos, endPos, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    def __init__(self, startPos, endPos, details=''):
        super().__init__(startPos, endPos, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, startPos, endPos, details='', context=''):
        super().__init__(startPos, endPos, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        err = f'{self.generateTraceback()}'
        err += f'{self.errorName}, {self.details}'
        err += f' \n\n{stringWithArrows(self.startPos.ftxt, self.startPos, self.endPos)}'
        return err

    def generateTraceback(self):
        result = ''
        pos = self.startPos
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.displayName}\n' + result
            pos = ctx.parentEntry
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

class ExpectedCharError(Error):
    def __init__(self, startPos, endPos, details):
        super().__init__(startPos, endPos, 'Expected Character', details)




##################################
# Decorations
##################################


def stringWithArrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0:
        idx_end = len(text)

    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)

    return result.replace('\t', '')
