# Object-oriented game simulator
# Based on game_simulator_v1.py by Turid Torheim, NMBU, 2026
 

from __future__ import annotations
from items import Weapon
 
 
class Character:
    """Represents a character in the RPG."""
 
    def __init__(self, name: str, hp_max: int = 100, damage: int = 10,
                 weapon: Weapon | None = None) -> None:
        """
        Initialise the character.
 
        Parameters
        ----------
        name : str
            The name of the character.
        hp_max : int, optional
            Max hit points, by default 100.
        damage : int, optional
            Damage dealt when the character attacks without a weapon,
            by default 10.
        weapon : Weapon | None, optional
            Equipped weapon, by default None (no weapon).
        """
        self.name = name
        # _hp is private: other objects should change it only through
        # take_damage() and heal(), so the HP always stays valid.
        self._hp = hp_max
        self.hp_max = hp_max
        self.damage = damage
        # Optional, so characters can still fight without a weapon.
        self.weapon = weapon
 
    def take_damage(self, amount: int) -> None:
        """
        Reduce the character's own HP.
 
        The HP never goes below 0.
 
        Parameters
        ----------
        amount : int
            Damage taken. Must not be negative.
 
        Raises
        ------
        ValueError
            If amount is negative.
        """
        # Negative damage would heal the character, which heal() is for.
        if amount < 0:
            raise ValueError('Damage cannot be negative.')
        self._hp = max(self._hp - amount, 0)
 
    def heal(self, amount: int) -> None:
        """
        Increase the character's own HP.
 
        The HP never goes above hp_max.
 
        Parameters
        ----------
        amount : int
            HP restored. Must not be negative.
 
        Raises
        ------
        ValueError
            If amount is negative.
        """
        if amount < 0:
            raise ValueError('Heal amount cannot be negative.')
        self._hp = min(self._hp + amount, self.hp_max)
 
    def attack(self, target: Character) -> None:
        """
        Attack and deal damage to the target character.
 
        With a weapon, the damage is rolled with the weapon's dice.
        Without a weapon, the base damage is used.
 
        Parameters
        ----------
        target : Character
            The character that is attacked.
        """
        # "is not None" is clearer than just "if self.weapon", since it
        # shows that we check whether a weapon is equipped.
        if self.weapon is not None:
            amount = self.weapon.roll_damage()
        else:
            amount = self.damage
        # The target changes its own HP. This keeps _hp private and lets
        # subclasses (e.g. Warrior in Task 4) change how damage is taken.
        target.take_damage(amount)
 
    def introduce(self) -> None:
        """Print a line that introduces the character."""
        print(f'Hi, my name is {self.name}!')
 
    @property
    def hp(self) -> int:
        """Read-only HP, so it cannot be edited directly from outside."""
        return self._hp
 
    @property
    def is_alive(self) -> bool:
        """True if the character has more than 0 HP, otherwise False."""
        # A property with no setter is read-only, and it is always up to
        # date because it is calculated from _hp every time.
        return self._hp > 0
 
    def __repr__(self) -> str:
        """Representation of the character object."""
        return (f'<Character name={self.name} hp={self.hp} '
                f'damage={self.damage} weapon={self.weapon}>')
 
    def __str__(self) -> str:
        """Readable description of the character object."""
        return (f'Character: {self.name} with {self.hp} HP and '
                f'{self.damage} damage')
 

class Warrior(Character):
    """A defensive character that reduces incoming damage with armor."""

    def __init__(self, name: str, hp_max: int = 100, damage: int = 10,
                 weapon: Weapon | None = None, armor: int = 5) -> None:
        """
        Initialise the warrior.

        Parameters
        ----------
        name : str
            The name of the character.
        hp_max : int, optional
            Max hit points, by default 100.
        damage : int, optional
            Damage dealt without a weapon, by default 10.
        weapon : Weapon | None, optional
            Equipped weapon, by default None.
        armor : int, optional
            Damage absorbed from each incoming attack, by default 5.
        """
        super().__init__(name, hp_max, damage, weapon)
        self.armor = armor

    def take_damage(self, amount: int) -> None:
        """
        Reduce the incoming damage by armor, then take the rest.

        Parameters
        ----------
        amount : int
            Damage before armor.
        """
        super().take_damage(max(amount - self.armor, 0))


class Mage(Character):
    """A character that uses mana for double-damage spell attacks."""

    SPELL_COST = 10
    MANA_RESTORED = 5

    def __init__(self, name: str, hp_max: int = 100, damage: int = 10,
                 weapon: Weapon | None = None, mana: int = 30,
                 mana_max: int = 30) -> None:
        """
        Initialise the mage.

        Parameters
        ----------
        name : str
            The name of the character.
        hp_max : int, optional
            Max hit points, by default 100.
        damage : int, optional
            Damage dealt without a weapon, by default 10.
        weapon : Weapon | None, optional
            Equipped weapon, by default None.
        mana : int, optional
            Current mana, by default 30.
        mana_max : int, optional
            Max mana, by default 30.
        """
        super().__init__(name, hp_max, damage, weapon)
        self.mana = mana
        self.mana_max = mana_max

    def attack(self, target: Character) -> None:
        """
        Attack the target.

        With at least 10 mana, cast a spell for double damage (no weapon used).
        Otherwise attack normally (with the weapon, if any) and restore 5 mana.

        Parameters
        ----------
        target : Character
            The character that is attacked.
        """
        if self.mana >= self.SPELL_COST:
            self.mana -= self.SPELL_COST
            target.take_damage(2 * self.damage)
        else:
            super().attack(target)
            self.mana = min(self.mana + self.MANA_RESTORED, self.mana_max)
 
if __name__ == '__main__':
    # Only runs when this file is run directly, not when it is imported.
    print('--- Task 1: Update the Character class ---')
    hero = Character('Hero', hp_max=30, damage=12)
    enemy = Character('Goblin', hp_max=20, damage=5)
    print(hero)
    print(enemy)
 
    hero.attack(enemy)
    print('After one attack:', repr(enemy))
    assert enemy.hp == 8
 
    # HP stops at 0 and the character dies.
    hero.attack(enemy)
    print('After two attacks:', repr(enemy), '| alive:', enemy.is_alive)
    assert enemy.hp == 0
    assert not enemy.is_alive
 
    # Healing stops at hp_max.
    hero.take_damage(10)
    hero.heal(50)
    print('Hero after taking 10 damage and healing 50:', hero.hp)
    assert hero.hp == hero.hp_max
 
    # is_alive is read-only, so trying to change it gives an error.
    try:
        hero.is_alive = False
    except AttributeError:
        print('is_alive is read-only')
 
    print('\n--- Task 3: Character with a weapon ---')
    from dice import Dice  # only needed for this test
 
    knight = Character('Knight', weapon=Weapon('Sword', Dice(sides=12)))
    dummy = Character('Dummy', hp_max=1000)
    print(repr(knight))
    for _ in range(5):
        hp_before = dummy.hp
        knight.attack(dummy)
        print('Sword hit for', hp_before - dummy.hp, 'damage')
        # The damage comes from the d12, not the base damage of 10.
        assert 1 <= hp_before - dummy.hp <= 12
