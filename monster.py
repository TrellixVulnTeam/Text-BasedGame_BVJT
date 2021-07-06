from numpy.random import choice
from calc_poss import Calculate
class Monster:

	def __init__(self, values ):
		self.monster = values[0]
		self.mon_health = values[1]
		self.mon_stamina = values[2]
		self.mon_damage =  values[3]
		self.mon_mana = values[4]
		self.mon_speed = values[5]
		self.mon_gold_drop = values[6]

	def print_monster_stats(self):
		print(
			"Monster:{}\nHealth:{}\nStamina:{}\nDamage:P{}\nMana:{}\nSpeed:{}, Gold Drop: {}"
			.format(
				self.monster,self.mon_health, self.mon_stamina, self.mon_damage
				,self.mon_mana, self.mon_speed, self.mon_gold_drop
				)
			)
	def is_dead(self):
		if self.mon_health <= 0:
			print("The monster has died!")
			return True

		else:
			print(
				"The health of the monster is at {}"
				.format(self.mon_health)
				)
			return False


class MonsterActions(Monster):
	def __init__(self, values):
		super().__init__(values)
		self.calculate_poss = Calculate()

	def attack(self, poss):
		print(self.monster)
		if self.monster == 'zombies':
			return choice(['Miss',16, 17, 18, 19, 20], p=poss)
			
		
		if self.monster == 'skeletons':
			return choice(['Miss', 6, 7, 8, 9, 10], p=poss)
			


	def dodge(self, poss):
		return choice(['Hit', 'Miss'], p=[poss, 1-poss] )


	def counter_attack(self, poss):
		print("The monster will now counter attack!")
		return choice([True, False], p=[1-poss, poss]) 

from pull import Pull

class MonsterEffects(Monster):

	def __init__(self, values, username, password):
		super().__init__(values)
		self.pull = Pull(username, password)
	def loses_stamina(self, to_lose):
			self.pull.update_values(
			"monsters SET stamina = {} - {} WHERE monster_name = '{}'"
			.format(self.mon_health, to_lose, self.monster))

	def monster_damaged(self, damage):
		print("The monster has been damaged {}".format(damage))
		self.pull.update_values(
			"monsters SET health = {} - {} WHERE monster_name = '{}'"
			.format(self.mon_health, damage, self.monster)
		)