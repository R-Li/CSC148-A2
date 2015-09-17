from move import Move


class TippyMove(Move):
    """A move in the game of Tippy.

    position: 2-tuple of int -- indicates the row number and column number to
                                place a circle or a cross
    """

    def __init__(self, position):
        """(TippyMove, 2-tuple of int) -> NoneType

        Initialze a new TippyMove that place a circle or cross at postion

        Assume the entries of position are positive integer that is less
        than the dimension of the grid.
        """
        self.position = position

    def __repr__(self):
        """(TippyMove) -> str

        Return a string representation of this TippyMove self.
        >>> m = TippyMove((1, 3))
        >>> m
        TippyMove((1, 3))
        """
        return "TippyMove({})".format(str(self.position))

    def __str__(self):
        """(TippyMove) -> str

        Return a convenient string representation of this TippyMove self.
        >>> m = TippyMove((1, 3))
        >>> print(m)
        Place a placeholder at the intersection of row 1 and column 3
        """
        # since python counts from 0, we add 1 to both coordinates to
        # make it more readable to the users
        return ("Place a placeholder at the intersection of row {} and"
                " column {}".format(str(self.position[0] + 1),
                                    str(self.position[1] + 1)))

    def __eq__(self, other):
        """(TippyMove, TippyMove) -> bool

        Return True iff the TippyMove is the same as other

        >>> m1 = TippyMove((1, 3))
        >>> m2 = TippyMove((2, 3))
        >>> m1 == m2
        False
        """
        return isinstance(other, TippyMove) and self.position == other.position


    
