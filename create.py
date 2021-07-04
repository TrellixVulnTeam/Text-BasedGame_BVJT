import psycopg2
import time
class Create:
     
     def __init__(self, username, password):
        self.acc_u_name = username
        self.acc_p_word = password
     




class Delete:
     def __init__(self, u_name, p_word, will_del):
        self.will_del = will_del
        self.acc_u_name = u_name
        self.acc_p_word = p_word
        self.deleted = True
     def delete_table(self):
        
            self.conn = psycopg2.connect(dbname=f'{self.acc_u_name}_passwords', user=f'{self.acc_u_name}', 
                                          password=f'{self.acc_p_word}', host='127.0.0.1' )
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT site_name FROM passwords WHERE site_name = %s;" % (f"'{self.will_del}'"))
            self.values = self.cur.fetchone()
            self.cur.execute("DELETE FROM %s WHERE %s = '%s'" % ("passwords", "site_name", self.will_del))
            self.conn.commit()
            self.cur.close()
            self.conn.close()
              
            if self.values != None:
               time.sleep(3)
               print("\nDeleted succesfully")
               self.deleted = True
            
            else:
               time.sleep(3)
               print("\nWrong site_name!")
               self.deleted = False 

class Pull:

    def __init__(self, u_name, p_word):
       
         self.acc_u_name = u_name
         self.acc_p_word = p_word

    def pull_table(self, statement): 
        self.conn = psycopg2.connect(dbname=f'{self.acc_u_name}_game', user=f'{self.acc_u_name}', 
                                          password=f'{self.acc_p_word}', host='127.0.0.1' )
        self.cur = self.conn.cursor()
        self.cur.execute("{}".format(statement))
        self.conn.commit()
        self.values = self.cur.fetchall()
        self.cur.close()
        self.conn.close()

        return self.values
    def pull_val(self, statement):
        self.conn = psycopg2.connect(dbname=f'{self.acc_u_name}_game', user=f'{self.acc_u_name}', 
                                          password=f'{self.acc_p_word}', host='127.0.0.1' )
        self.cur = self.conn.cursor()
        self.cur.execute("{}".format(statement))
        self.values = self.cur.fetchone()
        self.cur.close()
        self.conn.close()

        return self.values

    def update_values(self, statement):
        self.conn = psycopg2.connect(dbname=f'{self.acc_u_name}_game', user=f'{self.acc_u_name}', 
                                          password=f'{self.acc_p_word}', host='127.0.0.1' )
        self.cur = self.conn.cursor()
        self.cur.execute("UPDATE {}".format(statement))
        self.conn.commit()
        self.cur.close()
        self.conn.close()