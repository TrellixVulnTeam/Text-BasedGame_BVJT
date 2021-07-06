import time
import sys
from numpy.random import choice
import threading
from pull import Pull
from player import Player, PlayerActions, PlayerEffects
from monster import Monster, MonsterActions, MonsterEffects
from calc_poss import Calculate
class Combat:

    def __init__(self, username, password, monster):
        self.pull = Pull(username, password)
        self.calculate_poss = Calculate()
        self.monster_name = monster
        
        # These are for the values of the player.
        
        # Define the values for player actions.            
        self.player = PlayerActions(
                self.pull.pull_values('SELECT * FROM stats')
            ) 
        
        self.player_effects =  PlayerEffects(
                                            self.pull.pull_values('SELECT * FROM STATS'),
                                            username, password
                                            )
        
        # Define monster actions
        self.monster = MonsterActions(
                                    self.pull.pull_values("SELECT * FROM monsters WHERE monster_name = '{}'"
                                    .format(self.monster_name))
                                    )
        self.monster_effects = MonsterEffects(
                            self.pull.pull_values("SELECT * FROM monsters WHERE monster_name = '{}'"
                                                .format(self.monster_name))
                                                , username, password
                            )                            
    def options(self):

        print(
            "[1] Attack!\n",
            "[2] Run!\n",
            "[3] Defend!\n",
            "[4] Hide!\n",
            "[5] Check Stats\n"
                )
        return self.results()

    def results(self):
        chosen = input("Choose: ")

        if chosen == "1":
            self.monster.print_monster_stats()
            if self.monster.mon_stamina <= 10:
                print("The monster is tired!")
                self.monster_effects.monster_damaged(self.player.attack())
                return True if self.monster.is_dead() else False


            else:
                if self.monster.dodge(
                    self.calculate_poss.mon_calc_dodge(
                                self.monster.mon_health, self.monster.mon_stamina
                )) == 'Miss':
                    print("The monster dodged successfully and you missed!")
                    if self.monster.counter_attack(
                        self.calculate_poss.mon_counterattack_chance(
                                                        self.monster.mon_speed, self.monster.mon_stamina
                                                        )
                        ) is True:
                       self.player_effects.got_hit(
                                    self.monster.attack(
                                        self.calculate_poss.undeadmon_att_succ(self.monster.mon_health,
                                                                                 self.monster.mon_speed, 
                                                                                 self.monster.mon_stamina)
                                        )
                       )
                       self.player_effects.loses_stamina()
                       self.monster_effects.loses_stamina(self.calculate_poss.calculate_stamina_consumed(
                                                self.monster.mon_stamina
                                                    ))
                       return False
                        
                    else:
                        self.player_effects.loses_stamina()
                        self.monster_effects.loses_stamina(self.calculate_poss.calculate_stamina_consumed(
                                                    self.monster.mon_stamina))
                        return False
                else:
                    print("It hit!")
                    self.monster_effects.monster_damaged(self.player.attack())
                    self.player_effects.loses_stamina()
                    self.monster_effects.loses_stamina(self.calculate_poss.calculate_stamina_consumed(
                                                self.monster.mon_stamina
                                                ))
                    return True if self.monster.is_dead() else False

            
        elif chosen == "2":

            if self.player.run() == "Successful":
                print(" You have ran away!")
                self.player_effects.loses_stamina()
                self.monster_effects.loses_stamina(
                                        self.calculate_poss.calculate_stamina_consumed(
                                                    self.monster.mon_stamina
                                                    ))
                return True

            else:
                    self.player_effects.got_hit(
                                        self.monster.attack(
                                        self.calculate_poss.undeadmon_att_succ(
                                                            self.monster.mon_health, 
                                                            self.monster.mon_speed, 
                                                            self.monster.mon_stamina)
                                        ))
                    self.player_effects.loses_stamina()
                    self.monster_effects.loses_stamina(self.calculate_poss.calculate_stamina_consumed(self.monster.mon_stamina))
                    return False
                    
        elif chosen == "3":
            # Make a function that blocks the enemies attacks.
            # IF shield IN storage
                # Defend()
            if 'shield' in self.get.get_storage():
                if self.is_defended() is True:
                    self.player_effects.loses_stamina()
                    self.monster_effects.loses_stamina()
                else:
                    # Call self.player.got_hit()
                    # Call self.player.loses_stamina()
                    # Call self.monster.loses_stamina()
                    pass

            else: 
                print("You can't! You don't have a shield yet!")
            # Call player_loses_stamina
                self.player_effects.loses_stamina()
            # Call player_loses_health
                self.player_effects.got_hit(self.monster.attack(self.calculate_poss.undeadmon_att_succ(
                                                        self.monster.mon_health, 
                                                        self.monster.mon_speed, 
                                                        self.monster.mon_stamina
                )))
            # Call monster loses stamina
                self.monster_effects.loses_stamina(self.calculate_poss.calculate_stamina_consumed())

        elif chosen == "4":
            self.result = self.player.hide()
            
            if self.result == 'Successful':
                self.player_effects.loses_stamina()
                print("You hid succesfully!")
                return True
            
            elif self.result == 'The creature saw you!':
                print("The creature saw you and is now preparing for battle")
                return False
            
            else:
                print("the monster saw you and has now hit you!.")
                self.player_effects.got_hit(self.monster.attack(self.calculate_poss.undeadmon_att_succ(
                    self.monster.mon_health, self.monster.mon_speed, self.monster.mon_stamina
                    )))
                self.monster.loses_stamina(self.calculate_poss.calculate_stamina_consumed(self.monster.mon_stamina))
                return False
        
        elif chosen == "5":
            self.player.player_stats()

        
        else:
            print("Invalid Choice!")
            sys.exit() 
        


    def countdown(self):
        global time_sec
        time_sec = 5
        while time_sec:

            mins, secs = divmod(time_sec, 60)

            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            
            time.sleep(1)

            time_sec -= 1

        print('stop')
        return self.random_choice()
        

    def random_choice(self):
        return choice([self.attack(), self.run(), self.hide()], p=[0.33, 0.33, 0.34])
    
    
                
    def is_defended(self):
        # This is for the chances of defending an attack
        total =  self.calculate_poss.calc_success +  0.1 
        return choice([True, False], p=[total, abs(1-total)])

