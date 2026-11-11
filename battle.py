from __future__ import annotations

from character import Character


class Battle:
    """Turn-based combat between a hero and an enemy."""

    def __init__(self, hero: Character, enemy: Character) -> None:
        """
        Initialise the battle.

        Parameters
        ----------
        hero : Character
            The character who attacks first.
        enemy : Character
            The opponent.
        """
        self.hero = hero
        self.enemy = enemy

    def play_round(self) -> None:
        """The hero attacks the enemy, and if the enemy is alive, it attacks back."""
        self.hero.attack(self.enemy)
        if self.enemy.is_alive:
            self.enemy.attack(self.hero)

    def simulate_battle(self) -> Character:
        """
        Play rounds until one character is no longer alive.

        Returns
        -------
        Character
            The winner of the battle.
        """
        rounds = 0
        while self.hero.is_alive and self.enemy.is_alive:
            self.play_round()
            rounds += 1
            print(f'Round {rounds}: {self.hero.name} {self.hero.hp} HP, '
                  f'{self.enemy.name} {self.enemy.hp} HP')
        winner = self.hero if self.hero.is_alive else self.enemy
        print(f'{winner.name} wins after {rounds} rounds!')
        return winner
    