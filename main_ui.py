#--------------------------
#Credits:
#https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Create_your_first_GUI_application
#--------------------------

from scipy.io.wavfile import read,write

#tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import file_reader as fr
import audio_processor as ap
import numpy as np


#--------------------------

#Constants------------------------(START)
INPUT_FOLDER = 'input_wav/'
INTRO_SUBFODLER = INPUT_FOLDER+'intro/'
MIDDLE_SUBFODLER = INPUT_FOLDER+'middle/'
END_SUBFOLDER = INPUT_FOLDER+'end/'
MUSIC_SUBFOLDER = INPUT_FOLDER+'music/'
OUTPUT_FOLDER = 'output/'

MIN_LEVEL_PCT = 0
MAX_LEVEL_PCT = 200
LEVEL_DISPLAY_DECIMAL_POINTS = 2
FADE_LENGTH_SEC = 5
OUTPUT_SAMPLE_FREQUENCY = 44100

INTRO_MIDDLE_END_OUTPUT = 'ime_compiled.wav'
INTRO_MIDDLE_OUTPUT = 'im_compiled.wav'
MIDDLE_END = 'me_compiled.wav'
PEAK_LEVEL = 32767

#Constants------------------------(FINISH)

#Functions------------------------(START)
def btn_merge_tracks():
    intro_selection = combo_intro.get()
    middle_selection = combo_middle.get()
    end_selection = combo_end.get()
    music_selection = combo_music.get()

    intro_mid_end = chk_state_1.get()
    intro_mid = chk_state_2.get()
    middle_end = chk_state_3.get()

    #Read wav files
    intro_fhz, intro_wav = read(INTRO_SUBFODLER+intro_selection)
    middle_fhz, middle_wav = read(MIDDLE_SUBFODLER+middle_selection)
    end_fhz, end_wav = read(END_SUBFOLDER+end_selection)
    music_fhz, music_wav = read(MUSIC_SUBFOLDER+music_selection)

    print('intro_fhz',intro_fhz)
    print('middle_fhz',middle_fhz)
    print('end_fhz',end_fhz)
    print('music_fhz',music_fhz)

    #Get lengths of files
    intro_len = ap.get_length_samples(intro_wav)
    middle_len = ap.get_length_samples(middle_wav)
    end_len = ap.get_length_samples(end_wav)
    music_len = ap.get_length_samples(music_wav)

    #Get amplification levels
    slider_intro_pct = slider_intro_level.get()
    slider_middle_pct = slider_middle_level.get()
    slider_end_pct = slider_end_level.get()
    slider_music_pct = slider_music_level.get()
    print('slider_music_pct',slider_music_pct)

    #Bring to amplified levels
    amped_intro = ap.amplify_by_factor(intro_wav,slider_intro_pct)
    amped_middle = ap.amplify_by_factor(middle_wav,slider_middle_pct)
    amped_end = ap.amplify_by_factor(end_wav,slider_end_pct)
    amped_music = ap.amplify_by_factor(music_wav,slider_music_pct)
    

    print("amplification completed")

    if chk_state_1.get():
        foreground_total_len = intro_len + middle_len + end_len
        music_total_len = foreground_total_len+(FADE_LENGTH_SEC*2*music_fhz)#Multiplying by 2 for both fade in and fade out
        music_clipped = ap.slice_from_beginning(music_wav,music_total_len)
        music_faded_in_out = ap.fade_in_out(music_clipped,FADE_LENGTH_SEC*music_fhz)

        forground_merged = ap.merge_3_in_sequence(intro_wav,middle_wav,end_wav)
        
        print('music_fhz',music_fhz)
        output_1 = ap.mix_with_offset(music_faded_in_out,forground_merged,FADE_LENGTH_SEC*music_fhz)
        write(OUTPUT_FOLDER+INTRO_MIDDLE_END_OUTPUT, middle_fhz, forground_merged)
        messagebox.showinfo('Test Output',OUTPUT_FOLDER+INTRO_MIDDLE_END_OUTPUT)
        
        

def slide_any_update(new_level,lbl_updated):
    new_level_float = float(new_level)
    new_level_float_display = round(new_level_float, LEVEL_DISPLAY_DECIMAL_POINTS)
    new_level_float_display_text = 'Level {}%'
    lbl_updated.config(text = new_level_float_display_text.format(new_level_float_display))

