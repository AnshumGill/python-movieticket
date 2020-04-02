from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import *
import uuid

conn=connect("movieticketreservation.db")
root=Tk()
root.title("Movie Ticket Reservation System")
root.geometry("960x540+200+50")
root.resizable(False,False)
style=ttk.Style()
style.configure('TFrame',background="#FFE4C4")
style.configure('TButton',background="#FFE4C4",font=15)
style.configure('TLabel',background="#FFE4C4",font=15)
style.configure('TPanedwindow',background="#FFE4C4")

pwin=ttk.Panedwindow(root,orient=VERTICAL)
pwin.pack(fill=BOTH)
pwindow=ttk.Panedwindow(root,orient=HORIZONTAL)
pwindow.pack(fill=BOTH)

info=ttk.Frame(pwin,width=960,height=140,relief=RIDGE)
info.pack()

movNames=ttk.Frame(pwindow,width=300,height=540,relief=RIDGE)
movNames.pack()
movNames.config(padding=(15,15))

showTime=ttk.Frame(pwindow,width=660,height=540,relief=RIDGE)
showTime.pack()

pwindow.add(movNames)
pwindow.add(showTime)

pwin.add(info)
pwin.add(pwindow)

infoLabel=ttk.Label(info,text="Movie Ticket Reservation System",font=35).pack()


                
def button_movieName(Mname):
        showTimes=ttk.Frame(showTime,width=800,height=540)
        showTimes.place(x=10,y=10)
        timings=conn.execute("SELECT ShowTime, ShowID FROM show as t1 INNER JOIN movie as t2 ON t2.MovieID=t1.MovieID WHERE t2.Name=?",(Mname,)).fetchall()
        clear=ttk.Button(showTimes,text="Clear",command= showTimes.destroy).place(x=350,y=450)
        MovieName=ttk.Label(showTimes,text=Mname).place(x=400,y=10)
        synopsis=conn.execute("SELECT Synopsis FROM movie WHERE Name=?",(Mname,)).fetchone()
        syn=str(synopsis[0])
        pth=conn.execute("SELECT Poster FROM movie WHERE Name=?",(Mname,)).fetchone()
        path=str(pth[0])
        MovieSyn=ttk.Label(showTimes,text=syn,wraplength=500,justify=CENTER).place(x=250,y=60)
        img=PhotoImage(file=path)
        Poster=ttk.Label(showTimes,image=img)
        Poster.image=img
        Poster.place(x=10,y=10)
        k=0
        for i in timings:
                item=i[0]
                showid=str(i[1])
                timeButton=ttk.Button(showTimes,text=item,command=lambda x=item,y=showid: seatselect(x,y)).place(x=10+k,y=370)
                k+=120

def seatselect(time,showid):
        window=Toplevel(root)
        window.geometry("400x500+200+50")
        window.title("Select Your Seat")
        window.resizable(False,False)
        window.configure(background="#FFE4C4")
        movieid=conn.execute("SELECT MovieID FROM show WHERE ShowID=?",(showid,)).fetchone()
        movieid=str(movieid[0])
        screen=conn.execute("SELECT ScreenID FROM show WHERE ShowID=?",(showid,)).fetchone()
        screen=str(screen[0])
        seats=conn.execute("SELECT Seats FROM screen WHERE ScreenID=?",(screen,)).fetchone()
        seats=int(seats[0])
        seatnums=conn.execute("SELECT SeatNum FROM seats WHERE ScreenID=?",(screen,)).fetchall()
        seatnums=[i[0] for i in seatnums]
        cols=max(seatnums)
        screenlabel=ttk.Label(window,text="****Screen This Way****").grid(row=0,column=0,columnspan=cols)
        j=0
        for i  in range(1,cols+1):
                columnnum=ttk.Label(window,text=i).grid(row=1,column=j)
                j+=1
        j=0
        k=2
        for i in range(1,seats+1):
                seatButton=Button(window,text="|__|",command= lambda a=(k-1),b=(j+1),c=screen,d=showid,e=movieid,f=time: seatidfinder(a,b,c,d,e,f),height=2,width=3).grid(row=k,column=j)
                if(i%cols==0):
                        rownum=ttk.Label(window,text=(k-1)).grid(row=k,column=j+1)
                        k+=1
                        j-=(cols-1)
                else:
                        j+=1

def seatidfinder(row,column,screen,showid,movieid,time):
        seatid=conn.execute("SELECT SeatID FROM seats WHERE Row=? AND SeatNum=? AND ScreenID=?",(row,column,screen,)).fetchone()
        seatid=str(seatid[0])
        reserved=conn.execute("SELECT SeatID FROM seats_reserved WHERE SeatID=?",(seatid,)).fetchone()
        if reserved is None:
                window=Toplevel(root)
                window.geometry("400x250+200+50")
                window.title("Enter Your Details")
                window.resizable(False,False)
                window.configure(background="#FFE4C4")
                def reciept():
                        reservationid=str(uuid.uuid4())
                        reservationid=reservationid.upper()
                        reservationid=reservationid.replace("-","")
                        reservationid=reservationid[0:10]
                        addRow=conn.execute("INSERT INTO seats_reserved VALUES(?,?,?,?)",(seatid,screen,movieid,showid,))
                        addRow2=conn.execute("INSERT INTO reservation VALUES(?,?,?,?)",(reservationid,nameEntry.get(),phoneEntry.get(),seatid,))                       
                        conn.commit()
                        messagebox.showinfo(title="Success", message="Your reservation was successful, Thank You\nPlease make a note of your reservation ID: "+reservationid)
                        window.destroy()
                        
                movie=conn.execute("SELECT Name, RunTime, Language FROM movie WHERE MovieID=?",(movieid,)).fetchone()
                showid=conn.execute("SELECT ShowID FROM show WHERE MovieID=? AND ShowTime=?",(movieid,time,)).fetchone()

                showid=str(showid[0])
                moviename=str(movie[0])
                runtime=int(movie[1])
                lang=str(movie[2])

                nameEntry=StringVar(window)
                phoneEntry=StringVar(window)
                
                enter=ttk.Label(window,text="Please Enter your details: ").place(x=10,y=10)
                name=ttk.Label(window,text="Name-").place(x=10,y=30)
                nameEntry=ttk.Entry(window,width=24,textvariable=nameEntry)
                nameEntry.place(x=10,y=60)
                phn=ttk.Label(window,text="Phone Number-").place(x=200,y=30)
                phnEntry=ttk.Entry(window,width=24,textvariable=phoneEntry)
                phnEntry.place(x=200,y=60)
                info=ttk.Label(window,text="You have selected -").place(x=10,y=100)
                seatinfo=ttk.Label(window,text="Row: "+str(row)+" Seat Number: "+str(column)+" of the "+str(time)+" show").place(x=10,y=130)
                movieinfo=ttk.Label(window,text="For: "+moviename+"\nRun Time: "+str(runtime)+"\nLanguage: "+lang).place(x=10,y=160)                
                submit=ttk.Button(window,text="Submit",command=reciept).place(x=150,y=220)
        else:
                messagebox.showinfo(title="Sorry", message="Seat alredy Reserved, Please Try Again with another Seat")
        
cursor=conn.execute("SELECT Name FROM movie")

for i in cursor:
        item=i[0]
        button=ttk.Button(movNames, text=item,command=lambda x=item: button_movieName(x)).grid()
lbl=ttk.Label(movNames,text="1.Select Movie\n2.Select Show Time\n3.Select Seat",wraplength=120,justify=CENTER).grid()


root.mainloop()
conn.close()
