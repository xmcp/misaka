#coding=utf-8

#py2
from __future__ import division
range=xrange

from Tkinter import *
from ttk import *
import threading
import pyHook
import pythoncom
import time

tk=Tk()
tk.attributes('-toolwindow',True)
tk.attributes('-topmost',True)
tk.geometry('220x600')
tk.title('Misaka')

tk.columnconfigure(0,weight=1)
tk.columnconfigure(1,weight=1)
tk.rowconfigure(1,weight=1)

SPECIAL_KEYS={
    'Lcontrol','Lmenu','Lwin','Rcontrol','Rmenu','Rwin',
    'Escape','Snapshot','Home','End','Prior','Next','Return',
    'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
}
MOD_KEYS={
    'Lcontrol','Lmenu','Lwin','Rcontrol','Rmenu','Rwin',
}
SHIFT={'Lshift','Rshift'}
NICKNAME={
    'Up': '↑', 'Down': '↓', 'Left': '←', 'Right': '→', 'Tab': '⇥',
    'Return': '⏎', 'Space': '⎵', 'Back': '◁', 'Delete': '◀',
    'Escape': 'Esc', 'Snapshot': 'PrtSc', 'Prior': 'PgUp', 'Next': 'PgDn',
    'Lcontrol': 'Ctrl', 'Lmenu': 'Alt', 'Lwin': 'Win',
    'Rcontrol': 'Ctrl', 'Rmenu': 'Alt', 'Rwin': 'Win',
    'Oem_Minus': '-', 'Oem_Plus': '=',  'Oem_Comma': ',', 'Oem_Period': '.',
    'Oem_5': '\\', 'Oem_3': '`', 'Oem_2': '/', 'Oem_1': ';', 'Oem_7': "'", 'Oem_4': '[', 'Oem_6': ']',
}

holdkey=set()
last_time=0
paused=False
current_id=None
status='idle'

def hooker():
    hm=pyHook.HookManager()
    hm.SubscribeKeyDown(keydown)
    hm.SubscribeKeyUp(keyup)
    hm.HookKeyboard()
    pythoncom.PumpMessages()

def keydown(event):
    def proc():
        return NICKNAME.get(event.Key)
    
    global status
    global last_time
    global current_id
    holdkey.add(event.Key)
    
    if paused or event.Key in SHIFT:
        return True

    if current_id!=event.Window:
        current_id=event.Window
        if status!='idle':
            status='idle'
            t.insert(END,'\n')
        t.insert(END,u'\n✪ %s\n'%event.WindowName.decode('gbk','ignore'),'title')
    
    if status=='string':
        if event.Key in SPECIAL_KEYS or time.time()-last_time>5:
            status='idle'
            t.insert(END,'\n')
    if status=='idle':
        if event.Key in SPECIAL_KEYS:
            status='modkey'
        else:
            status='string'
            t.insert(END,'""','info')

    if status=='string':
        t.insert('end - 2 chars',proc() or (chr(event.Ascii) if event.Ascii else '⍰'),'string')
        if event.Key=='Return':
            status='idle'
            t.insert(END,'\n')
    else: #status=='modkey'
        if any((s in holdkey for s in SHIFT)):
            t.insert('end',' Shift ','modkey')
            for s in SHIFT:
                holdkey.discard(s)
        t.insert('end',' %s '%(proc() or event.Key),'modkey' if event.Key in MOD_KEYS else 'key')
    
    t.see('end - 2 chars')
    last_time=time.time()
    return True

def keyup(event):
    global status
    holdkey.discard(event.Key)
    if status=='modkey' and not holdkey:
        status='idle'
        t.insert('end','\n')
    return True

def pause(*_):
    global paused
    paused=not paused
    pausebtn['text']='已暂停' if paused else '暂停'

def clear(*_):
    t.delete(1.0,'end - 2 chars linestart')

pausebtn=Button(tk,text='暂停',command=pause)
pausebtn.grid(row=0,column=0,sticky='we')
Button(tk,text='清空',command=clear).grid(row=0,column=1,sticky='we')

t=Text(tk,font='Consolas -18')
t.grid(row=1,column=0,columnspan=2,sticky='nswe')

t.tag_config('warning',foreground='#fff',background='#f00')
t.tag_config('string',foreground='#00f')
t.tag_config('info',foreground='#aaa')
t.tag_config('modkey',foreground='#000',background='#ff0')
t.tag_config('key',foreground='#fff',background='#444')
t.tag_config('title',foreground='#444',font='黑体 -12')

threading.Thread(target=hooker).start()
t.insert(1.0,'注意：输入密码时请暂停记录按键\n','warning')
mainloop()
