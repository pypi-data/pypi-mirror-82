# The StrBuf is used by the parser that interprets a parameters command.

class StringReader():
    """A class that lets the user read characters from the underlying string.

    Alas, io.StringIO doesn't have a straightforward eof() method, which would
    have made this implementation unnecessary.

    """
    def __init__(self, content):
        """Create a strBuf from a string."""
        self.content = content
        self.len = len(content)
        self._next = 0

    def next(self):
        """Return the next character from the strBuf, or None at EOF."""
        if self._next < self.len:
            ch = self.content[self._next]
            self._next += 1
            return ch

    def backup(self):
        if self._next > 1:
            self._next -= 1

    def eof(self):
        """Return True if the strBuf is at EOF."""
        return self._next >= self.len

    def __str__(self):
        """Return a string representation of a strBuf.

        The next character is marked by a preceding '^'; this will of course be
        not very helpful with a string containing this character.

        """
        head = self.content[:self._next]
        tail = self.content[self._next:]
        show = head + "^" + tail
        return "<{} {}>".format(self.__class__.__name__, repr(show))

