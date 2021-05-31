from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.constants import ACTIVE, BOTH, DISABLED, E, FLAT, LEFT, N, NORMAL, RAISED, RIGHT, S, W
from tkinter.font import BOLD, ITALIC
import random
import requests

   
clientnumber=input('Enter your mobile number subscribed: ')
if len(clientnumber)!=10 or clientnumber.isdigit()==False:
    print("Invalid mobile number")
    quit()

otp=random.randrange(100000,1000000)

url = "https://www.fast2sms.com/dev/bulkV2"

querystring = {"authorization":"JoqkyeF7O0lfTzDcYKVbpXQrtxWAI5h1NnUB6Z4SvEw8RjmuLGztvoJRdExSg3VuOqH1yIfUpFnCw2KL","sender_id":"FSTSMS","message":otp,"route":"q","numbers":clientnumber}

headers = {
    'cache-control': "no-cache"
}

response = requests.request("GET", url, headers=headers, params=querystring)
user=input("Enter otp - ")




inp=""
msgbg="snow2"
msgfg="Black"
inpbg="snow"
inpfg="black"
winbg="floral white"
butbg="antiquewhite1"
butfg="black"


f=("Arial Narrow",11,BOLD)


win=tkinter.Tk()
win.title("Chat Room")
win.iconbitmap(r"logo4.ico")
win.configure(bg=winbg)

def colourscheme():
    
    global inp
    global msgbg
    global msgfg
    global inpbg
    global inpfg
    global winbg
    global butbg
    global butfg
  

    inp=input_colour.get()
    list2_output.delete(0,tkinter.END)
    if inp=="L" or inp=="D" or inp=="l" or inp=="d":
        but2_enter.config(state=DISABLED)
        input_colour.config(state=DISABLED)
        but3_submit.config(state=ACTIVE)
        list2_output.insert(tkinter.END,"Successful")
        if inp=="l" or inp=="L":
            msgbg="snow2"
            msgfg="Black"
            inpbg="snow"
            inpfg="black"
            winbg="floral white"
            butbg="antiquewhite1"
            butfg="black"
            
        else:
            msgbg="gray20"
            msgfg="dark turquoise"
            inpbg="gray35"
            inpfg="white"
            winbg="gray60"
            butbg="gray30"
            butfg="white"
            
    else:
        list2_output.insert(tkinter.END,"*Please enter L/l or D/d")


def submit():
   
    inp=input_colour.get()
    username=input_name.get()
    list1_output.delete(0,tkinter.END)
    list1_output.insert(tkinter.END,f"Welcome '{username}' to the Chat Room!")
    list2_output.delete(0,tkinter.END)
    if inp=="l" or inp=="L":
        list2_output.insert(tkinter.END,f"Light Mode is active")
    elif inp=="d" or inp=="D":
        list2_output.insert(tkinter.END,f"Dark Mode is active")

    win.config(bg=winbg)
    label_enter_name.config(bg=msgbg,fg=msgfg)
    input_name.config(bg=inpbg,fg=inpfg)
    but1_enter.config(bg=msgbg,fg=msgfg)
    list1_output.config(bg=msgbg,fg=msgfg)
    label_lightdark.config(bg=msgbg,fg=msgfg)
    input_colour.config(bg=inpbg,fg=inpfg)
    but2_enter.config(bg=msgbg,fg=msgfg)
    list2_output.config(bg=msgbg,fg=msgfg)
    but3_submit.config(bg=msgbg,fg=msgfg)
    message_list.config(bg=msgbg,fg=msgfg)
    message_input.config(bg=inpbg,fg=inpfg)
    #send_button.config(bg=msgbg,fg=msgfg)
    #exit_button.config(bg=msgbg,fg=msgfg)


    message_input.config(state=NORMAL)
    send_button.config(state=ACTIVE)
    but3_submit.config(state=DISABLED)
   

def receive():
    
     #receives messages
    while True:
        try:
            msg=client_socket.recv(SIZE).decode("utf8")
            message_list.insert(tkinter.END,msg)
        except OSError:  #if client has left the chat.
            break


def send(event=None):  #event is passed by binders,pressing enter works as send button
    
    #send messages
    msg=message_display.get()
    msg.strip()
    message_display.set("")  #clears input field
    if msg.isspace()==False:
        client_socket.send(bytes(msg,"utf8"))
    if msg=="{quit}":
        client_socket.close()
        win.destroy()  #closes the window
    

