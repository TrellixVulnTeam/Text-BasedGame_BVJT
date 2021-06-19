import psycopg2
from create import Create, Pull
class User():
    # This is the user class
    def __init__(self, u_name, p_word):
        self.acc_u_name = u_name
        self.acc_p_word = p_word
        self.active = True
        self.create = Create(self.acc_u_name, self.acc_p_word)
        self.pull = Pull()
        self.pull.add_username(self.acc_u_name)
        self.pull.add_password(self.acc_p_word)
        self.to_input = {
                'player':[
                        'player_name, health, stamina, damage, gold, mana', 
                        'VALUES ({}, {}, {}, {}, {}, {})'.format(f"'{self.acc_u_name}'", 50, 60, 70, 80, 0)
                ],
                'monsters': [
                          'monster_name, health, stamina, speed, damage, gold_drop, mana',
                          'VALUES({}, {}, {}, {}, {}, {}, {})'.format("'zombies'", 50, 40, 10, 20, 30, 0),
                          'VALUES({}, {}, {}, {}, {}, {}, {})'.format("'skeletons'", 20, 70, 40, 10, 50, 0),
                          'VALUES({}, {}, {}, {}, {}, {}, {})'.format("'wolves'", 55, 80, 50, 30, 80, 0),
                          ],
                'merchant': [
                            'merchant_id, merchant_name, merchant_location',
                            'VALUES({}, {}, {})'.format("'MER001'", "'Ben'", "'Temple'")
                        ],
                'items': [
                        'item_name, damage, durability, selling_price, purchasing_price',
                        'VALUES({}, {}, {}, {}, {})'.format("'normal_sword'", 20, 50, 10, 30),   
                        'VALUES({}, {}, {}, {}, {})'.format("'shield'", 0, 100, 20, 40),   
                        'VALUES({}, {}, {}, {}, {})'.format("'dagger'", 10, 60, 5, 20)   
                       ],
                'merchant_storage': [
                        'merchant_id, item_name, quantity',
                        'VALUES({}, {}, {})'.format("'MER001'", "'normal_sword'", 6),
                        'VALUES({}, {}, {})'.format("'MER001'", "'shield'", 3),
                        'VALUES({}, {}, {})'.format("'MER001'", "'dagger'",  10)                     
                ],
            }

        self.to_create = {
                "player":
                         'player_name varchar(50) PRIMARY KEY NOT NULL,'+
                         'health int NOT NULL, stamina int NOT NULL,'+ 
                         'damage int NOT NULL, gold int NOT NULL, mana int NOT NULL'
                ,

                "items":
                        'item_name varchar(100) PRIMARY KEY NOT NULL,' +
                        'damage int NOT NULL, durability int NOT NULL,' +
                        'selling_price int NOT NULL, purchasing_price int NOT NULL'
                ,

                "storage": 
                        'player_name varchar(50) NOT NULL references player(player_name),'+
                        'item_name varchar(100) NOT NULL references items(item_name), quantity int NOT NULL'
                ,

                "monsters": 
                          'monster_name varchar(50) PRIMARY KEY NOT NULL,' +
                          'health int NOT NULL, stamina int NOT NULL, damage int NOT NULL, mana int NOT NULL,' +
                          'speed int NOT NULL, gold_drop int NOT NULL' 
                ,

                "merchant":
                        'merchant_id varchar(100) PRIMARY KEY NOT NULL, merchant_name varchar(50) NOT NULL,' +
                        'merchant_location varchar(150) NOT NULL'
                ,

                "merchant_storage":  
                         'merchant_id varchar(50) NOT NULL references merchant(merchant_id),' +
                         'item_name varchar(100) NOT NULL references items(item_name), quantity int NOT NULL'
                ,

                "item_ordered":
                        'merchant_id varchar(50) NOT NULL references merchant(merchant_id),'+
                        'item_name varchar(100) NOT NULL references items(item_name), damage int NOT NULL,'+
                        'quantity int NOT NULL, durability int NOT NULL, purchasing_price int NOT NULL, '+
                        'total_price int NOT NULL'
                ,

        }

    def auth(self):
        """ This used in order to autheticate the user while also registering it if not registered yet"""
        if ';' in self.acc_u_name:
            print("\n\nNo semicolons allowed!")
            self.active = False
        else:

            try:

                self.conn = psycopg2.connect(dbname=f"{self.acc_u_name}_passwords", user=f"{self.acc_u_name}",
                             password=f"{self.acc_p_word}", host="127.0.0.1")

                self.cur = self.conn.cursor()

                self.cur.execute(f"SELECT * FROM passwords;")

                self.cur.fetchone()
                
                self.cur.close()
                
                self.conn.close()

                

            except:

                print("damn")

                self.create.create_user()

                self.create.create_db()

                self.create.create_table(self.to_create)

                self.create.input_val(self.to_input)

                print("We've already registered you")










             