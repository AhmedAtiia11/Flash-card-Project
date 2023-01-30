from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
selected_word={'French': 'Word', 'English': 'Word'}

#-------------------------Read CSV File----------------------------#

try:
    data=pandas.read_csv("./data/words_to_learn.csv")
except:
    data=pandas.read_csv("./data/french_words.csv")
    data_dict=data.to_dict(orient="records")
else:    
    data_dict=data.to_dict(orient="records")


#-------------------------Select Random Word function----------------------------#

def chosen_word():
    global selected_word
    selected_word=random.choice(data_dict)
    
#---------------------------Next Card function----------------------------#

def next_card():
    global timer
    chosen_word()
    window.after_cancel(timer)
    canvas.itemconfig(current_img,image=back_card_img)    
    canvas.itemconfig(title,text="French",fill="white")
    canvas.itemconfig(word,text=f'{selected_word["French"]}',fill="white")
    timer=window.after(3000,func=flip_card)

#-------------------------word_is_known function----------------------------#

def word_is_known():
    data_dict.remove(selected_word)
    print(len(data_dict))
    words_to_learn = pandas.DataFrame(data_dict)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()

#-------------------------flip_card function----------------------------#

def flip_card():
    canvas.itemconfig(current_img,image=front_card_img)
    canvas.itemconfig(title,text="English",fill="black")
    canvas.itemconfig(word,text=f'{selected_word["English"]}',fill="black")
    
#--------------------------Screen Setup--------------------------------------#
window=Tk()
window.title("Flash Card Project")
window.config(padx=20,pady=20,bg=BACKGROUND_COLOR)

#Images
back_card_img=PhotoImage(file="./images/card_back.png")
front_card_img=PhotoImage(file="./images/card_front.png")
right_img=PhotoImage(file="./images/right.png")
cross_img=PhotoImage(file="./images/wrong.png")

#Create image
canvas=Canvas(width=800,height=540,highlightthickness=0,bg=BACKGROUND_COLOR)
current_img=canvas.create_image(400,270,image=back_card_img)
canvas.grid(row=0,column=1,columnspan=2)

#Text
title=canvas.create_text(400,150,text='',font=("Arial",40,"italic"),fill="white")
word=canvas.create_text(400,263,text='',font=("Arial",40,"bold"),fill="white")

#Right Button
right_button=Button(image=right_img,highlightthickness=0,command=word_is_known)
right_button.grid(row=1,column=2)

#cross Button
cross_button=Button(image=cross_img,highlightthickness=0,command=next_card)
cross_button.grid(row=1,column=1)

#Start up Word
timer=window.after(3000,func=flip_card)
next_card()
window.mainloop()