def send_name():
    
    username=input_name.get()
    list1_output.delete(0,tkinter.END)
    if username=="" or username.isspace()==True:
        list1_output.insert(tkinter.END,"*Please enter a name")
    else:
        but1_enter.config(state=DISABLED)
        input_name.config(state=DISABLED)
        but2_enter.config(state=ACTIVE)
        output=f"Welcome '{username}' ! Customise your window - Light or Dark"
        list1_output.insert(tkinter.END,output)
        client_socket.send(bytes(username,"utf8"))
    
    

def exit():
     client_socket.send(bytes("{quit}","utf8"))
     win.destroy()



label_enter_name=tkinter.Label(win,text="Enter your username ",width=20,bg=msgbg,fg=msgfg,font=("Arial",11,),relief=FLAT)
label_enter_name.grid(row=0,column=0,sticky=N+E+W+S)

input_name=tkinter.Entry(win,width=25,bg=inpbg,fg=inpfg,font=("Arial",11))
input_name.grid(row=0,column=1,sticky=N+E+W+S)

but1_enter=tkinter.Button(win,text="Enter",command=send_name,width=5,relief=RAISED,bg=butbg,fg=butfg,font=("Arial",11))
but1_enter.grid(row=0,column=2,sticky=N+E+W+S)

list1_output=tkinter.Listbox(win,width=60,height=1,bg=msgbg,fg=msgfg,font=("Arial",13),relief=FLAT)
list1_output.grid(row=1,column=0,columnspan=3,sticky=N+E+W+S)

label_lightdark=tkinter.Label(win,text="Enter L for Light or D for Dark",width=20,bg=msgbg,fg=msgfg,font=("Arial",11),relief=FLAT)
label_lightdark.grid(row=2,column=0,sticky=N+E+W+S)

input_colour=tkinter.Entry(win,width=25,bg=inpbg,fg=inpfg,font=("Arial",11),relief=FLAT)
input_colour.grid(row=2,column=1,sticky=N+E+W+S)

but2_enter=tkinter.Button(win,text="Enter",command=colourscheme,width=5,state=DISABLED,relief=RAISED,bg=butbg,fg=butfg,font=("Arial",11))
but2_enter.grid(row=2,column=2,sticky=N+E+W+S)

list2_output=tkinter.Listbox(win,width=60,height=1,bg=msgbg,fg=msgfg,font=("Arial",13),relief=FLAT)
list2_output.grid(row=3,column=0,columnspan=3,sticky=N+E+W+S)

but3_submit=tkinter.Button(win,text="Submit",width=50,state=DISABLED,command=submit,relief=RAISED,bg="pale green1",fg=butfg,font=("Arial",11))
but3_submit.grid(row=4,column=0,sticky=N+E+W+S,columnspan=3)

messages_frame=tkinter.Frame(win,width=40,height=15)   #frame to display text messages
messages_frame.grid(row=5,column=0,columnspan=3,sticky=N+E+W+S)

message_display=tkinter.StringVar()  #for the messages to be sent
message_display.set("")    

scrollbar=tkinter.Scrollbar(messages_frame)
message_list=tkinter.Listbox(messages_frame,height=20,width=60,bg=msgbg,fg=msgfg,font=("Arial",12,BOLD),yscrollcommand=tkinter.Scrollbar.set,relief=FLAT)
message_list.pack(side=LEFT)
scrollbar.config(command=message_list.yview) 
scrollbar.pack(side=RIGHT,fill=BOTH)

message_input=tkinter.Entry(win, textvariable=message_display,width=50,bg=inpbg,fg=inpfg,state=DISABLED,font=("Arial",11),relief=FLAT)
message_input.bind("<Return>",send)   #on pressing enter it sends the msg to server file
message_input.grid(row=6,column=0,columnspan=2,sticky=N+E+W+S)

send_button=tkinter.Button(win,text=">>",command=send,bg="lavender",fg="white",width=5,state=DISABLED,font=("Arial",11,BOLD))  # image=sendbut
send_button.grid(row=6,column=2,sticky=N+E+W+S)

exit_button=tkinter.Button(win,text="Exit",command=exit,width=5,font=("Arial",11),bg="salmon1",fg=butfg)
exit_button.grid(row=7,column=0,sticky=N+E+W+S,columnspan=3)

"socket-"

HOST='127.0.0.1'
PORT=55000

SIZE=2048
ADDR=(HOST, PORT)

client_socket=socket(AF_INET,SOCK_STREAM)
client_socket.connect(ADDR)     #instead of binding we connect it to the server

receive_thread=Thread(target=receive)
receive_thread.start()

if __name__=="__main__":
    if str(otp)==user:
        print("Access granted")
    else:
        print("Access denied")
        exit()
        quit()

tkinter.mainloop()  #starts GUI execution