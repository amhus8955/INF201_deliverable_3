# Dice class for the game simulator
 
import random
 
 
class Dice:
    """An n-sided dice that gives a random number from 1 to sides."""
 
    def __init__(self, sides: int = 6) -> None:
        """
        Create a dice with a given number of sides.
 
        Parameters
        ----------
        sides : int, optional
            Number of sides, at least 2, by default 6.
 
        Raises
        ------
        ValueError
            If sides is less than 2.
        """
        # A dice with 0 or 1 side would not be random, so it is not allowed.
        if sides < 2:
            raise ValueError('A dice must have at least 2 sides.')
        self.sides = sides
 
    def roll(self) -> int:
        """
        Roll the dice.
 
        Returns
        -------
        int
            A random whole number from 1 to sides, both included.
        """
        return random.randint(1, self.sides)
 
    def __call__(self) -> int:
        """
        Roll the dice by calling the object, e.g. d20() instead of
        d20.roll().
 
        Returns
        -------
        int
            The same as roll().
        """
        # Reuses roll(), so the dice logic is only written in one place.
        return self.roll()
 
    def __repr__(self) -> str:
        """Representation of the dice, e.g. Dice(sides=6)."""
        return f'Dice(sides={self.sides})'
 
 
if __name__ == '__main__':
    print('--- Task 2: Introducing randomness with a Dice class ---')
    d6 = Dice()
    d20 = Dice(sides=20)
    print(d6, d20)
    assert repr(d6) == 'Dice(sides=6)'
 
    rolls = [d20.roll() for _ in range(1000)]
    print('d20.roll():', rolls[:10])
    print('d20():     ', [d20() for _ in range(10)])
    # All rolls must be between 1 and 20.
    assert min(rolls) >= 1 and max(rolls) <= 20
 
    try:
        Dice(sides=1)
    except ValueError as error:
        print('Dice(sides=1) gives an error:', error)
