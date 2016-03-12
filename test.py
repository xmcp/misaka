import pythoncom
import pyHook
import win32api
import win32con as con
import comtypes, comtypes.client

def callback(event):
    print 'MessageName:',event.MessageName
    print 'Message:',event.Message
    print 'Time:',event.Time
    print 'Window:',event.Window
    print 'WindowName:',event.WindowName
    print 'Ascii:', event.Ascii, chr(event.Ascii)
    print 'Key:', event.Key
    print 'KeyID:', event.KeyID
    print 'ScanCode:', event.ScanCode
    print 'Extended:', event.Extended
    print 'Injected:', event.Injected
    print 'Alt', event.Alt
    print 'Transition', event.Transition
    print '---'
    return True
    
hm=pyHook.HookManager()
hm.KeyDown=callback
hm.HookKeyboard()
pythoncom.PumpMessages()