def slide_intro_update(new_level):
    slide_any_update(new_level,lbl_intro_level)

def slide_middle_update(new_level):
    slide_any_update(new_level,lbl_middle_level)

def slide_end_update(new_level):
    slide_any_update(new_level,lbl_end_level)

def slide_music_update(new_level):
    slide_any_update(new_level,lbl_music_level)
#Functions------------------------(FINISH)

#User Interface------------------------(START)
window = Tk()

window.title("Audio Compiler Automation")
window.geometry('720x200')

lbl_intro = Label(window, text="Intro")
lbl_intro.grid(column=0, row=0)

combo_intro = Combobox(window)
combo_intro['values']= fr.get_file_list('input_wav/intro')
combo_intro.current(0) #set the selected item
combo_intro.grid(column=0, row=1)


lbl_middle = Label(window, text="Middle")
lbl_middle.grid(column=1, row=0)

combo_middle = Combobox(window)
combo_middle['values']= fr.get_file_list('input_wav/middle')
combo_middle.current(0) #set the selected item
combo_middle.grid(column=1, row=1)


lbl_end = Label(window, text="End")
lbl_end.grid(column=2, row=0)

combo_end = Combobox(window)
combo_end['values']= fr.get_file_list('input_wav/end')
combo_end.current(0) #set the selected item
combo_end.grid(column=2, row=1)

lbl_music = Label(window, text="Music")
lbl_music.grid(column=3, row=0)

combo_music = Combobox(window)
combo_music['values']= fr.get_file_list('input_wav/music')
combo_music.current(0) #set the selected item
combo_music.grid(column=3, row=1)

chk_state_1 = BooleanVar()
chk_state_1.set(True) #set check state
chk_1 = Checkbutton(window, text='Intro+Middle+End', var=chk_state_1)
chk_1.grid(sticky="W",column=4, row=2)

chk_state_2 = BooleanVar()
chk_state_2.set(True) #set check state
chk_2 = Checkbutton(window, text='Intro+Middle', var=chk_state_2)
chk_2.grid(sticky="W",column=4, row=3)

chk_state_3 = BooleanVar()
chk_state_3.set(True) #set check state
chk_3 = Checkbutton(window, text='Intro+End', var=chk_state_3)
chk_3.grid(sticky="W",column=4, row=4)


slider_intro_level = Scale(window, from_=MIN_LEVEL_PCT, to=MAX_LEVEL_PCT, orient=HORIZONTAL,command=slide_intro_update)
slider_intro_level.set(100)
slider_intro_level.grid(column=0, row=3)

lbl_intro_level = Label(window, text=("Level {}%").format(slider_intro_level.get()))
lbl_intro_level.grid(column=0, row=2)

slider_middle_level = Scale(window, from_=MIN_LEVEL_PCT, to=MAX_LEVEL_PCT, orient=HORIZONTAL,command=slide_middle_update)
slider_middle_level.set(100)
slider_middle_level.grid(column=1, row=3)

lbl_middle_level = Label(window, text=("Level {}%").format(slider_middle_level.get()))
lbl_middle_level.grid(column=1, row=2)

slider_end_level = Scale(window, from_=MIN_LEVEL_PCT, to=MAX_LEVEL_PCT, orient=HORIZONTAL,command=slide_end_update)
slider_end_level.set(100)
slider_end_level.grid(column=2, row=3)

lbl_end_level = Label(window, text=("Level {}%").format(slider_end_level.get()))
lbl_end_level.grid(column=2, row=2)

slider_music_level = Scale(window, from_=MIN_LEVEL_PCT, to=MAX_LEVEL_PCT, orient=HORIZONTAL,command=slide_music_update)
slider_music_level.set(100)
slider_music_level.grid(column=3, row=3)

lbl_music_level = Label(window, text=("Level {}%").format(slider_music_level.get()))
lbl_music_level.grid(column=3, row=2)

btn_generate = Button(window, text="Generate Audio",command=btn_merge_tracks)
btn_generate.grid(column=0, row=5)

window.mainloop()