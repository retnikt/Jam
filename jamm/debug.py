from tkinter import *
from tkinter.ttk import Entry, Notebook
import tkinter.messagebox
import evdev.ecodes


class DebugWindow(Tk):
    def __init__(self, *args, **kwargs):
        super(DebugWindow, self).__init__(*args, **kwargs)
        self.geometry("500x500")
        self.title("jamm Debug Tool")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.devices = [evdev.InputDevice(i) for i in evdev.list_devices()]
        if not self.devices:
            self.after(100, self.no_devices)

        self.listbox = Listbox(self, font=(10,))
        self.reload = Button(self, text="Reload", command=self.do_reload)
        self.close = Button(self, text="Close", command=self.destroy)
        self.info = Button(self, text="Info", command=self.do_info)
        self.toggle_info_button_enabled(None)
        self.listbox.bind("<<ListboxSelect>>", self.toggle_info_button_enabled)
        self.do_reload()
        self.listbox.grid(columnspan=3, sticky=NSEW)
        self.info.grid(row=1, column=1, sticky=NSEW)
        self.reload.grid(row=1, column=0, sticky=NSEW)
        self.close.grid(row=1, column=2, sticky=NSEW)

    def no_devices(self):
        tkinter.messagebox.showerror("Error",
                                     "No devices found. Did you run this tool as root?")
        self.destroy()

    # noinspection PyUnusedLocal
    def toggle_info_button_enabled(self, *junk):
        if len(self.listbox.curselection()) != 1:  # one item is selected
            self.info.config(state=DISABLED)
        else:
            self.info.config(state=ACTIVE)

    # noinspection PyUnusedLocal
    def do_reload(self, *junk):
        # get available debugWindow
        self.devices = [evdev.InputDevice(i) for i in evdev.list_devices()]
        self.devices.reverse()
        # insert all devices
        self.listbox.delete(0, END)
        [self.listbox.insert(END, "{id} {name}".format(
            name=i.name, id=i.fn[16:])) for i in self.devices]

    # noinspection PyUnusedLocal
    def do_info(self, *junk):
        selected = self.listbox.curselection()
        InfoWindow(self.devices[selected[0]])


class InfoWindow(Toplevel):
    def __init__(self, device: evdev.InputDevice, *args, **kwargs):
        super(InfoWindow, self).__init__(*args, **kwargs)
        self.geometry("500x500")
        self.title("Info - {name}".format(name=device.name))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.notebook = Notebook(self)
        general = GeneralTab(self.notebook, device)
        self.notebook.add(general, text="General")
        leds = LEDTab(self.notebook, device)
        self.notebook.add(leds, text="LEDs")
        self.notebook.columnconfigure(0, weight=1)

        self.close = Button(self, text="Close", command=self.destroy)
        self.notebook.grid(row=0, column=0, sticky=NSEW)
        self.close.grid(row=1, sticky=NSEW)


class MyIntVar(IntVar):
    def __init__(self, second, *args, **kwargs):
        super(MyIntVar, self).__init__(*args, **kwargs)
        self.second = second


class LEDTab(Frame):
    def __init__(self, parent, device: evdev.InputDevice, *args, **kwargs):
        super(LEDTab, self).__init__(parent, *args, **kwargs)
        self.device = device
        # generate checkboxes for LED states
        # var.second stores LED id
        # var.value stores state of checkbox
        self.led_checkboxes = [(i, Checkbutton(self, var=i, text=evdev.ecodes.LED[i.second], state=ACTIVE)) for i in
                               [MyIntVar(second=j) for j in self.device.capabilities()[evdev.ecodes.EV_LED]]]

        self.update_checkboxes()
        column = 1
        for var, box in self.led_checkboxes:
            box.grid(row=0, column=column)
            column += 1

    def checkbox_callback(self, event):
        for var, box in self.led_checkboxes:
            if box == event.widget:  # this is the correct widget
                self.device.set_led(var.second, var.get())

    def update_checkboxes(self):
        on_leds = self.device.leds()  # leds that are on for device
        all_leds = self.device.capabilities()[evdev.ecodes.EV_LED]  # available leds for device
        leds = []  # status of all leds
        for available_led in all_leds:
            leds.append((available_led, int(available_led in on_leds)))  # append led id + state to list
        for var, box in self.led_checkboxes:
            var.set(leds[var.second])  # set checkbox


class GeneralTab(Frame):
    def __init__(self, parent, device: evdev.InputDevice, *args, **kwargs):
        super(GeneralTab, self).__init__(parent, *args, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.name_label = Label(self, text="Name", anchor=W, font=(10,))
        self.name_label.grid(row=0, column=0, sticky=W, ipadx=10)
        self.name_entry = Entry(self, font=(10,))
        self.name_entry.insert(0, device.name)
        self.name_entry.configure(state="readonly")
        self.name_entry.grid(row=0, column=1, sticky=NSEW)

        self.path_label = Label(self, text="Device Path", anchor=W, font=(10,))
        self.path_label.grid(row=1, column=0, sticky=W, ipadx=10)
        self.path_entry = Entry(self, font=(10,))
        self.path_entry.insert(0, device.fn)
        self.path_entry.configure(state="readonly")
        self.path_entry.grid(row=1, column=1, sticky=NSEW)

        self.phys_label = Label(self, text="Physical Path", anchor=W, font=(10,))
        self.phys_label.grid(row=2, column=0, sticky=W, ipadx=10)
        self.phys_entry = Entry(self, font=(10,))
        self.phys_entry.insert(0, device.phys)
        self.phys_entry.configure(state="readonly")
        self.phys_entry.grid(row=2, column=1, sticky=NSEW)

        self.veid_label = Label(self, text="Vendor ID", anchor=W, font=(10,))
        self.veid_label.grid(row=3, column=0, sticky=W, ipadx=10)
        self.veid_entry = Entry(self, font=(10,))
        self.veid_entry.insert(0, device.info.vendor)
        self.veid_entry.configure(state="readonly")
        self.veid_entry.grid(row=3, column=1, sticky=NSEW)

        self.prid_label = Label(self, text="Product ID", anchor=W, font=(10,))
        self.prid_label.grid(row=4, column=0, sticky=W, ipadx=10)
        self.prid_entry = Entry(self, font=(10,))
        self.prid_entry.insert(0, device.info.product)
        self.prid_entry.configure(state="readonly")
        self.prid_entry.grid(row=4, column=1, sticky=NSEW)

        self.vers_label = Label(self, text="Device Version", anchor=W, font=(10,))
        self.vers_label.grid(row=5, column=0, sticky=W, ipadx=10)
        self.vers_entry = Entry(self, font=(10,))
        self.vers_entry.insert(0, device.info.version)
        self.vers_entry.configure(state="readonly")
        self.vers_entry.grid(row=5, column=1, sticky=NSEW)

        self.bust_label = Label(self, text="Bus Type", anchor=W, font=(10,))
        self.bust_label.grid(row=6, column=0, sticky=W, ipadx=10)
        self.bust_entry = Entry(self, font=(10,))
        self.bust_entry.insert(0, device.info.bustype)
        self.bust_entry.configure(state="readonly")
        self.bust_entry.grid(row=6, column=1, sticky=NSEW)


if __name__ == "__main__":
    window = DebugWindow()
    window.mainloop()
