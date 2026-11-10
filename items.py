# Items the characters can hold 
 
from dice import Dice
 
 
class Weapon:
    """A weapon that deals damage based on a dice roll."""
 
    def __init__(self, name: str, damage_dice: Dice) -> None:
        """
        Create a weapon.
 
        Parameters
        ----------
        name : str
            The name of the weapon, e.g. 'Sword'.
        damage_dice : Dice
            The dice that decides how much damage the weapon deals.
        """
        self.name = name
        # The weapon HAS a dice (composition), instead of making its own
        # random numbers. Then the same Dice class can be reused anywhere.
        self.damage_dice = damage_dice
 
    def roll_damage(self) -> int:
        """
        Roll the weapon's dice to find the damage.
 
        Returns
        -------
        int
            The damage dealt by this attack.
        """
        return self.damage_dice.roll()
 
    def __repr__(self) -> str:
        """Representation of the weapon, e.g. Weapon(name='Sword', ...)."""
        return f'Weapon(name={self.name!r}, damage_dice={self.damage_dice})'
 
 
if __name__ == '__main__':
    print('--- Task 3: Create items ---')
    sword = Weapon('Sword', Dice(sides=12))
    print(sword)
    damages = [sword.roll_damage() for _ in range(1000)]
    print('Sword damage:', damages[:10])
    assert min(damages) >= 1 and max(damages) <= 12
