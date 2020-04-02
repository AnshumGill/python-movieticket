from sqlite3 import *
import uuid
def id_gen(str_len=5):
        random=str(uuid.uuid4())
        random=random.upper()
        random=random.replace("-","")
        return random[0:str_len]
conn=connect("movieticketreservation.db")
row,seatnum=1,1
for i in range(70):
        seatid=id_gen()
        if (seatnum==1):
                seatnum=1
                row+=1
        conn.execute("INSERT INTO seats VALUES(?,?,?,'SF01')",(seatid,row,seatnum))
        seatnum+=1
conn.commit()
conn.close()

