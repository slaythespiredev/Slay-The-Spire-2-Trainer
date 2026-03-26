import threading
import time
import keyboard
import random
import os

print("PRE Post: Hello!")
print("PRE Post: Please, wait a bit.")

class GameState:
    def __init__(self):
        self.hp = 80
        self.shield = 20
        self.energy = 3
        self.gold = 100
        self.score = 0
        self.speed = 1.0

        self.enemy_can_move = True
        self.one_hit_kill = False
        self.damage_multiplier = 1.0
        self.defense_multiplier = 1.0

        self.infinite_hp = False
        self.infinite_shield = False
        self.infinite_energy = False

        self.always_potion = False
        self.always_upgrade = False
        self.always_rare = False
        self.legendary_relics = False

        self.gold_multiplier = 1.0
        self.free_shop = False

        self.auto_battle = False
        self.infinite_rerolls = False

state = GameState()


class Trainer:
    def __init__(self, state):
        self.state = state
        self.running = True

    def start(self):
        threading.Thread(target=self.loop, daemon=True).start()
        threading.Thread(target=self.hotkeys, daemon=True).start()

    def loop(self):
        while self.running:
            time.sleep(1 / self.state.speed)

            if self.state.infinite_hp:
                self.state.hp = 999

            if self.state.infinite_shield:
                self.state.shield = 999

            if self.state.infinite_energy:
                self.state.energy = 99

            dmg = random.randint(5, 15)

            if self.state.one_hit_kill:
                dmg *= 100

            dmg *= self.state.damage_multiplier

            if not self.state.enemy_can_move:
                dmg = 0

            self.state.hp -= int(dmg / self.state.defense_multiplier)

            gold_gain = random.randint(5, 20) * self.state.gold_multiplier
            self.state.gold += int(gold_gain)

            self.state.score += int(10 * self.state.gold_multiplier)

            print(f"HP:{self.state.hp} SH:{self.state.shield} EN:{self.state.energy} GOLD:{self.state.gold} SCORE:{self.state.score}")

            if self.state.hp <= 0:
                if self.state.auto_battle:
                    self.state.hp = 999
                else:
                    print("GAME OVER")
                    self.running = False

    def hotkeys(self):
        keyboard.add_hotkey("num 1", self.toggle, "infinite_hp")
        keyboard.add_hotkey("num 2", self.toggle, "infinite_shield")
        keyboard.add_hotkey("num 3", self.toggle, "infinite_energy")
        keyboard.add_hotkey("num 9", self.toggle, "enemy_can_move")
        keyboard.add_hotkey("num 0", self.toggle, "one_hit_kill")

        keyboard.add_hotkey("ctrl+num 1", self.edit_gold)
        keyboard.add_hotkey("ctrl+num 2", self.set_gold_multiplier)
        keyboard.add_hotkey("ctrl+num 3", self.toggle, "free_shop")

        keyboard.add_hotkey("num 5", self.toggle, "always_potion")
        keyboard.add_hotkey("num 6", self.toggle, "always_upgrade")
        keyboard.add_hotkey("num 7", self.toggle, "always_rare")
        keyboard.add_hotkey("num 8", self.toggle, "legendary_relics")

        keyboard.add_hotkey("ctrl+num 8", self.set_speed)

        keyboard.wait()

    def toggle(self, attr):
        val = not getattr(self.state, attr)
        setattr(self.state, attr, val)
        print(f"{attr.upper()}: {val}")

    def edit_gold(self):
        self.state.gold = 9999
        print("GOLD SET")

    def set_gold_multiplier(self):
        self.state.gold_multiplier = 5.0
        print("GOLD MULTI: 5.0x")

    def set_speed(self):
        self.state.speed = 2.0
        print("GAME SPEED: 2.0x")


class Profiles:
    def __init__(self, state):
        self.state = state

    def god_mode(self):
        self.state.infinite_hp = True
        self.state.infinite_energy = True
        self.state.one_hit_kill = True
        self.state.gold_multiplier = 10.0

    def legit(self):
        self.state.infinite_hp = False
        self.state.one_hit_kill = False
        self.state.gold_multiplier = 1.0

    def speedrun(self):
        self.state.speed = 3.0
        self.state.one_hit_kill = True

    def farming(self):
        self.state.gold_multiplier = 10.0
        self.state.always_rare = True

    def custom(self):
        pass


def main():
    print("Slay The Spire 2 Trainer")
    print("Loaded!")
    print("Press F5 in-game")

    trainer = Trainer(state)
    profiles = Profiles(state)

    keyboard.add_hotkey("f5", profiles.god_mode)
    keyboard.add_hotkey("f6", profiles.legit)
    keyboard.add_hotkey("f7", profiles.speedrun)
    keyboard.add_hotkey("f8", profiles.farming)

    trainer.start()

    while trainer.running:
        time.sleep(1)


if __name__ == "__main__":
    main()
