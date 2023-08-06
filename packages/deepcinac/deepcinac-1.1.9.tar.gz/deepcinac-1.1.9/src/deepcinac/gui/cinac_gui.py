# Ignore warnings
import warnings

warnings.filterwarnings('ignore')

import numpy as np
import sys
from datetime import datetime
import hdf5storage
import h5py
import matplotlib
from sys import platform
# import cv2
from matplotlib.colors import LinearSegmentedColormap
import scipy.stats as stats
import time
from matplotlib.figure import SubplotParams

# if not using TkAgg, crash on MacOsX
matplotlib.use("TkAgg")
import scipy.io as sio
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from PIL import ImageTk, Image
import math
# import matplotlib.gridspec as gridspec
# import matplotlib.image as mpimg

from matplotlib import patches
import scipy.signal as signal
import matplotlib.image as mpimg
from random import randint
import scipy.ndimage.morphology as morphology
import os
from PIL import ImageDraw
import PIL
from shapely import geometry
# from PIL import ImageTk
from itertools import cycle
from matplotlib import animation
import matplotlib.gridspec as gridspec
import yaml
from tkinter import messagebox

from deepcinac.utils.cells_map_utils import CellsCoord, create_cells_coord_from_suite_2p, \
    get_coords_extracted_from_fiji

from deepcinac.utils.utils import load_movie, get_source_profile_param, scale_polygon_to_source, \
    get_continous_time_periods, smooth_convolve, build_raster_dur_from_onsets_peaks, norm01, get_tree_dict_as_a_list

from deepcinac.utils.cinac_file_utils import CinacFileReader, CinacFileWriter, read_cell_type_categories_yaml_file

from deepcinac.cinac_structures import CinacRecording, CinacDataMovie

if sys.version_info[0] < 3:
    import Tkinter as tk
    from Tkinter import *
    from Tkinter import ttk
else:
    import tkinter as tk
    import tkinter.filedialog as filedialog
    from tkinter import *
    from tkinter import ttk

NWB_PACKAGE_AVAILABLE = True
try:
    from pynwb import NWBHDF5IO
    from pynwb.ophys import TwoPhotonSeries, ImageSegmentation, Fluorescence
    from pynwb.image import ImageSeries
except ImportError:
    NWB_PACKAGE_AVAILABLE = False


def event_lambda(f, *args, **kwds):
    return lambda f=f, args=args, kwds=kwds: f(*args, **kwds)


class DataAndParam:
    def __init__(self, path_data=None):
        self.time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        # path and file_name of the CI movie.
        # used to save it in the cinac file if necessary
        self.ci_movie_file_name = None
        # Normalized version of the movie
        self.tiff_movie = None
        # Non normalized, used to save it in the cinac file if necessary
        self.non_norm_tiff_movie = None
        self.avg_cell_map_img = None
        self.coord_obj = None
        self.spike_nums = None
        self.peak_nums = None
        self.doubtful_frames_nums = None
        self.mvt_frames_nums = None
        self.to_agree_peak_nums = None
        self.to_agree_spike_nums = None
        self.traces = None
        self.raw_traces = None
        self.raster_dur = None
        self.path_data = path_data
        self.inter_neurons = None
        self.cells_to_remove = None
        self.cells_map_img = None
        # 2d array n_cells * n_frames of float representing the predictions of the classifier
        # value between 0 and 1
        self.classifier_predictions = None
        # list of 2d array representing the inference of neuronal activity by given methods chosent by the user
        self.other_rasters = []
        self.classifier_predictions = None
        self.classifier_weights_file = None
        self.classifier_model_file = None
        # list of tuple of at least 3 int representing cell, first_frame, last_frame. A segment that has been annoted
        # for ground truth
        self.gt_segments = list()
        self.invalid_cells = None
        # take as key int representing the cell index, and as value a string representing the cell type
        self.cell_type_dict = dict()
        # will be a dict with key the cell_id and value a dict with key the cell_type and value the prediction
        self.cell_type_classifier_predictions = None
        # "multi_class", "binary"
        self.cell_type_classifier_category = None
        # cell types to display, if not None, then cell types fields will be displayed in the GUI
        # list of str
        self.cell_types_for_classifier = None
        # key is an int and value a str representing the cell_type
        self.cell_type_from_code_dict = None
        self.cell_type_classifier_weights_file = None
        self.cell_type_classifier_model_file = None
        # indicate if only the raw traces can be displayed
        self.only_raw_traces_option = False


class MySessionButton(Button):

    def __init__(self, master):
        # ------ constants for controlling layout ------
        button_width = 10
        button_height = 10

        button_padx = "10m"  ### (2)
        button_pady = "1m"  ### (2)
        # -------------- end constants ----------------

        Button.__init__(self, master)
        self.configure(
            width=button_width,  ### (1)
            height=button_height,
            padx=button_padx,  ### (2)
            pady=button_pady  ### (2)
        )


def raise_above_all(window):
    """
    Take a window as argument (like tk.root()) and put it on front of all other
    Args:
        window:

    Returns:

    """
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)


def set_menu_from_list(keys, menu_tk, menu_variable, favorite_key):
    # Reset var and delete all old options
    menu_variable.set('')
    menu_tk['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    for choice in keys:
        menu_tk['menu'].add_command(label=choice, command=tk._setit(menu_variable, choice))
    if favorite_key is not None:
        menu_variable.set(favorite_key)


def load_menu_from_file(file_name, menu_tk, menu_variable, keyword_for_key=None):
    """
    Take a tkinter OptionMenu instance and load it using the fields of a matlab or npy file.
    Args:
        file_name: string
        menu_tk: OptionMenu instance
        menu_variable: Variable from the menu
        keyword_for_key: string, keyword, if found in one of the field, this field will be selected by default
        in the menu

    Returns: a list of string representing the options of the menu

    """
    favorite_key = None
    if file_name.endswith(".mat"):
        data = hdf5storage.loadmat(file_name)
        keys = []
        for key, value in data.items():
            # just to add non hidden data
            if not key.startswith("__") and (isinstance(value, np.ndarray)):
                # TODO: See to display the shape of the array in the menu
                keys.append(key)
                if keyword_for_key is not None:
                    if keyword_for_key in key:
                        favorite_key = key
                else:
                    favorite_key = key
        if (favorite_key is None) and (len(keys) > 0):
            favorite_key = keys[0]
    elif file_name.endswith(".npz"):
        data = np.load(file_name, allow_pickle=True)
        keys = list(data.keys())
        if keyword_for_key is not None:
            for key in keys:
                if keyword_for_key in key:
                    favorite_key = key
        else:
            favorite_key = keys[0]
        if (favorite_key is None) and (len(keys) > 0):
            favorite_key = keys[0]
    else:
        return []
    # print(f"keys {keys}")
    # Reset var and delete all old options
    menu_variable.set('')
    menu_tk['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    for choice in keys:
        menu_tk['menu'].add_command(label=choice, command=tk._setit(menu_variable, choice))
    if favorite_key is not None:
        menu_variable.set(favorite_key)

    return keys


class RawFormatOptionModule(tk.Frame):

    def __init__(self, button_text, label_text, with_file_dialog,
                 file_dialog_filetypes, file_dialog_title, root,
                 mandatory, with_only_label=False,
                 with_check_box=False, label_check_box=None,
                 check_box_active_by_default=True,
                 active_label_text=None,
                 with_option_menu=False,
                 with_spin_box=False,
                 menu_keyword_for_key=None,
                 fct_to_call_at_update=None,
                 last_path_open=None,
                 height_button=3, command_fct=None, default_path=None, master=None):
        # last_path_open is a list of one element

        tk.Frame.__init__(self, master=master)
        self.pack(side=TOP, expand=YES, fill=BOTH)

        self.button = MySessionButton(self)
        self.button["text"] = button_text
        self.button["fg"] = "red" if mandatory else "black"

        self.button.pack(side=LEFT)
        self.button.config(height=height_button)
        self.with_file_dialog = with_file_dialog
        self.button["command"] = event_lambda(self.button_action)

        empty_label = Label(self, text=" ")
        empty_label.pack(side=LEFT, expand=FALSE, fill=None)

        frame_for_label = self
        if with_option_menu:
            frame_for_label = Frame(self)
            frame_for_label.pack(side=LEFT,
                                 expand=YES,
                                 fill=BOTH)

        self.with_spin_box = with_spin_box
        if with_spin_box:
            self.var_spin_box = StringVar(frame_for_label)
            values_spin_box = [np.round(v, 2) for v in np.arange(0.05, 1, 0.05)]
            self.spin_box = Spinbox(frame_for_label,
                                    values=values_spin_box,
                                    fg="black", justify=CENTER,
                                    width=4, textvariable=self.var_spin_box,
                                    state="readonly")
            self.var_spin_box.set("0.5")
            self.spin_box.pack(side=LEFT)
            self.spin_box.pack_forget()
        else:
            self.label = Label(frame_for_label)
            self.label["text"] = label_text
            if with_option_menu:
                self.label.pack(side=TOP)
            else:
                self.label.pack(side=LEFT)

        self.with_check_box = with_check_box
        if with_option_menu:
            if with_check_box:
                check_box_frame = Frame(frame_for_label)
                check_box_frame.pack(side=TOP,
                                     expand=TRUE,
                                     fill=BOTH)

            self.menu_variable = StringVar(self)
            if with_check_box:
                self.menu = OptionMenu(check_box_frame, self.menu_variable, [])
            else:
                self.menu = OptionMenu(frame_for_label, self.menu_variable, [])
            self.menu.config(width=20)
            if with_check_box:
                self.menu.pack(side=LEFT)
            else:
                self.menu.pack(side=TOP)
            self.menu.pack_forget()
            self.menu_keys = []

            self.check_box_active_by_default = check_box_active_by_default
            self.is_check_box_active = check_box_active_by_default
            if with_check_box:
                label_check_box = label_check_box if label_check_box is not None else ""
                self.check_box_var = IntVar()
                self.check_box = Checkbutton(check_box_frame, text=label_check_box, variable=self.check_box_var,
                                             onvalue=1,
                                             offvalue=0)
                self.check_box["command"] = event_lambda(self.check_box_action)
                # zoom on by default
                if check_box_active_by_default:
                    self.check_box.select()

                self.check_box.pack(side=LEFT)
                self.check_box.pack_forget()

        self.file_name = None
        self.last_path_open = last_path_open
        self.default_path = default_path
        self.file_dialog_filetypes = file_dialog_filetypes
        self.file_dialog_title = file_dialog_title
        self.root = root
        self.fct_to_call_at_update = fct_to_call_at_update
        self.mandatory = mandatory
        self.with_option_menu = with_option_menu
        self.menu_keyword_for_key = menu_keyword_for_key
        self.activated = False
        self.exclusive_modules = []
        self.slave_module = None
        self.master_module = None
        self.with_only_label = with_only_label
        self.active_label_text = active_label_text

    def check_box_action(self):
        # using this method as check_box_var doesn't work (at least on Linux)
        self.is_check_box_active = not self.is_check_box_active

    def button_action(self):
        if self.master_module is not None:
            # master module need to be activated for the slave module to be activated
            if not self.master_module.activated:
                return

        if self.with_file_dialog:
            self.set_file_value()
        elif self.with_spin_box:
            if self.activated:
                self.deactivate()
            else:
                self.activate_spin_box()
        elif self.with_only_label:
            if self.activated:
                self.deactivate()
            else:
                self.activate_only_label()

    def activate_only_label(self, enabling_button=False):
        self.activated = True
        self.button["fg"] = "green"
        if enabling_button:
            self.button['state'] = 'normal'
        self.label["text"] = self.active_label_text
        if len(self.exclusive_modules) > 0:
            for module in self.exclusive_modules:
                module.deactivate()

    def activate_spin_box(self):
        self.activated = True
        self.button["fg"] = "green"
        self.spin_box.pack(side=LEFT)
        if len(self.exclusive_modules) > 0:
            for module in self.exclusive_modules:
                module.deactivate()

    def set_file_value(self, with_file_dialog=True, file_name=None):
        if with_file_dialog:
            if self.last_path_open[0] is not None:
                initial_dir = self.last_path_open
            else:
                initial_dir = self.default_path

            file_name = filedialog.askopenfilename(
                initialdir=initial_dir,
                filetypes=self.file_dialog_filetypes,
                title=self.file_dialog_title,
                parent=self.root)

            # to put the window on the top
            self.root.lift()

        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            if not self.mandatory:
                self.deactivate()
                if self.fct_to_call_at_update is not None:
                    self.fct_to_call_at_update()
            return

        if len(self.exclusive_modules) > 0:
            for module in self.exclusive_modules:
                module.deactivate()

        self.activated = True
        if self.with_option_menu:
            if file_name.endswith(".mat") or file_name.endswith(".npz"):
                self.menu_keys = load_menu_from_file(file_name=file_name, menu_tk=self.menu,
                                                     menu_variable=self.menu_variable,
                                                     keyword_for_key=self.menu_keyword_for_key)
                if self.with_check_box:
                    self.menu.pack(side=LEFT)
                else:
                    self.menu.pack(side=TOP)
            else:
                self.menu_variable.set('')
                self.menu['menu'].delete(0, 'end')
                self.menu.pack_forget()

            if self.with_check_box:
                self.check_box.pack(side=LEFT)

        self.button["fg"] = "green"
        self.file_name = file_name
        self.last_path_open[0], file_name_only = get_file_name_and_path(file_name)
        self.label["text"] = file_name_only
        if self.fct_to_call_at_update is not None:
            self.fct_to_call_at_update()

    def deactivate(self, disabling_button=False):
        """
        Deactivate the module
        Returns:

        """

        self.activated = False

        self.button["fg"] = "black"
        if disabling_button:
            self.button['state'] = DISABLED  # ''normal
        self.file_name = None
        if self.with_spin_box:
            self.spin_box.pack_forget()
            return
        else:
            self.label["text"] = ""
            if self.with_option_menu:
                self.menu_variable.set('')
                self.menu['menu'].delete(0, 'end')
                self.menu_keys = []
                self.menu.pack_forget()
        if self.with_check_box:
            self.check_box.pack_forget()
        # deactivating module that depend on this one
        if self.slave_module is not None:
            self.slave_module.deactivate()

    def add_exclusive_modules(self, exclusive_modules):
        """
        Means that only one among self and exclusive_modules can be activated at once.
        When one is activated, the other are deactivated
        Args:
            exclusive_modules: list of instance of RawFormatOptionModule

        Returns:

        """

        self.exclusive_modules.extend(exclusive_modules)

    def get_config_as_dict(self):
        """
        From the data gui in widgets, build a dictionnary used to save the parameters
        Returns:

        """
        config_dict = dict()
        if self.with_file_dialog:
            config_dict["file_name"] = self.file_name

        if self.with_option_menu:
            config_dict["menu_keys"] = self.menu_keys
            if len(self.menu_keys) > 0:
                config_dict["menu_key"] = self.menu_variable.get()
            if self.with_check_box:
                config_dict["check_box_var"] = self.is_check_box_active

        if self.with_only_label:
            config_dict["activated"] = self.activated

        if self.with_spin_box:
            config_dict["spin_box_value"] = float(self.spin_box.get())
            config_dict["activated"] = self.activated

        return config_dict

    def set_config_from_dict(self, config_dict):
        """
        From the data gui in widgets, build a dictionnary used to save the parameters
        Returns:

        """
        if self.with_file_dialog:
            self.file_name = config_dict.get("file_name", None)
            self.set_file_value(with_file_dialog=False, file_name=self.file_name)

        if self.with_option_menu:
            self.menu_keys = config_dict.get("menu_keys", [])
            menu_key = config_dict.get("menu_key", None)
            set_menu_from_list(keys=self.menu_keys, menu_tk=self.menu,
                               menu_variable=self.menu_variable, favorite_key=menu_key)
            if self.with_check_box:
                self.check_box_var.set(config_dict.get("check_box_var", int(self.check_box_active_by_default)))
                self.is_check_box_active = config_dict.get("check_box_var", bool(self.check_box_active_by_default))

        if self.with_only_label:
            self.activated = config_dict.get("activated", False)
            if self.activated:
                self.activate_only_label()

        if self.with_spin_box:
            spin_box_value = config_dict.get("spin_box_value", None)
            if spin_box_value is not None:
                self.var_spin_box.set(f"{spin_box_value}")
            self.activated = config_dict.get("activated", False)
            if self.activated:
                self.activate_spin_box()


class ChoiceRawFormatFrame(tk.Frame):

    def __init__(self, default_path=None, master=None):
        # ------ constants for controlling layout ------
        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        # -------------- end constants ----------------
        self.root = Tk()
        # self.root.protocol("WM_DELETE_WINDOW", self.validation_before_closing)
        # self.root.title(f"Session {session_number}")
        tk.Frame.__init__(self, master=self.root)
        self.pack(
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            padx=buttons_frame_padx,
            pady=buttons_frame_pady
        )
        self.default_path = default_path
        self.option_menu_variable = None
        # to avoid garbage collector
        self.buttons = dict()
        self.go_button = None
        self.last_path_open = [None]

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # ---- buttons and labels ----
        self.launch_gui_button = None
        self.button_frame = None
        self.canvas = None

        self.is_display_only_raw_traces_check_box_active = True
        self.display_only_raw_traces_check_box_var = None
        # self.check_box
        self.display_only_raw_traces_check_box = None

        # a module represent an instance of RawFormatOptionModule
        # key is a string representing the name of the module
        # and the value is the instance of RawFormatOptionModule
        self.modules_dict = dict()

        self.load_last_used_config_button = None
        self.load_config_button = None
        self.save_config_button = None

        # ---- files' name ----
        self.movie_file_name = None
        self.coords_file_name = None
        self.gt_file_name = None
        # file in which we save automatically the params of the last movie opened
        my_path = os.path.abspath(os.path.dirname(__file__))
        self.last_open_params_file = os.path.join(my_path, "last_open_params.yaml")

        # ----- data ---------
        self.predictions = None

        self.create_buttons()

    def __configure(self, event):
        # update the scrollbars to match the size of the inner frame
        # size = self.button_frame.winfo_reqwidth(), self.button_frame.winfo_reqheight()
        # self.canvas.config(scrollregion="0 0 %s %s" % size)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=min(self.screen_width, 600),
                              height=min(self.screen_height, 1000))

    def create_buttons(self):
        """
        Create buttons
        Returns:

        """
        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        hbar = Scrollbar(self, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)

        canvas = Canvas(self)
        self.canvas = canvas

        hbar.config(command=canvas.xview)
        vbar.config(command=canvas.yview)

        # canvas.config(width=300, height=300)
        canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        canvas.pack(side=LEFT, expand=True, fill=BOTH)
        # canvas.pack(side=TOP, anchor=NW, padx=10, pady=10)

        # reset the view
        # (always do this if you don't use scrollbars)
        # canvas.xview("moveto", 0)
        # canvas.yview("moveto", 0)

        # create the inner frame
        button_frame = Frame(canvas)
        self.button_frame = button_frame
        button_frame.pack(side=LEFT,
                          expand=True,
                          fill=BOTH)

        self.launch_gui_button = MySessionButton(button_frame)
        self.launch_gui_button["text"] = "Launch GUI"
        self.launch_gui_button['state'] = DISABLED
        self.launch_gui_button.config(height=3)
        self.launch_gui_button.pack(side=TOP)
        self.launch_gui_button["command"] = event_lambda(self.launch_exploratory_gui)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # ----------------------- LOADING / SAVING CONFIG SECTION -----------------------
        config_frame = Frame(button_frame)
        config_frame.pack(side=TOP,
                          expand=YES,
                          fill=BOTH)

        empty_label = Label(config_frame, text=" ")
        empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        if os.path.isfile(self.last_open_params_file):
            self.load_last_used_config_button = MySessionButton(config_frame)
            self.load_last_used_config_button["text"] = "Load last used params"
            self.load_last_used_config_button.pack(side=LEFT)
            self.load_last_used_config_button.config(height=2)
            self.load_last_used_config_button["command"] = event_lambda(self.load_last_used_config)

            empty_label = Label(config_frame, text="  ")
            empty_label.pack(side=LEFT, expand=FALSE, fill=None)

        self.load_config_button = MySessionButton(config_frame)
        self.load_config_button["text"] = "Load params"
        self.load_config_button.pack(side=LEFT)
        self.load_config_button.config(height=2)
        self.load_config_button["command"] = event_lambda(self.load_config)

        empty_label = Label(config_frame, text="  ")
        empty_label.pack(side=LEFT, expand=FALSE, fill=None)

        self.save_config_button = MySessionButton(config_frame)
        self.save_config_button["text"] = "Save params"
        self.save_config_button.pack(side=LEFT)
        self.save_config_button.config(height=2)
        self.save_config_button["command"] = event_lambda(self.save_config)

        empty_label = Label(config_frame, text=" ")
        empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.is_display_only_raw_traces_check_box_active = False
        self.display_only_raw_traces_check_box_var = IntVar()
        # self.check_box
        self.display_only_raw_traces_check_box = Checkbutton(button_frame, text="Display only raw fluorescence signal",
                                                   variable=self.display_only_raw_traces_check_box_var,
                                                   onvalue=1,
                                                   offvalue=0)
        self.display_only_raw_traces_check_box["command"] = event_lambda(self.display_only_raw_traces_check_box_action)
        # zoom on by default
        if self.is_display_only_raw_traces_check_box_active:
            self.display_only_raw_traces_check_box.select()
        self.display_only_raw_traces_check_box.pack(side=TOP)

        # ----------------------- BUTTONS TO SELECT DATA -----------------------

        self.modules_dict["movie"] = RawFormatOptionModule(button_text="Movie", label_text=" " * 50,
                                                           with_file_dialog=True,
                                                           file_dialog_filetypes=(
                                                               ("Tiff files", "*.tif"), ("Tiff files", "*.tiff")),
                                                           file_dialog_title="Select a movie", root=self.root,
                                                           mandatory=True,
                                                           fct_to_call_at_update=self.update_launch_gui_button,
                                                           last_path_open=self.last_path_open,
                                                           height_button=3, command_fct=None,
                                                           default_path=self.default_path,
                                                           master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["caiman_coords"] = RawFormatOptionModule(button_text="CaImAn coords",
                                                                   label_text=" " * 50, with_file_dialog=True,
                                                                   with_check_box=True,
                                                                   label_check_box="matlab indexing",
                                                                   file_dialog_filetypes=
                                                                   (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                    ("Matlab files", "*.mat")),
                                                                   file_dialog_title="Select cells coordinate",
                                                                   root=self.root,
                                                                   mandatory=False,
                                                                   fct_to_call_at_update=self.update_launch_gui_button,
                                                                   with_option_menu=True,
                                                                   last_path_open=self.last_path_open,
                                                                   height_button=3, command_fct=None,
                                                                   default_path=self.default_path,
                                                                   master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["suite2p_iscell"] = RawFormatOptionModule(button_text="Suite2p iscell",
                                                                    label_text=" " * 50, with_file_dialog=True,
                                                                    with_check_box=False,
                                                                    file_dialog_filetypes=
                                                                    (("Numpy files", "*.npy"),),
                                                                    file_dialog_title="Select iscell file",
                                                                    root=self.root,
                                                                    mandatory=False,
                                                                    fct_to_call_at_update=self.update_launch_gui_button,
                                                                    with_option_menu=False,
                                                                    last_path_open=self.last_path_open,
                                                                    height_button=3, command_fct=None,
                                                                    default_path=self.default_path,
                                                                    master=button_frame)

        self.modules_dict["suite2p_stat"] = RawFormatOptionModule(button_text="Suite2p stat",
                                                                  label_text=" " * 50, with_file_dialog=True,
                                                                  with_check_box=False,
                                                                  file_dialog_filetypes=
                                                                  (("Numpy files", "*.npy"),),
                                                                  file_dialog_title="Select stat file",
                                                                  root=self.root,
                                                                  mandatory=False,
                                                                  fct_to_call_at_update=self.update_launch_gui_button,
                                                                  with_option_menu=False,
                                                                  last_path_open=self.last_path_open,
                                                                  height_button=3, command_fct=None,
                                                                  default_path=self.default_path,
                                                                  master=button_frame)
        self.modules_dict["suite2p_spks"] = RawFormatOptionModule(button_text="Suite2p spikes",
                                                                  label_text=" " * 50, with_file_dialog=True,
                                                                  with_check_box=False,
                                                                  file_dialog_filetypes=
                                                                  (("Numpy files", "*.npy"),),
                                                                  file_dialog_title="Select spks file",
                                                                  root=self.root,
                                                                  mandatory=False,
                                                                  with_option_menu=False,
                                                                  last_path_open=self.last_path_open,
                                                                  height_button=3, command_fct=None,
                                                                  default_path=self.default_path,
                                                                  master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["fiji_coords"] = RawFormatOptionModule(button_text="Fiji coords",
                                                                   label_text=" " * 50, with_file_dialog=True,
                                                                   with_check_box=False,
                                                                   file_dialog_filetypes= (("Zip files", "*.zip"),
                                                                                           ("Roi files", "*.roi")),
                                                                   file_dialog_title="Select cells contours",
                                                                   root=self.root,
                                                                   mandatory=False,
                                                                   fct_to_call_at_update=self.update_launch_gui_button,
                                                                   with_option_menu=False,
                                                                   last_path_open=self.last_path_open,
                                                                   height_button=3, command_fct=None,
                                                                   default_path=self.default_path,
                                                                   master=button_frame)

        self.modules_dict["caiman_coords"].add_exclusive_modules([self.modules_dict["suite2p_iscell"],
                                                                  self.modules_dict["suite2p_stat"],
                                                                  self.modules_dict["suite2p_spks"],
                                                                  self.modules_dict["fiji_coords"]])
        self.modules_dict["fiji_coords"].add_exclusive_modules([self.modules_dict["suite2p_iscell"],
                                                                  self.modules_dict["suite2p_stat"],
                                                                  self.modules_dict["suite2p_spks"],
                                                                  self.modules_dict["caiman_coords"]])
        self.modules_dict["suite2p_iscell"].add_exclusive_modules([self.modules_dict["caiman_coords"],
                                                                   self.modules_dict["fiji_coords"]])
        self.modules_dict["suite2p_stat"].add_exclusive_modules([self.modules_dict["caiman_coords"],
                                                                 self.modules_dict["fiji_coords"]])
        self.modules_dict["suite2p_spks"].add_exclusive_modules([self.modules_dict["caiman_coords"],
                                                                 self.modules_dict["fiji_coords"]])

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["predictions"] = RawFormatOptionModule(button_text="Activity predictions",
                                                                 label_text=" " * 50, with_file_dialog=True,
                                                                 file_dialog_filetypes=
                                                                 (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                  ("Matlab files", "*.mat")),
                                                                 file_dialog_title="Select activity predictions",
                                                                 root=self.root,
                                                                 mandatory=False,
                                                                 with_option_menu=True,
                                                                 menu_keyword_for_key="predictions",
                                                                 last_path_open=self.last_path_open,
                                                                 height_button=3, command_fct=None,
                                                                 default_path=self.default_path,
                                                                 master=button_frame)

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["classifier_model"] = RawFormatOptionModule(button_text="Classifier model",
                                                                      label_text=" " * 50, with_file_dialog=True,
                                                                      file_dialog_filetypes=
                                                                      (("Json file", "*.json"),),
                                                                      file_dialog_title="Select json model file",
                                                                      root=self.root,
                                                                      mandatory=False,
                                                                      with_option_menu=False,
                                                                      last_path_open=self.last_path_open,
                                                                      height_button=3, command_fct=None,
                                                                      default_path=self.default_path,
                                                                      master=button_frame)

        self.modules_dict["classifier_weights"] = RawFormatOptionModule(button_text="Classifier Weights",
                                                                        label_text=" " * 50, with_file_dialog=True,
                                                                        file_dialog_filetypes=(("h5 file", "*.h5"),),
                                                                        file_dialog_title="Select h5 weights file",
                                                                        root=self.root,
                                                                        mandatory=False,
                                                                        with_option_menu=False,
                                                                        last_path_open=self.last_path_open,
                                                                        height_button=3, command_fct=None,
                                                                        default_path=self.default_path,
                                                                        master=button_frame)

        self.modules_dict["classifier_weights"].add_exclusive_modules([self.modules_dict["predictions"]])
        self.modules_dict["classifier_model"].add_exclusive_modules([self.modules_dict["predictions"]])
        self.modules_dict["predictions"].add_exclusive_modules([self.modules_dict["classifier_weights"],
                                                                self.modules_dict["classifier_model"]])

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["gt_file"] = RawFormatOptionModule(button_text="Ground Truth (GT)",
                                                             label_text=" " * 50, with_file_dialog=True,
                                                             file_dialog_filetypes=
                                                             (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                              ("Matlab files", "*.mat")),
                                                             file_dialog_title="Select a GT file",
                                                             root=self.root,
                                                             mandatory=False,
                                                             with_option_menu=True,
                                                             menu_keyword_for_key="raster",
                                                             last_path_open=self.last_path_open,
                                                             height_button=3, command_fct=None,
                                                             default_path=self.default_path,
                                                             master=button_frame)

        self.modules_dict["gt_onsets_file"] = RawFormatOptionModule(button_text="Ground Truth onsets",
                                                                    label_text=" " * 50, with_file_dialog=True,
                                                                    file_dialog_filetypes=
                                                                    (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                     ("Matlab files", "*.mat")),
                                                                    file_dialog_title="Select a GT onsets file",
                                                                    root=self.root,
                                                                    mandatory=False,
                                                                    with_option_menu=True,
                                                                    menu_keyword_for_key="onsets",
                                                                    last_path_open=self.last_path_open,
                                                                    height_button=3, command_fct=None,
                                                                    default_path=self.default_path,
                                                                    master=button_frame)

        self.modules_dict["gt_peaks_file"] = RawFormatOptionModule(button_text="Ground Truth peaks",
                                                                   label_text=" " * 50, with_file_dialog=True,
                                                                   file_dialog_filetypes=
                                                                   (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                    ("Matlab files", "*.mat")),
                                                                   file_dialog_title="Select a GT peaks file",
                                                                   root=self.root,
                                                                   mandatory=False,
                                                                   with_option_menu=True,
                                                                   menu_keyword_for_key="peaks",
                                                                   last_path_open=self.last_path_open,
                                                                   height_button=3, command_fct=None,
                                                                   default_path=self.default_path,
                                                                   master=button_frame)

        # gt_pred_frame = Frame(button_frame)
        # gt_pred_frame.pack(side=TOP,
        #                    expand=YES,
        #                    fill=BOTH)

        self.modules_dict["gt_pred"] = RawFormatOptionModule(button_text="Predictions as GT",
                                                             label_text=" " * 50, with_spin_box=True,
                                                             with_file_dialog=None,
                                                             file_dialog_filetypes=None,
                                                             file_dialog_title=None,
                                                             root=self.root,
                                                             mandatory=False,
                                                             with_option_menu=False,
                                                             last_path_open=self.last_path_open,
                                                             height_button=3, command_fct=None,
                                                             default_path=self.default_path,
                                                             master=button_frame)
        self.modules_dict["predictions"].slave_module = self.modules_dict["gt_pred"]
        self.modules_dict["gt_pred"].master_module = self.modules_dict["predictions"]

        # automatic_gt_frame = Frame(button_frame)
        # automatic_gt_frame.pack(side=TOP,
        #                         expand=YES,
        #                         fill=BOTH)

        self.modules_dict["automatic_gt"] = RawFormatOptionModule(button_text="Automatic GT",
                                                                  label_text=" " * 50, with_only_label=True,
                                                                  active_label_text="automatic GT",
                                                                  with_file_dialog=None,
                                                                  file_dialog_filetypes=None,
                                                                  file_dialog_title=None,
                                                                  root=self.root,
                                                                  mandatory=False,
                                                                  with_option_menu=False,
                                                                  last_path_open=self.last_path_open,
                                                                  height_button=3, command_fct=None,
                                                                  default_path=self.default_path,
                                                                  master=button_frame)
        self.modules_dict["automatic_gt"].add_exclusive_modules([self.modules_dict["gt_file"],
                                                                 self.modules_dict["gt_pred"],
                                                                 self.modules_dict["gt_onsets_file"],
                                                                 self.modules_dict["gt_peaks_file"]])
        self.modules_dict["gt_file"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                            self.modules_dict["gt_pred"],
                                                            self.modules_dict["gt_onsets_file"],
                                                            self.modules_dict["gt_peaks_file"]])
        self.modules_dict["gt_pred"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                            self.modules_dict["gt_file"],
                                                            self.modules_dict["gt_onsets_file"],
                                                            self.modules_dict["gt_peaks_file"]])

        self.modules_dict["gt_onsets_file"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                                   self.modules_dict["gt_file"],
                                                                   self.modules_dict["gt_pred"]])

        self.modules_dict["gt_peaks_file"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                                  self.modules_dict["gt_file"],
                                                                  self.modules_dict["gt_pred"]])
        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # --------------- Raster 1 section  ---------------
        self.modules_dict["raster_1"] = RawFormatOptionModule(button_text="Raster 1",
                                                              label_text=" " * 50, with_file_dialog=True,
                                                              file_dialog_filetypes=
                                                              (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                               ("Matlab files", "*.mat")),
                                                              file_dialog_title="Select raster 1",
                                                              root=self.root,
                                                              mandatory=False,
                                                              with_option_menu=True,
                                                              menu_keyword_for_key="raster",
                                                              last_path_open=self.last_path_open,
                                                              height_button=3, command_fct=None,
                                                              default_path=self.default_path,
                                                              master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # --------------- Raster 2 section  ---------------
        self.modules_dict["raster_2"] = RawFormatOptionModule(button_text="Raster 2",
                                                              label_text=" " * 50, with_file_dialog=True,
                                                              file_dialog_filetypes=
                                                              (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                               ("Matlab files", "*.mat")),
                                                              file_dialog_title="Select raster 2",
                                                              root=self.root,
                                                              mandatory=False,
                                                              with_option_menu=True,
                                                              menu_keyword_for_key="raster",
                                                              last_path_open=self.last_path_open,
                                                              height_button=3, command_fct=None,
                                                              default_path=self.default_path,
                                                              master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["cell_type_yaml_file"] = RawFormatOptionModule(button_text="Cell type config",
                                                                         label_text=" " * 50, with_file_dialog=True,
                                                                         file_dialog_filetypes=
                                                                         (("Yaml files", "*.yaml"),
                                                                          ("Yaml files", "*.yml")),
                                                                         file_dialog_title="Select cell type config",
                                                                         root=self.root,
                                                                         mandatory=False,
                                                                         with_option_menu=True,
                                                                         last_path_open=self.last_path_open,
                                                                         height_button=3, command_fct=None,
                                                                         default_path=self.default_path,
                                                                         master=button_frame)

        self.modules_dict["cell_type_predictions"] = RawFormatOptionModule(button_text="Cell type predictions",
                                                                           label_text=" " * 50, with_file_dialog=True,
                                                                           file_dialog_filetypes=
                                                                           (("Numpy files", "*.npy"),
                                                                            ("Numpy files", "*.npz"),
                                                                            ("Matlab files", "*.mat")),
                                                                           file_dialog_title="Select cells predictions",
                                                                           root=self.root,
                                                                           mandatory=False,
                                                                           with_option_menu=False,
                                                                           menu_keyword_for_key="predictions",
                                                                           last_path_open=self.last_path_open,
                                                                           height_button=3, command_fct=None,
                                                                           default_path=self.default_path,
                                                                           master=button_frame)

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["cell_type_classifier_model"] = RawFormatOptionModule(
            button_text="Cell type model",
            label_text=" " * 50, with_file_dialog=True,
            file_dialog_filetypes=
            (("Json file", "*.json"),),
            file_dialog_title="Select json model file",
            root=self.root,
            mandatory=False,
            with_option_menu=False,
            last_path_open=self.last_path_open,
            height_button=3, command_fct=None,
            default_path=self.default_path,
            master=button_frame)

        self.modules_dict["cell_type_classifier_weights"] = RawFormatOptionModule(
            button_text="Cell type weights",
            label_text=" " * 50,
            with_file_dialog=True,
            file_dialog_filetypes=(
                ("h5 file", "*.h5"),),
            file_dialog_title="Select h5 weights file",
            root=self.root,
            mandatory=False,
            with_option_menu=False,
            last_path_open=self.last_path_open,
            height_button=3, command_fct=None,
            default_path=self.default_path,
            master=button_frame)
        #
        # self.modules_dict["cell_type_classifier_weights"].add_exclusive_modules(
        #     [self.modules_dict["cell_type_predictions"]])
        # self.modules_dict["cell_type_classifier_model"].add_exclusive_modules(
        #     [self.modules_dict["cell_type_predictions"]])
        # self.modules_dict["cell_type_predictions"].add_exclusive_modules(
        #     [self.modules_dict["cell_type_classifier_weights"],
        #      self.modules_dict["cell_type_classifier_model"]])
        self.modules_dict["cell_type_yaml_file"].slave_module = self.modules_dict["cell_type_predictions"]
        self.modules_dict["cell_type_yaml_file"].slave_module = self.modules_dict["cell_type_classifier_weights"]
        self.modules_dict["cell_type_yaml_file"].slave_module = self.modules_dict["cell_type_classifier_model"]
        self.modules_dict["cell_type_predictions"].master_module = self.modules_dict["cell_type_yaml_file"]
        self.modules_dict["cell_type_classifier_weights"].master_module = self.modules_dict["cell_type_yaml_file"]
        self.modules_dict["cell_type_classifier_model"].master_module = self.modules_dict["cell_type_yaml_file"]

        # track changes to its size
        button_frame.bind('<Configure>', self.__configure)

        # place the frame inside the canvas (this also
        # runs the __configure method)
        self.canvas.create_window(0, 0, window=button_frame, anchor=NW)

    def display_only_raw_traces_check_box_action(self):
        # using this method as check_box_var doesn't work (at least on Linux)
        self.is_display_only_raw_traces_check_box_active = not self.is_display_only_raw_traces_check_box_active

    def launch_exploratory_gui(self):
        """

        Returns:

        """
        # first we check if the data is correct

        # message box display
        # messagebox.showerror("Error", "Error message")
        # messagebox.showwarning("Warning", "Warning message")
        # messagebox.showinfo("Information", "Informative message")

        data_and_param = DataAndParam()

        movie_file_name = self.modules_dict["movie"].file_name

        data_and_param.ci_movie_file_name = movie_file_name

        if self.default_path is None:
            self.default_path, _ = get_file_name_and_path(movie_file_name)

        # we normalize the movie for the classifier
        non_norm_tiff_movie, tiff_movie = load_movie(file_name=movie_file_name, with_normalization=True,
                                                     verbose=True, both_instances=True)
        avg_cell_map_img = np.mean(tiff_movie, axis=0)
        n_frames = tiff_movie.shape[0]

        spks_file_name = None
        is_cell_file_name = None
        if self.modules_dict["caiman_coords"].activated:
            coords_file_name = self.modules_dict["caiman_coords"].file_name
            attr_name = None
            if self.modules_dict["caiman_coords"].with_option_menu:
                attr_name = self.modules_dict["caiman_coords"].menu_variable.get()

            coords_data = load_data_from_npy_or_mat_file(file_name=coords_file_name, data_descr="Caiman coords",
                                                         attr_name=attr_name)
            if coords_file_name.endswith(".mat"):
                coords_data = coords_data[0]

            matlab_indexing = bool(self.modules_dict["caiman_coords"].is_check_box_active)
            # print(f'matlab_indexing {self.modules_dict["caiman_coords"].is_check_box_active}')
            # now creating CellsCoord instance
            coord_obj = CellsCoord(coords=coords_data, pixel_masks=None, nb_lines=tiff_movie.shape[1],
                                   nb_col=tiff_movie.shape[2],
                                   from_matlab=matlab_indexing, invert_xy_coord=False)
        elif self.modules_dict["fiji_coords"].activated:
            coords_file_name = self.modules_dict["fiji_coords"].file_name
            coords_data = get_coords_extracted_from_fiji(file_name=coords_file_name)
            coord_obj = CellsCoord(coords=coords_data, pixel_masks=None, nb_lines=tiff_movie.shape[1],
                                   nb_col=tiff_movie.shape[2],
                                   from_matlab=True, invert_xy_coord=False)
        elif self.modules_dict["suite2p_stat"].activated:
            is_cell_file_name = self.modules_dict["suite2p_iscell"].file_name
            stat_file_name = self.modules_dict["suite2p_stat"].file_name
            coord_obj = create_cells_coord_from_suite_2p(is_cell_file_name=is_cell_file_name,
                                                         stat_file_name=stat_file_name,
                                                         movie_dimensions=tiff_movie.shape[1:])
            spks_file_name = self.modules_dict["suite2p_spks"].file_name
        n_cells = coord_obj.n_cells
        # print(f"n_cells {n_cells}")
        other_rasters = []
        if self.modules_dict["raster_1"].activated:
            file_name = self.modules_dict["raster_1"].file_name
            attr_name = None
            if self.modules_dict["raster_1"].with_option_menu:
                attr_name = self.modules_dict["raster_1"].menu_variable.get()

            raster_1_data = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Raster 1",
                                                           attr_name=attr_name)

            # first we check that the data fit the movie dimension and the numer of cells
            if raster_1_data.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Raster 1 dimensions {raster_1_data.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            other_rasters.append(raster_1_data)

        if self.modules_dict["raster_2"].activated:
            file_name = self.modules_dict["raster_2"].file_name
            attr_name = None
            if self.modules_dict["raster_2"].with_option_menu:
                attr_name = self.modules_dict["raster_2"].menu_variable.get()

            raster_2_data = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Raster 2",
                                                           attr_name=attr_name)
            if raster_2_data.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Raster 2 dimensions {raster_2_data.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            other_rasters.append(raster_2_data)

        if spks_file_name is not None:
            is_cell = None
            if is_cell_file_name is not None:
                is_cell = np.load(is_cell_file_name,
                                  allow_pickle=True)
            spks_suite2p = np.load(spks_file_name,
                                   allow_pickle=True)
            spks_filtered = np.zeros((n_cells, spks_suite2p.shape[1]))
            real_cell_index = 0
            for cell in np.arange(len(spks_suite2p)):
                if is_cell is not None:
                    if is_cell[cell][0] == 0:
                        continue
                spks_filtered[real_cell_index] = spks_suite2p[cell]
                real_cell_index += 1
            other_rasters.append(spks_filtered)


        raster_dur = None
        if self.modules_dict["predictions"].activated:
            file_name = self.modules_dict["predictions"].file_name
            attr_name = None
            if self.modules_dict["predictions"].with_option_menu:
                attr_name = self.modules_dict["predictions"].menu_variable.get()

            predictions = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Predictions",
                                                         attr_name=attr_name)
            if predictions.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Predictions dimensions {predictions.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            data_and_param.classifier_predictions = predictions

            if self.modules_dict["gt_pred"].activated:
                # then we produce the raster dur based on the predictions using threshold the prediction_threshold
                prediction_threshold = 0.5
                predicted_raster_dur = np.zeros((n_cells, n_frames), dtype="int8")

                for cell in np.arange(n_cells):
                    predicted_raster_dur[cell, predictions[cell] >= prediction_threshold] = 1
                raster_dur = predicted_raster_dur

        if self.modules_dict["gt_file"].activated:
            file_name = self.modules_dict["gt_file"].file_name
            attr_name = None
            if self.modules_dict["gt_file"].with_option_menu:
                attr_name = self.modules_dict["gt_file"].menu_variable.get()

            raster_dur = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="GT file",
                                                        attr_name=attr_name)
            if raster_dur.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"GT file dimensions {raster_dur.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return

        onsets = None
        peaks = None
        if self.modules_dict["gt_onsets_file"].activated:
            if not self.modules_dict["gt_peaks_file"].activated:
                messagebox.showerror("Error", f"GT onsets and peaks file need to be both specified")
                return

            file_name = self.modules_dict["gt_onsets_file"].file_name
            attr_name = None
            if self.modules_dict["gt_onsets_file"].with_option_menu:
                attr_name = self.modules_dict["gt_onsets_file"].menu_variable.get()

            onsets = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="GT onsets file",
                                                    attr_name=attr_name)
            if onsets.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"GT onsets file dimensions {raster_dur.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return

            file_name = self.modules_dict["gt_peaks_file"].file_name
            attr_name = None
            if self.modules_dict["gt_peaks_file"].with_option_menu:
                attr_name = self.modules_dict["gt_peaks_file"].menu_variable.get()

            peaks = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="GT peaks file",
                                                   attr_name=attr_name)
            if peaks.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"GT peaks file dimensions {raster_dur.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return

            # now building raster_dur
            raster_dur = build_raster_dur_from_onsets_peaks(onsets=onsets, peaks=peaks)

        if self.modules_dict["gt_peaks_file"].activated:
            if not self.modules_dict["gt_onsets_file"].activated:
                messagebox.showerror("Error", f"GT onsets and peaks file need to be both specified")
                return

        if raster_dur is not None:
            if onsets is None:
                onsets = np.zeros((n_cells, n_frames), dtype="int8")
                peaks = np.zeros((n_cells, n_frames), dtype="int8")
                for cell in np.arange(n_cells):
                    transient_periods = get_continous_time_periods(raster_dur[cell])
                    for transient_period in transient_periods:
                        onset = transient_period[0]
                        peak = transient_period[1]
                        # if onset == peak:
                        #     print("onset == peak")
                        onsets[cell, onset] = 1
                        peaks[cell, peak] = 1
            data_and_param.peak_nums = peaks
            data_and_param.spike_nums = onsets

        if self.modules_dict["classifier_model"].activated and self.modules_dict["classifier_weights"].activated:
            classifier_model_file = self.modules_dict["classifier_model"].file_name
            data_and_param.classifier_model_file = classifier_model_file
            classifier_weights_file = self.modules_dict["classifier_weights"].file_name
            data_and_param.classifier_weights_file = classifier_weights_file

        data_and_param.tiff_movie = tiff_movie
        data_and_param.non_norm_tiff_movie = non_norm_tiff_movie
        data_and_param.coord_obj = coord_obj
        data_and_param.avg_cell_map_img = avg_cell_map_img
        data_and_param.raw_traces = coord_obj.build_raw_traces_from_movie(movie=tiff_movie)
        # smoothing the trace, but no demixing
        data_and_param.traces = np.copy(data_and_param.raw_traces)
        do_traces_smoothing(data_and_param.traces)
        data_and_param.only_raw_traces_option = self.is_display_only_raw_traces_check_box_active

        data_and_param.other_rasters = other_rasters

        # computing all potential peaks and onset from smooth_trace
        all_potential_peaks = np.zeros((n_cells, n_frames), dtype="int8")
        all_potential_onsets = np.zeros((n_cells, n_frames), dtype="int8")
        # then we do an automatic detection
        for cell in np.arange(n_cells):
            peaks, properties = signal.find_peaks(x=data_and_param.traces[cell], distance=2)
            all_potential_peaks[cell, peaks] = 1

        for cell in np.arange(n_cells):
            onsets = []
            diff_values = np.diff(data_and_param.traces[cell])
            for index, value in enumerate(diff_values):
                if index == (len(diff_values) - 1):
                    continue
                if value < 0:
                    if diff_values[index + 1] >= 0:
                        onsets.append(index + 1)
            all_potential_onsets[cell, np.array(onsets)] = 1
        data_and_param.all_potential_peaks = all_potential_peaks
        data_and_param.all_potential_onsets = all_potential_onsets

        if self.modules_dict["automatic_gt"].activated:
            # we fill it with all potential peaks and onsets
            data_and_param.peak_nums = data_and_param.all_potential_peaks
            data_and_param.spike_nums = data_and_param.all_potential_onsets
        elif data_and_param.peak_nums is None:
            # otherwise empty detection
            data_and_param.peak_nums = np.zeros((coord_obj.n_cells, n_frames), dtype="int8")
            data_and_param.spike_nums = np.zeros((coord_obj.n_cells, n_frames), dtype="int8")

        if self.modules_dict["cell_type_yaml_file"].activated:
            cell_type_yaml_file = self.modules_dict["cell_type_yaml_file"].file_name
            cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
                read_cell_type_categories_yaml_file(yaml_file=cell_type_yaml_file, using_multi_class=1)
            # cell types to display
            data_and_param.cell_types_for_classifier = list(cell_type_from_code_dict.values())
            data_and_param.cell_type_from_code_dict = cell_type_from_code_dict
            if multi_class_arg or (len(cell_type_from_code_dict) > 2):
                data_and_param.cell_type_classifier_category = "multi_class"
            else:
                data_and_param.cell_type_classifier_category = "binary"
            if self.modules_dict["cell_type_predictions"].activated:
                cell_type_predictions_file_name = self.modules_dict["cell_type_predictions"].file_name

                cell_type_predictions = load_data_from_npy_or_mat_file(file_name=cell_type_predictions_file_name,
                                                                       data_descr="Cell type predictions",
                                                                       attr_name="predictions")
                if not cell_type_predictions_file_name.endswith(".npy"):
                    cells = load_data_from_npy_or_mat_file(file_name=cell_type_predictions_file_name,
                                                           data_descr="Cell type predictions",
                                                           attr_name="cells")
                else:
                    cells = np.arange(len(cell_type_predictions))
                # all cells might not have been predicted, so we just check if the number of cells predicted
                # is not greater than the number of cells available

                # TODO: See which dimension to check ?
                if len(cell_type_predictions) > n_cells:
                    messagebox.showerror("Error", f"Cell type predictions dimensions {len(cell_type_predictions)} "
                                                  f"is superior to "
                                                  f"the number of ROIs {coord_obj.n_cells}")
                    return

                # dict with key being the cell id, and value being a dict with key the cell_type and value the prediction
                cell_type_classifier_predictions = dict()
                for cell_index, cell in enumerate(cells):
                    cell_type_classifier_predictions[cell] = dict()
                    cell_type_prediction = cell_type_predictions[cell_index]
                    if isinstance(cell_type_prediction, float):
                        pass
                    else:
                        for cell_type_code, pred_value in enumerate(cell_type_prediction):
                            cell_type = cell_type_from_code_dict[cell_type_code]
                            cell_type_classifier_predictions[cell][cell_type] = pred_value

                data_and_param.cell_type_classifier_predictions = cell_type_classifier_predictions
                # TODO: See to change predictions according to info in yaml file
                # TODO: Ideally data_and_param.cell_type_classifier_predictions will be a dict
                #  with key the cell id and value a dict with key the cell_type and value a float
                #  representing the value
                #  using then data_and_param.cell_type_classifier_category to determine how to get the result
                # TODO: Make sure the predictions are compatible with the yaml file info
                # data_and_param.cell_type_classifier_predictions = cell_type_predictions
            elif self.modules_dict["cell_type_classifier_weights"].activated:
                if not self.modules_dict["cell_type_classifier_model"].activated:
                    messagebox.showerror("Error", f"Cell type classifier weight and moddel files need to "
                                                  f"be both specified")
                    return
                data_and_param.cell_type_classifier_weights_file = \
                    self.modules_dict["cell_type_classifier_weights"].file_name
                data_and_param.cell_type_classifier_model_file = \
                    self.modules_dict["cell_type_classifier_model"].file_name

        self.save_config(file_name=self.last_open_params_file)

        f = ManualOnsetFrame(data_and_param=data_and_param, default_path=self.default_path)
        f.mainloop()

    def load_last_used_config(self):
        with open(self.last_open_params_file, 'r') as stream:
            args_from_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        if args_from_yaml is not None:
            self.set_config_from_dict(args_from_yaml)

    def load_config(self):
        """

        Returns: None

        """
        if self.last_path_open[0] is not None:
            initial_dir = self.last_path_open[0]
        else:
            initial_dir = self.default_path

        file_name = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=(("YAML files", "*.yml"), ("YAML files", "*.yaml")),
            title="Load configuration",
            parent=self.root)

        # to put the window on the top
        self.root.lift()

        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            return None

        with open(file_name, 'r') as stream:
            args_from_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        if args_from_yaml is not None:
            self.set_config_from_dict(args_from_yaml)
        # setting a new default_path
        self.default_path, _ = get_file_name_and_path(file_name)

    def save_config(self, file_name=None):
        if self.last_path_open[0] is not None:
            initial_dir = self.last_path_open[0]
        else:
            initial_dir = self.default_path

        if file_name is None:
            file_name = filedialog.asksaveasfilename(
                initialdir=initial_dir,
                filetypes=(("YAML files", "*.yml"), ("YAML files", "*.yaml")),
                title="Save configuration",
                parent=self.root)

        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            return

        if (not file_name.endswith(".yml")) and (not file_name.endswith(".yaml")):
            file_name = file_name + ".yaml"

        with open(file_name, 'w') as outfile:
            yaml.dump(self.get_config_as_dict(), outfile, default_flow_style=False)

    def get_config_as_dict(self):
        """
        From the data gui in widgets, build a dictionnary used to save the paramters
        Returns:

        """
        config_dict = dict()

        for name_module, module in self.modules_dict.items():
            config_dict[name_module] = module.get_config_as_dict()

        return config_dict

    def set_config_from_dict(self, config_dict):
        """
        From the data gui in widgets, build a dictionnary used to save the parameters
        Returns:

        """
        for name_module, module_config in config_dict.items():
            self.modules_dict[name_module].set_config_from_dict(module_config)
        # TODO: verify if files exists

    def update_launch_gui_button(self):
        """
        Update the launch gui button depending on the file being selected
        Returns:

        """
        if self.modules_dict["movie"].activated and (self.modules_dict["caiman_coords"].activated or
                                                     self.modules_dict["suite2p_stat"].activated or
                                                     self.modules_dict["fiji_coords"].activated):
            self.launch_gui_button['state'] = "normal"
        else:
            self.launch_gui_button['state'] = DISABLED


def load_data_from_npy_or_mat_file(file_name, data_descr, attr_name=None):
    """
    Load data from a numpy or matlab file (.npz, .npz or .mat)
    Args:
        file_name:
        data_descr: string used to display error message if the file is not in the good format
        attr_name:

    Returns:


    """
    if file_name.endswith(".npy"):
        data = np.load(file_name, allow_pickle=True)
    elif file_name.endswith(".npz"):
        data = np.load(file_name, allow_pickle=True)
        data = data[attr_name]
    elif file_name.endswith(".mat"):  # .mat
        data = hdf5storage.loadmat(file_name)
        data = data[attr_name]
    else:
        messagebox.showerror("Error", "Caiman coords file extension must be .npy, .npz or .mat")
        return

    return data


class ChoiceFormatFrame(tk.Frame):

    def __init__(self, default_path=None, master=None):
        # ------ constants for controlling layout ------
        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        # -------------- end constants ----------------
        tk.Frame.__init__(self, master)
        self.pack(
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            padx=buttons_frame_padx,
            pady=buttons_frame_pady,
        )

        # to avoid garbage collector
        self.format_selection_buttons = dict()
        self.default_path = default_path
        self.create_buttons()

    def create_buttons(self):
        colors = ["blue", "red", "green"]
        # for c in colors:
        #     ttk.Style().configure(f'black/{c}.TButton', foreground='black', background=f'{c}')
        data_to_load = ["RAW DATA", "CINAC DATA", "NWB"]

        button_frame = Frame(self)
        button_frame.pack(side=TOP,
                          expand=YES,
                          fill=BOTH)  #
        # height=50,

        for i, format_str in enumerate(data_to_load):
            # create a frame for each mouse, so the button will on the same line
            button = MySessionButton(button_frame)
            button["text"] = f'{format_str}'
            button["fg"] = colors[i]
            # button['state'] = "normal"
            # c = colors[i % len(colors)]
            # button["style"] = f'black/{c}.TButton'
            button.pack(side=LEFT)
            self.format_selection_buttons[format_str] = button
            button["command"] = event_lambda(self.open_option_format_frame, format_str=format_str)

    def open_option_format_frame(self, format_str):
        if format_str == "RAW DATA":
            f = ChoiceRawFormatFrame(default_path=self.default_path)
            f.mainloop()
        elif format_str == "CINAC DATA":
            f = ChoiceCinacFormatFrame(default_path=self.default_path)
            f.mainloop()
        elif format_str == "NWB":
            if NWB_PACKAGE_AVAILABLE:
                f = ChoiceNwbFormatFrame(default_path=self.default_path)
                f.mainloop()
            else:
                messagebox.showerror("Error", f"You need to install 'pynwb' package to read NWB files.")


def display_loading_window(message, fct_to_run, args_for_fct):
    result = None

    def task():
        global result
        # The window will stay open until this function call ends.
        result = fct_to_run(**args_for_fct)
        root.destroy()
        return result

    root = tk.Tk()
    root.title("Example")

    label = tk.Label(root, text=message)
    label.pack()

    root.after(200, task)
    root.mainloop()

    return result


class ChoiceNwbFormatFrame(tk.Frame):

    def __init__(self, default_path=None, master=None):
        # ------ constants for controlling layout ------
        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        # -------------- end constants ----------------
        self.root = Tk()
        # self.root.protocol("WM_DELETE_WINDOW", self.validation_before_closing)
        # self.root.title(f"Session {session_number}")
        tk.Frame.__init__(self, master=self.root)
        self.pack(
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            padx=buttons_frame_padx,
            pady=buttons_frame_pady
        )
        self.default_path = default_path
        self.option_menu_variable = None
        self.last_path_open = [None]

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # ---- buttons and labels ----
        self.launch_gui_button = None
        self.select_nwb_file_button = None
        self.button_frame = None
        self.canvas = None
        self.height_button = 3

        # a module represent an instance of RawFormatOptionModule
        # key is a string representing the name of the module
        # and the value is the instance of RawFormatOptionModule
        self.modules_dict = dict()

        # ----- data ---------
        self.last_path_open = [None]
        self.nwb_file_name = None
        self.nwb_data = None
        self.ci_movies_dict = None
        # take path to segmentation as keys and store the list used to get it from NWB
        self.segmentation_str_to_list = dict()
        self.neuronal_data_to_list = dict()

        # ----- creating the GUI panel ----

        # scrollbars
        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        hbar = Scrollbar(self, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)

        canvas = Canvas(self)
        self.canvas = canvas

        hbar.config(command=canvas.xview)
        vbar.config(command=canvas.yview)

        # canvas.config(width=300, height=300)
        canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        canvas.pack(side=LEFT, expand=True, fill=BOTH)
        # canvas.pack(side=TOP, anchor=NW, padx=10, pady=10)0)

        # create the inner frame
        button_frame = Frame(canvas)
        self.button_frame = button_frame
        button_frame.pack(side=LEFT,
                          expand=True,
                          fill=BOTH)

        self.launch_gui_button = MySessionButton(button_frame)
        self.launch_gui_button["text"] = "Launch GUI"
        self.launch_gui_button['state'] = DISABLED
        self.launch_gui_button.config(height=self.height_button)
        self.launch_gui_button.pack(side=TOP)
        self.launch_gui_button["command"] = event_lambda(self.launch_exploratory_gui)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # ------- CINAC FRAME -------
        self.select_nwb_frame = Frame(self.button_frame)
        self.select_nwb_frame.pack(side=TOP, expand=YES, fill=BOTH)

        self.nwb_button = MySessionButton(self.select_nwb_frame)
        self.nwb_button["text"] = "Select NWB file"
        self.nwb_button["fg"] = "black"

        self.nwb_button.pack(side=LEFT)
        self.nwb_button.config(height=self.height_button)
        self.nwb_button["command"] = event_lambda(self.select_nwb_file)

        empty_label = Label(self.select_nwb_frame, text=" ")
        empty_label.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.nwb_info_frame = Frame(self.select_nwb_frame)
        self.nwb_info_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        self.nwb_label_frame = Frame(self.nwb_info_frame)
        self.nwb_label_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.nwb_label = Label(self.nwb_label_frame)
        self.nwb_label["text"] = " " * 10
        self.nwb_label.pack(side=LEFT)
        empty_label = Label(self.nwb_label_frame, text=" ")
        empty_label.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.nwb_movie_frame = Frame(self.nwb_info_frame)
        self.nwb_movie_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.nwb_movie_label = Label(self.nwb_movie_frame)
        self.nwb_movie_label["text"] = " " * 10
        self.nwb_movie_label.pack(side=LEFT)

        self.ci_movie_menu_variable = StringVar(self)
        self.ci_movie_menu = OptionMenu(self.nwb_movie_frame, self.ci_movie_menu_variable, [])
        self.ci_movie_menu.config(width=20)
        self.ci_movie_menu.pack(side=LEFT)
        self.ci_movie_menu.pack_forget()

        self.nwb_segmentation_frame = Frame(self.nwb_info_frame)
        self.nwb_segmentation_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.segmentation_label = Label(self.nwb_segmentation_frame)
        self.segmentation_label["text"] = " " * 10
        self.segmentation_label.pack(side=LEFT)

        self.segmentation_menu_variable = StringVar(self)
        self.segmentation_menu = OptionMenu(self.nwb_segmentation_frame, self.segmentation_menu_variable, [])
        self.segmentation_menu.config(width=20)
        self.segmentation_menu.pack(side=LEFT)
        self.segmentation_menu.pack_forget()

        self.nwb_neuronal_data_frame = Frame(self.nwb_info_frame)
        self.nwb_neuronal_data_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.nwb_neuronal_data_label = Label(self.nwb_neuronal_data_frame)
        self.nwb_neuronal_data_label["text"] = " " * 10
        self.nwb_neuronal_data_label.pack(side=LEFT)

        self.nwb_neuronal_data_menu_variable = StringVar(self)
        self.nwb_neuronal_data_menu = OptionMenu(self.nwb_neuronal_data_frame, self.nwb_neuronal_data_menu_variable, [])
        self.nwb_neuronal_data_menu.config(width=20)
        self.nwb_neuronal_data_menu.pack(side=LEFT)
        self.nwb_neuronal_data_menu.pack_forget()

        self.is_neuronal_data_check_box_active = True
        self.neuronal_data_check_box_var = IntVar()
        # self.check_box
        self.neuronal_data_check_box = Checkbutton(self.nwb_neuronal_data_frame, text="Use it",
                                     variable=self.neuronal_data_check_box_var,
                                     onvalue=1,
                                     offvalue=0)
        self.neuronal_data_check_box["command"] = event_lambda(self.neuronal_data_check_box_action)
        # zoom on by default
        if self.is_neuronal_data_check_box_active:
            self.neuronal_data_check_box.select()
        self.neuronal_data_check_box.pack(side=LEFT)
        self.neuronal_data_check_box.pack_forget()

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["predictions"] = RawFormatOptionModule(button_text="Activity predictions",
                                                                 label_text=" " * 50, with_file_dialog=True,
                                                                 file_dialog_filetypes=
                                                                 (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                  ("Matlab files", "*.mat")),
                                                                 file_dialog_title="Select activity predictions",
                                                                 root=self.root,
                                                                 mandatory=False,
                                                                 with_option_menu=True,
                                                                 menu_keyword_for_key="predictions",
                                                                 last_path_open=self.last_path_open,
                                                                 height_button=3, command_fct=None,
                                                                 default_path=self.default_path,
                                                                 master=button_frame)

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["classifier_model"] = RawFormatOptionModule(button_text="Classifier model",
                                                                      label_text=" " * 50, with_file_dialog=True,
                                                                      file_dialog_filetypes=
                                                                      (("Json file", "*.json"),),
                                                                      file_dialog_title="Select json model file",
                                                                      root=self.root,
                                                                      mandatory=False,
                                                                      with_option_menu=False,
                                                                      last_path_open=self.last_path_open,
                                                                      height_button=3, command_fct=None,
                                                                      default_path=self.default_path,
                                                                      master=button_frame)

        self.modules_dict["classifier_weights"] = RawFormatOptionModule(button_text="Classifier Weights",
                                                                        label_text=" " * 50, with_file_dialog=True,
                                                                        file_dialog_filetypes=(("h5 file", "*.h5"),),
                                                                        file_dialog_title="Select h5 weights file",
                                                                        root=self.root,
                                                                        mandatory=False,
                                                                        with_option_menu=False,
                                                                        last_path_open=self.last_path_open,
                                                                        height_button=3, command_fct=None,
                                                                        default_path=self.default_path,
                                                                        master=button_frame)

        self.modules_dict["classifier_weights"].add_exclusive_modules([self.modules_dict["predictions"]])
        self.modules_dict["classifier_model"].add_exclusive_modules([self.modules_dict["predictions"]])
        self.modules_dict["predictions"].add_exclusive_modules([self.modules_dict["classifier_weights"],
                                                                self.modules_dict["classifier_model"]])

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["gt_file"] = RawFormatOptionModule(button_text="Ground Truth (GT)",
                                                             label_text=" " * 50, with_file_dialog=True,
                                                             file_dialog_filetypes=
                                                             (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                              ("Matlab files", "*.mat")),
                                                             file_dialog_title="Select a GT file",
                                                             root=self.root,
                                                             mandatory=False,
                                                             with_option_menu=True,
                                                             menu_keyword_for_key="raster",
                                                             last_path_open=self.last_path_open,
                                                             height_button=3, command_fct=None,
                                                             default_path=self.default_path,
                                                             master=button_frame)

        self.modules_dict["gt_onsets_file"] = RawFormatOptionModule(button_text="Ground Truth onsets",
                                                                    label_text=" " * 50, with_file_dialog=True,
                                                                    file_dialog_filetypes=
                                                                    (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                     ("Matlab files", "*.mat")),
                                                                    file_dialog_title="Select a GT onsets file",
                                                                    root=self.root,
                                                                    mandatory=False,
                                                                    with_option_menu=True,
                                                                    menu_keyword_for_key="onsets",
                                                                    last_path_open=self.last_path_open,
                                                                    height_button=3, command_fct=None,
                                                                    default_path=self.default_path,
                                                                    master=button_frame)

        self.modules_dict["gt_peaks_file"] = RawFormatOptionModule(button_text="Ground Truth peaks",
                                                                   label_text=" " * 50, with_file_dialog=True,
                                                                   file_dialog_filetypes=
                                                                   (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                    ("Matlab files", "*.mat")),
                                                                   file_dialog_title="Select a GT peaks file",
                                                                   root=self.root,
                                                                   mandatory=False,
                                                                   with_option_menu=True,
                                                                   menu_keyword_for_key="peaks",
                                                                   last_path_open=self.last_path_open,
                                                                   height_button=3, command_fct=None,
                                                                   default_path=self.default_path,
                                                                   master=button_frame)

        # gt_pred_frame = Frame(button_frame)
        # gt_pred_frame.pack(side=TOP,
        #                    expand=YES,
        #                    fill=BOTH)

        self.modules_dict["gt_pred"] = RawFormatOptionModule(button_text="Predictions as GT",
                                                             label_text=" " * 50, with_spin_box=True,
                                                             with_file_dialog=None,
                                                             file_dialog_filetypes=None,
                                                             file_dialog_title=None,
                                                             root=self.root,
                                                             mandatory=False,
                                                             with_option_menu=False,
                                                             last_path_open=self.last_path_open,
                                                             height_button=3, command_fct=None,
                                                             default_path=self.default_path,
                                                             master=button_frame)
        self.modules_dict["predictions"].slave_module = self.modules_dict["gt_pred"]
        self.modules_dict["gt_pred"].master_module = self.modules_dict["predictions"]

        # automatic_gt_frame = Frame(button_frame)
        # automatic_gt_frame.pack(side=TOP,
        #                         expand=YES,
        #                         fill=BOTH)

        self.modules_dict["automatic_gt"] = RawFormatOptionModule(button_text="Automatic GT",
                                                                  label_text=" " * 50, with_only_label=True,
                                                                  active_label_text="automatic GT",
                                                                  with_file_dialog=None,
                                                                  file_dialog_filetypes=None,
                                                                  file_dialog_title=None,
                                                                  root=self.root,
                                                                  mandatory=False,
                                                                  with_option_menu=False,
                                                                  last_path_open=self.last_path_open,
                                                                  height_button=3, command_fct=None,
                                                                  default_path=self.default_path,
                                                                  master=button_frame)
        self.modules_dict["automatic_gt"].add_exclusive_modules([self.modules_dict["gt_file"],
                                                                 self.modules_dict["gt_pred"],
                                                                 self.modules_dict["gt_onsets_file"],
                                                                 self.modules_dict["gt_peaks_file"]])
        self.modules_dict["gt_file"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                            self.modules_dict["gt_pred"],
                                                            self.modules_dict["gt_onsets_file"],
                                                            self.modules_dict["gt_peaks_file"]])
        self.modules_dict["gt_pred"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                            self.modules_dict["gt_file"],
                                                            self.modules_dict["gt_onsets_file"],
                                                            self.modules_dict["gt_peaks_file"]])

        self.modules_dict["gt_onsets_file"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                                   self.modules_dict["gt_file"],
                                                                   self.modules_dict["gt_pred"]])

        self.modules_dict["gt_peaks_file"].add_exclusive_modules([self.modules_dict["automatic_gt"],
                                                                  self.modules_dict["gt_file"],
                                                                  self.modules_dict["gt_pred"]])
        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # --------------- Raster 1 section  ---------------
        self.modules_dict["raster_1"] = RawFormatOptionModule(button_text="Raster 1",
                                                              label_text=" " * 50, with_file_dialog=True,
                                                              file_dialog_filetypes=
                                                              (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                               ("Matlab files", "*.mat")),
                                                              file_dialog_title="Select raster 1",
                                                              root=self.root,
                                                              mandatory=False,
                                                              with_option_menu=True,
                                                              menu_keyword_for_key="raster",
                                                              last_path_open=self.last_path_open,
                                                              height_button=3, command_fct=None,
                                                              default_path=self.default_path,
                                                              master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # --------------- Raster 2 section  ---------------
        self.modules_dict["raster_2"] = RawFormatOptionModule(button_text="Raster 2",
                                                              label_text=" " * 50, with_file_dialog=True,
                                                              file_dialog_filetypes=
                                                              (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                               ("Matlab files", "*.mat")),
                                                              file_dialog_title="Select raster 2",
                                                              root=self.root,
                                                              mandatory=False,
                                                              with_option_menu=True,
                                                              menu_keyword_for_key="raster",
                                                              last_path_open=self.last_path_open,
                                                              height_button=3, command_fct=None,
                                                              default_path=self.default_path,
                                                              master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["cell_type_yaml_file"] = RawFormatOptionModule(button_text="Cell type config",
                                                                         label_text=" " * 50, with_file_dialog=True,
                                                                         file_dialog_filetypes=
                                                                         (("Yaml files", "*.yaml"),
                                                                          ("Yaml files", "*.yml")),
                                                                         file_dialog_title="Select cell type config",
                                                                         root=self.root,
                                                                         mandatory=False,
                                                                         with_option_menu=True,
                                                                         last_path_open=self.last_path_open,
                                                                         height_button=3, command_fct=None,
                                                                         default_path=self.default_path,
                                                                         master=button_frame)

        self.modules_dict["cell_type_predictions"] = RawFormatOptionModule(button_text="Cell type predictions",
                                                                           label_text=" " * 50, with_file_dialog=True,
                                                                           file_dialog_filetypes=
                                                                           (("Numpy files", "*.npy"),
                                                                            ("Numpy files", "*.npz"),
                                                                            ("Matlab files", "*.mat")),
                                                                           file_dialog_title="Select cells predictions",
                                                                           root=self.root,
                                                                           mandatory=False,
                                                                           with_option_menu=False,
                                                                           menu_keyword_for_key="predictions",
                                                                           last_path_open=self.last_path_open,
                                                                           height_button=3, command_fct=None,
                                                                           default_path=self.default_path,
                                                                           master=button_frame)

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["cell_type_classifier_model"] = RawFormatOptionModule(
            button_text="Cell type model",
            label_text=" " * 50, with_file_dialog=True,
            file_dialog_filetypes=
            (("Json file", "*.json"),),
            file_dialog_title="Select json model file",
            root=self.root,
            mandatory=False,
            with_option_menu=False,
            last_path_open=self.last_path_open,
            height_button=3, command_fct=None,
            default_path=self.default_path,
            master=button_frame)

        self.modules_dict["cell_type_classifier_weights"] = RawFormatOptionModule(
            button_text="Cell type weights",
            label_text=" " * 50,
            with_file_dialog=True,
            file_dialog_filetypes=(
                ("h5 file", "*.h5"),),
            file_dialog_title="Select h5 weights file",
            root=self.root,
            mandatory=False,
            with_option_menu=False,
            last_path_open=self.last_path_open,
            height_button=3, command_fct=None,
            default_path=self.default_path,
            master=button_frame)
        #
        # self.modules_dict["cell_type_classifier_weights"].add_exclusive_modules(
        #     [self.modules_dict["cell_type_predictions"]])
        # self.modules_dict["cell_type_classifier_model"].add_exclusive_modules(
        #     [self.modules_dict["cell_type_predictions"]])
        # self.modules_dict["cell_type_predictions"].add_exclusive_modules(
        #     [self.modules_dict["cell_type_classifier_weights"],
        #      self.modules_dict["cell_type_classifier_model"]])
        self.modules_dict["cell_type_yaml_file"].slave_module = self.modules_dict["cell_type_predictions"]
        self.modules_dict["cell_type_yaml_file"].slave_module = self.modules_dict["cell_type_classifier_weights"]
        self.modules_dict["cell_type_yaml_file"].slave_module = self.modules_dict["cell_type_classifier_model"]
        self.modules_dict["cell_type_predictions"].master_module = self.modules_dict["cell_type_yaml_file"]
        self.modules_dict["cell_type_classifier_weights"].master_module = self.modules_dict["cell_type_yaml_file"]
        self.modules_dict["cell_type_classifier_model"].master_module = self.modules_dict["cell_type_yaml_file"]

        empty_label = Label(self.button_frame, text=" " * 100)
        empty_label.pack(side=TOP, expand=FALSE, fill=None)

        # self.deactivate_all_buttons()

        # track changes to its size
        button_frame.bind('<Configure>', self.__configure)

        # place the frame inside the canvas (this also
        # runs the __configure method)
        self.canvas.create_window(0, 0, window=button_frame, anchor=NW)

    def neuronal_data_check_box_action(self):
        # using this method as check_box_var doesn't work (at least on Linux)
        self.is_neuronal_data_check_box_active = not self.is_neuronal_data_check_box_active

    def activate_all_buttons(self):
        self.modules_dict["predictions"].activate_only_label(enabling_button=True)
        self.modules_dict["classifier_model"].activate_only_label(enabling_button=True)
        self.modules_dict["classifier_weights"].activate_only_label(enabling_button=True)
        self.modules_dict["raster_1"].activate_only_label(enabling_button=True)
        self.modules_dict["raster_2"].activate_only_label(enabling_button=True)

    def deactivate_all_buttons(self):
        self.modules_dict["predictions"].deactivate(disabling_button=True)
        self.modules_dict["classifier_model"].deactivate(disabling_button=True)
        self.modules_dict["classifier_weights"].deactivate(disabling_button=True)
        self.modules_dict["raster_1"].deactivate(disabling_button=True)
        self.modules_dict["raster_2"].deactivate(disabling_button=True)

    def __configure(self, event):
        # update the scrollbars to match the size of the inner frame
        # size = self.button_frame.winfo_reqwidth(), self.button_frame.winfo_reqheight()
        # self.canvas.config(scrollregion="0 0 %s %s" % size)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=min(self.screen_width, 600),
                              height=min(self.screen_height, 1000))

    def select_nwb_file(self):
        """
        Open a file dialog to select to cinac file to open
        and then change the GUI accordingly
        Returns:

        """
        if self.default_path is not None:
            initial_dir = self.default_path
        else:
            initial_dir = None

        file_name = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=(("NWB files", "*.nwb"),),
            title="Select NWB file",
            parent=self.root)

        # to put the window on the top
        self.root.lift()

        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            return

        self.launch_gui_button['state'] = "normal"

        previous_nwb_file_name = self.nwb_file_name
        self.nwb_file_name = file_name
        self.default_path, file_name_only = get_file_name_and_path(file_name)
        self.nwb_label["text"] = file_name_only

        io = NWBHDF5IO(file_name, 'r')
        self.nwb_data = io.read()

        """
            dict with as key a string identifying the movie, and as value a dict of CI movies
            a string as file_name if external, or a 3d array

        """
        self.ci_movies_dict = dict()
        only_2_photons = True

        for key, acquisition_data in self.nwb_data.acquisition.items():
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                if image_series.format == "external":
                    movie_file_name = image_series.external_file[0]
                    movie_data = movie_file_name
                else:
                    movie_data = image_series.data
                self.ci_movies_dict[key] = movie_data

        if len(self.ci_movies_dict) == 0:
            if previous_nwb_file_name is not None:
                self.nwb_file_name = previous_nwb_file_name
                self.default_path, file_name_only = get_file_name_and_path(previous_nwb_file_name)
                self.nwb_label["text"] = file_name_only
            else:
                self.nwb_file_name = None
                self.nwb_label["text"] = " " * 10
            messagebox.showerror("Error", f"No 2p calcium imaging movie in  {file_name_only}")
            return

        segmentation_dict = self._get_segmentations()
        if len(segmentation_dict) == 0:
            if previous_nwb_file_name is not None:
                self.nwb_file_name = previous_nwb_file_name
                self.default_path, file_name_only = get_file_name_and_path(previous_nwb_file_name)
                self.nwb_label["text"] = file_name_only
            else:
                self.nwb_file_name = None
                self.nwb_label["text"] = " " * 10
            messagebox.showerror("Error", f"No segmentation in  {file_name_only}")
            return

        # excluding fluorescence traces
        roi_response_series_dict = self._get_roi_response_series(keywords_to_exclude=["trace"])
        # print(f"roi_response_series_dict {roi_response_series_dict}")

        # Reset var and delete all old options
        self.ci_movie_menu_variable.set('')
        self.ci_movie_menu['menu'].delete(0, 'end')
        # Insert list of new options (tk._setit hooks them up to var)
        for choice in self.ci_movies_dict.keys():
            self.ci_movie_menu['menu'].add_command(label=choice, command=tk._setit(self.ci_movie_menu_variable, choice))
        # if favorite_key is not None:
        self.ci_movie_menu_variable.set(list(self.ci_movies_dict.keys())[0])
        self.ci_movie_menu.pack(side=LEFT)
        self.nwb_movie_label["text"] = "CI movie       "

        segmentations_list = get_tree_dict_as_a_list(segmentation_dict)
        self.segmentation_str_to_list = dict()
        # Reset var and delete all old options
        self.segmentation_menu_variable.set('')
        self.segmentation_menu['menu'].delete(0, 'end')
        # Insert list of new options (tk._setit hooks them up to var)
        to_select = ""
        for segmentation_keys in segmentations_list:
            segmentation_keys_str = " / ".join(segmentation_keys)
            self.segmentation_str_to_list[segmentation_keys_str] = segmentation_keys
            self.segmentation_menu['menu'].add_command(label=segmentation_keys_str,
                                                       command=tk._setit(self.ci_movie_menu_variable,
                                                                         segmentation_keys_str))
            to_select = segmentation_keys_str
        # if favorite_key is not None:
        self.segmentation_menu_variable.set(to_select)
        self.segmentation_menu.pack(side=LEFT)
        self.segmentation_label["text"] = "Segmentation  "

        # neuronal data
        neuronal_data_list = get_tree_dict_as_a_list(roi_response_series_dict)
        self.neuronal_data_to_list = dict()

        # Reset var and delete all old options
        self.nwb_neuronal_data_menu_variable.set('')
        self.nwb_neuronal_data_menu['menu'].delete(0, 'end')
        if len(neuronal_data_list) > 0:
            # Insert list of new options (tk._setit hooks them up to var)
            to_select = ""
            for neuronal_data_keys in neuronal_data_list:
                neuronal_data_str = " / ".join(neuronal_data_keys)
                self.neuronal_data_to_list[neuronal_data_str] = neuronal_data_keys
                self.nwb_neuronal_data_menu['menu'].add_command(label=neuronal_data_str,
                                                           command=tk._setit(self.nwb_neuronal_data_menu_variable,
                                                                             neuronal_data_str))
                to_select = neuronal_data_str
            # if favorite_key is not None:
            self.nwb_neuronal_data_menu_variable.set(to_select)
            self.nwb_neuronal_data_menu.pack(side=LEFT)
            self.neuronal_data_check_box.pack(side=LEFT)
            self.nwb_neuronal_data_label["text"] = "Neuronal data      "

    def _get_segmentations(self):
        """

        Returns: a dict that for each step till plane_segmentation represents the different option.
        First dict will have as keys the name of the modules, then for each modules the value will be a new dict
        with keys the ImageSegmentation names and then the value will be a list representing the segmentation plane

        """
        segmentation_dict = dict()
        for name_mod, mod in self.nwb_data.modules.items():
            segmentation_dict[name_mod] = dict()
            no_keys_added = True
            for key, value in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of ImageSegmentation
                if isinstance(value, ImageSegmentation):
                    no_keys_added = False
                    image_seg = value
                    # key is the name of segmentation, and value a list of plane_segmentation
                    segmentation_dict[name_mod][key] = []
                    # print(f"get_segmentations {name_mod} key {key}")
                    for plane_seg_name in image_seg.plane_segmentations.keys():
                        # print(f"get_segmentations plane_seg_name {plane_seg_name}")
                        segmentation_dict[name_mod][key].append(plane_seg_name)
            if no_keys_added:
                del segmentation_dict[name_mod]

        # it could be empty, but if it would matter, it should have been check by method check_data in CicadaAnalysis
        return segmentation_dict

    def get_pixel_mask(self, segmentation_info):
        """
        Return pixel_mask which is a list of list of pair of integers representing the pixels coordinate (x, y) for each
        cell. the list length is the same as the number of cells.
        Args:
            segmentation_info: a list of 3 elements: first one being the name of the module, then the name
            of image_segmentation and then the name of the segmentation plane.

        Returns:

        """
        if len(segmentation_info) < 3:
            return None

        name_module = segmentation_info[0]
        mod = self.nwb_data.modules[name_module]

        name_mode = segmentation_info[1]
        name_plane_seg = segmentation_info[2]
        plane_seg = mod[name_mode].get_plane_segmentation(name_plane_seg)

        if 'pixel_mask' not in plane_seg:
            return None

        return plane_seg['pixel_mask']

    def _get_roi_response_serie_data(self, keys):
        """

        Args:
            keys: lsit of string allowing to get the roi repsonse series wanted

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in self.nwb_data.modules:
            return None

        if keys[1] not in self.nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self.nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        return np.array(self.nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series[keys[2]].data)

    def _get_roi_response_series(self, keywords_to_exclude=None):
        """
                param:
                keywords_to_exclude: if not None, list of str, if one of neuronal data has this keyword,
                then we don't add it to the choices

                Returns: a list or dict of objects representing all roi response series (rrs) names
                rrs could represents raw traces, or binary raster, and its link to a given segmentation.
                The results returned should allow to identify the segmentation associated.
                Object could be strings, or a list of strings, that identify a rrs and give information
                how to get there.

        """
        rrs_dict = dict()
        for name_mod, mod in self.nwb_data.modules.items():
            rrs_dict[name_mod] = dict()
            for key, fluorescence in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of pynwb.ophys.Fluorescence
                if isinstance(fluorescence, Fluorescence):
                    rrs_dict[name_mod][key] = []
                    for name_rrs, rrs in fluorescence.roi_response_series.items():
                        if keywords_to_exclude is not None:
                            to_exclude = False
                            for keyword in keywords_to_exclude:
                                if keyword in name_rrs:
                                    to_exclude = True
                                    break
                            if to_exclude:
                                continue
                        rrs_dict[name_mod][key].append(name_rrs)
                    if len(rrs_dict[name_mod][key]) == 0:
                        del rrs_dict[name_mod][key]
            if len(rrs_dict[name_mod]) == 0:
                del rrs_dict[name_mod]

        return rrs_dict

    def launch_exploratory_gui(self):
        """

        Returns:

        """
        # first we check if the data is correct

        # message box display
        # messagebox.showerror("Error", "Error message")
        # messagebox.showwarning("Warning", "Warning message")
        # messagebox.showinfo("Information", "Informative message")

        data_and_param = DataAndParam()

        if self.default_path is None:
            self.default_path, _ = get_file_name_and_path(self.nwb_file_name)

        # .set(list(self.ci_movies_dict
        movie_data = self.ci_movies_dict[self.ci_movie_menu_variable.get()]

        # we normalize the movie for the classifier
        non_norm_tiff_movie, tiff_movie = load_movie(file_name=movie_data, with_normalization=True,
                                                     verbose=True, both_instances=True)
        avg_cell_map_img = np.mean(tiff_movie, axis=0)
        n_frames = tiff_movie.shape[0]

        segmentation_info = self.segmentation_str_to_list[self.segmentation_menu_variable.get()]
        if len(segmentation_info) != 3:
            messagebox.showerror("Error", f"Issue to get the pixel mask in the NWB file, seems like the information"
                                          f"is not at the right depth.")
            return
        pixel_mask = self.get_pixel_mask(segmentation_info=segmentation_info)

        if pixel_mask is None:
            messagebox.showerror("Error", f"Issue with the pixel mask in the NWB file, might not be available")
            return

        # pixel_mask of type pynwb.core.VectorIndex
        # each element of the list will be a sequences of tuples of 3 floats representing x, y and a float between
        # 0 and 1 (not used in this case)
        pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]
        coord_obj = CellsCoord(pixel_masks=pixel_mask_list, from_matlab=False, invert_xy_coord=False)

        n_cells = coord_obj.n_cells
        # print(f"n_cells {n_cells}")
        other_rasters = []
        if self.modules_dict["raster_1"].activated:
            file_name = self.modules_dict["raster_1"].file_name
            attr_name = None
            if self.modules_dict["raster_1"].with_option_menu:
                attr_name = self.modules_dict["raster_1"].menu_variable.get()

            raster_1_data = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Raster 1",
                                                           attr_name=attr_name)

            # first we check that the data fit the movie dimension and the numer of cells
            if raster_1_data.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Raster 1 dimensions {raster_1_data.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            other_rasters.append(raster_1_data)

        if self.modules_dict["raster_2"].activated:
            file_name = self.modules_dict["raster_2"].file_name
            attr_name = None
            if self.modules_dict["raster_2"].with_option_menu:
                attr_name = self.modules_dict["raster_2"].menu_variable.get()

            raster_2_data = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Raster 2",
                                                           attr_name=attr_name)
            if raster_2_data.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Raster 2 dimensions {raster_2_data.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            other_rasters.append(raster_2_data)

        raster_dur = None
        if self.modules_dict["predictions"].activated:
            file_name = self.modules_dict["predictions"].file_name
            attr_name = None
            if self.modules_dict["predictions"].with_option_menu:
                attr_name = self.modules_dict["predictions"].menu_variable.get()

            predictions = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Predictions",
                                                         attr_name=attr_name)
            if predictions.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Predictions dimensions {predictions.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            data_and_param.classifier_predictions = predictions

            if self.modules_dict["gt_pred"].activated:
                # then we produce the raster dur based on the predictions using threshold the prediction_threshold
                prediction_threshold = 0.5
                predicted_raster_dur = np.zeros((n_cells, n_frames), dtype="int8")

                for cell in np.arange(n_cells):
                    predicted_raster_dur[cell, predictions[cell] >= prediction_threshold] = 1
                raster_dur = predicted_raster_dur

        if self.modules_dict["gt_file"].activated:
            file_name = self.modules_dict["gt_file"].file_name
            attr_name = None
            if self.modules_dict["gt_file"].with_option_menu:
                attr_name = self.modules_dict["gt_file"].menu_variable.get()

            raster_dur = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="GT file",
                                                        attr_name=attr_name)
            if raster_dur.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"GT file dimensions {raster_dur.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return

        onsets = None
        peaks = None
        if self.modules_dict["gt_onsets_file"].activated:
            if not self.modules_dict["gt_peaks_file"].activated:
                messagebox.showerror("Error", f"GT onsets and peaks file need to be both specified")
                return

            file_name = self.modules_dict["gt_onsets_file"].file_name
            attr_name = None
            if self.modules_dict["gt_onsets_file"].with_option_menu:
                attr_name = self.modules_dict["gt_onsets_file"].menu_variable.get()

            onsets = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="GT onsets file",
                                                    attr_name=attr_name)
            if onsets.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"GT onsets file dimensions {raster_dur.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return

            file_name = self.modules_dict["gt_peaks_file"].file_name
            attr_name = None
            if self.modules_dict["gt_peaks_file"].with_option_menu:
                attr_name = self.modules_dict["gt_peaks_file"].menu_variable.get()

            peaks = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="GT peaks file",
                                                   attr_name=attr_name)
            if peaks.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"GT peaks file dimensions {raster_dur.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return

            # now building raster_dur
            raster_dur = build_raster_dur_from_onsets_peaks(onsets=onsets, peaks=peaks)

        if self.modules_dict["gt_peaks_file"].activated:
            if not self.modules_dict["gt_onsets_file"].activated:
                messagebox.showerror("Error", f"GT onsets and peaks file need to be both specified")
                return

        # now if raster_dur is still None and neuronal data from nwb is available, we use it
        if (raster_dur is None) and len(self.neuronal_data_to_list) > 0 and self.is_neuronal_data_check_box_active:
            neuronal_data_info = self.neuronal_data_to_list[self.nwb_neuronal_data_menu_variable.get()]
            neuronal_data = self._get_roi_response_serie_data(keys=neuronal_data_info)
            # first we make sure it is binary
            if len(np.unique(neuronal_data)) > 2:
                print("Neuronal data select from NWB is not binary. ")
            else:
                raster_dur = neuronal_data

        if raster_dur is not None:
            if onsets is None:
                onsets = np.zeros((n_cells, n_frames), dtype="int8")
                peaks = np.zeros((n_cells, n_frames), dtype="int8")
                for cell in np.arange(n_cells):
                    transient_periods = get_continous_time_periods(raster_dur[cell])
                    for transient_period in transient_periods:
                        onset = transient_period[0]
                        peak = transient_period[1]
                        # if onset == peak:
                        #     print("onset == peak")
                        onsets[cell, onset] = 1
                        peaks[cell, peak] = 1
            data_and_param.peak_nums = peaks
            data_and_param.spike_nums = onsets

        if self.modules_dict["classifier_model"].activated and self.modules_dict["classifier_weights"].activated:
            classifier_model_file = self.modules_dict["classifier_model"].file_name
            data_and_param.classifier_model_file = classifier_model_file
            classifier_weights_file = self.modules_dict["classifier_weights"].file_name
            data_and_param.classifier_weights_file = classifier_weights_file

        data_and_param.tiff_movie = tiff_movie
        data_and_param.non_norm_tiff_movie = non_norm_tiff_movie
        data_and_param.coord_obj = coord_obj
        data_and_param.avg_cell_map_img = avg_cell_map_img
        data_and_param.raw_traces = coord_obj.build_raw_traces_from_movie(movie=tiff_movie)
        # smoothing the trace, but no demixing
        data_and_param.traces = np.copy(data_and_param.raw_traces)
        do_traces_smoothing(data_and_param.traces)

        data_and_param.other_rasters = other_rasters

        # computing all potential peaks and onset from smooth_trace
        all_potential_peaks = np.zeros((n_cells, n_frames), dtype="int8")
        all_potential_onsets = np.zeros((n_cells, n_frames), dtype="int8")
        # then we do an automatic detection
        for cell in np.arange(n_cells):
            peaks, properties = signal.find_peaks(x=data_and_param.traces[cell], distance=2)
            all_potential_peaks[cell, peaks] = 1

        for cell in np.arange(n_cells):
            onsets = []
            diff_values = np.diff(data_and_param.traces[cell])
            for index, value in enumerate(diff_values):
                if index == (len(diff_values) - 1):
                    continue
                if value < 0:
                    if diff_values[index + 1] >= 0:
                        onsets.append(index + 1)
            if len(onsets) > 0:
                all_potential_onsets[cell, np.array(onsets)] = 1
        data_and_param.all_potential_peaks = all_potential_peaks
        data_and_param.all_potential_onsets = all_potential_onsets

        if self.modules_dict["automatic_gt"].activated:
            # we fill it with all potential peaks and onsets
            data_and_param.peak_nums = data_and_param.all_potential_peaks
            data_and_param.spike_nums = data_and_param.all_potential_onsets
        elif data_and_param.peak_nums is None:
            # otherwise empty detection
            data_and_param.peak_nums = np.zeros((coord_obj.n_cells, n_frames), dtype="int8")
            data_and_param.spike_nums = np.zeros((coord_obj.n_cells, n_frames), dtype="int8")

        if self.modules_dict["cell_type_yaml_file"].activated:
            cell_type_yaml_file = self.modules_dict["cell_type_yaml_file"].file_name
            cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
                read_cell_type_categories_yaml_file(yaml_file=cell_type_yaml_file, using_multi_class=1)
            # cell types to display
            data_and_param.cell_types_for_classifier = list(cell_type_from_code_dict.values())
            data_and_param.cell_type_from_code_dict = cell_type_from_code_dict
            if multi_class_arg or (len(cell_type_from_code_dict) > 2):
                data_and_param.cell_type_classifier_category = "multi_class"
            else:
                data_and_param.cell_type_classifier_category = "binary"
            if self.modules_dict["cell_type_predictions"].activated:
                cell_type_predictions_file_name = self.modules_dict["cell_type_predictions"].file_name

                cell_type_predictions = load_data_from_npy_or_mat_file(file_name=cell_type_predictions_file_name,
                                                                       data_descr="Cell type predictions",
                                                                       attr_name="predictions")
                if not cell_type_predictions_file_name.endswith(".npy"):
                    cells = load_data_from_npy_or_mat_file(file_name=cell_type_predictions_file_name,
                                                           data_descr="Cell type predictions",
                                                           attr_name="cells")
                else:
                    cells = np.arange(len(cell_type_predictions))
                # all cells might not have been predicted, so we just check if the number of cells predicted
                # is not greater than the number of cells available

                # TODO: See which dimension to check ?
                if len(cell_type_predictions) > n_cells:
                    messagebox.showerror("Error", f"Cell type predictions dimensions {len(cell_type_predictions)} "
                                                  f"is superior to "
                                                  f"the number of ROIs {coord_obj.n_cells}")
                    return

                # dict with key being the cell id, and value being a dict with key the cell_type and value the prediction
                cell_type_classifier_predictions = dict()
                for cell_index, cell in enumerate(cells):
                    cell_type_classifier_predictions[cell] = dict()
                    cell_type_prediction = cell_type_predictions[cell_index]
                    if isinstance(cell_type_prediction, float):
                        pass
                    else:
                        for cell_type_code, pred_value in enumerate(cell_type_prediction):
                            cell_type = cell_type_from_code_dict[cell_type_code]
                            cell_type_classifier_predictions[cell][cell_type] = pred_value

                data_and_param.cell_type_classifier_predictions = cell_type_classifier_predictions
                # TODO: See to change predictions according to info in yaml file
                # TODO: Ideally data_and_param.cell_type_classifier_predictions will be a dict
                #  with key the cell id and value a dict with key the cell_type and value a float
                #  representing the value
                #  using then data_and_param.cell_type_classifier_category to determine how to get the result
                # TODO: Make sure the predictions are compatible with the yaml file info
                # data_and_param.cell_type_classifier_predictions = cell_type_predictions
            elif self.modules_dict["cell_type_classifier_weights"].activated:
                if not self.modules_dict["cell_type_classifier_model"].activated:
                    messagebox.showerror("Error", f"Cell type classifier weight and moddel files need to "
                                                  f"be both specified")
                    return
                data_and_param.cell_type_classifier_weights_file = \
                    self.modules_dict["cell_type_classifier_weights"].file_name
                data_and_param.cell_type_classifier_model_file = \
                    self.modules_dict["cell_type_classifier_model"].file_name
        f = ManualOnsetFrame(data_and_param=data_and_param, default_path=self.default_path)
        f.mainloop()


class ChoiceCinacFormatFrame(tk.Frame):

    def __init__(self, default_path=None, master=None):
        # ------ constants for controlling layout ------
        buttons_frame_padx = "3m"
        buttons_frame_pady = "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        # -------------- end constants ----------------
        self.root = Tk()
        # self.root.protocol("WM_DELETE_WINDOW", self.validation_before_closing)
        # self.root.title(f"Session {session_number}")
        tk.Frame.__init__(self, master=self.root)
        self.pack(
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            padx=buttons_frame_padx,
            pady=buttons_frame_pady
        )
        self.default_path = default_path
        self.option_menu_variable = None
        self.last_path_open = [None]

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # ---- buttons and labels ----
        self.launch_gui_button = None
        self.select_cinac_file_button = None
        self.select_movie_button = None
        self.button_frame = None
        self.canvas = None
        self.height_button = 3

        # a module represent an instance of RawFormatOptionModule
        # key is a string representing the name of the module
        # and the value is the instance of RawFormatOptionModule
        self.modules_dict = dict()

        # ---- files' name ----
        self.coords_file_name = None

        # ----- data ---------
        self.ci_movie_file_name = None
        self.cinac_file_name = None
        self.cinac_file_reader = None
        # list of segments with ground truth available
        self.gt_segments_list = []
        self.last_path_open = [None]

        # ----- creating the GUI panel ----

        # scrollbars
        vbar = Scrollbar(self, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        hbar = Scrollbar(self, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)

        canvas = Canvas(self)
        self.canvas = canvas

        hbar.config(command=canvas.xview)
        vbar.config(command=canvas.yview)

        # canvas.config(width=300, height=300)
        canvas.config(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        canvas.pack(side=LEFT, expand=True, fill=BOTH)
        # canvas.pack(side=TOP, anchor=NW, padx=10, pady=10)0)

        # create the inner frame
        button_frame = Frame(canvas)
        self.button_frame = button_frame
        button_frame.pack(side=LEFT,
                          expand=True,
                          fill=BOTH)

        self.launch_gui_button = MySessionButton(button_frame)
        self.launch_gui_button["text"] = "Launch GUI"
        self.launch_gui_button['state'] = DISABLED
        self.launch_gui_button.config(height=self.height_button)
        self.launch_gui_button.pack(side=TOP)
        self.launch_gui_button["command"] = event_lambda(self.launch_exploratory_gui)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # ------- CINAC FRAME -------
        self.select_cinac_frame = Frame(self.button_frame)
        self.select_cinac_frame.pack(side=TOP, expand=YES, fill=BOTH)

        self.cinac_button = MySessionButton(self.select_cinac_frame)
        self.cinac_button["text"] = "Select CINAC file"
        self.cinac_button["fg"] = "black"

        self.cinac_button.pack(side=LEFT)
        self.cinac_button.config(height=self.height_button)
        self.cinac_button["command"] = event_lambda(self.select_cinac_file)

        empty_label = Label(self.select_cinac_frame, text=" ")
        empty_label.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.cinac_label = Label(self.select_cinac_frame)
        self.cinac_label["text"] = " "
        self.cinac_label.pack(side=LEFT)

        empty_label = Label(self.select_cinac_frame, text=" ")
        empty_label.pack(side=LEFT, expand=TRUE, fill=BOTH)

        empty_label = Label(self.button_frame, text=" ")
        empty_label.pack(side=TOP, expand=FALSE, fill=None)

        # ------- CI MOVIE FRAME -------
        self.ci_movie_frame = Frame(self.button_frame)
        self.ci_movie_frame.pack(side=TOP, expand=YES, fill=BOTH)

        empty_label = Label(self.ci_movie_frame, text=" ")
        empty_label.pack(side=RIGHT, expand=TRUE, fill=BOTH)

        self.ci_movie_label = Label(self.ci_movie_frame)
        self.ci_movie_label["text"] = " "
        self.ci_movie_label.pack(side=RIGHT)

        empty_label = Label(self.ci_movie_frame, text=" ")
        empty_label.pack(side=RIGHT, expand=TRUE, fill=BOTH)

        self.ci_movie_button = MySessionButton(self.ci_movie_frame)
        self.ci_movie_button["text"] = " CI movie "
        self.ci_movie_button['state'] = DISABLED
        self.ci_movie_button.config(height=self.height_button)
        self.ci_movie_button["command"] = event_lambda(self.select_ci_movie)
        self.ci_movie_button.pack(side=RIGHT)
        # self.ci_movie_button.pack_forget()

        empty_label = Label(self.button_frame, text=" ")
        empty_label.pack(side=TOP, expand=FALSE, fill=None)

        # ------- LISTBOX FRAME -------
        self.list_box_frame = Frame(self.button_frame)
        self.list_box_frame.pack(side=TOP, expand=YES, fill=BOTH)

        empty_label = Label(self.list_box_frame, text=" ")
        empty_label.pack(side=LEFT, expand=TRUE, fill=BOTH)

        self.label_and_list_box_frame = Frame(self.list_box_frame)
        self.label_and_list_box_frame.pack(side=LEFT, expand=NO, fill="x")

        self.n_frames_gt_label = Label(self.label_and_list_box_frame)
        self.n_frames_gt_label["text"] = " "
        self.n_frames_gt_label.pack(side=TOP)

        self.n_active_frames_label = Label(self.label_and_list_box_frame)
        self.n_active_frames_label["text"] = " "
        self.n_active_frames_label.pack(side=TOP)

        scrollbar_frame = Frame(self.label_and_list_box_frame)
        scrollbar_frame.pack(side=TOP, expand=NO, fill="x")

        scrollbar = Scrollbar(scrollbar_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # listbox displaying the segments in the CINAC file
        self.list_box = Listbox(scrollbar_frame, bd=0,
                                background="white", selectmode=EXTENDED,  # selectmode=BROWSE,
                                exportselection=0,
                                height=15, selectbackground="red", highlightcolor="red",
                                font=("Arial", 10), yscrollcommand=scrollbar.set)
        # default height is 10
        # self.list_box.bind("<Double-Button-1>", self.select_cinac_file)
        # self.list_box.bind('<<ListboxSelect>>', self.segments_to_save_list_box_click)

        # width=20
        self.list_box.pack()

        # attach listbox to scrollbar
        scrollbar.config(command=self.list_box.yview)

        empty_label = Label(self.list_box_frame, text=" ")
        empty_label.pack(side=LEFT, expand=TRUE, fill=BOTH)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["predictions"] = RawFormatOptionModule(button_text="Predictions",
                                                                 label_text=" " * 50, with_file_dialog=True,
                                                                 file_dialog_filetypes=
                                                                 (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                                  ("Matlab files", "*.mat")),
                                                                 file_dialog_title="Select cells coordinate",
                                                                 root=self.root,
                                                                 mandatory=False,
                                                                 with_option_menu=True,
                                                                 menu_keyword_for_key="predictions",
                                                                 last_path_open=self.last_path_open,
                                                                 height_button=3, command_fct=None,
                                                                 default_path=self.default_path,
                                                                 master=button_frame)

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.modules_dict["classifier_model"] = RawFormatOptionModule(button_text="Classifier model",
                                                                      label_text=" " * 50, with_file_dialog=True,
                                                                      file_dialog_filetypes=
                                                                      (("Json file", "*.json"),),
                                                                      file_dialog_title="Select json model file",
                                                                      root=self.root,
                                                                      mandatory=False,
                                                                      with_option_menu=False,
                                                                      last_path_open=self.last_path_open,
                                                                      height_button=3, command_fct=None,
                                                                      default_path=self.default_path,
                                                                      master=button_frame)

        self.modules_dict["classifier_weights"] = RawFormatOptionModule(button_text="Classifier Weights",
                                                                        label_text=" " * 50, with_file_dialog=True,
                                                                        file_dialog_filetypes=(("h5 file", "*.h5"),),
                                                                        file_dialog_title="Select h5 weights file",
                                                                        root=self.root,
                                                                        mandatory=False,
                                                                        with_option_menu=False,
                                                                        last_path_open=self.last_path_open,
                                                                        height_button=3, command_fct=None,
                                                                        default_path=self.default_path,
                                                                        master=button_frame)

        self.modules_dict["classifier_weights"].add_exclusive_modules([self.modules_dict["predictions"]])
        self.modules_dict["classifier_model"].add_exclusive_modules([self.modules_dict["predictions"]])
        self.modules_dict["predictions"].add_exclusive_modules([self.modules_dict["classifier_weights"],
                                                                self.modules_dict["classifier_model"]])

        empty_label = Label(button_frame)
        empty_label["text"] = " "
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # --------------- Raster 1 section  ---------------
        self.modules_dict["raster_1"] = RawFormatOptionModule(button_text="Raster 1",
                                                              label_text=" " * 50, with_file_dialog=True,
                                                              file_dialog_filetypes=
                                                              (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                               ("Matlab files", "*.mat")),
                                                              file_dialog_title="Select raster 1",
                                                              root=self.root,
                                                              mandatory=False,
                                                              with_option_menu=True,
                                                              menu_keyword_for_key="raster",
                                                              last_path_open=self.last_path_open,
                                                              height_button=3, command_fct=None,
                                                              default_path=self.default_path,
                                                              master=button_frame)

        empty_label = Label(button_frame, text=" ")
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # --------------- Raster 2 section  ---------------
        self.modules_dict["raster_2"] = RawFormatOptionModule(button_text="Raster 2",
                                                              label_text=" " * 50, with_file_dialog=True,
                                                              file_dialog_filetypes=
                                                              (("Numpy files", "*.npy"), ("Numpy files", "*.npz"),
                                                               ("Matlab files", "*.mat")),
                                                              file_dialog_title="Select raster 2",
                                                              root=self.root,
                                                              mandatory=False,
                                                              with_option_menu=True,
                                                              menu_keyword_for_key="raster",
                                                              last_path_open=self.last_path_open,
                                                              height_button=3, command_fct=None,
                                                              default_path=self.default_path,
                                                              master=button_frame)

        empty_label = Label(self.button_frame, text=" " * 100)
        empty_label.pack(side=TOP, expand=FALSE, fill=None)

        self.deactivate_all_buttons()

        # track changes to its size
        button_frame.bind('<Configure>', self.__configure)

        # place the frame inside the canvas (this also
        # runs the __configure method)
        self.canvas.create_window(0, 0, window=button_frame, anchor=NW)

    def launch_exploratory_gui_for_a_segment(self, segment_selected):
        """
        Launch the exploratory GUI for a given segment
        Args:
            segment_selected: tuple of 3 int representing the cell, first_frame and last_frame

        Returns:

        """
        data_and_param = DataAndParam()
        segment_mode = True

        # now we want to load just the movie corresponding to this segment

        # already normalized movie
        tiff_movie = self.cinac_file_reader.get_segment_ci_movie(segment_selected)
        if tiff_movie is None:
            print(f"No movie for segment {segment_selected}")
            return

        if len(tiff_movie.shape) == 4:
            shape_list = tiff_movie.shape
            print("## launch_exploratory_gui_for_a_segment len(tiff_movie.shape) == 4")
            # then we remove the last dimension
            tiff_movie = np.reshape(tiff_movie, shape_list[:-1])

        avg_cell_map_img = np.mean(tiff_movie, axis=0)
        n_frames = tiff_movie.shape[0]

        coords_data = self.cinac_file_reader.get_segment_cells_contour(segment_selected)
        coords_data = [np.vstack((coord_data[0], coord_data[1])) for coord_data in coords_data]
        coord_obj = CellsCoord(coords=coords_data, pixel_masks=None, nb_lines=tiff_movie.shape[1],
                               nb_col=tiff_movie.shape[2],
                               from_matlab=False, invert_xy_coord=False)

        n_cells = coord_obj.n_cells

        raster_dur = np.zeros((n_cells, n_frames), dtype="int8")
        raster_dur[0, :] = self.cinac_file_reader.get_segment_raster_dur(segment_selected)

        spike_nums = np.zeros((n_cells, n_frames), dtype="int8")
        peak_nums = np.zeros((n_cells, n_frames), dtype="int8")
        for cell in np.arange(n_cells):
            transient_periods = get_continous_time_periods(raster_dur[cell])
            for transient_period in transient_periods:
                onset = transient_period[0]
                peak = transient_period[1]
                spike_nums[cell, onset] = 1
                peak_nums[cell, peak] = 1
        data_and_param.peak_nums = peak_nums
        data_and_param.spike_nums = spike_nums

        # invalid cells
        invalid_cells = self.cinac_file_reader.get_segment_invalid_cells(segment_selected)
        if invalid_cells is not None:
            # print(f"segment: {segment_selected}, invalid_cells {invalid_cells}")
            data_and_param.invalid_cells = invalid_cells
        raster_dur = np.zeros((n_cells, n_frames), dtype="int8")

        # 2d array representing the doubtful frames
        doubtful_frames_nums = np.zeros((n_cells, n_frames), dtype="int8")
        doubtful_frames_nums[0, :] = self.cinac_file_reader.get_segment_doubtful_frames(segment_selected)
        data_and_param.doubtful_frames_nums = doubtful_frames_nums

        data_and_param.tiff_movie = tiff_movie
        data_and_param.non_norm_tiff_movie = None
        data_and_param.coord_obj = coord_obj
        data_and_param.avg_cell_map_img = avg_cell_map_img
        data_and_param.raw_traces = coord_obj.build_raw_traces_from_movie(movie=tiff_movie)

        # smoothing the trace, but no demixing
        data_and_param.traces = np.copy(data_and_param.raw_traces)
        do_traces_smoothing(data_and_param.traces)

        # computing all potential peaks and onset from smooth_trace
        all_potential_peaks = np.zeros((n_cells, n_frames), dtype="int8")
        all_potential_onsets = np.zeros((n_cells, n_frames), dtype="int8")
        # then we do an automatic detection
        for cell in np.arange(n_cells):
            peaks, properties = signal.find_peaks(x=data_and_param.traces[cell], distance=2)
            if len(peaks) > 0:
                all_potential_peaks[cell, peaks] = 1

        for cell in np.arange(n_cells):
            onsets = []
            diff_values = np.diff(data_and_param.traces[cell])
            for index, value in enumerate(diff_values):
                if index == (len(diff_values) - 1):
                    continue
                if value < 0:
                    if diff_values[index + 1] >= 0:
                        onsets.append(index + 1)
            if len(onsets) > 0:
                all_potential_onsets[cell, np.array(onsets)] = 1
        data_and_param.all_potential_peaks = all_potential_peaks
        data_and_param.all_potential_onsets = all_potential_onsets

        # 0 because the cell of interest always has index 0
        data_and_param.cell_type_dict[0] = \
            self.cinac_file_reader.get_segment_cell_type(segment=segment_selected)

        title = f"cell {segment_selected[0]}, {segment_selected[1]} - {segment_selected[2]}"

        top = tk.Toplevel(self.root)
        f = ManualOnsetFrame(data_and_param=data_and_param, default_path=self.default_path,
                             segment_mode=segment_mode, parent=top, title=title)

        f.pack(fill="both", expand=True)
        # f.mainloop()

    def launch_exploratory_gui(self):
        """

        Returns:

        """
        # first we check if the data is correct

        # message box display
        # messagebox.showerror("Error", "Error message")
        # messagebox.showwarning("Warning", "Warning message")
        # messagebox.showinfo("Information", "Informative message")

        data_and_param = DataAndParam()
        segment_mode = False

        if self.ci_movie_file_name is None:
            # then a segment need to be selected
            cur_selection = self.list_box.curselection()
            if len(cur_selection) == 0:
                messagebox.showerror("Error", "You need to select a segment using the listbox")
                return
            # print(f"cur_selection {cur_selection}")
            # maximum number of windows opened
            max_windows_opened = 10
            for index_selection, index_clicked in enumerate(cur_selection):
                if index_selection >= max_windows_opened:
                    break
                segment_selected = self.gt_segments_list[int(index_clicked)]
                # print(f"index_clicked {index_clicked}")
                self.launch_exploratory_gui_for_a_segment(segment_selected=segment_selected)
            # if we close it then we have to select the cinac file again to open other segments
            # self.cinac_file_reader.close_file()
            return

        data_and_param.ci_movie_file_name = self.ci_movie_file_name

        # we normalize the movie for the classifier
        # non_norm_tiff_movie, tiff_movie = display_loading_window(message = "Loading the movie",
        #                                                          fct_to_run = load_movie,
        #                                                          args_for_fct={"file_name": self.ci_movie_file_name,
        #                                                                        "with_normalization": True,
        #                                                                        "verbose": True,
        #                                                                        "both_instances": True})
        non_norm_tiff_movie, tiff_movie = load_movie(file_name=self.ci_movie_file_name, with_normalization=True,
                                                     verbose=True, both_instances=True)

        avg_cell_map_img = np.mean(tiff_movie, axis=0)
        n_frames = tiff_movie.shape[0]

        coords_data = self.cinac_file_reader.get_coords_full_movie()
        coords_data = [np.vstack((coord_data[0], coord_data[1])) for coord_data in coords_data]
        coord_obj = CellsCoord(coords=coords_data, pixel_masks=None, nb_lines=tiff_movie.shape[1],
                               nb_col=tiff_movie.shape[2],
                               from_matlab=False, invert_xy_coord=False)

        n_cells = coord_obj.n_cells

        raster_dur = np.zeros((n_cells, n_frames), dtype="int8")
        self.cinac_file_reader.fill_raster_dur_from_segments(raster_dur)

        spike_nums = np.zeros((n_cells, n_frames), dtype="int8")
        peak_nums = np.zeros((n_cells, n_frames), dtype="int8")
        for cell in np.arange(n_cells):
            transient_periods = get_continous_time_periods(raster_dur[cell])
            for transient_period in transient_periods:
                onset = transient_period[0]
                peak = transient_period[1]
                # if onset == peak:
                #     print("onset == peak")
                spike_nums[cell, onset] = 1
                peak_nums[cell, peak] = 1
        data_and_param.peak_nums = peak_nums
        data_and_param.spike_nums = spike_nums

        # invalid cells
        invalid_cells = self.cinac_file_reader.get_invalid_cells()
        if invalid_cells is not None:
            data_and_param.invalid_cells = invalid_cells

        # 2d array representing the doubtful frames
        doubtful_frames_nums = np.zeros((n_cells, n_frames), dtype="int8")
        self.cinac_file_reader.fill_doubtful_frames_from_segments(doubtful_frames_nums)
        data_and_param.doubtful_frames_nums = doubtful_frames_nums

        other_rasters = []
        if self.modules_dict["raster_1"].activated and (self.modules_dict["raster_1"].file_name is not None):
            file_name = self.modules_dict["raster_1"].file_name
            attr_name = None
            if self.modules_dict["raster_1"].with_option_menu:
                attr_name = self.modules_dict["raster_1"].menu_variable.get()

            raster_1_data = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Raster 1",
                                                           attr_name=attr_name)

            # first we check that the data fit the movie dimension and the number of cells
            if raster_1_data.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Raster 1 dimensions {raster_1_data.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            other_rasters.append(raster_1_data)

        if self.modules_dict["raster_2"].activated and (self.modules_dict["raster_2"].file_name is not None):
            file_name = self.modules_dict["raster_2"].file_name
            attr_name = None
            if self.modules_dict["raster_2"].with_option_menu:
                attr_name = self.modules_dict["raster_2"].menu_variable.get()

            raster_2_data = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Raster 2",
                                                           attr_name=attr_name)
            if raster_2_data.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Raster 2 dimensions {raster_2_data.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            other_rasters.append(raster_2_data)

        if self.modules_dict["predictions"].activated:
            file_name = self.modules_dict["predictions"].file_name
            attr_name = None
            if self.modules_dict["predictions"].with_option_menu:
                attr_name = self.modules_dict["predictions"].menu_variable.get()

            predictions = load_data_from_npy_or_mat_file(file_name=file_name, data_descr="Predictions",
                                                         attr_name=attr_name)
            if predictions.shape != (n_cells, n_frames):
                messagebox.showerror("Error", f"Predictions dimensions {predictions.shape} don't match "
                                              f"the number of ROIs and movie length {(coord_obj.n_cells, n_frames)}")
                return
            data_and_param.classifier_predictions = predictions

        if self.modules_dict["classifier_model"].activated and self.modules_dict["classifier_weights"].activated:
            classifier_model_file = self.modules_dict["classifier_model"].file_name
            data_and_param.classifier_model_file = classifier_model_file
            classifier_weights_file = self.modules_dict["classifier_weights"].file_name
            data_and_param.classifier_weights_file = classifier_weights_file

        data_and_param.gt_segments = self.cinac_file_reader.get_all_segments()
        data_and_param.cell_type_dict = self.cinac_file_reader.get_all_cell_types()

        data_and_param.tiff_movie = tiff_movie
        data_and_param.non_norm_tiff_movie = non_norm_tiff_movie
        data_and_param.coord_obj = coord_obj
        data_and_param.avg_cell_map_img = avg_cell_map_img
        data_and_param.raw_traces = coord_obj.build_raw_traces_from_movie(movie=tiff_movie)
        # smoothing the trace, but no demixing
        data_and_param.traces = np.copy(data_and_param.raw_traces)
        do_traces_smoothing(data_and_param.traces)

        data_and_param.other_rasters = other_rasters

        # computing all potential peaks and onset from smooth_trace
        all_potential_peaks = np.zeros((n_cells, n_frames), dtype="int8")
        all_potential_onsets = np.zeros((n_cells, n_frames), dtype="int8")
        # then we do an automatic detection
        for cell in np.arange(n_cells):
            peaks, properties = signal.find_peaks(x=data_and_param.traces[cell], distance=2)
            all_potential_peaks[cell, peaks] = 1

        for cell in np.arange(n_cells):
            onsets = []
            diff_values = np.diff(data_and_param.traces[cell])
            for index, value in enumerate(diff_values):
                if index == (len(diff_values) - 1):
                    continue
                if value < 0:
                    if diff_values[index + 1] >= 0:
                        onsets.append(index + 1)
            all_potential_onsets[cell, np.array(onsets)] = 1
        data_and_param.all_potential_peaks = all_potential_peaks
        data_and_param.all_potential_onsets = all_potential_onsets

        # self.cinac_file_reader.close_file()

        f = ManualOnsetFrame(data_and_param=data_and_param, default_path=self.default_path,
                             segment_mode=segment_mode)
        f.mainloop()

    def select_ci_movie(self):
        """
                Open a file dialog to select to calcium imagine movie
                Returns:

                """
        if self.default_path is not None:
            initial_dir = self.default_path
        else:
            initial_dir = None

        file_name = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=(("Tiff files", "*.tif"), ("Tiff files", "*.tiff")),
            title="Select CINAC file",
            parent=self.root)

        # to put the window on the top
        self.root.lift()

        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            self.ci_movie_file_name = None
            self.ci_movie_label["text"] = " "
            self.deactivate_all_buttons()
            return

        # if self.ci_movie_file_name is None:
        #     self.ci_movie_button.pack(side=RIGHT)
        self.activate_all_buttons()
        self.ci_movie_file_name = file_name
        self.default_path, file_name_only = get_file_name_and_path(file_name)
        self.ci_movie_label["text"] = file_name_only

    def activate_all_buttons(self):
        self.modules_dict["predictions"].activate_only_label(enabling_button=True)
        self.modules_dict["classifier_model"].activate_only_label(enabling_button=True)
        self.modules_dict["classifier_weights"].activate_only_label(enabling_button=True)
        self.modules_dict["raster_1"].activate_only_label(enabling_button=True)
        self.modules_dict["raster_2"].activate_only_label(enabling_button=True)

    def deactivate_all_buttons(self):
        self.modules_dict["predictions"].deactivate(disabling_button=True)
        self.modules_dict["classifier_model"].deactivate(disabling_button=True)
        self.modules_dict["classifier_weights"].deactivate(disabling_button=True)
        self.modules_dict["raster_1"].deactivate(disabling_button=True)
        self.modules_dict["raster_2"].deactivate(disabling_button=True)

    def select_cinac_file(self):
        """
        Open a file dialog to select to cinac file to open
        and then change the GUI accordingly
        Returns:

        """
        if self.default_path is not None:
            initial_dir = self.default_path
        else:
            initial_dir = None

        file_name = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=(("CINAC files", "*.cinac"),),
            title="Select CINAC file",
            parent=self.root)

        # to put the window on the top
        self.root.lift()

        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            return

        self.launch_gui_button['state'] = "normal"

        self.cinac_file_name = file_name
        self.default_path, file_name_only = get_file_name_and_path(file_name)
        self.cinac_label["text"] = file_name_only

        # --- Reading the CINAC file ---
        self.cinac_file_reader = CinacFileReader(file_name=self.cinac_file_name)
        ci_movie_file_name = self.cinac_file_reader.get_ci_movie_file_name()
        if ci_movie_file_name is not None and os.path.exists(ci_movie_file_name):
            self.ci_movie_file_name = ci_movie_file_name
            ci_file_path, ci_file_name_only = get_file_name_and_path(self.ci_movie_file_name)
            self.ci_movie_label["text"] = ci_file_name_only
            # then we activate the button allowing to select predictions, raster etc...
            self.activate_all_buttons()
        elif self.cinac_file_reader.with_full_data():
            self.ci_movie_button['state'] = "normal"
            self.ci_movie_label["text"] = ""
            self.ci_movie_file_name = None
            self.deactivate_all_buttons()

        self.gt_segments_list = self.cinac_file_reader.get_all_segments()
        n_frames_gt = self.cinac_file_reader.get_n_frames_gt()
        n_active_frames = self.cinac_file_reader.get_n_active_frames()
        self.n_frames_gt_label["text"] = f"{n_frames_gt} frames"
        self.n_active_frames_label["text"] = f"{n_active_frames} active"
        self.list_box.delete('0', 'end')
        for period_index, period in enumerate(self.gt_segments_list):
            self.list_box.insert(END, f"{period[0]} / {period[1]}-{period[2]}")
            if period_index % 2 != 0:
                self.list_box.itemconfig(period_index, {'bg': 'royalblue'})
            else:
                self.list_box.itemconfig(period_index, {'bg': 'cornflowerblue'})

    def __configure(self, event):
        # update the scrollbars to match the size of the inner frame
        # size = self.button_frame.winfo_reqwidth(), self.button_frame.winfo_reqheight()
        # self.canvas.config(scrollregion="0 0 %s %s" % size)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=min(self.screen_width, 600),
                              height=min(self.screen_height, 1000))


class ManualAction:
    def __init__(self, session_frame, neuron, is_saved, x_limits=None, y_limits=None):
        self.session_frame = session_frame
        self.neuron = neuron
        self.is_saved = is_saved
        # tuple representing the limit of the plot when the action was done, used to get the same zoom
        # when undo or redo
        self.x_limits = x_limits
        self.y_limits = y_limits

    def undo(self):
        pass

    def redo(self):
        pass


class RemoveOnsetAction(ManualAction):
    def __init__(self, removed_times, **kwargs):
        super().__init__(**kwargs)
        self.removed_times = removed_times

    def undo(self):
        super().undo()
        self.session_frame.onset_times[self.neuron, self.removed_times] = 1
        self.session_frame.spike_nums[self.neuron, self.removed_times] = 1

    def redo(self):
        super().redo()

        self.session_frame.onset_times[self.neuron, self.removed_times] = 0
        self.session_frame.spike_nums[self.neuron, self.removed_times] = 0


class RemovePeakAction(ManualAction):
    def __init__(self, removed_times, amplitudes, removed_onset_action=None, **kwargs):
        super().__init__(**kwargs)
        self.removed_times = removed_times
        self.amplitudes = amplitudes
        self.removed_onset_action = removed_onset_action

    def undo(self):
        super().undo()
        self.session_frame.peak_nums[self.neuron, self.removed_times] = self.amplitudes
        if self.removed_onset_action is not None:
            self.removed_onset_action.undo()

    def redo(self):
        super().redo()
        self.session_frame.peak_nums[self.neuron, self.removed_times] = 0
        if self.removed_onset_action is not None:
            self.removed_onset_action.redo()


class AgreePeakAction(ManualAction):
    def __init__(self, agreed_peaks_index, agree_onset_action, agreed_peaks_values,
                 peaks_added, **kwargs):
        super().__init__(**kwargs)
        self.agreed_peaks_index = agreed_peaks_index
        self.agree_onset_action = agree_onset_action
        self.agreed_peaks_values = agreed_peaks_values
        self.peaks_added = peaks_added

    def undo(self):
        super().undo()
        self.session_frame.to_agree_peak_nums[self.neuron, self.agreed_peaks_index] = self.agreed_peaks_values
        self.session_frame.peak_nums[self.neuron, self.peaks_added] = 0
        if self.agree_onset_action is not None:
            self.agree_onset_action.undo()
        else:
            self.session_frame.update_to_agree_label()

    def redo(self):
        super().redo()
        self.session_frame.to_agree_peak_nums[self.neuron, self.agreed_peaks_index] = 0
        self.session_frame.peak_nums[self.neuron, self.peaks_added] = 1
        if self.agree_onset_action is not None:
            self.agree_onset_action.redo()
        else:
            self.session_frame.update_to_agree_label()


class DontAgreePeakAction(ManualAction):
    def __init__(self, not_agreed_peaks_index, dont_agree_onset_action, not_agreed_peaks_values,
                 **kwargs):
        super().__init__(**kwargs)
        self.not_agreed_peaks_index = not_agreed_peaks_index
        self.dont_agree_onset_action = dont_agree_onset_action
        self.not_agreed_peaks_values = not_agreed_peaks_values

    def undo(self):
        super().undo()
        self.session_frame.to_agree_peak_nums[self.neuron, self.not_agreed_peaks_index] = self.not_agreed_peaks_values
        if self.dont_agree_onset_action is not None:
            self.dont_agree_onset_action.undo()
        else:
            self.session_frame.update_to_agree_label()

    def redo(self):
        super().redo()
        self.session_frame.to_agree_peak_nums[self.neuron, self.not_agreed_peaks_index] = 0
        if self.dont_agree_onset_action is not None:
            self.dont_agree_onset_action.redo()
        else:
            self.session_frame.update_to_agree_label()


class DontAgreeOnsetAction(ManualAction):
    def __init__(self, not_agreed_onsets_index, not_agreed_onsets_values, **kwargs):
        super().__init__(**kwargs)
        self.not_agreed_onsets_index = not_agreed_onsets_index
        self.not_agreed_onsets_values = not_agreed_onsets_values

    def undo(self):
        super().undo()
        self.session_frame.to_agree_spike_nums[
            self.neuron, self.not_agreed_onsets_index] = self.not_agreed_onsets_values
        self.session_frame.update_to_agree_label()

    def redo(self):
        super().redo()
        self.session_frame.to_agree_spike_nums[self.neuron, self.not_agreed_onsets_index] = 0
        self.session_frame.update_to_agree_label()


class AgreeOnsetAction(ManualAction):
    def __init__(self, agreed_onsets_index, agreed_onsets_values, onsets_added, **kwargs):
        super().__init__(**kwargs)
        self.agreed_onsets_index = agreed_onsets_index
        self.onsets_added = onsets_added
        self.agreed_onsets_values = agreed_onsets_values

    def undo(self):
        super().undo()
        self.session_frame.to_agree_spike_nums[self.neuron, self.agreed_onsets_index] = self.agreed_onsets_values
        self.session_frame.onset_times[self.neuron, self.onsets_added] = 0
        self.session_frame.spike_nums[self.neuron, self.onsets_added] = 0
        self.session_frame.update_to_agree_label()

    def redo(self):
        super().redo()
        self.session_frame.to_agree_spike_nums[self.neuron, self.agreed_onsets_index] = 0
        self.session_frame.onset_times[self.neuron, self.onsets_added] = 1
        self.session_frame.spike_nums[self.neuron, self.onsets_added] = 1
        self.session_frame.update_to_agree_label()


class AddOnsetAction(ManualAction):
    def __init__(self, added_time, add_peak_action=None, **kwargs):
        """

        :param added_time:
        :param add_peak_action: if not None, means a add peak action has been associated to an add onset
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.added_time = added_time
        self.add_peak_action = add_peak_action

    def undo(self):
        super().undo()
        self.session_frame.onset_times[self.neuron, self.added_time] = 0
        self.session_frame.spike_nums[self.neuron, self.added_time] = 0
        if self.add_peak_action is not None:
            self.add_peak_action.undo()

    def redo(self):
        super().redo()
        self.session_frame.onset_times[self.neuron, self.added_time] = 1
        self.session_frame.spike_nums[self.neuron, self.added_time] = 1
        if self.add_peak_action is not None:
            self.add_peak_action.redo()


class AddThemAllAction(ManualAction):
    def __init__(self, first_frame, last_frame, old_peak_values, new_peak_values, old_onset_values,
                 new_onset_values, **kwargs):
        super().__init__(**kwargs)
        self.first_frame = first_frame
        self.last_frame = last_frame
        self.old_peak_values = old_peak_values
        self.new_peak_values = new_peak_values
        self.old_onset_values = old_onset_values
        self.new_onset_values = new_onset_values

    def undo(self):
        super().undo()
        self.session_frame.peak_nums[self.neuron, self.first_frame:self.last_frame + 1] = self.old_peak_values
        self.session_frame.onset_times[self.neuron, self.first_frame:self.last_frame + 1] = self.old_onset_values
        self.session_frame.spike_nums[self.neuron, self.first_frame:self.last_frame + 1] = self.old_onset_values

    def redo(self):
        super().redo()
        self.session_frame.peak_nums[self.neuron, self.first_frame:self.last_frame + 1] = self.new_peak_values
        self.session_frame.onset_times[self.neuron, self.first_frame:self.last_frame + 1] = self.new_onset_values
        self.session_frame.spike_nums[self.neuron, self.first_frame:self.last_frame + 1] = self.new_onset_values


class AddSegmentToSaveAction(ManualAction):
    def __init__(self, segment_list, segment_added, **kwargs):
        super().__init__(**kwargs)
        self.segment_list = segment_list
        self.segment_added = segment_added

    def undo(self):
        super().undo()
        self.session_frame.segments_to_save_list = self.segment_list.copy()
        self.session_frame.update_segments_to_save_list_box()

    def redo(self):
        super().redo()
        self.session_frame.segments_to_save_list = self.segment_list.copy()
        self.session_frame.segments_to_save_list.append(self.segment_added)
        self.session_frame.update_segments_to_save_list_box()


class RemoveSegmentToSaveAction(ManualAction):
    def __init__(self, segment_list, segment_added, index_to_remove, **kwargs):
        super().__init__(**kwargs)
        self.segment_list = segment_list
        self.segment_added = segment_added
        self.index_to_remove = index_to_remove

    def undo(self):
        super().undo()
        self.session_frame.segments_to_save_list = self.segment_list.copy()
        self.session_frame.update_segments_to_save_list_box()

    def redo(self):
        super().redo()
        self.session_frame.remove_segment_to_save(index_to_remove=self.index_to_remove)


class AddPeakAction(ManualAction):
    def __init__(self, added_time, amplitude, **kwargs):
        super().__init__(**kwargs)
        self.added_time = added_time
        self.amplitude = amplitude

    def undo(self):
        super().undo()
        self.session_frame.peak_nums[self.neuron, self.added_time] = 0

    def redo(self):
        super().redo()
        self.session_frame.peak_nums[self.neuron, self.added_time] = 1


class AddDoubtfulFramesAction(ManualAction):
    def __init__(self, x_from, x_to, backup_values, **kwargs):
        super().__init__(**kwargs)
        self.x_from = x_from
        self.x_to = x_to
        self.backup_values = backup_values

    def undo(self):
        super().undo()
        self.session_frame.doubtful_frames_nums[self.neuron, self.x_from:self.x_to] = self.backup_values
        self.session_frame.update_doubtful_frames_periods(cell=self.neuron)

    def redo(self):
        super().redo()
        self.session_frame.doubtful_frames_nums[self.neuron, self.x_from:self.x_to] = 1
        self.session_frame.update_doubtful_frames_periods(cell=self.neuron)


class RemoveDoubtfulFramesAction(ManualAction):
    def __init__(self, removed_times, **kwargs):
        super().__init__(**kwargs)
        self.removed_times = removed_times

    def undo(self):
        super().undo()
        self.session_frame.doubtful_frames_nums[self.neuron, self.removed_times] = 1
        self.session_frame.update_doubtful_frames_periods(cell=self.neuron)

    def redo(self):
        super().redo()
        self.session_frame.doubtful_frames_nums[self.neuron, self.removed_times] = 0
        self.session_frame.update_doubtful_frames_periods(cell=self.neuron)


class AddMvtFramesAction(ManualAction):
    def __init__(self, x_from, x_to, backup_values, **kwargs):
        super().__init__(**kwargs)
        self.x_from = x_from
        self.x_to = x_to
        self.backup_values = backup_values

    def undo(self):
        super().undo()
        self.session_frame.mvt_frames_nums[self.neuron, self.x_from:self.x_to] = self.backup_values
        self.session_frame.update_mvt_frames_periods(cell=self.neuron)

    def redo(self):
        super().redo()
        self.session_frame.mvt_frames_nums[self.neuron, self.x_from:self.x_to] = 1
        self.session_frame.update_mvt_frames_periods(cell=self.neuron)


class RemoveMvtFramesAction(ManualAction):
    def __init__(self, removed_times, **kwargs):
        super().__init__(**kwargs)
        self.removed_times = removed_times

    def undo(self):
        super().undo()
        self.session_frame.mvt_frames_nums[self.neuron, self.removed_times] = 1
        self.session_frame.update_mvt_frames_periods(cell=self.neuron)

    def redo(self):
        super().redo()
        self.session_frame.mvt_frames_nums[self.neuron, self.removed_times] = 0
        self.session_frame.update_mvt_frames_periods(cell=self.neuron)


def get_file_name_and_path(path_file):
    # to get real index, remove 1
    last_slash_index = len(path_file) - path_file[::-1].find("/")
    if last_slash_index == -1:
        return None, None,

    # return path and file_name
    return path_file[:last_slash_index], path_file[last_slash_index:]


def do_traces_smoothing(traces):
    # TODO: try butternot filter for a high band filter and then use signal.filtfilt for shifting the smooth signal.
    # smoothing the trace
    windows = ['hanning', 'hamming', 'bartlett', 'blackman']
    i_w = 1
    window_length = 7  # 11
    for i in np.arange(traces.shape[0]):
        smooth_signal = smooth_convolve(x=traces[i], window_len=window_length,
                                        window=windows[i_w])
        beg = (window_length - 1) // 2
        traces[i] = smooth_signal[beg:-beg]


class MyCanvas(FigureCanvasTkAgg):
    def __init__(self, figure, parent_frame, manual_onset_frame):
        FigureCanvasTkAgg.__init__(self, figure, parent_frame)

    def button_press_event(self, event, **args):
        print(f"{event.__dict__}")
        # Event attributes
        # {'serial': 517, 'num': 1, 'height': '??', 'keycode': '??', 'state': 0, 'time': 1091938502, 'width': '??',
        # 'x': 399, 'y': 135, 'char': '??', 'send_event': False, 'keysym': '??', 'keysym_num': '??',
        # 'type': <EventType.ButtonPress: '4'>, 'widget': <tkinter.Canvas object .!manualonsetframe.!frame2.!canvas>,
        # 'x_root': 455, 'y_root': 267, 'delta': 0}
        # num is the button number
        if 'dblclick' not in args:
            dblclick = False
        else:
            dblclick = True
        print(f"event['x']: {event.x}, event['y']: {event.x}, dblclick: {dblclick}")
        super().button_press_event(event, **args)


class ManualOnsetFrame(tk.Frame):
    # use by trace_combo_box to select the trace to display
    RAW_TRACE = "Cell"
    RAW_TRACE_WITHOUT_OVERLAP = "Cell no over"
    NEUROPIL_TRACE = "Neuropil (Np)"
    RAW_M_NEUROPIL_TRACE = "Cell no over - Np"

    def __init__(self, data_and_param, default_path=None, segment_mode=False, parent=None, title=None):
        """

        Args:
            data_and_param:
            default_path:
            segment_mode: if True, means the data represent just a segment used for Ground Truth.
            Then all options won't be available. It won't be possible to zoom, to modify the ground truth etc...
        """

        self.segment_mode = segment_mode
        # ------ constants for controlling layout ------
        top_buttons_frame_padx = "2m"
        top_buttons_frame_pady = "2m"
        top_buttons_frame_ipadx = "1m"
        top_buttons_frame_ipady = "1m"
        # -------------- end constants ----------------

        cm_data = [[0.2081, 0.1663, 0.5292], [0.2116238095, 0.1897809524, 0.5776761905],
                   [0.212252381, 0.2137714286, 0.6269714286], [0.2081, 0.2386, 0.6770857143],
                   [0.1959047619, 0.2644571429, 0.7279], [0.1707285714, 0.2919380952,
                                                          0.779247619], [0.1252714286, 0.3242428571, 0.8302714286],
                   [0.0591333333, 0.3598333333, 0.8683333333], [0.0116952381, 0.3875095238,
                                                                0.8819571429],
                   [0.0059571429, 0.4086142857, 0.8828428571],
                   [0.0165142857, 0.4266, 0.8786333333], [0.032852381, 0.4430428571,
                                                          0.8719571429], [0.0498142857, 0.4585714286, 0.8640571429],
                   [0.0629333333, 0.4736904762, 0.8554380952], [0.0722666667, 0.4886666667,
                                                                0.8467], [0.0779428571, 0.5039857143, 0.8383714286],
                   [0.079347619, 0.5200238095, 0.8311809524], [0.0749428571, 0.5375428571,
                                                               0.8262714286],
                   [0.0640571429, 0.5569857143, 0.8239571429],
                   [0.0487714286, 0.5772238095, 0.8228285714], [0.0343428571, 0.5965809524,
                                                                0.819852381], [0.0265, 0.6137, 0.8135],
                   [0.0238904762, 0.6286619048,
                    0.8037619048], [0.0230904762, 0.6417857143, 0.7912666667],
                   [0.0227714286, 0.6534857143, 0.7767571429], [0.0266619048, 0.6641952381,
                                                                0.7607190476],
                   [0.0383714286, 0.6742714286, 0.743552381],
                   [0.0589714286, 0.6837571429, 0.7253857143],
                   [0.0843, 0.6928333333, 0.7061666667], [0.1132952381, 0.7015, 0.6858571429],
                   [0.1452714286, 0.7097571429, 0.6646285714], [0.1801333333, 0.7176571429,
                                                                0.6424333333],
                   [0.2178285714, 0.7250428571, 0.6192619048],
                   [0.2586428571, 0.7317142857, 0.5954285714], [0.3021714286, 0.7376047619,
                                                                0.5711857143],
                   [0.3481666667, 0.7424333333, 0.5472666667],
                   [0.3952571429, 0.7459, 0.5244428571], [0.4420095238, 0.7480809524,
                                                          0.5033142857], [0.4871238095, 0.7490619048, 0.4839761905],
                   [0.5300285714, 0.7491142857, 0.4661142857], [0.5708571429, 0.7485190476,
                                                                0.4493904762],
                   [0.609852381, 0.7473142857, 0.4336857143],
                   [0.6473, 0.7456, 0.4188], [0.6834190476, 0.7434761905, 0.4044333333],
                   [0.7184095238, 0.7411333333, 0.3904761905],
                   [0.7524857143, 0.7384, 0.3768142857], [0.7858428571, 0.7355666667,
                                                          0.3632714286], [0.8185047619, 0.7327333333, 0.3497904762],
                   [0.8506571429, 0.7299, 0.3360285714], [0.8824333333, 0.7274333333, 0.3217],
                   [0.9139333333, 0.7257857143, 0.3062761905], [0.9449571429, 0.7261142857,
                                                                0.2886428571],
                   [0.9738952381, 0.7313952381, 0.266647619],
                   [0.9937714286, 0.7454571429, 0.240347619], [0.9990428571, 0.7653142857,
                                                               0.2164142857], [0.9955333333, 0.7860571429, 0.196652381],
                   [0.988, 0.8066, 0.1793666667], [0.9788571429, 0.8271428571, 0.1633142857],
                   [0.9697, 0.8481380952, 0.147452381], [0.9625857143, 0.8705142857, 0.1309],
                   [0.9588714286, 0.8949, 0.1132428571], [0.9598238095, 0.9218333333,
                                                          0.0948380952], [0.9661, 0.9514428571, 0.0755333333],
                   [0.9763, 0.9831, 0.0538]]

        self.parula_map = LinearSegmentedColormap.from_list('parula', cm_data)

        if parent is None:
            self.root = Tk()
            self.root.protocol("WM_DELETE_WINDOW", self.validation_before_closing)
        else:
            self.root = parent
        # self.root.title(f"Session {session_number}")
        tk.Frame.__init__(self, master=self.root)
        if title is not None:
            self.root.title(title)
        self.pack(
            ipadx=top_buttons_frame_ipadx,
            ipady=top_buttons_frame_ipady,
            padx=top_buttons_frame_padx,
            pady=top_buttons_frame_pady,
        )
        # self.pack()

        # ------------ colors  -----------------
        # TODO: put option for different color set (skins), use http://colorbrewer2.org
        self.color_onset = "#225ea8"  # "darkblue" #"darkgoldenrod" #"dimgrey"
        self.color_raw_trace = "#ffffcc"  # "light yellow"
        self.color_early_born = "darkgreen"
        self.color_peak = "#41b6c4"  # "blue"
        self.color_edge_peak = "#a1dab4"  # "white"
        self.color_peak_under_threshold = "red"
        self.color_threshold_line = "red"  # "cornflowerblue"
        self.color_mark_to_remove = "white"
        self.color_run_period = "lightcoral"
        # self.color_raw_trace = "darkgoldenrod"
        self.color_trace = "#a1dab4"  # "cornflowerblue"
        self.classifier_filling_color = "#2c7fb8"
        self.color_transient_predicted_to_look_at = "#ffffcc"
        self.color_bg_predicted_transient_list_box = "#41b6c4"
        self.color_text_gui_default = "#225ea8"
        # dark gray
        self.background_color = "#252525"
        self.map_img_bg_color = "#252525"
        # ------------- colors (end) --------

        # filename on which to save spikenums, is defined when save as is clicked
        self.save_file_name = None
        # path where to save the file_name
        self.save_path = default_path
        self.save_checked_predictions_dir = default_path
        self.display_threshold = False
        # to display a color code for the peaks depending on the correlation between the source and transient profile
        # changed when clicking on the checkbox
        self.display_correlations = False
        # if False, remove this option, compute faster when loading a cell
        self.correlation_for_each_peak_option = True
        # in number of frames, one frame = 100 ms
        self.decay = 10
        # factor to multiply to decay to define delay between onset and peak
        self.decay_factor = 1
        # number of std of trace to add to the threshold
        self.nb_std_thresold = 0.1
        self.correlation_thresold = 0.5
        self.data_and_param = data_and_param

        self.other_rasters = self.data_and_param.other_rasters
        # checkingif data is binary, if not, we put the value between 0 and 1 for display purpose
        if (self.other_rasters is not None) and len(self.other_rasters) > 0:
            for raster_index, raster in enumerate(self.other_rasters):
                unique_values = np.unique(raster)
                if len(unique_values) <= 2 and np.min(unique_values) >= 0 and np.max(unique_values) <= 1:
                    continue
                raster = raster.astype("float")
                for cell in np.arange(len(raster)):
                    raster[cell] = norm01(raster[cell])
                self.other_rasters[raster_index] = raster

        self.other_rasters_colors = ["green", "cornflowerblue", "orange"]

        # will be a 2D array of len n_cells * n_frames and the value
        # will correspond to the correlation of the peak transient
        # at that frame (if identified, value will be -2 for non identified peak)
        self.peaks_correlation = None
        # dict with key an int representing the cell, and as value a set of int (cells)
        self.overlapping_cells = self.data_and_param.coord_obj.intersect_cells

        # use to display the square around the cell in avg map
        # the first key is an int representing the length of the square, the second int represent the cell number.
        self.square_coord_around_cell_dict = dict()
        # neuron's trace displayed
        self.current_neuron = 0
        self.tiff_movie = self.data_and_param.tiff_movie
        self.n_frames = len(self.tiff_movie)
        self.center_coord = self.data_and_param.coord_obj.center_coord
        self.path_data = self.data_and_param.path_data
        self.spike_nums = data_and_param.spike_nums
        self.nb_neurons = self.data_and_param.coord_obj.n_cells
        self.nb_times = self.n_frames
        # take as key int representing the cell index, and as value a string representing the cell type
        self.cell_type_dict = self.data_and_param.cell_type_dict

        self.raw_traces = self.data_and_param.raw_traces
        # constructued in self._build_traces(), build from pixels only of a cell
        self.raw_traces_without_overlap = None
        self.smooth_traces = self.data_and_param.traces
        self.normalize_traces()
        # will contains the differents trace for each cell (neuropil, raw trace, etc...)
        self.traces_dict = dict()
        self.traces_color_dict = dict()
        self.traces_color_dict[self.RAW_TRACE] = self.color_raw_trace
        self.traces_color_dict[self.RAW_TRACE_WITHOUT_OVERLAP] = "orange"
        self.traces_color_dict[self.NEUROPIL_TRACE] = "blue"
        self.traces_color_dict[self.RAW_M_NEUROPIL_TRACE] = "cornflowerblue"

        self._build_traces()
        # indicate which traces need to be display now, corresponds to a key of self.traces_dict
        self.actual_traces_str = [self.RAW_TRACE]
        # fluorescence signal that will be displayed over the movie animation
        # use to keep in memory the signal fitted to the movie in order to save memory. 
        self.traces_for_movie_dict = dict()
        self.traces_for_movie_with_zoom_dict = dict()

        # will be initialize in the function normalize_traces
        self.ratio_traces = None
        # we plot a trace that show the ratio between smooth_traces and raw_traces
        # it could be useful if the smooth_traces is partially demixed
        self.use_ratio_traces = False
        self.nb_times_traces = len(self.raw_traces[0, :])
        # dimension reduction in order to fit to smooth_traces times, for onset times
        self.onset_times = np.zeros((self.nb_neurons, self.nb_times), dtype="int8")
        self.onset_numbers_label = None
        self.update_onset_times()
        self.peak_nums = self.data_and_param.peak_nums
        self.to_agree_peak_nums = self.data_and_param.to_agree_peak_nums
        self.to_agree_spike_nums = self.data_and_param.to_agree_spike_nums
        # print(f"len(peak_nums) {len(peak_nums)}")
        self.display_mvt = False

        self.source_profile_dict = dict()
        self.source_profile_dict_for_map_of_all_cells = dict()
        # key is int (cell), value is a list with the source profile used for correlation, and the mask
        self.source_profile_correlation_dict = dict()
        # key is the cell and then value is a dict with key the tuple transient (onset, peak)
        # self.corr_source_transient = dict()

        # initializing inter_neurons and cells_to_remove
        self.inter_neurons = np.zeros(self.nb_neurons, dtype="uint8")
        if self.data_and_param.inter_neurons is not None:
            for inter_neuron in self.data_and_param.inter_neurons:
                self.inter_neurons[inter_neuron] = 1
        self.cells_to_remove = np.zeros(self.nb_neurons, dtype="bool")
        if self.data_and_param.cells_to_remove is not None:
            # self.data_and_param.cells_to_remove is actually a list of one array with all cells to remove as an int
            for cell_to_remove in self.data_and_param.cells_to_remove:
                self.cells_to_remove[cell_to_remove] = 1
        if self.data_and_param.invalid_cells is not None:
            self.cells_to_remove = self.data_and_param.invalid_cells

        # Key cell,
        # value: list of tuple of 2 int indicating the beginning and end of each corrupt frames period
        self.doubtful_frames_periods = dict()
        if self.data_and_param.doubtful_frames_nums is not None:
            self.doubtful_frames_nums = self.data_and_param.doubtful_frames_nums
            for cell in np.arange(self.nb_neurons):
                self.update_doubtful_frames_periods(cell=cell)
        else:
            self.doubtful_frames_nums = np.zeros((self.nb_neurons, self.nb_times_traces), dtype="int8")

        # Key cell,
        # value: list of tuple of 2 int indicating the beginning and end of each mvt frames period
        # TODO: decomment to reactivate mvt
        # not used, aim to display period of movement from the subject recorded
        self.mvt_frames_periods = None  # dict()
        # if self.data_and_param.mvt_frames_nums is not None:
        #     self.mvt_frames_nums = self.data_and_param.mvt_frames_nums
        #     for cell in np.arange(self.nb_neurons):
        #         self.update_mvt_frames_periods(cell=cell)
        # else:
        #     self.mvt_frames_nums = np.zeros((self.nb_neurons, self.nb_times_traces), dtype="int8")

        # indicate if an action might remove or add an onset
        self.add_onset_mode = False
        self.remove_onset_mode = False
        self.add_peak_mode = False
        self.remove_peak_mode = False
        self.remove_all_mode = False
        self.add_doubtful_frames_mode = False
        self.remove_doubtful_frames_mode = False
        self.add_mvt_frames_mode = False
        self.remove_mvt_frames_mode = False
        self.dont_agree_mode = False
        self.agree_mode = False
        self.center_segment_mode = False
        # default length of a segment for ground truth
        self.segment_to_center_length = 200
        # x coordinate of the center of the segment for ground_truth
        self.center_segment_coord = None
        # used to remove under the threshold (std or correlation value)
        self.peaks_under_threshold_index = None
        # to know if the actual displayed is saved
        self.is_saved = True
        # used to known if the mouse has been moved between the click and the release
        self.last_click_position = (-1, -1)
        self.first_click_to_remove = None
        self.click_corr_coord = None
        # not used anymore for the UNDO action
        # self.last_action = None
        # list of the last action, used for the undo method, the last one being the last
        self.last_actions = []
        # list of action that has been undone
        self.undone_actions = []

        # check if a transient classifier model is available
        self.classifier_model_file = data_and_param.classifier_model_file
        self.classifier_weights_file = data_and_param.classifier_weights_file
        self.classifier_model = None
        self.cinac_recording = None
        if (self.classifier_model_file is not None) and (self.classifier_weights_file is not None):
            try:
                import tensorflow as tf
                tf_version = tf.__version__
                if tf_version[0] == "2":
                    from tensorflow.keras.models import model_from_json
                else:
                    from keras.models import model_from_json
            except ImportError as import_error:
                print("Seems like you don't have the Keras or tensorflow package installed")
                raise import_error

            # Model reconstruction from JSON file
            with open(self.classifier_model_file, 'r') as f:
                self.classifier_model = model_from_json(f.read())

            # Load weights into the new model
            self.classifier_model.load_weights(self.classifier_weights_file)

            # creating an instance of CinacRecording used for the classifier
            self.cinac_recording = CinacRecording(identifier="cinac_gui")
            cinac_movie = CinacDataMovie(movie=self.tiff_movie, already_normalized=True)
            self.cinac_recording.set_movie(cinac_movie)
            self.cinac_recording.coord_obj = self.data_and_param.coord_obj

        # check if a cell type classifier model is available
        self.cell_types_for_classifier = self.data_and_param.cell_types_for_classifier
        self.cell_type_from_code_dict = self.data_and_param.cell_type_from_code_dict
        self.cell_type_classifier_model_file = data_and_param.cell_type_classifier_model_file
        self.cell_type_classifier_weights_file = data_and_param.cell_type_classifier_weights_file
        # dict with key being the cell id, and value being a dict with key the cell_type and value the prediction
        self.cell_type_classifier_predictions = self.data_and_param.cell_type_classifier_predictions
        # indicate if cell_type predictions are already loaded, if Not model and weight files will be used to predict
        # if available
        self.cell_type_predictions_loaded = True
        # dict with key being the cell id, and value being a dict with key the cell_type and value the prediction
        if self.cell_type_classifier_predictions is None:
            self.cell_type_predictions_loaded = False
            self.cell_type_classifier_predictions = dict()
        self.cell_type_classifier_model = None
        # if True, then we display the cell type labels
        self.display_cell_type_classifier_field = False
        if (self.cell_types_for_classifier is not None) and \
                (((self.cell_type_classifier_weights_file is not None) and (
                        self.cell_type_classifier_model_file is not None)) \
                 or (self.cell_type_classifier_predictions is not None)):
            self.display_cell_type_classifier_field = True
            if (self.cell_type_classifier_weights_file is not None) and \
                    (self.cell_type_classifier_model_file is not None):
                if self.cinac_recording is None:
                    # creating an instance of CinacRecording used for the classifier
                    self.cinac_recording = CinacRecording(identifier="cinac_gui")
                    cinac_movie = CinacDataMovie(movie=self.tiff_movie, already_normalized=True)
                    self.cinac_recording.set_movie(cinac_movie)
                    self.cinac_recording.coord_obj = self.data_and_param.coord_obj

        self.show_transient_classifier = False
        self.transient_classifier_threshold = 0.5
        # try to improve predictions
        self.prediction_improvement_mode = False
        # key is cell index, value is a np.array of length n_frames with value to 1 if prediction is considered as False
        self.prediction_improvement_dict = dict()
        # key is int representing the cell number, and value will be an array of 2D with line representing the frame index
        # and the colums being a float reprenseing for each frame
        # the probability for the cell to be active for each class
        self.transient_prediction = dict()
        # first key is an int (cell), value is a dict
        # the second key is a float representing a threshold, and the value is a list of tuple
        self.transient_prediction_periods = dict()
        # the cell and frame (tuple) in which a vertical line
        # will be draw to indicate at which transient we're looking at
        self.last_predicted_transient_selected = None
        # checking if a prediction results are already loaded in mouse_sessions
        if self.data_and_param.classifier_predictions is not None:
            print(f"Activity classifier predictions available")
            for cell in np.arange(self.nb_neurons):
                self.transient_prediction_periods[cell] = dict()
                cell_predictions = self.data_and_param.classifier_predictions[cell]
                cell_predictions = cell_predictions.reshape((len(cell_predictions), 1))
                self.transient_prediction[cell] = cell_predictions
        # each key is a cell, the value is a binary array with 1 between onsets and peaks
        # used for predictions
        self.raster_dur_for_a_cell = dict()
        # the prediction values border for which we would like the check the transients
        self.uncertain_prediction_values = (0.25, 0.65)
        # list of tuple (cell, first frame, last frame (included), max prediction)
        self.transient_prediction_periods_to_check = []
        # set of tuple (cell, first frame, last frame (included))
        self.segments_to_save_list = self.data_and_param.gt_segments
        # use to display the square around the cell in avg map
        # if True, display a frame representing what will be given to the classifier
        # given the list_box_segment value
        self.display_classifier_frame_around_cell = not self.segment_mode
        # if True, display a frame representing the part that will be zoom when the movie will be played
        self.display_zoom_frame_around_cell = not self.segment_mode
        # indicate if the zoom is active while playing the movie
        self.size_zoom_pixels = 80
        # we adapt the zoom_pixels to the size of the movie
        min_dim_movie = min(self.tiff_movie.shape[1], self.tiff_movie.shape[2])

        if self.segment_mode or (min_dim_movie < self.size_zoom_pixels):
            self.movie_zoom_mode = False
        else:
            self.movie_zoom_mode = True

        # polygon patches use to display the square, need to be kept in memory
        self.square_classifier_patch = None
        self.square_zoom_patch = None

        # to print transient predictions stat only once
        self.print_transients_predictions_stat = False
        # TODO change it by a list of other infered neuronal activity
        self.caiman_spike_nums = None

        # Three Vertical frames to start
        # -------------- left frame (start) ----------------
        left_side_frame = Frame(self)
        left_side_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        # self.spin_box_button = Spinbox(left_side_frame, from_=0, to=self.nb_neurons - 1, fg="blue", justify=CENTER,
        #                                width=4, state="readonly")
        # self.spin_box_button["command"] = event_lambda(self.spin_box_update)
        # # self.spin_box_button.config(command=event_lambda(self.spin_box_update))
        # self.spin_box_button.pack(side=LEFT)

        empty_label = Label(left_side_frame)
        empty_label["text"] = ""
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # self.neuron_string_var = StringVar()
        entry_neuron_frame = Frame(left_side_frame)
        entry_neuron_frame.pack(side=TOP, expand=NO, fill="x")
        self.neuron_entry_widget = Entry(entry_neuron_frame, fg=self.color_text_gui_default, justify=CENTER,
                                         width=3)
        self.neuron_entry_widget.insert(0, "0")
        self.neuron_entry_widget.bind("<KeyRelease>", self.go_to_neuron_button_action)
        # self.neuron_string_var.set("0")
        # self.neuron_string_var.trace("w", self.neuron_entry_change)
        # self.neuron_entry_widget.focus_set()
        self.neuron_entry_widget.pack(side=LEFT, expand=YES, fill="x")

        self.go_button = Button(entry_neuron_frame)
        self.go_button["text"] = ' GO '
        self.go_button["fg"] = self.color_text_gui_default
        self.go_button["command"] = event_lambda(self.go_to_neuron_button_action)
        self.go_button.pack(side=LEFT, expand=YES, fill="x")

        change_neuron_frame = Frame(left_side_frame)
        change_neuron_frame.pack(side=TOP, expand=NO, fill="x")

        self.prev_button = Button(change_neuron_frame)
        self.prev_button["text"] = '<-'
        self.prev_button["fg"] = self.color_text_gui_default
        self.prev_button['state'] = DISABLED  # ''normal
        self.prev_button["command"] = event_lambda(self.select_previous_neuron)
        self.prev_button.pack(side=LEFT, expand=YES, fill="x")

        # empty_label = Label(change_neuron_frame)
        # empty_label["text"] = ""
        # empty_label.pack(side=LEFT)

        self.neuron_label = Label(change_neuron_frame)
        self.neuron_label["text"] = f"0 / {self.nb_neurons - 1}"
        self.neuron_label["fg"] = "red"
        self.neuron_label.pack(side=LEFT, expand=YES, fill="x")

        # empty_label = Label(change_neuron_frame)
        # empty_label["text"] = ""
        # empty_label.pack(side=LEFT)

        self.next_button = Button(change_neuron_frame)
        self.next_button["text"] = '->'
        self.next_button["fg"] = self.color_text_gui_default
        self.next_button["command"] = event_lambda(self.select_next_neuron)
        self.next_button.pack(side=LEFT, expand=YES, fill="x")

        # empty_label = Label(left_side_frame)
        # empty_label["text"] = " " * 2
        # empty_label.pack(side=LEFT)
        sep = ttk.Separator(left_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        self.add_doubtful_frames_mode_button = Button(left_side_frame)
        self.add_doubtful_frames_mode_button["text"] = ' + DOUBT OFF '
        self.add_doubtful_frames_mode_button["fg"] = 'red'
        self.add_doubtful_frames_mode_button["command"] = self.add_doubtful_frames_switch_mode
        self.add_doubtful_frames_mode_button.pack(side=TOP)
        # expand=NO, fill="x"
        # empty_label = Label(left_side_frame)
        # empty_label["text"] = " " * 1
        # empty_label.pack(side=LEFT)

        self.remove_doubtful_frames_button = Button(left_side_frame)
        self.remove_doubtful_frames_button["text"] = ' - DOUBT OFF '
        self.remove_doubtful_frames_button["fg"] = 'red'
        self.remove_doubtful_frames_button["command"] = self.remove_doubtful_frames_switch_mode
        self.remove_doubtful_frames_button.pack(side=TOP)

        if self.mvt_frames_periods is not None:
            sep = ttk.Separator(left_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            self.add_mvt_frames_mode_button = Button(left_side_frame)
            self.add_mvt_frames_mode_button["text"] = ' + MVT OFF '
            self.add_mvt_frames_mode_button["fg"] = 'red'
            self.add_mvt_frames_mode_button["command"] = self.add_mvt_frames_switch_mode
            self.add_mvt_frames_mode_button.pack(side=TOP)

            self.remove_mvt_frames_button = Button(left_side_frame)
            self.remove_mvt_frames_button["text"] = ' - MVT OFF '
            self.remove_mvt_frames_button["fg"] = 'red'
            self.remove_mvt_frames_button["command"] = self.remove_mvt_frames_switch_mode
            self.remove_mvt_frames_button.pack(side=TOP)

        sep = ttk.Separator(left_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        onsets_frame = Frame(left_side_frame)
        onsets_frame.pack(side=TOP)

        onsets_button_frame = Frame(onsets_frame)
        onsets_button_frame.pack(side=LEFT)

        # if True, means when we add an onset a peak is added just after
        self.add_onset_with_peak = False

        self.add_onset_button = Button(onsets_button_frame)
        self.add_onset_button["text"] = ' + ONSET OFF '
        self.add_onset_button["fg"] = 'red'
        self.add_onset_button["command"] = self.add_onset_switch_mode
        self.add_onset_button.pack(side=TOP)

        self.remove_onset_button = Button(onsets_button_frame)
        self.remove_onset_button["text"] = ' - ONSET OFF '
        self.remove_onset_button["fg"] = 'red'
        self.remove_onset_button["command"] = self.remove_onset_switch_mode
        self.remove_onset_button.pack(side=TOP)

        onsets_label_frame = Frame(onsets_frame)
        onsets_label_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        # empty_label = Label(onsets_label_frame)
        # empty_label["text"] = ""
        # empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.onset_numbers_label = Label(onsets_label_frame)
        self.onset_numbers_label["text"] = f" {self.numbers_of_onset()} "
        self.onset_numbers_label.pack(side=TOP, expand=YES, fill=BOTH)

        # empty_label = Label(onsets_label_frame)
        # empty_label["text"] = ""
        # empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        sep = ttk.Separator(left_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        peaks_frame = Frame(left_side_frame)
        peaks_frame.pack(side=TOP)

        peaks_button_frame = Frame(peaks_frame)
        peaks_button_frame.pack(side=LEFT)

        self.add_peak_button = Button(peaks_button_frame)
        self.add_peak_button["text"] = ' + PEAK OFF '
        self.add_peak_button["fg"] = 'red'
        self.add_peak_button["command"] = self.add_peak_switch_mode
        self.add_peak_button.pack(side=TOP)

        self.remove_peak_button = Button(peaks_button_frame)
        self.remove_peak_button["text"] = ' - PEAK OFF '
        self.remove_peak_button["fg"] = 'red'
        self.remove_peak_button["command"] = self.remove_peak_switch_mode
        self.remove_peak_button.pack(side=TOP)

        peaks_label_frame = Frame(peaks_frame)
        peaks_label_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        self.peak_numbers_label = Label(peaks_label_frame)
        self.peak_numbers_label["text"] = f" {self.numbers_of_peak()} "
        self.peak_numbers_label.pack(side=TOP, expand=YES, fill=BOTH)

        sep = ttk.Separator(left_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        self.remove_all_button = Button(left_side_frame)
        self.remove_all_button["text"] = ' - ALL OFF '
        self.remove_all_button["fg"] = 'red'
        self.remove_all_button["command"] = self.remove_all_switch_mode
        self.remove_all_button.pack(side=TOP)

        sep = ttk.Separator(left_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        # button to add all onsets and peaks possible over the current window and cell
        self.add_them_all_button = Button(left_side_frame)
        self.add_them_all_button["text"] = 'ADD THEM ALL'
        self.add_them_all_button["fg"] = 'black'
        self.add_them_all_button["command"] = self.add_them_all
        self.add_them_all_button.pack(side=TOP)

        self.agree_button = None
        self.dont_agree_button = None
        if (self.to_agree_spike_nums is not None) and (self.to_agree_peak_nums is not None):
            if (np.sum(self.to_agree_spike_nums) > 0) or (np.sum(self.to_agree_peak_nums) > 0):
                sep = ttk.Separator(left_side_frame)
                sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

                # deal with fusion over onsets & peaks over 2 different gui selections
                self.agree_button = Button(left_side_frame)
                self.agree_button["text"] = 'Y'
                self.agree_button["fg"] = 'red'
                self.agree_button["command"] = self.agree_switch_mode
                self.agree_button.pack(side=TOP)

                # empty_label = Label(left_side_frame)
                # empty_label["text"] = "" * 1
                # empty_label.pack(side=TOP)

                self.to_agree_label = Label(left_side_frame)
                self.to_agree_label["text"] = f"{self.numbers_of_onset_to_agree()}/" \
                                              f"{self.numbers_of_peak_to_agree()}"
                self.to_agree_label.pack(side=TOP)

                # empty_label = Label(left_side_frame)
                # empty_label["text"] = "" * 1
                # empty_label.pack(side=TOP)

                self.dont_agree_button = Button(left_side_frame)
                self.dont_agree_button["text"] = 'N'
                self.dont_agree_button["fg"] = 'red'
                self.dont_agree_button["command"] = self.dont_agree_switch_mode
                self.dont_agree_button.pack(side=TOP)
            else:
                self.to_agree_label = None
        else:
            self.to_agree_label = None

        # TODO: Put to False in november
        deactivate_prediction_list_box_for_now = False
        self.predictions_list_box = None
        if (not deactivate_prediction_list_box_for_now) and (not self.segment_mode) and (
                ((self.classifier_weights_file is not None) and (self.classifier_model_file is not None)) \
                or (self.data_and_param.classifier_predictions is not None)):
            sep = ttk.Separator(left_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            pred_values_frame = Frame(left_side_frame)
            pred_values_frame.pack(side=TOP, expand=NO, fill="x")
            empty_label = Label(pred_values_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

            self.pred_value_1_entry_widget = Entry(pred_values_frame, fg=self.color_text_gui_default, justify=CENTER,
                                                   width=4)
            self.pred_value_1_entry_widget.insert(0, f"{self.uncertain_prediction_values[0]}")
            self.pred_value_1_entry_widget.pack(side=LEFT)
            empty_label = Label(pred_values_frame)
            empty_label["text"] = " - "
            empty_label.pack(side=LEFT)
            self.pred_value_2_entry_widget = Entry(pred_values_frame, fg=self.color_text_gui_default, justify=CENTER,
                                                   width=4)
            self.pred_value_2_entry_widget.insert(0, f"{self.uncertain_prediction_values[1]}")
            self.pred_value_2_entry_widget.pack(side=LEFT)

            self.ok_pred_button = Button(pred_values_frame)
            self.ok_pred_button["text"] = ' OK '
            self.ok_pred_button["fg"] = self.color_text_gui_default
            self.ok_pred_button["command"] = self.update_uncertain_prediction_values
            self.ok_pred_button.pack(side=LEFT)

            empty_label = Label(pred_values_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

            # if predictions are available, then we display a listbox that will allow to visualize predictions
            # that are in a certain range in order to confirm their accuracy
            segments_list_frame = Frame(left_side_frame)
            segments_list_frame.pack(side=TOP, expand=NO, fill="x")

            scrollbar = Scrollbar(segments_list_frame)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.last_index_selected_predictions_list_box = None

            self.predictions_list_box = Listbox(segments_list_frame, bd=0, selectmode=BROWSE,
                                                height=15, selectbackground="red", highlightcolor="red",
                                                font=("Arial", 10), yscrollcommand=scrollbar.set)
            # default height is 10, selectmode=SINGLE
            self.predictions_list_box.bind("<Double-Button-1>", self.predictions_list_box_double_click)

            self.predictions_list_box.bind('<<ListboxSelect>>', self.predictions_list_box_click)
            # width=20
            self.predictions_list_box.pack()

            self.update_transient_prediction_periods_to_check()

            # attach listbox to scrollbar
            scrollbar.config(command=self.predictions_list_box.yview)

        self.center_segment_button = None
        # segment mode, means the use just open pre-recorded ground truth segment
        if not self.segment_mode:
            sep = ttk.Separator(left_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            # widget that will contain the number of frames a segment should be when the user click on the
            # the fluorescence in order to center the activity
            center_segment_frame = Frame(left_side_frame)
            center_segment_frame.pack(side=TOP, expand=NO, fill="x")
            self.center_segment_entry_widget = Entry(center_segment_frame, fg=self.color_text_gui_default,
                                                     justify=CENTER,
                                                     width=4)
            self.center_segment_entry_widget.insert(0, f"{self.segment_to_center_length}")
            self.center_segment_entry_widget.bind("<KeyRelease>", self.center_segment_button_action)
            # self.neuron_string_var.set("0")
            # self.neuron_string_var.trace("w", self.neuron_entry_change)
            # self.neuron_entry_widget.focus_set()
            self.center_segment_entry_widget.pack(side=LEFT, expand=YES, fill="x")

            # when pressed, center_segment mode is activated
            self.center_segment_button = Button(center_segment_frame)
            self.center_segment_button["text"] = ' OFF '
            self.center_segment_button["fg"] = "red"
            self.center_segment_button["command"] = event_lambda(self.center_segment_button_action)
            self.center_segment_button.pack(side=LEFT, expand=YES, fill="x")

        empty_label = Label(left_side_frame)
        empty_label["text"] = ""
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)
        # -------------- left side frame (end) ----------------

        ################################################################################
        ################################ Middle frame with plot ################################
        ################################################################################
        canvas_frame = Frame(self, padx=0, pady=0, bg=self.background_color)
        canvas_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        top_bar_canvas_frame = Frame(canvas_frame, padx=0, pady=0, bg=self.background_color)
        top_bar_canvas_frame.pack(side=TOP, expand=YES, fill=BOTH)

        main_plot_frame = Frame(canvas_frame, padx=0, pady=0, bg=self.background_color)
        main_plot_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.main_plot_frame = main_plot_frame

        self.display_background_img = False

        # plt.ion()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        # print(f"screen_width {self.screen_width}, screen_height {self.screen_height}")
        if (self.screen_width < 2000) or (self.screen_height < 1200):
            self.fig = plt.figure(figsize=(10, 3))
        else:
            self.fig = plt.figure(figsize=(16, 8))  # 10, 4
        self.fig.patch.set_facecolor(self.background_color)
        # self.plot_canvas = MyCanvas(self.fig, canvas_frame, self)
        self.plot_canvas = FigureCanvasTkAgg(self.fig, main_plot_frame)
        # self.plot_canvas.get_tk_widget().configure(bg=self.background_color)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.motion)
        # self.plot_canvas.
        #     bind("<Button-1>", self.callback_click_fig())

        # self.gs = gridspec.GridSpec(2, 1, width_ratios=[1], height_ratios=[5, 1])
        # using gridspec even for one plot, but could be useful if we want to add plot.
        self.gs = gridspec.GridSpec(1, 1, width_ratios=[1], height_ratios=[1])
        # self.gs.update(hspace=0.05)
        # ax1 = plt.subplot(gs[0])
        # ax2 = plt.subplot(gs[1])
        self.axe_plot = None
        self.ax1_bottom_scatter = None
        self.ax1_top_scatter = None
        self.line1 = None
        self.line2 = None
        self.plot_graph(first_time=True)

        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)

        color_toolbar = self.background_color
        self.toolbar = NavigationToolbar2Tk(self.plot_canvas, main_plot_frame)
        # self.toolbar.config(background=color_toolbar)
        # self.toolbar._message_label.config(background=color_toolbar)
        self.toolbar.update()
        # for button in self.toolbar.winfo_children():
        #     button.config(background=color_toolbar)
        self.toolbar.pack(side=TOP, fill=BOTH, expand=NO)

        self.map_frame = Frame(top_bar_canvas_frame)
        self.map_frame.pack(side=LEFT, expand=NO, fill="x")

        # tif movie loading
        self.last_img_displayed = None
        self.trace_movie_p1 = None
        self.trace_movie_p2 = None
        self.play_movie = False
        # coordinate for the zoom mode
        self.x_beg_movie = 0
        self.x_end_movie = 0
        self.y_beg_movie = 0
        self.y_end_movie = 0
        self.n_frames_movie = 1
        self.first_frame_movie = 0
        self.last_frame_movie = 1
        # to avoid garbage collector
        self.anim_movie = None
        self.last_frame_label = None
        # delay between 2 frames, in ms
        self.movie_delay = 10
        # frames to be played by the movie
        self.movie_frames = None
        self.background_img_file_names = []

        self.background_imgs = []
        for file_name in self.background_img_file_names:
            if not file_name.startswith("."):
                self.background_imgs.append(mpimg.imread(file_name, 0))

        self.n_background_img = len(self.background_imgs)
        self.background_img_to_display = -1

        # first key is the cell, value a dict
        # second key is the frame, value is a list of int representing the value of each pixel
        self.pixels_value_by_cell_and_frame = dict()

        if (self.data_and_param.avg_cell_map_img is not None) or (self.tiff_movie is not None):
            if (self.screen_width < 2000) or (self.screen_height < 1200):
                self.map_img_fig = plt.figure(figsize=(3, 3))
            else:
                self.map_img_fig = plt.figure(figsize=(4, 4))
            self.map_img_fig.patch.set_facecolor(self.map_img_bg_color)

            self.background_map_fig = None
            self.axe_plot_map_img = None
            self.cell_contour = None
            self.cell_contour_movie = None
            # determine how pixels around a cell are kept when saving only the cell surrounding
            # in order to train a classifier
            self.segment_window_in_pixels = 25
            # creating all cell_contours
            self.cell_contours = dict()
            n_pixels_x = self.tiff_movie.shape[2]
            n_pixels_y = self.tiff_movie.shape[1]
            self.cell_in_pixel = np.ones((n_pixels_y, n_pixels_x), dtype="int16")
            self.cell_in_pixel *= -1

            pixel_masks = self.data_and_param.coord_obj.pixel_masks

            for cell in np.arange(self.nb_neurons):
                # cell contour
                coords = self.data_and_param.coord_obj.coords[cell]
                xy = coords.transpose()
                self.cell_contours[cell] = patches.Polygon(xy=xy,
                                                           fill=False, linewidth=0, facecolor="red",
                                                           edgecolor="red",
                                                           zorder=15, lw=0.6)

                # bw = np.zeros((n_pixels_x, n_pixels_y), dtype="int8")
                # # morphology.binary_fill_holes(input
                # # print(f"coord[1, :] {coord[1, :]}")
                # bw[coord[1, :], coord[0, :]] = 1
                #
                # # used to know which cell has been clicked
                # img_filled = np.zeros((n_pixels_x, n_pixels_y), dtype="int8")
                # # specifying output, otherwise binary_fill_holes return a boolean array
                # morphology.binary_fill_holes(bw, output=img_filled)
                img_filled = self.data_and_param.coord_obj.get_cell_mask(cell=cell,
                                                                         dimensions=self.tiff_movie.shape[1:])
                for pixel in np.arange(n_pixels_y):
                    y_coords = np.where(img_filled[pixel, :])[0]
                    if len(y_coords) > 0:
                        self.cell_in_pixel[pixel, y_coords] = cell

            self.map_img_canvas = FigureCanvasTkAgg(self.map_img_fig, self.map_frame)
            # self.map_img_canvas.get_tk_widget().configure(bg="blue")
            self.map_img_fig.canvas.mpl_connect('button_release_event', self.onrelease_map)
            self.plot_map_img(first_time=True)

            self.map_img_canvas.draw()
            self.map_img_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)

        self.update_plot(new_neuron=True)

        self.magnifier_frame = Frame(top_bar_canvas_frame, bg=self.background_color)
        self.magnifier_frame.pack(side=LEFT, expand=YES, fill="x")
        if (self.screen_width < 2000) or (self.screen_height < 1200):
            self.magnifier_fig = plt.figure(figsize=(3, 3))
        else:
            self.magnifier_fig = plt.figure(figsize=(4, 4))
        self.magnifier_fig.patch.set_facecolor(self.background_color)
        self.axe_plot_magnifier = None
        # represent the x_value on which the magnifier is centered
        self.x_center_magnified = None
        # how many frames before and after the center
        self.magnifier_range = 50
        # self.plot_canvas = MyCanvas(self.fig, canvas_frame, self)
        self.magnifier_canvas = FigureCanvasTkAgg(self.magnifier_fig, self.magnifier_frame)
        # self.magnifier_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 0.1, 'h_pad': 0.1})
        # used to update the plot
        self.magnifier_marker = None
        self.magnifier_line = None
        self.plot_magnifier(first_time=True)

        self.magnifier_canvas.draw()
        # self.magnifier_canvas.get_tk_widget().configure(bg=self.background_color)
        self.magnifier_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)

        ################################################################################
        # ############################### right side frame #############################
        ################################################################################
        right_side_frame = Frame(self)
        right_side_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        # tells if the movie is active
        self.movie_mode = False

        # show the source profile of the active cell associate to the transient profile of the selected transient
        # as well as source profile of overlapping cells, and then display the correlation between each source profile
        # and their corresponding transient
        self.source_mode = False

        # to vertically center the buttons
        empty_label = Label(right_side_frame)
        empty_label["text"] = ""
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # ---------------------------------------------
        # ComboBox to choose the fluorescene to display to display
        self.actual_traces_str = [self.RAW_TRACE]
        self.trace_check_boxes = dict()
        for trace_str in self.traces_dict.keys():
            source_var = IntVar()
            trace_check_box = Checkbutton(right_side_frame, text=trace_str, variable=source_var,
                                          onvalue=1,
                                          offvalue=0)

            if trace_str == self.RAW_TRACE:
                trace_check_box.select()
            trace_check_box["command"] = event_lambda(self.switch_trace_to_be_displayed, trace_str=trace_str)
            trace_check_box.pack(side=TOP)
            self.trace_check_boxes[trace_str] = trace_check_box

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        # to display the source profile of a transient
        self.source_var = IntVar()
        self.source_check_box = Checkbutton(right_side_frame, text="source", variable=self.source_var,
                                            onvalue=1,
                                            offvalue=0)

        if self.source_mode:
            self.source_check_box.select()
        self.source_check_box["command"] = event_lambda(self.switch_source_profile_mode)
        self.source_check_box.pack(side=TOP)

        self.zoom_movie_check_box = None
        if (not self.segment_mode) and (min_dim_movie > self.size_zoom_pixels):
            sep = ttk.Separator(right_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            self.zoom_movie_var = IntVar()
            self.zoom_movie_check_box = Checkbutton(right_side_frame, text="zoom", variable=self.zoom_movie_var,
                                                    onvalue=1,
                                                    offvalue=0)
            if self.movie_zoom_mode:
                self.zoom_movie_check_box.select()
            self.zoom_movie_check_box["command"] = event_lambda(self.activate_movie_zoom)
            self.zoom_movie_check_box.pack(side=TOP)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        if self.tiff_movie is not None:
            # empty_label = Label(right_side_frame)
            # empty_label["text"] = " " * 1
            # empty_label.pack(side=TOP)

            self.movie_button = Button(right_side_frame)
            self.movie_button["text"] = ' movie OFF '
            self.movie_button["fg"] = "black"
            self.movie_button["command"] = event_lambda(self.switch_movie_mode)
            self.movie_button.pack(side=TOP)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        if self.mvt_frames_periods is not None:
            # empty_label = Label(right_side_frame)
            # empty_label["text"] = " " * 1
            # empty_label.pack(side=TOP)

            self.display_mvt_button = Button(right_side_frame)

            self.display_mvt_button["text"] = ' mvt OFF '
            self.display_mvt_button["fg"] = "black"

            self.display_mvt_button["command"] = event_lambda(self.switch_mvt_display)
            self.display_mvt_button.pack(side=TOP)

            sep = ttk.Separator(right_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        self.magnifier_button = Button(right_side_frame)
        self.magnifier_button["text"] = ' magnified OFF '
        self.magnifier_button["fg"] = "black"
        self.magnifier_mode = False
        self.magnifier_button["command"] = event_lambda(self.switch_magnifier)
        self.magnifier_button.pack(side=TOP)

        if ((self.classifier_weights_file is not None) and (self.classifier_model_file is not None)) \
                or (self.data_and_param.classifier_predictions is not None):
            sep = ttk.Separator(right_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            transient_classifier_frame = Frame(right_side_frame)
            transient_classifier_frame.pack(side=TOP, expand=NO, fill=BOTH)

            empty_label = Label(transient_classifier_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

            self.transient_classifier_var = IntVar()
            self.transient_classifier_check_box = Checkbutton(transient_classifier_frame, text="tc",
                                                              variable=self.transient_classifier_var, onvalue=1,
                                                              offvalue=0, fg=self.color_threshold_line)
            self.transient_classifier_check_box["command"] = event_lambda(self.transient_classifier_check_box_action)
            self.transient_classifier_check_box.pack(side=LEFT)

            # empty_label = Label(right_side_frame)
            # empty_label["text"] = " " * 1
            # empty_label.pack(side=TOP)
            # from_=1, to=3
            # self.var_spin_box_threshold = StringVar(right_side_frame)
            var = StringVar(transient_classifier_frame)
            self.spin_box_transient_classifier = Spinbox(transient_classifier_frame,
                                                         values=list(np.arange(0.05, 1, 0.05)),
                                                         fg=self.color_text_gui_default, justify=CENTER,
                                                         width=3, textvariable=var,
                                                         state="readonly")  # , textvariable=self.var_spin_box_threshold)
            var.set("0.5")
            # self.var_spin_box_threshold.set(0.5)
            self.spin_box_transient_classifier["command"] = event_lambda(self.spin_box_transient_classifier_update)
            # self.spin_box_button.config(command=event_lambda(self.spin_box_update))
            self.spin_box_transient_classifier.pack(side=LEFT)

            empty_label = Label(transient_classifier_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        self.remove_cell_button = Button(right_side_frame)
        if self.cells_to_remove[self.current_neuron] == 0:
            self.remove_cell_button["text"] = ' valid cell '
            self.remove_cell_button["fg"] = "black"
        else:
            self.remove_cell_button["text"] = ' invalid cell '
            self.remove_cell_button["fg"] = "red"
        self.remove_cell_button["command"] = event_lambda(self.remove_cell)
        self.remove_cell_button.pack(side=TOP)

        self.cell_type_entry_widget = None
        # so if we display just a segment, we don't need
        if not self.segment_mode:
            sep = ttk.Separator(right_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            cell_type_frame = Frame(right_side_frame)
            cell_type_frame.pack(side=TOP, expand=NO, fill="x")

            empty_label = Label(cell_type_frame)
            empty_label["text"] = "Cell Type"
            empty_label.pack(side=TOP, expand=YES, fill=BOTH)
            self.cell_type_entry_widget = Entry(cell_type_frame, fg=self.color_text_gui_default, justify=CENTER,
                                                width=3)
            cell_type_str = self.cell_type_dict.get(self.current_neuron, "")
            self.cell_type_entry_widget.insert(0, cell_type_str)
            self.cell_type_entry_widget.bind("<KeyRelease>", self.cell_type_action)
            self.cell_type_entry_widget.pack(side=TOP, expand=YES, fill="x")

        if self.display_cell_type_classifier_field:
            sep = ttk.Separator(right_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)
            #
            # empty_label = Label(cell_type_classifier_frame)
            # empty_label["text"] = ""
            # empty_label.pack(side=LEFT, expand=YES, fill=BOTH)
            if not self.cell_type_predictions_loaded:
                self.cell_type_classifier_button = Button(right_side_frame)
                self.cell_type_classifier_button["text"] = ' classify '
                self.cell_type_classifier_button["fg"] = "black"
                self.cell_type_classifier_button["command"] = event_lambda(self.cell_type_classifier_button_action)
                self.cell_type_classifier_button.pack(side=TOP)

            # labels displaying the probability for each cell type
            self.cell_type_name_label_dict = dict()
            self.cell_type_predictions_label_dict = dict()

            for cell_type in self.cell_types_for_classifier:
                cell_type_classifier_frame = Frame(right_side_frame)
                cell_type_classifier_frame.pack(side=TOP, expand=NO, fill=BOTH)

                empty_label = Label(cell_type_classifier_frame)
                empty_label["text"] = ""
                empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

                cell_type_label = Label(cell_type_classifier_frame)
                cell_type_label["text"] = cell_type
                cell_type_label.pack(side=LEFT, expand=YES, fill=BOTH)
                self.cell_type_name_label_dict[cell_type] = cell_type_label

                cell_type_predictions_label = Label(cell_type_classifier_frame)
                cell_type_predictions_label["text"] = ""
                cell_type_predictions_label.pack(side=LEFT, expand=YES, fill=BOTH)
                self.cell_type_predictions_label_dict[cell_type] = cell_type_predictions_label

                empty_label = Label(cell_type_classifier_frame)
                empty_label["text"] = ""
                empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        if self.tiff_movie is not None and self.correlation_for_each_peak_option:
            correlation_frame = Frame(right_side_frame)
            correlation_frame.pack(side=TOP, expand=NO, fill=BOTH)

            empty_label = Label(correlation_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

            self.peaks_correlation = np.ones(self.raw_traces.shape)
            self.peaks_correlation *= -2

            self.correlation_var = IntVar()
            self.correlation_check_box = Checkbutton(correlation_frame, text="corr", variable=self.correlation_var,
                                                     onvalue=1,
                                                     offvalue=0, fg=self.color_threshold_line)
            self.correlation_check_box["command"] = event_lambda(self.correlation_check_box_action)
            # self.correlation_check_box.select()

            self.correlation_check_box.pack(side=LEFT)

            self.spin_box_correlation = Spinbox(correlation_frame, values=list(np.round(np.arange(0.05, 1, 0.05), 2)),
                                                fg=self.color_text_gui_default,
                                                justify=CENTER,
                                                width=4,
                                                state="readonly")  # , textvariable=self.var_spin_box_threshold)
            # self.var_spin_box_threshold.set(0.9)
            self.spin_box_correlation["command"] = event_lambda(self.spin_box_correlation_update)
            # self.spin_box_button.config(command=event_lambda(self.spin_box_update))
            self.spin_box_correlation.pack(side=LEFT)

            empty_label = Label(correlation_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        threshold_frame = Frame(right_side_frame)
        threshold_frame.pack(side=TOP, expand=NO, fill=BOTH)

        empty_label = Label(threshold_frame)
        empty_label["text"] = ""
        empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        self.treshold_var = IntVar()
        self.threshold_check_box = Checkbutton(threshold_frame, text="std", variable=self.treshold_var, onvalue=1,
                                               offvalue=0, fg=self.color_threshold_line)
        self.threshold_check_box["command"] = event_lambda(self.threshold_check_box_action)
        self.threshold_check_box.pack(side=LEFT)

        # from_=1, to=3
        # self.var_spin_box_threshold = StringVar(right_side_frame)
        self.spin_box_threshold = Spinbox(threshold_frame, values=list(np.arange(0.1, 5, 0.1)),
                                          fg=self.color_text_gui_default,
                                          justify=CENTER,
                                          width=3, state="readonly")  # , textvariable=self.var_spin_box_threshold)
        # self.var_spin_box_threshold.set(0.9)
        self.spin_box_threshold["command"] = event_lambda(self.spin_box_threshold_update)
        # self.spin_box_button.config(command=event_lambda(self.spin_box_update))
        self.spin_box_threshold.pack(side=LEFT)

        empty_label = Label(threshold_frame)
        empty_label["text"] = ""
        empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        self.remove_peaks_under_threshold_button = Button(right_side_frame)
        self.remove_peaks_under_threshold_button["text"] = ' DEL PEAKS '
        self.remove_peaks_under_threshold_button["fg"] = "red"
        self.remove_peaks_under_threshold_button['state'] = DISABLED  # ''normal
        self.remove_peaks_under_threshold_button["command"] = event_lambda(self.remove_peaks_under_threshold)
        self.remove_peaks_under_threshold_button.pack(side=TOP)

        sep = ttk.Separator(right_side_frame)
        sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

        undo_frame = Frame(right_side_frame)
        undo_frame.pack(side=TOP, expand=NO, fill=BOTH)

        empty_label = Label(undo_frame)
        empty_label["text"] = ""
        empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        self.undo_button = Button(undo_frame)
        self.undo_button["text"] = ' UNDO '
        self.undo_button["fg"] = self.color_text_gui_default
        self.undo_button['state'] = DISABLED  # ''normal
        self.undo_button["command"] = event_lambda(self.undo_action)
        self.undo_button.pack(side=LEFT)

        self.redo_button = Button(undo_frame)
        self.redo_button["text"] = ' REDO '
        self.redo_button["fg"] = self.color_text_gui_default
        self.redo_button['state'] = DISABLED  # ''normal
        self.redo_button["command"] = event_lambda(self.redo_action)
        self.redo_button.pack(side=LEFT)

        empty_label = Label(undo_frame)
        empty_label["text"] = ""
        empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

        self.segments_to_save_list_box = None
        if not self.segment_mode:
            # ######### ListBox displaying the segments to save
            sep = ttk.Separator(right_side_frame)
            sep.pack(side=TOP, fill=BOTH, padx=0, pady=10)

            add_segment_frame = Frame(right_side_frame)
            add_segment_frame.pack(side=TOP, expand=NO, fill=BOTH)

            empty_label = Label(add_segment_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

            self.add_segment_button = Button(add_segment_frame)
            self.add_segment_button["text"] = ' ADD GT '
            self.add_segment_button["fg"] = self.color_text_gui_default
            self.add_segment_button['state'] = "normal"
            self.add_segment_button["command"] = event_lambda(self.add_current_segment_to_save_list)
            self.add_segment_button.pack(side=LEFT)

            var = StringVar(add_segment_frame)
            self.spin_box_pixels_around_cell = Spinbox(add_segment_frame,
                                                       values=list(np.arange(5, max(n_pixels_x, n_pixels_y) + 1, 1)),
                                                       fg=self.color_text_gui_default, justify=CENTER,
                                                       width=4, textvariable=var,
                                                       state="readonly")  # , textvariable=self.spin_box_pixels_around_cell)
            if min(n_pixels_x, n_pixels_y) >= self.segment_window_in_pixels:
                var.set(f"{self.segment_window_in_pixels}")
            else:
                var.set(f"{min(n_pixels_x, n_pixels_y)}")
                self.segment_window_in_pixels = min(n_pixels_x, n_pixels_y)
            # self.spin_box_pixels_around_cell.set(25)
            self.spin_box_pixels_around_cell["command"] = event_lambda(self.spin_box_pixels_around_cell_update)
            self.spin_box_pixels_around_cell.pack(side=LEFT)

            empty_label = Label(add_segment_frame)
            empty_label["text"] = ""
            empty_label.pack(side=LEFT, expand=YES, fill=BOTH)

            self.last_index_selected_segments_to_save_list_box = None

            segments_list_frame = Frame(right_side_frame)
            segments_list_frame.pack(side=TOP, expand=NO, fill="x")

            # indicate how many frames have been added to ground truth labeled segments
            self.n_frames_gt_label = Label(segments_list_frame)
            self.n_frames_gt_label["text"] = " "
            self.n_frames_gt_label.pack(side=TOP)

            # indicate how many "active" frames have been added to ground truth labeled segments
            self.n_active_frames_gt_label = Label(segments_list_frame)
            self.n_active_frames_gt_label["text"] = " "
            self.n_active_frames_gt_label.pack(side=TOP)

            scrollbar_frame = Frame(segments_list_frame)
            scrollbar_frame.pack(side=TOP, expand=NO, fill="x")

            scrollbar = Scrollbar(scrollbar_frame)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.segments_to_save_list_box = Listbox(scrollbar_frame, bd=0, selectmode=BROWSE,
                                                     height=10, selectbackground="red", highlightcolor="red",
                                                     font=("Arial", 10), yscrollcommand=scrollbar.set)
            # default height is 10
            self.segments_to_save_list_box.bind("<Double-Button-1>", self.segments_to_save_list_box_double_click)
            self.segments_to_save_list_box.bind('<<ListboxSelect>>', self.segments_to_save_list_box_click)

            # width=20
            self.segments_to_save_list_box.pack()

            # attach listbox to scrollbar
            scrollbar.config(command=self.segments_to_save_list_box.yview)

            self.update_segments_to_save_list_box(initial_loading=True)

            self.save_segments_button = Button(right_side_frame)
            self.save_segments_button["text"] = ' SAVE '
            self.save_segments_button["fg"] = self.color_text_gui_default
            if self.save_file_name:
                # means the data has been loaded using a .cinac file that will be uploaded is using the save button
                self.save_segments_button['state'] = 'normal'
            else:
                self.save_segments_button['state'] = DISABLED
            self.save_segments_button["command"] = event_lambda(self.save_segments)
            self.save_segments_button.pack(side=TOP)

            self.save_segments_as_button = Button(right_side_frame)
            self.save_segments_as_button["text"] = ' SAVE AS '
            self.save_segments_as_button["fg"] = self.color_text_gui_default
            self.save_segments_as_button['state'] = 'normal'  # ''normal
            self.save_segments_as_button["command"] = event_lambda(self.save_segments_as)
            self.save_segments_as_button.pack(side=TOP)

        # to vertically center the buttons
        empty_label = Label(right_side_frame)
        empty_label["text"] = ""
        empty_label.pack(side=TOP, expand=YES, fill=BOTH)

        # used for association of keys
        self.keys_pressed = dict()
        self.root.bind("<KeyRelease>", self.key_release_action)
        self.root.bind("<KeyPress>", self.key_press_action)

    def neuron_entry_change(self, *args):
        print(f"Neuron: {self.neuron_string_var.get()}")

    def switch_michou(self):
        # can't display images while playing the movie
        if (not self.display_background_img) and self.play_movie:
            return

        if self.display_background_img:
            self.display_background_img = False
            if not self.play_movie:
                self.update_plot_map_img(after_michou=True)
        else:
            self.display_background_img = True
            self.background_img_to_display = randint(0, self.n_background_img - 1)
            self.update_plot_map_img()

    def _build_traces(self):
        """
        Build different fluorescence signal for each cell.
        Fill the self.traces_dict, each key is a trace description (str), and each value is a 2d array
        (n cells * n frames)
        Returns:

        """
        self.traces_dict[self.RAW_TRACE] = self.raw_traces
        # if True, then only raw traces is available
        if self.data_and_param.only_raw_traces_option:
            return

        self.raw_traces_without_overlap = self.data_and_param.coord_obj.\
            build_raw_traces_from_movie(movie=self.tiff_movie, without_overlap=True)

        for cell in np.arange(self.nb_neurons):
            self.raw_traces_without_overlap[cell] = stats.zscore(self.raw_traces_without_overlap[cell])

        self.traces_dict[self.RAW_TRACE_WITHOUT_OVERLAP] = self.raw_traces_without_overlap


        # then we build the neuropil ones
        # mask of the cells content
        cells_mask = np.zeros((self.tiff_movie.shape[1], self.tiff_movie.shape[2]), dtype="bool")
        neuropil_traces = np.zeros((self.nb_neurons, self.tiff_movie.shape[0]))
        for cell in np.arange(self.nb_neurons):
            mask = self.data_and_param.coord_obj.get_cell_mask(cell=cell,
                                                               dimensions=(
                                                                   self.tiff_movie.shape[1],
                                                                   self.tiff_movie.shape[2]))
            cells_mask[mask] = 1

        square_size = 20
        for cell in np.arange(self.nb_neurons):
            len_x = self.tiff_movie.shape[2]
            len_y = self.tiff_movie.shape[1]
            x_beg, x_end, y_beg, y_end = \
                self.square_coord_around_cell(cell=self.current_neuron, size_square=square_size,
                                              x_len_max=len_x, y_len_max=len_y)

            neuropil_mask = np.zeros((self.tiff_movie.shape[1], self.tiff_movie.shape[2]), dtype="bool")

            neuropil_mask[y_beg:y_end, x_beg:x_end] = 1
            neuropil_mask[cells_mask] = 0
            neuropil_traces[cell, :] = np.mean(self.tiff_movie[:, neuropil_mask], axis=1)
            # V1: z-score normalization on neuropile
            # neuropil_traces[cell, :] = (neuropil_traces[cell, :] - np.mean(neuropil_traces[cell, :])) \
            #                            / np.std(neuropil_traces[cell, :])
            # V2: z-score normalization of neuropile on raw trace mean and std
            neuropil_traces[cell, :] = stats.zscore(neuropil_traces[cell])

        self.traces_dict[self.NEUROPIL_TRACE] = neuropil_traces
        self.traces_dict[self.RAW_M_NEUROPIL_TRACE] = self.raw_traces_without_overlap - neuropil_traces

    def switch_movie_mode(self, from_movie_button=True):
        if from_movie_button and (not self.movie_mode):
            self.swith_all_click_actions(initiator="switch_movie_mode")

        if self.movie_mode:
            self.movie_button["text"] = ' movie OFF '
            self.movie_button["fg"] = "black"
            self.movie_mode = False
            if self.play_movie:
                self.play_movie = False
                if self.anim_movie is not None:
                    self.anim_movie.event_source.stop()
                    self.update_contour_for_cell(cell=self.current_neuron)
                    self.update_plot_map_img(after_michou=True, after_movie=True)
        else:
            self.movie_button["text"] = ' movie ON '
            self.movie_button["fg"] = "red"
            self.movie_mode = True

        if self.first_click_to_remove is not None:
            self.first_click_to_remove = None
            self.update_plot()

    def switch_mvt_display(self):
        if self.display_mvt:
            self.display_mvt_button["text"] = ' mvt OFF '
            self.display_mvt_button["fg"] = "black"
            self.display_mvt = False
        else:
            self.display_mvt_button["text"] = ' mvt ON '
            self.display_mvt_button["fg"] = "red"
            self.display_mvt = True
        self.update_plot()

    def switch_magnifier(self):
        if self.magnifier_mode:
            self.magnifier_button["text"] = ' magnified OFF '
            self.magnifier_button["fg"] = "black"
            self.magnifier_mode = False
        else:
            self.magnifier_button["text"] = ' magnified ON '
            self.magnifier_button["fg"] = "red"
            self.magnifier_mode = True
            if self.source_mode:
                self.switch_source_profile_mode(from_check_box=False, from_key_shortcut=False, from_magnifier=True)

    def set_inter_neuron(self):
        if self.inter_neurons[self.current_neuron] == 0:
            self.inter_neuron_button["text"] = " IN "
            self.inter_neuron_button["fg"] = "red"
            self.inter_neurons[self.current_neuron] = 1
        else:
            self.inter_neuron_button["text"] = " not IN "
            self.inter_neuron_button["fg"] = "black"
            self.inter_neurons[self.current_neuron] = 0
        self.unsaved()

    def remove_cell(self):
        if self.cells_to_remove[self.current_neuron] == 0:
            self.remove_cell_button["text"] = " invalid cell "
            self.remove_cell_button["fg"] = "red"
            self.cells_to_remove[self.current_neuron] = 1
        else:
            self.remove_cell_button["text"] = " valid cell "
            self.remove_cell_button["fg"] = "black"
            self.cells_to_remove[self.current_neuron] = 0
        self.update_plot()
        self.unsaved()

    def clear_and_update_center_segment_entry_widget(self):
        self.center_segment_entry_widget.delete(first=0, last=END)
        self.center_segment_entry_widget.insert(0, f"{self.segment_to_center_length}")

    def clear_and_update_entry_neuron_widget(self):
        self.neuron_entry_widget.delete(first=0, last=END)
        self.neuron_entry_widget.insert(0, f"{self.current_neuron}")

    def clear_and_update_entry_cell_type_widget(self):
        if self.cell_type_entry_widget is None:
            return
        self.cell_type_entry_widget.delete(first=0, last=END)
        cell_type = self.cell_type_dict.get(self.current_neuron, "")
        self.cell_type_entry_widget.insert(0, cell_type)

    def update_uncertain_prediction_values(self, event=None):
        """
        Update the widget that contain the limit of the prediction we want to look at
        :param event:
        :return:
        """
        pred_value_1 = self.pred_value_1_entry_widget.get()
        pred_value_2 = self.pred_value_2_entry_widget.get()
        error = False
        try:
            pred_value_1 = float(pred_value_1)
            pred_value_2 = float(pred_value_2)
        except (ValueError, TypeError) as e:
            # error if a value that is not an int is selected
            error = True
        # print(f"pred_value_1 {pred_value_1}, pred_value_2 {pred_value_2}")
        if not error:
            if pred_value_1 < 0:
                error = True
            if pred_value_2 > 1:
                error = True
            if pred_value_2 <= pred_value_1:
                error = True
        if error:
            self.pred_value_1_entry_widget.delete(first=0, last=END)
            self.pred_value_1_entry_widget.insert(0, f"{self.uncertain_prediction_values[0]}")

            self.pred_value_2_entry_widget.delete(first=0, last=END)
            self.pred_value_2_entry_widget.insert(0, f"{self.uncertain_prediction_values[1]}")
            return

        self.uncertain_prediction_values = (np.round(pred_value_1, 2), np.round(pred_value_2, 2))
        self.update_transient_prediction_periods_to_check()
        # if an item was selected previously, then the new selected one if index 0
        if self.last_index_selected_predictions_list_box is not None:
            self.last_index_selected_predictions_list_box = 0

    def center_segment_button_action(self, event=None):
        segment_length = self.center_segment_entry_widget.get()
        try:
            segment_length = int(segment_length)
        except (ValueError, TypeError) as e:
            # error if a value that is not an int is selected
            self.clear_and_update_center_segment_entry_widget()
            return

        if (segment_length < 0) or (segment_length > (self.n_frames // 2)):
            self.clear_and_update_center_segment_entry_widget()
            return

        self.segment_to_center_length = segment_length

        self.update_transient_prediction_periods_to_check()

        if ((event is not None) and (event.keysym == 'Return')) or (event is None):
            self.center_segment_swith_mode()

    def cell_type_action(self, event=None):
        """
        Action called when the entry widget for cell type is called
        Args:
            event:

        Returns:

        """
        if self.cell_type_entry_widget is None:
            return

        cell_type_entry = self.cell_type_entry_widget.get()
        if cell_type_entry.strip() == "":
            if self.current_neuron in self.cell_type_dict:
                del self.cell_type_dict[self.current_neuron]
        else:
            self.cell_type_dict[self.current_neuron] = cell_type_entry

    def go_to_neuron_button_action(self, event=None):
        # print("go_to_neuron_button_action")
        neuron_selected = self.neuron_entry_widget.get()
        try:
            neuron_selected = int(neuron_selected)
        except (ValueError, TypeError) as e:
            # error if a value that is not an int is selected
            # print("clear entry")
            self.clear_and_update_entry_neuron_widget()
            return
        if neuron_selected == self.current_neuron:
            return

        if (neuron_selected < 0) or (neuron_selected > (self.nb_neurons - 1)):
            self.clear_and_update_entry_neuron_widget()
            return

        if (event is not None) and (event.keysym == 'Return'):
            self.update_neuron(new_neuron=neuron_selected)
        if event is None:
            self.update_neuron(new_neuron=neuron_selected)

    def key_press_action(self, event):
        # print(f"pressed keysym {event.keysym}, keycode {event.keycode}, keysym_num {event.keysym_num}, "
        #       f"state {event.state}")
        if event.keysym in ["Meta_L", "Control_L"]:
            self.keys_pressed[event.keysym] = 1

    def key_release_action(self, event):
        # "Meta_L" keysym for command key
        # "Control_L" keysym for control key
        if event.keysym in self.keys_pressed:
            del self.keys_pressed[event.keysym]
        # print(f"event.keysym_num {event.keysym_num}")
        # if 0, means the key was not recognized, we empty the dict
        if event.keysym_num == 0:
            self.keys_pressed = dict()
        # print(f"released keysym {event.keysym}, keycode {event.keycode}, keysym_num {event.keysym_num}, "
        #       f"state {event.state}")
        # print(f"event.keysym {event.keysym}")
        if event.char in ["o", "O", "+"]:
            self.add_onset_switch_mode()
        if event.char in ["i", "I"]:
            self.add_onset_switch_mode(with_peak=True)
        elif event.char in ["p", "P", "*"]:
            self.add_peak_switch_mode()
        elif event.char in ["G", "g"]:
            self.add_current_segment_to_save_list()
        elif event.char in ["a", "A"]:
            self.move_zoom(to_the_left=False)
            # so the back button will come back to the curren view
            self.toolbar.push_current()
        elif event.char in ["q", "Q"]:
            self.move_zoom(to_the_left=True)
            # so the back button will come back to the curren view
            self.toolbar.push_current()
        elif event.char in ["r", "R", "-"]:
            self.remove_all_switch_mode()
        # elif event.char in ["B"]:
        #     if self.display_background_img is False:
        #         self.display_background_img = True
        #         self.update_plot_map_img()
        #     start_time = time.time()
        #     self.save_sources_profile_map(key_cmap=event.char)
        #     stop_time = time.time()
        #     print(f"Time for producing source profiles map: "
        #           f"{np.round(stop_time - start_time, 3)} s")
        #     if self.display_background_img is True:
        #         self.display_background_img = False
        #         self.update_plot_map_img(after_michou=True)
        elif event.char in ["m", "M"]:
            self.switch_magnifier()
        elif event.char in ["J"]:
            self.switch_prediction_improvement_mode()
        # elif event.char in ["i", "I"]:
        #     if self.n_background_img > 0:
        #         self.switch_michou()
        elif event.char in ["z", "Z"] and not self.segment_mode:
            self.activate_movie_zoom(from_check_box=False)
        # TODO: reactive Save key shortcut
        elif event.char in ["S"] and (not self.segment_mode):
            self.save_segments_as()
        elif event.char in ["T"]:
            self.go_to_next_cell_with_same_type()
        elif event.char in ["s"] and (self.tiff_movie is not None):
            self.switch_source_profile_mode(from_check_box=False, from_key_shortcut=True)
            # print(f"s self.keys_pressed {self.keys_pressed}")
            # if "Control_L" in self.keys_pressed:
            #     print("s with control")
        elif (event.keysym == "space") and (self.tiff_movie is not None):
            self.switch_movie_mode()
        elif (event.keysym in ["y", "Y"]) and (self.agree_button is not None):
            self.agree_switch_mode()
        elif (event.keysym in ["n", "N"]) and (self.dont_agree_button is not None):
            self.dont_agree_switch_mode()
        elif (event.keysym in ["c", "C"]) and (not self.segment_mode) and (self.center_segment_button is not None):
            self.center_segment_swith_mode()

        if event.keysym == 'Right':
            # C as cell
            if ("Meta_L" in self.keys_pressed) or ("Control_L" in self.keys_pressed):
                # ctrl-right, we move to next neuron
                self.select_next_neuron()
            else:
                self.move_zoom(to_the_left=False)
                # so the back button will come back to the curren view
                self.toolbar.push_current()
        elif event.keysym == 'Left':
            if ("Meta_L" in self.keys_pressed) or ("Control_L" in self.keys_pressed):
                self.select_previous_neuron()
            else:
                self.move_zoom(to_the_left=True)
                self.toolbar.push_current()

    def detect_onset_associated_to_peak(self, peak_times):
        """
        Return an array with the onset times (from trace time) associated to the peak_times.
        We look before each peak_time (1sec before), for current_neurons
        :param peak_times:
        :return:
        """
        onsets_detected = []
        for peak_time in peak_times:
            # looking for the peak preceding the onset
            limit_index_search = max((peak_time - (self.decay * self.decay_factor)), 0)
            if peak_time == limit_index_search:
                continue
            onset_times = np.where(self.onset_times[self.current_neuron, limit_index_search:(peak_time + 1)] > 0)[0]
            onset_times += limit_index_search
            onsets_detected.extend(list(onset_times))

        return np.array(onsets_detected)

    def update_onset_times(self):
        # onset_times as values up to 2
        for n, neuron in enumerate(self.spike_nums):
            self.onset_times[n, :] = neuron
        if self.onset_numbers_label is not None:
            self.onset_numbers_label["text"] = f" {self.numbers_of_onset()} "

    def numbers_of_onset(self):
        return len(np.where(self.onset_times[self.current_neuron, :] > 0)[0])

    def numbers_of_peak(self):
        return len(np.where(self.peak_nums[self.current_neuron, :] > 0)[0])

    def numbers_of_onset_to_agree(self):
        if self.to_agree_spike_nums is None:
            return 0
        return len(np.where(self.to_agree_spike_nums[self.current_neuron, :] > 0)[0])

    def numbers_of_peak_to_agree(self):
        if self.to_agree_peak_nums is None:
            return 0
        return len(np.where(self.to_agree_peak_nums[self.current_neuron, :] > 0)[0])

    def swith_all_click_actions(self, initiator):
        if (initiator != "remove_onset_switch_mode") and self.remove_onset_mode:
            self.remove_onset_switch_mode(from_remove_onset_button=False)
        if (initiator != "remove_peak_switch_mode") and self.remove_peak_mode:
            self.remove_peak_switch_mode(from_remove_peak_button=False)
        if (initiator != "add_peak_switch_mode") and self.add_peak_mode:
            self.add_peak_switch_mode(from_add_peak_button=False)
        if (initiator != "remove_all_switch_mode") and self.remove_all_mode:
            self.remove_all_switch_mode(from_remove_all_button=False)
        if (initiator != "switch_movie_mode") and self.movie_mode:
            self.switch_movie_mode(from_movie_button=False)
        if (initiator != "add_onset_switch_mode") and self.add_onset_mode:
            self.add_onset_switch_mode(from_add_onset_button=False)
        if (initiator != "switch_source_profile_mode") and self.source_mode:
            self.switch_source_profile_mode(from_check_box=False, from_key_shortcut=True)
        if (initiator != "add_doubtful_frames_switch_mode") and self.add_doubtful_frames_mode:
            self.add_doubtful_frames_switch_mode(from_add_doubtful_frames_button=False)
        if (initiator != "remove_doubtful_frames_switch_mode") and self.remove_doubtful_frames_mode:
            self.remove_doubtful_frames_switch_mode(from_remove_doubtful_frames_button=False)
        if (initiator != "add_mvt_frames_switch_mode") and self.add_mvt_frames_mode:
            self.add_mvt_frames_switch_mode(from_add_mvt_frames_button=False)
        if (initiator != "remove_mvt_frames_switch_mode") and self.remove_mvt_frames_mode:
            self.remove_mvt_frames_switch_mode(from_remove_mvt_frames_button=False)
        if (initiator != "agree_switch_mode") and self.agree_mode:
            self.agree_switch_mode(from_agree_button=False)
        if (initiator != "dont_agree_switch_mode") and self.dont_agree_mode:
            self.dont_agree_switch_mode(from_dont_agree_button=False)
        if (initiator != "center_segment_swith_mode") and self.center_segment_mode:
            self.center_segment_swith_mode(from_center_segment_button=False)

    def center_segment_swith_mode(self, from_center_segment_button=True):
        # if it was called due to the action of pressing the center_segment button,
        # we're not calling the remove switch mode
        if from_center_segment_button and (not self.center_segment_mode):
            self.swith_all_click_actions(initiator="center_segment_swith_mode")
        self.center_segment_mode = not self.center_segment_mode
        if self.center_segment_mode:
            self.center_segment_button["fg"] = 'green'
            self.center_segment_button["text"] = ' ON  '
        else:
            self.center_segment_button["fg"] = 'red'
            self.center_segment_button["text"] = ' OFF '
            self.center_segment_coord = None
            self.update_plot(amplitude_zoom_fit=False)

    def switch_prediction_improvement_mode(self):
        """
        Allows to display a signal that might change a prediction according for ex to neuropil
        variation or transient correlation. Mode only active if predictions are available
        Returns:

        """
        if not self.prediction_improvement_mode and (self.current_neuron not in self.transient_prediction):
            # the mode is activated only if the current_cell is in transient_prediction
            print("Trying to activate improvement mode even so neuron is not in transients predictions")
            return
        self.prediction_improvement_mode = not self.prediction_improvement_mode
        if self.current_neuron in self.transient_prediction:
            self.compute_prediction_improvement_for_cell(cell=self.current_neuron)
        self.update_plot()

    def compute_prediction_improvement_for_cell(self, cell):
        """
        COmpute prediction improvement only if predictions available for this cell
        Args:
            cell:

        Returns:

        """
        if cell not in self.transient_prediction:
            return

        # now we want to change the prediction to zero if the prediction does pass 0.5 threshold and we think it's
        # wrong
        predictions = self.transient_prediction[cell]
        if len(predictions.shape) == 1:
            predicted_raster_dur = np.zeros(len(predictions), dtype="int8")
        else:
            predicted_raster_dur = np.zeros(predictions.shape[0], dtype="int8")
        threshold_tc = 0.5
        if len(predictions.shape) == 1:
            real_transient_frames = predictions >= threshold_tc
            self.prediction_improvement_dict[cell] = np.copy(predictions)
        elif predictions.shape[1] == 1:
            real_transient_frames = predictions[:, 0] >= threshold_tc
            self.prediction_improvement_dict[cell] = np.copy(predictions[:, 0])
        else:
            # don't work for multi-class
            return

        predicted_raster_dur[real_transient_frames] = 1
        active_periods = get_continous_time_periods(predicted_raster_dur)

        for period in active_periods:
            first_frame = period[0]
            last_frame = period[1]

            corr_value = self.corr_between_source_and_transient(cell=cell, transient=period)
            overlapping_cells = self.overlapping_cells[self.current_neuron]
            overlapping_corr_values = np.zeros(len(overlapping_cells))
            for index, overlapping_cell in enumerate(overlapping_cells):
                overlapping_corr_values[index] = self.corr_between_source_and_transient(cell=overlapping_cell,
                                                                                        transient=period)
            high_corr_on_overlaping_cell = False
            if len(overlapping_cells) > 0 and np.max(overlapping_corr_values) > 0.7:
                high_corr_on_overlaping_cell = True

            if corr_value < 0.25 and high_corr_on_overlaping_cell:
                print(f"Low corr value {np.round(corr_value, 2)} in cell "
                      f"{cell} for transient {first_frame} - {last_frame}")
                self.prediction_improvement_dict[cell][first_frame:last_frame+1] = 0
                continue

            # then we look at neuropil
            lowest_neuropil_value = np.min(self.traces_dict[self.NEUROPIL_TRACE][cell, first_frame:last_frame+1])
            highest_neuropil_value = np.max(self.traces_dict[self.NEUROPIL_TRACE][cell, first_frame:last_frame + 1])
            diff_neuropil = highest_neuropil_value - lowest_neuropil_value
            lowest_raw_value = np.min(self.traces_dict[self.RAW_TRACE][cell, first_frame:last_frame + 1])
            highest_raw_value = np.max(self.traces_dict[self.RAW_TRACE][cell, first_frame:last_frame + 1])
            diff_raw = highest_raw_value - lowest_raw_value
            threshold_ratio_neuropil_raw = 0.7
            if (diff_raw * threshold_ratio_neuropil_raw) < lowest_neuropil_value:
                # then activation is probably due to neuropil
                print(f"High neuropil in cell "
                      f"{cell} for transient {first_frame} - {last_frame}")
                self.prediction_improvement_dict[cell][first_frame:last_frame + 1] = 0


    def add_onset_switch_mode(self, with_peak=False, from_add_onset_button=True):
        """

        Args:
            with_peak: if True, then a peak after onset will be added automatically
            from_add_onset_button:

        Returns:

        """
        # if it was called due to the action of pressing the add_onset button, we're not calling the remove switch mode
        if from_add_onset_button and (not self.add_onset_mode):
            self.swith_all_click_actions(initiator="add_onset_switch_mode")
        self.add_onset_mode = not self.add_onset_mode
        if self.add_onset_mode:
            self.add_onset_button["fg"] = 'green'
            self.add_onset_button["text"] = ' + ONSET ON  '
        else:
            self.add_onset_button["fg"] = 'red'
            self.add_onset_button["text"] = ' + ONSET OFF '

        self.add_onset_with_peak = with_peak

    def remove_onset_switch_mode(self, from_remove_onset_button=True):
        # deactivating other button
        if from_remove_onset_button and (not self.remove_onset_mode):
            self.swith_all_click_actions(initiator="remove_onset_switch_mode")
        self.remove_onset_mode = not self.remove_onset_mode

        if self.remove_onset_mode:
            self.remove_onset_button["fg"] = 'green'
            self.remove_onset_button["text"] = ' - ONSET ON  '
            self.first_click_to_remove = None
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.remove_onset_button["fg"] = 'red'
            self.remove_onset_button["text"] = ' - ONSET OFF '

    def add_doubtful_frames_switch_mode(self, from_add_doubtful_frames_button=True):
        if from_add_doubtful_frames_button and (not self.add_doubtful_frames_mode):
            self.swith_all_click_actions(initiator="add_doubtful_frames_switch_mode")

        self.add_doubtful_frames_mode = not self.add_doubtful_frames_mode
        if self.add_doubtful_frames_mode:
            self.add_doubtful_frames_mode_button["fg"] = 'green'
            self.add_doubtful_frames_mode_button["text"] = ' + DOUBT ON '
            self.first_click_to_remove = None
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.add_doubtful_frames_mode_button["fg"] = 'red'
            self.add_doubtful_frames_mode_button["text"] = ' + DOUBT OFF '

    def remove_doubtful_frames_switch_mode(self, from_remove_doubtful_frames_button=True):
        # deactivating other button
        if from_remove_doubtful_frames_button and (not self.remove_doubtful_frames_mode):
            self.swith_all_click_actions(initiator="remove_doubtful_frames_switch_mode")

        self.remove_doubtful_frames_mode = not self.remove_doubtful_frames_mode
        if self.remove_doubtful_frames_mode:
            self.remove_doubtful_frames_button["fg"] = 'green'
            self.remove_doubtful_frames_button["text"] = ' - DOUBT ON '
            self.first_click_to_remove = None
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.remove_doubtful_frames_button["fg"] = 'red'
            self.remove_doubtful_frames_button["text"] = ' - DOUBT OFF '

    def add_mvt_frames_switch_mode(self, from_add_mvt_frames_button=True):
        if from_add_mvt_frames_button and (not self.add_mvt_frames_mode):
            self.swith_all_click_actions(initiator="add_mvt_frames_switch_mode")

        self.add_mvt_frames_mode = not self.add_mvt_frames_mode
        if self.add_mvt_frames_mode:
            self.add_mvt_frames_mode_button["fg"] = 'green'
            self.add_mvt_frames_mode_button["text"] = ' + MVT ON '
            self.first_click_to_remove = None
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.add_mvt_frames_mode_button["fg"] = 'red'
            self.add_mvt_frames_mode_button["text"] = ' + MVT OFF '

    def remove_mvt_frames_switch_mode(self, from_remove_mvt_frames_button=True):
        # deactivating other button
        if from_remove_mvt_frames_button and (not self.remove_mvt_frames_mode):
            self.swith_all_click_actions(initiator="remove_mvt_frames_switch_mode")

        self.remove_mvt_frames_mode = not self.remove_mvt_frames_mode
        if self.remove_mvt_frames_mode:
            self.remove_mvt_frames_button["fg"] = 'green'
            self.remove_mvt_frames_button["text"] = ' - MVT ON '
            self.first_click_to_remove = None
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.remove_mvt_frames_button["fg"] = 'red'
            self.remove_mvt_frames_button["text"] = ' - MVT OFF '

    def update_transient_prediction_periods_to_check(self):
        # checking if a prediction results are already loaded in mouse_sessions
        # self.transient_prediction contains prediction for each cell
        if len(self.transient_prediction) == 0:
            return
        # first key is an int (cell), and the value is a list of tuple representing the border of the period
        # with prediction being uncertain
        # list of tupe, first int is the cell index, second is the first frame of the beginning of the window, and
        # last frame is the last frame of the window
        self.transient_prediction_periods_to_check = []
        for cell in np.arange(self.nb_neurons):
            if cell not in self.transient_prediction:
                continue
            predictions = self.transient_prediction[cell]
            predicted_raster_dur = np.zeros(predictions.shape[0], dtype="int8")
            if predictions.shape[1] == 1:
                real_transient_frames = predictions[:, 0] >= self.uncertain_prediction_values[0]
            elif predictions.shape[1] == 3:
                # real transient, fake ones, other (neuropil, decay etc...)
                # keeping predictions about real transient when superior
                # to other prediction on the same frame
                max_pred_by_frame = np.max(predictions, axis=1)
                real_transient_frames = np.logical_and((predictions[:, 0] >= self.uncertain_prediction_values[0]),
                                                       (predictions[:, 0] == max_pred_by_frame))
            elif predictions.shape[1] == 2:
                # real transient, fake ones
                # keeping predictions about real transient superior to the threshold
                # and superior to other prediction on the same frame
                max_pred_by_frame = np.max(predictions, axis=1)
                real_transient_frames = np.logical_and((predictions[:, 0] >= self.uncertain_prediction_values[0]),
                                                       (predictions[:, 0] == max_pred_by_frame))
            predicted_raster_dur[real_transient_frames] = 1
            active_periods = get_continous_time_periods(predicted_raster_dur)
            # now we want to remove all period for whch prediction is > at self.uncertain_prediction_values[1]
            # aka the upper threshold
            # active_periods_to_keep = []
            # number of frames before and after the middle of the transient
            # n_frames_around = 100
            for period in active_periods:
                max_pred = np.max(predictions[period[0]:period[1] + 1, 0])
                if max_pred <= self.uncertain_prediction_values[1]:
                    middle = int((period[0] + period[1]) / 2)
                    first_frame = middle - int(self.segment_to_center_length // 2)
                    if (first_frame >= 0) and ((first_frame + self.segment_to_center_length - 1) <
                                               self.nb_times_traces):
                        last_frame = first_frame + self.segment_to_center_length - 1
                    elif first_frame < 0:
                        first_frame = 0
                        last_frame = first_frame + self.segment_to_center_length - 1
                    else:
                        last_frame = self.nb_times_traces - 1
                        first_frame = last_frame - (self.segment_to_center_length - 1)

                    self.transient_prediction_periods_to_check.append((cell, first_frame, last_frame,
                                                                       np.round(max_pred, 2), middle))
        # then we update the list_box
        self.update_predictions_list_box()

    def update_predictions_list_box(self, keep_same_selected_index=False):
        if self.predictions_list_box is None:
            return
        self.predictions_list_box.delete('0', 'end')

        first_index_current_neuron = 0
        for period_index, period in enumerate(self.transient_prediction_periods_to_check):
            self.predictions_list_box.insert(END, f"{period[0]} / {period[3]} / {period[1]}-{period[2]}")
            if (period[0] == self.current_neuron) and (first_index_current_neuron == 0):
                first_index_current_neuron = period_index
            if period in self.segments_to_save_list:
                self.predictions_list_box.itemconfig(period_index, bg=self.color_bg_predicted_transient_list_box)
            else:
                self.predictions_list_box.itemconfig(period_index, bg="white")
            # self.predictions_list_box.itemconfig(period_index, fg="red")
        # used to scroll until the index is visible
        if self.last_index_selected_predictions_list_box is not None:
            cell_selected = self.transient_prediction_periods_to_check[self.last_index_selected_predictions_list_box][0]
            if cell_selected == self.current_neuron:
                self.predictions_list_box.see(self.last_index_selected_predictions_list_box)
            else:
                self.predictions_list_box.see(first_index_current_neuron)
        else:
            self.predictions_list_box.see(first_index_current_neuron)

        if self.last_index_selected_predictions_list_box is not None and keep_same_selected_index:
            self.predictions_list_box.select_set(self.last_index_selected_predictions_list_box)
            self.predictions_list_box.activate(self.last_index_selected_predictions_list_box)
            # self.predictions_list_box.event_generate("<<ListboxSelect>>")

    def update_segments_to_save_list_box(self, initial_loading=False):
        if self.segments_to_save_list_box is None:
            return

        n_frames_gt = 0
        n_active_frames = 0

        # to save memory, the key is an int representing the cell index
        raster_dur_dict = dict()

        self.segments_to_save_list_box.delete('0', 'end')
        for period_index, period in enumerate(self.segments_to_save_list):
            if period_index % 2 == 0:
                bg_color = 'cornflowerblue'
            else:
                bg_color = 'royalblue'
            # cell / first_frame-last_frame
            self.segments_to_save_list_box.insert(END, f"{period[0]} / {period[1]}-{period[2]}")
            self.segments_to_save_list_box.itemconfig(period_index, {'bg': bg_color})
            cell = period[0]
            n_frames_gt += period[2] - period[1] + 1
            # computing the raster_dur so we can get the number of active frames
            if cell in raster_dur_dict:
                raster_dur = raster_dur_dict[cell]
            else:
                raster_dur = np.zeros(self.nb_times, dtype="int8")
                peaks_index = np.where(self.peak_nums[cell, :] > 0)[0]
                onsets_index = np.where(self.onset_times[cell, :] > 0)[0]
                for onset_index in onsets_index:
                    peaks_after = np.where(peaks_index > onset_index)[0]
                    if len(peaks_after) == 0:
                        continue
                    peaks_after = peaks_index[peaks_after]
                    peak_after = peaks_after[0]
                    raster_dur[onset_index:peak_after + 1] = 1
                raster_dur_dict[cell] = raster_dur
            raster_dur = raster_dur[period[1]:period[2] + 1]
            n_active_frames += len(np.where(raster_dur)[0])
            # if an item was previously selected, then the new one is index 0
            if self.last_index_selected_segments_to_save_list_box is not None:
                self.last_index_selected_segments_to_save_list_box = 0

        self.n_frames_gt_label["text"] = f"{n_frames_gt} frames"
        self.n_active_frames_gt_label["text"] = f"{n_active_frames} active"

        if initial_loading:
            return

        if len(self.segments_to_save_list) > 0:
            self.save_segments_button['state'] = 'normal'
        else:
            self.save_segments_button['state'] = DISABLED

    def segments_to_save_list_box_double_click(self, evt):
        """
        Called when a double click is done on segments to save list_box.
        It removes from the list the element that is double clicked
        Args:
            evt:

        Returns:

        """

        cur_selection = evt.widget.curselection()

        if len(cur_selection) == 0:
            return
        index_clicked = int(cur_selection[0])
        period = self.segments_to_save_list[index_clicked]
        segments_list_copy = self.segments_to_save_list.copy()
        self.remove_segment_to_save(index_to_remove=index_clicked)

        self.update_last_action(RemoveSegmentToSaveAction(segment_list=segments_list_copy,
                                                          segment_added=period, index_to_remove=index_clicked,
                                                          session_frame=self,
                                                          neuron=self.current_neuron, is_saved=self.is_saved))

    def remove_segment_to_save(self, index_to_remove):
        period = self.segments_to_save_list[index_to_remove]
        if len(self.transient_prediction_periods_to_check) > 0:
            # TODO: check if this part still works
            try:
                index_predictions_list_box = self.transient_prediction_periods_to_check.index(period)
                self.predictions_list_box.itemconfig(index_predictions_list_box, bg="white")
            except ValueError:
                # it might happen if the list of transients has been updated
                pass

        # now we remove this period from the segments periods and update the listbox
        del self.segments_to_save_list[index_to_remove]
        self.update_segments_to_save_list_box()

    def change_prediction_transient_to_look_at(self, period):
        """
        CHange the plot such as the period indicated is displayed
        :param period: a tuple of len 4: cell, x_left, x_right, pred
        :return:
        """
        new_neuron = period[0]
        new_left_x_limit, new_right_x_limit = (period[1], period[2])
        if len(period) > 4:
            # set the cell and frame in which a vertical line will be draw
            # to indicate at which transient we're looking at
            self.last_predicted_transient_selected = (period[0], period[4])
        frames_around = 0
        new_left_x_limit = max(0, new_left_x_limit - frames_around)
        new_right_x_limit = min(new_right_x_limit + frames_around, self.nb_times_traces - 1)

        new_top_y_limit = np.max(self.raw_traces[new_neuron, new_left_x_limit:new_right_x_limit + 1]) + 0.5
        new_bottom_y_limit = np.min(self.raw_traces[new_neuron, new_left_x_limit:new_right_x_limit + 1]) - 0.5

        new_x_limit = (new_left_x_limit, new_right_x_limit)
        new_y_limit = (new_bottom_y_limit, new_top_y_limit)
        if new_neuron == self.current_neuron:
            self.update_plot(new_x_limit=new_x_limit, new_y_limit=new_y_limit, amplitude_zoom_fit=False)
        else:
            self.update_neuron(new_neuron=new_neuron,
                               new_x_limit=new_x_limit, new_y_limit=new_y_limit, amplitude_zoom_fit=False)

    def predictions_list_box_click(self, evt):
        # print(f"evt.char {evt.char}")
        cur_selection = evt.widget.curselection()

        if len(cur_selection) == 0:
            return

        index_clicked = int(cur_selection[0])

        if self.last_index_selected_predictions_list_box is None:
            self.last_index_selected_predictions_list_box = index_clicked
        else:
            if self.last_index_selected_predictions_list_box == index_clicked:
                return
            self.last_index_selected_predictions_list_box = index_clicked

        # lines commented below was tryouts in order to avoid the caveats that the space bar
        # activated the click on the last item selected. Only solution found, save the last
        # index selected, such as done above.
        # putting the background of the selected item to red and then removing the selection
        # this avoid that for exemple the space touch activate the listbox
        # self.update_predictions_list_box()
        # self.predictions_list_box.itemconfig(index_clicked, {'bg': "red"})
        # self.predictions_list_box.bind('<FocusOut>', lambda e: self.predictions_list_box.selection_clear(0, END))
        # self.predictions_list_box.select_clear(0, END)
        # putting focus on the plot canvas instead
        # self.plot_canvas.get_tk_widget().focus_set()

        period = self.transient_prediction_periods_to_check[index_clicked]
        self.change_prediction_transient_to_look_at(period=period)

    def segments_to_save_list_box_click(self, evt):
        cur_selection = evt.widget.curselection()
        if len(cur_selection) == 0:
            return
        index_clicked = int(cur_selection[0])

        # to avoid activation by the space bar
        if self.last_index_selected_segments_to_save_list_box is None:
            self.last_index_selected_segments_to_save_list_box = index_clicked
        else:
            if self.last_index_selected_segments_to_save_list_box == index_clicked:
                return
            self.last_index_selected_segments_to_save_list_box = index_clicked

        period = self.segments_to_save_list[index_clicked]
        self.change_prediction_transient_to_look_at(period=period)

    def predictions_list_box_double_click(self, evt):
        cur_selection = evt.widget.curselection()
        if len(cur_selection) == 0:
            return
        index_cliked = int(cur_selection[0])
        period = self.transient_prediction_periods_to_check[index_cliked]
        if period in self.segments_to_save_list:
            # it means it has already been added to checked transients
            return
        self.segments_to_save_list.append(period)
        self.predictions_list_box.itemconfig(index_cliked, bg=self.color_bg_predicted_transient_list_box)
        self.update_segments_to_save_list_box()

    def add_current_segment_to_save_list(self):
        """
        Add the current view as a segment.
        The view should have a minimum of 10 frames.
        The view should not be already added.
        Returns:

        """
        first_frame, last_frame = self.axe_plot.get_xlim()
        first_frame = int(first_frame)
        last_frame = int(last_frame)
        first_frame = max(0, first_frame)
        last_frame = min(last_frame, self.n_frames - 1)

        if last_frame - first_frame < 10:
            return

        cell = self.current_neuron
        period = (cell, first_frame, last_frame, -1)
        copy_list = self.segments_to_save_list.copy()

        if period in self.segments_to_save_list:
            return

        self.segments_to_save_list.append(period)
        self.update_segments_to_save_list_box()
        self.update_last_action(AddSegmentToSaveAction(segment_list=copy_list, segment_added=period,
                                                       session_frame=self,
                                                       neuron=self.current_neuron, is_saved=self.is_saved))

    def update_contour_for_cell(self, cell):
        # used in order to have access to contour after animation
        # cell contour
        coord = self.data_and_param.coord_obj.coords[cell]
        xy = coord.transpose()
        self.cell_contours[cell] = patches.Polygon(xy=xy,
                                                   fill=False, linewidth=0, facecolor="red",
                                                   edgecolor="red",
                                                   zorder=15, lw=0.6)

    def agree_switch_mode(self, from_agree_button=True):
        if from_agree_button and (not self.agree_mode):
            self.swith_all_click_actions(initiator="agree_switch_mode")
        self.agree_mode = not self.agree_mode

        if self.agree_mode:
            self.agree_button["fg"] = 'green'
            # in case one click would have been made when remove onset was activated
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.agree_button["fg"] = 'red'

    def dont_agree_switch_mode(self, from_dont_agree_button=True):
        if from_dont_agree_button and (not self.dont_agree_mode):
            self.swith_all_click_actions(initiator="dont_agree_switch_mode")
        self.dont_agree_mode = not self.dont_agree_mode

        if self.dont_agree_mode:
            self.dont_agree_button["fg"] = 'green'
            # in case one click would have been made when remove onset was activated
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.dont_agree_button["fg"] = 'red'

    def remove_peak_switch_mode(self, from_remove_peak_button=True):
        if from_remove_peak_button and (not self.remove_peak_mode):
            self.swith_all_click_actions(initiator="remove_peak_switch_mode")
        self.remove_peak_mode = not self.remove_peak_mode

        if self.remove_peak_mode:
            self.remove_peak_button["fg"] = 'green'
            self.remove_peak_button["text"] = ' - PEAK ON  '
            # in case one click would have been made when remove onset was activated
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.remove_peak_button["fg"] = 'red'
            self.remove_peak_button["text"] = ' - PEAK OFF '

    def remove_all_switch_mode(self, from_remove_all_button=True):
        if from_remove_all_button and (not self.remove_all_mode):
            self.swith_all_click_actions(initiator="remove_all_switch_mode")
        self.remove_all_mode = not self.remove_all_mode

        if self.remove_all_mode:
            self.remove_all_button["fg"] = 'green'
            self.remove_all_button["text"] = ' - ALL ON '
            # in case one click would have been made when remove onset was activated
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
        else:
            if self.first_click_to_remove is not None:
                self.first_click_to_remove = None
                self.update_plot()
            self.remove_all_button["fg"] = 'red'
            self.remove_all_button["text"] = ' - ALL OFF '

    def onrelease_map(self, event):
        """
                        Action when a mouse button is released on cell map
                        :param event:
                        :return:
        """
        if event.dblclick:
            return

        if event.xdata is None:
            return

        # print(f"event.xdata {event.xdata}, event.ydata {event.ydata}")
        x = int(event.xdata)
        y = int(event.ydata)

        new_neuron = self.cell_in_pixel[y, x]
        if new_neuron >= 0:
            if new_neuron != self.current_neuron:
                self.update_neuron(new_neuron=new_neuron)
        # print(f"cell: {self.cell_in_pixel[y, x]}")

    def onrelease(self, event):
        """
                Action when a mouse button is released
                :param event:
                :return:
        """
        if (not self.remove_onset_mode) and (not self.add_onset_mode) and (not self.remove_peak_mode) \
                and (not self.add_peak_mode) and (not self.add_doubtful_frames_mode) \
                and (not self.remove_doubtful_frames_mode) and (not self.add_mvt_frames_mode) \
                and (not self.remove_mvt_frames_mode) \
                and (not self.remove_all_mode) and (not self.movie_mode) \
                and (not self.source_mode) and (not self.agree_mode) and (not self.dont_agree_mode) \
                and (not self.center_segment_mode):
            return

        if event.dblclick:
            return

        if event.xdata is None:
            return

        if self.last_click_position[0] != event.xdata:
            # the mouse has been moved between the pressing and the release
            return

        if self.add_onset_mode or self.add_peak_mode or self.source_mode:
            if (event.xdata < 0) or (event.xdata > (self.nb_times_traces - 1)):
                return
            if self.add_onset_mode:
                self.add_onset(int(round(event.xdata)))
            elif self.add_peak_mode:
                self.add_peak(at_time=int(round(event.xdata)), amplitude=event.ydata)
            elif self.source_mode:
                # we want to display the source and transient profile of the selected transient
                # print(f"self.source_mode click release {event.xdata}")
                transient = None
                # creating temporary variable so we can add to_agree_onsets & peaks in case it exists
                if self.to_agree_spike_nums is not None:
                    tmp_onset_times = np.copy(self.onset_times[self.current_neuron])
                    tmp_onset_times[self.to_agree_spike_nums[self.current_neuron] > 0] = 1
                    tmp_peak_nums = np.copy(self.peak_nums[self.current_neuron])
                    tmp_peak_nums[self.to_agree_peak_nums[self.current_neuron] > 0] = 1
                else:
                    tmp_onset_times = self.onset_times[self.current_neuron]
                    tmp_peak_nums = self.peak_nums[self.current_neuron]
                # we check if we are between an onset and a peak
                onsets_frames = np.where(tmp_onset_times)[0]
                peaks_frames = np.where(tmp_peak_nums)[0]
                # closest onset before the click
                onsets_before_index = np.where(onsets_frames <= event.xdata)[0]
                if len(onsets_before_index) == 0:
                    # print("len(onsets_before_index) == 0")
                    return
                first_onset_before_frame = onsets_frames[onsets_before_index[-1]]
                # print(f"first_onset_before_frame {first_onset_before_frame}")
                # closest peak before onset
                peaks_before_index = np.where(peaks_frames <= event.xdata)[0]
                # onset should be after peak, otherwise it means the click was not between an onset and a peak and
                # so we choose the previous transient
                if len(peaks_before_index) != 0:
                    first_peak_before_frame = peaks_frames[peaks_before_index[-1]]
                    # print(f"first_peak_before_frame {first_peak_before_frame}")
                    if first_peak_before_frame > first_onset_before_frame:
                        transient = (first_onset_before_frame, first_peak_before_frame)

                if transient is None:
                    # closet peak after the click
                    peaks_after_index = np.where(peaks_frames >= event.xdata)[0]
                    # means we are at the end
                    if len(peaks_after_index) == 0:
                        return
                    first_peak_after_frame = peaks_frames[peaks_after_index[0]]
                    # print(f"first_peak_after_frame {first_peak_after_frame}")
                    # closest onset after the click
                    onsets_after_index = np.where(onsets_frames >= event.xdata)[0]
                    # the peak should be before the onset
                    if len(onsets_after_index) != 0:
                        first_onset_after_frame = onsets_frames[onsets_after_index[0]]
                        # print(f"first_onset_after_frame {first_onset_after_frame}")
                        if first_onset_after_frame < first_peak_after_frame:
                            # print(f"first_onset_after_frame < first_peak_after_frame")
                            return
                    transient = (first_onset_before_frame, first_peak_after_frame)
                # print(f"transient {transient}")
                self.click_corr_coord = {"x": int(round(event.xdata)), "y": event.ydata}
                self.update_plot()
                self.plot_source_transient(transient=transient)
            return

        if self.remove_onset_mode or self.remove_peak_mode or \
                self.remove_all_mode or self.movie_mode or \
                self.add_doubtful_frames_mode or self.remove_doubtful_frames_mode or \
                self.add_mvt_frames_mode or self.remove_mvt_frames_mode or self.agree_mode or self.dont_agree_mode:
            if self.first_click_to_remove is not None:
                if self.remove_onset_mode:
                    self.remove_onset(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.remove_peak_mode:
                    self.remove_peak(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.movie_mode:
                    self.start_playing_movie(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.add_doubtful_frames_mode:
                    self.add_doubtful_frames(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.remove_doubtful_frames_mode:
                    self.remove_doubtful_frames(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.add_mvt_frames_mode:
                    self.add_mvt_frames(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.remove_mvt_frames_mode:
                    self.remove_mvt_frames(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.remove_all_mode:
                    self.remove_all(x_from=self.first_click_to_remove["x"], x_to=int(math.ceil(event.xdata)))
                elif self.agree_mode:
                    self.agree_on_fusion(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
                elif self.dont_agree_mode:
                    self.dont_agree_on_fusion(x_from=self.first_click_to_remove["x"], x_to=int(round(event.xdata)))
            else:
                self.first_click_to_remove = {"x": int(round(event.xdata)), "y": event.ydata}
                self.update_plot()

        if self.center_segment_mode:
            # then we change the display, we want a window of length self.segment_to_center_length
            # centered on center_x_coord as much as possible
            self.center_segment_coord = (int(round(event.xdata)), event.ydata)
            new_left_x_limit = self.center_segment_coord[0] - int(self.segment_to_center_length // 2)
            if (new_left_x_limit >= 0) and ((new_left_x_limit + self.segment_to_center_length - 1) <
                                            self.nb_times_traces):
                new_right_x_limit = new_left_x_limit + self.segment_to_center_length - 1
            elif new_left_x_limit < 0:
                new_left_x_limit = 0
                new_right_x_limit = new_left_x_limit + self.segment_to_center_length - 1
            else:
                new_right_x_limit = self.nb_times_traces - 1
                new_left_x_limit = new_right_x_limit - (self.segment_to_center_length - 1)
            new_top_y_limit = np.max(self.raw_traces[self.current_neuron,
                                     new_left_x_limit:new_right_x_limit + 1]) + 0.5
            new_bottom_y_limit = np.min(self.raw_traces[self.current_neuron,
                                        new_left_x_limit:new_right_x_limit + 1]) - 0.5

            new_x_limit = (new_left_x_limit, new_right_x_limit)
            new_y_limit = (new_bottom_y_limit, new_top_y_limit)
            self.update_plot(new_x_limit=new_x_limit, new_y_limit=new_y_limit, amplitude_zoom_fit=False)
            # so the back button will come back to the curren view
            self.toolbar.push_current()

    def motion(self, event):
        """
        Action when the mouse is moved
        :param event:
        :return:
        """
        if not self.magnifier_mode:
            return

        if (not self.add_onset_mode) and (not self.remove_onset_mode) \
                and (not self.add_peak_mode) and (not self.remove_peak_mode) \
                and (not self.remove_all_mode):
            return

        if event.xdata is None:
            return

        if (event.xdata < 0) or (event.xdata > (self.nb_times_traces - 1)):
            return

        # TODO keep track of the speed of the movement, if it moves too fast, don't update the
        #  plot
        change_frame_ref = False
        if self.x_center_magnified is None:
            self.x_center_magnified = event.xdata
            change_frame_ref = True
        else:
            # changing the window only when there is a change > 20% of the range
            if np.abs(event.xdata - self.x_center_magnified) >= (self.magnifier_range * 0.5):
                self.x_center_magnified = event.xdata
                change_frame_ref = True

        self.update_plot_magnifier(mouse_x_position=event.xdata, mouse_y_position=event.ydata,
                                   change_frame_ref=change_frame_ref)

        # print(f"Mouse position: {event.xdata} { event.ydata}")

    def onclick(self, event):
        """
        Action when a mouse button is pressed
        :param event:
        :return:
        """
        if event.xdata is not None:
            self.last_click_position = (event.xdata, event.ydata)

    def remove_onset(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not removing any onset
        modification_done = (np.sum(self.onset_times[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            removed_times = np.where(self.onset_times[self.current_neuron, x_from:x_to] > 0)[0] + x_from
            self.onset_times[self.current_neuron, x_from:x_to] = 0
            self.spike_nums[self.current_neuron, x_from:x_to] = 0
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()
            self.update_last_action(RemoveOnsetAction(removed_times=removed_times, session_frame=self,
                                                      neuron=self.current_neuron, is_saved=self.is_saved,
                                                      x_limits=(left_x_limit, right_x_limit),
                                                      y_limits=(bottom_limit, top_limit)))
        # update to remove the cross of the first click
        self.update_after_onset_change()

    def dont_agree_on_fusion(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not removing any onsets or peaks doubtful
        modification_done = (np.sum(self.to_agree_spike_nums[self.current_neuron, x_from:x_to]) > 0) or \
                            (np.sum(self.to_agree_peak_nums[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            # for the UNDO button
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()

            dont_agree_onset_action = None
            # we remove onsets from the to_agree in the interval
            not_agreed_onsets_index = np.where((self.to_agree_spike_nums[self.current_neuron, x_from:x_to]))[0]
            if len(not_agreed_onsets_index) > 0:
                not_agreed_onsets_index += x_from
                not_agreed_onsets_values = np.copy(self.to_agree_spike_nums[self.current_neuron,
                                                                            not_agreed_onsets_index])
                self.to_agree_spike_nums[self.current_neuron, not_agreed_onsets_index] = 0
                dont_agree_onset_action = DontAgreeOnsetAction(not_agreed_onsets_index=not_agreed_onsets_index,
                                                               not_agreed_onsets_values=not_agreed_onsets_values,
                                                               session_frame=self,
                                                               neuron=self.current_neuron, is_saved=self.is_saved,
                                                               x_limits=(left_x_limit, right_x_limit),
                                                               y_limits=(bottom_limit, top_limit))

            # we remove onsets from the to_agree in the interval and add them to onsets_times
            not_agreed_peaks_index = np.where((self.to_agree_peak_nums[self.current_neuron, x_from:x_to]))[0]
            if len(not_agreed_peaks_index) > 0:
                not_agreed_peaks_index += x_from
                not_agreed_peaks_values = np.copy(self.to_agree_peak_nums[self.current_neuron,
                                                                          not_agreed_peaks_index])
                self.to_agree_peak_nums[self.current_neuron, not_agreed_peaks_index] = 0

                left_x_limit, right_x_limit = self.axe_plot.get_xlim()
                bottom_limit, top_limit = self.axe_plot.get_ylim()
                self.update_last_action(DontAgreePeakAction(not_agreed_peaks_index=not_agreed_peaks_index,
                                                            not_agreed_peaks_values=not_agreed_peaks_values,
                                                            session_frame=self,
                                                            dont_agree_onset_action=dont_agree_onset_action,
                                                            neuron=self.current_neuron, is_saved=self.is_saved,
                                                            x_limits=(left_x_limit, right_x_limit),
                                                            y_limits=(bottom_limit, top_limit)))
            elif dont_agree_onset_action is not None:
                self.update_last_action(dont_agree_onset_action)

            self.update_to_agree_label()
        # update to remove the cross of the first click
        self.update_after_onset_change()

    def agree_on_fusion(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not keeping any onsets or peaks doubtful
        modification_done = (np.sum(self.to_agree_spike_nums[self.current_neuron, x_from:x_to]) > 0) or \
                            (np.sum(self.to_agree_peak_nums[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            # for the UNDO button
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()

            agree_onset_action = None
            # we remove onsets from the to_agree in the interval and add them to onsets_times
            agreed_onsets_index = np.where((self.to_agree_spike_nums[self.current_neuron, x_from:x_to]))[0]
            if len(agreed_onsets_index) > 0:
                agreed_onsets_index += x_from
                # then we keep only the one with the bigger value (represents the nb of person that agree)
                agreed_onsets_values = np.copy(self.to_agree_spike_nums[self.current_neuron, agreed_onsets_index])
                if len(agreed_onsets_index) > 1:
                    index_max = np.argmax(self.to_agree_spike_nums[self.current_neuron,
                                                                   agreed_onsets_index[::-1]])
                    onsets_added = agreed_onsets_index[::-1][index_max]
                    self.onset_times[self.current_neuron, agreed_onsets_index[::-1][index_max]] = 1
                    self.spike_nums[self.current_neuron, agreed_onsets_index[::-1][index_max]] = 1
                else:
                    onsets_added = agreed_onsets_index
                    self.onset_times[self.current_neuron, agreed_onsets_index] = 1
                    self.spike_nums[self.current_neuron, agreed_onsets_index] = 1

                self.to_agree_spike_nums[self.current_neuron, agreed_onsets_index] = 0
                agree_onset_action = AgreeOnsetAction(agreed_onsets_index=agreed_onsets_index,
                                                      agreed_onsets_values=agreed_onsets_values,
                                                      onsets_added=onsets_added,
                                                      session_frame=self,
                                                      neuron=self.current_neuron, is_saved=self.is_saved,
                                                      x_limits=(left_x_limit, right_x_limit),
                                                      y_limits=(bottom_limit, top_limit))

            # we remove onsets from the to_agree in the interval and add them to onsets_times
            agreed_peaks_index = np.where((self.to_agree_peak_nums[self.current_neuron, x_from:x_to]))[0]
            if len(agreed_peaks_index) > 0:
                agreed_peaks_index += x_from
                # then we keep only the ones with the bigger value (represents the nb of person that agree)
                agreed_peaks_values = np.copy(self.to_agree_peak_nums[self.current_neuron, agreed_peaks_index])
                if len(agreed_peaks_index) > 1:
                    index_max = np.argmax(self.to_agree_peak_nums[self.current_neuron, agreed_peaks_index])
                    peaks_added = agreed_peaks_index[index_max]
                    self.peak_nums[self.current_neuron, agreed_peaks_index[index_max]] = 1
                else:
                    peaks_added = agreed_peaks_index
                    self.peak_nums[self.current_neuron, agreed_peaks_index] = 1
                self.to_agree_peak_nums[self.current_neuron, agreed_peaks_index] = 0

                left_x_limit, right_x_limit = self.axe_plot.get_xlim()
                bottom_limit, top_limit = self.axe_plot.get_ylim()
                self.update_last_action(AgreePeakAction(agreed_peaks_index=agreed_peaks_index,
                                                        agreed_peaks_values=agreed_peaks_values,
                                                        peaks_added=peaks_added,
                                                        session_frame=self, agree_onset_action=agree_onset_action,
                                                        neuron=self.current_neuron, is_saved=self.is_saved,
                                                        x_limits=(left_x_limit, right_x_limit),
                                                        y_limits=(bottom_limit, top_limit)))
            elif agree_onset_action is not None:
                self.update_last_action(agree_onset_action)

            self.update_to_agree_label()
        # update to remove the cross of the first click
        self.update_after_onset_change()

    def remove_all(self, x_from, x_to):
        # remove onset and peaks
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        # adding 1 because we go up to frame -1 when removing
        x_to += 1
        if x_to < 0:
            x_to = 0
        elif x_to > self.nb_times_traces:
            x_to = self.nb_times_traces

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not removing any onset
        modification_done = (np.sum(self.onset_times[self.current_neuron, x_from:x_to]) > 0) or \
                            (np.sum(self.peak_nums[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            removed_times = np.where(self.onset_times[self.current_neuron, x_from:x_to] > 0)[0] + x_from
            self.onset_times[self.current_neuron, x_from:x_to] = 0
            self.spike_nums[self.current_neuron, x_from:x_to] = 0
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()
            removed_onset_action = RemoveOnsetAction(removed_times=removed_times, session_frame=self,
                                                     neuron=self.current_neuron, is_saved=self.is_saved,
                                                     x_limits=(left_x_limit, right_x_limit),
                                                     y_limits=(bottom_limit, top_limit))
            removed_times = np.where(self.peak_nums[self.current_neuron, x_from:x_to] > 0)[0] + x_from
            amplitudes = self.peak_nums[self.current_neuron, removed_times]
            self.peak_nums[self.current_neuron, x_from:x_to] = 0
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()
            self.update_last_action(RemovePeakAction(removed_times=removed_times, amplitudes=amplitudes,
                                                     session_frame=self, removed_onset_action=removed_onset_action,
                                                     neuron=self.current_neuron, is_saved=self.is_saved,
                                                     x_limits=(left_x_limit, right_x_limit),
                                                     y_limits=(bottom_limit, top_limit)))
            # no more undone_actions
            self.undone_actions = []
            self.redo_button['state'] = DISABLED
            self.unsaved()
            self.undo_button['state'] = 'normal'
        # update to remove the cross of the first click
        self.update_after_onset_change()

    def remove_peaks_under_threshold(self):
        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        left_x_limit = int(max(left_x_limit, 0))
        right_x_limit = int(min(right_x_limit, self.nb_times_traces - 1))

        # peaks = np.where(self.peak_nums[self.current_neuron, left_x_limit:right_x_limit] > 0)[0]
        # peaks += left_x_limit
        # threshold = self.get_threshold()
        # peaks_under_threshold = np.where(self.smooth_traces[self.current_neuron, peaks] < threshold)[0]
        # if len(peaks_under_threshold) == 0:
        #     return
        # removed_times = peaks[peaks_under_threshold]
        # amplitudes = self.peak_nums[self.current_neuron, peaks][peaks_under_threshold]

        if len(self.peaks_under_threshold_index) == 0:
            return

        peaks_to_remove = np.where(np.logical_and(self.peaks_under_threshold_index >= left_x_limit,
                                                  self.peaks_under_threshold_index <= right_x_limit))[0]
        if len(peaks_to_remove) == 0:
            return

        removed_times = self.peaks_under_threshold_index[peaks_to_remove]

        # should be useless, as we don't keep amplitudes anymore, but too lazy to change the code that follows
        amplitudes = self.peak_nums[self.current_neuron, removed_times]

        self.peak_nums[self.current_neuron, removed_times] = 0
        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        bottom_limit, top_limit = self.axe_plot.get_ylim()
        onset_times_to_remove = self.detect_onset_associated_to_peak(removed_times)
        removed_onset_action = None
        if len(onset_times_to_remove) > 0:
            self.onset_times[self.current_neuron, onset_times_to_remove] = 0
            self.spike_nums[self.current_neuron, onset_times_to_remove] = 0
            removed_onset_action = RemoveOnsetAction(removed_times=onset_times_to_remove,
                                                     session_frame=self,
                                                     neuron=self.current_neuron, is_saved=self.is_saved,
                                                     x_limits=(left_x_limit, right_x_limit),
                                                     y_limits=(bottom_limit, top_limit))
        self.update_last_action(RemovePeakAction(removed_times=removed_times, amplitudes=amplitudes,
                                                 session_frame=self,
                                                 removed_onset_action=removed_onset_action,
                                                 neuron=self.current_neuron, is_saved=self.is_saved,
                                                 x_limits=(left_x_limit, right_x_limit),
                                                 y_limits=(bottom_limit, top_limit)))
        # no more undone_actions
        self.undone_actions = []
        self.redo_button['state'] = DISABLED
        self.unsaved()
        self.undo_button['state'] = 'normal'

        self.update_after_onset_change()

    def remove_peak(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not removing any onset
        modification_done = (np.sum(self.peak_nums[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            removed_times = np.where(self.peak_nums[self.current_neuron, x_from:x_to] > 0)[0] + x_from
            amplitudes = self.peak_nums[self.current_neuron, removed_times]
            self.peak_nums[self.current_neuron, x_from:x_to] = 0
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()
            self.update_last_action(RemovePeakAction(removed_times=removed_times, amplitudes=amplitudes,
                                                     session_frame=self,
                                                     neuron=self.current_neuron, is_saved=self.is_saved,
                                                     x_limits=(left_x_limit, right_x_limit),
                                                     y_limits=(bottom_limit, top_limit)))
            # no more undone_actions
            self.undone_actions = []
            self.redo_button['state'] = DISABLED
            self.unsaved()
            self.undo_button['state'] = 'normal'
        # update to remove the cross of the first click at least
        self.update_after_onset_change()

    def switch_trace_to_be_displayed(self, trace_str):
        """
                Called when one of the trace checkbox change selection. Allows to change the trace displayed

                Returns:

        """
        if trace_str in self.actual_traces_str:
            # then we remove it
            self.actual_traces_str.remove(trace_str)
            self.trace_check_boxes[trace_str].deselect()
        else:
            self.trace_check_boxes[trace_str].select()
            self.actual_traces_str.append(trace_str)

        # there should be at least one trace displayed, default is RAW_TRACE
        if len(self.actual_traces_str) == 0:
            self.actual_traces_str.append(self.RAW_TRACE)
            self.trace_check_boxes[self.RAW_TRACE].select()

        # # we put new_trace at True, so the y-axis is updated
        self.update_plot(new_trace=True)

    def switch_source_profile_mode(self, from_check_box=True, from_key_shortcut=False, from_magnifier=False):
        # if from_key_shortcut is True, means we need to uncheck the check_box
        if not self.source_mode:
            self.swith_all_click_actions(initiator="switch_source_profile_mode")

        if from_check_box:
            self.source_mode = not self.source_mode
        else:
            if not self.source_mode:
                self.source_check_box.select()
            else:
                self.source_check_box.deselect()
            self.source_mode = not self.source_mode
        if not self.source_mode:
            self.first_click_to_remove = None
            self.update_plot()
        elif not from_magnifier:
            if self.magnifier_mode:
                self.switch_magnifier()

    def activate_movie_zoom(self, from_check_box=True):
        if self.zoom_movie_check_box is None:
            return

        if from_check_box:
            self.movie_zoom_mode = not self.movie_zoom_mode
        else:
            # from z keyboard
            if self.tiff_movie is None:
                return
            if not self.movie_zoom_mode:
                self.zoom_movie_check_box.select()
            else:
                self.zoom_movie_check_box.deselect()
            self.movie_zoom_mode = not self.movie_zoom_mode
        if self.display_zoom_frame_around_cell:
            self.update_plot_map_img()

    def set_transient_classifier_prediction_for_cell(self, cell):
        if cell in self.transient_prediction:
            return

        if (self.cinac_recording is None) or (self.classifier_model is None):
            return

        try:
            from deepcinac.cinac_predictor import predict_transient_from_model
        except ImportError as import_error:
            print("Seems like you are missing a package, is it tensorflow ? ")
            raise import_error


        use_data_augmentation = False
        overlap_value = 0.5
        cell_to_predict = cell
        cinac_recording_for_prediction = self.cinac_recording

        # first updating cinac_recording according to cells_to_remove
        if np.sum(self.cells_to_remove) > 0:
            # creating a new cinac_recording as it may
            cinac_recording = CinacRecording(identifier="cinac_gui")
            cinac_movie = CinacDataMovie(movie=self.tiff_movie, already_normalized=True)
            cinac_recording.set_movie(cinac_movie)
            # print("set_transient_classifier_prediction_for_cell updating cinac_recording with invalid cells")
            coord_obj = self.data_and_param.coord_obj
            new_coords_data = []
            number_of_cells_removed = 0
            for cell_index, cell_coord in enumerate(coord_obj.coords):
                if self.cells_to_remove[cell_index] > 0:
                    # updating the cell to predict index according to cells removed
                    if cell_index < cell:
                        cell_to_predict -= 1
                    number_of_cells_removed += 1
                    continue
                new_coords_data.append(cell_coord)
            coords_data = new_coords_data
            cinac_recording.set_rois_2d_array(coord=coords_data, from_matlab=False)
            # print(f"New cell index {cell_to_predict} instead of {cell}, {number_of_cells_removed} removed")
            cinac_recording_for_prediction = cinac_recording

        predictions = predict_transient_from_model(cinac_recording=cinac_recording_for_prediction,
                                                   cell=cell_to_predict, model=self.classifier_model,
                                                   n_frames=self.peak_nums.shape[1],
                                                   overlap_value=overlap_value,
                                                   pixels_around=0,
                                                   use_data_augmentation=use_data_augmentation,
                                                   buffer=0)
        # TODO: buffer changed to one the 20th of march 2020, used to be 0,
        #   changed again to 0 on 10th of april instead of 1

        # predictions as two dimension, first one represents the frame, the second one the prediction
        # for each class
        self.transient_prediction[cell] = predictions
        self.transient_prediction_periods[cell] = dict()

    def transient_classifier_check_box_action(self):
        self.show_transient_classifier = not self.show_transient_classifier
        if self.show_transient_classifier:
            self.set_transient_classifier_prediction_for_cell(self.current_neuron)
            self.print_transients_predictions_stat = True
        self.update_plot()

    def set_cell_type_classifier_prediction_for_cell(self, cell):
        if cell in self.cell_type_classifier_predictions:
            return

        if (self.cinac_recording is None) or (self.cell_type_classifier_model_file is None) or \
                (self.cell_type_classifier_weights_file is None):
            return

        # the import is done here the program can run without tensorflow installed in case not predictions are needed
        try:
            from deepcinac.cinac_predictor import CinacPredictor
        except ImportError as import_error:
            print("Seems like you are missing a package, is it tensorflow ? ")
            raise import_error

        self.cell_type_classifier_predictions[cell] = dict()
        """
              Then we decide which network will be used for predicting the cells' activity.

              A dictionnary with key a tuple of 3 elements is used.

              The 3 elements are:

                   (string) the model file name (.json extension)
                   (string) the weights of the network file name (.h5 extension)
                   (string) identifier for this configuration, will be used to name the output file
                   The dictionnary will contain as value the cells to be predicted by the key configuration. 
                   If the value is set to None, then all the cells will be predicted using this configuration.
        """

        model_files_dict = dict()
        # we just one to predict the cell of interest, which is the first cell
        model_files_dict[(self.cell_type_classifier_model_file, self.cell_type_classifier_weights_file,
                          "cinac_gui")] = np.array([cell])

        """
        We now create an instance of CinacPredictor and add the CinacRecording we have just created.

        It's possible to add more than one instance of CinacRecording, they will be predicted on the same run then.

        The argument removed_cells_mapping allows to remove cells from the segmentation. 
        This could be useful as the network take in consideration the adjacent cells to predict the activity, 
        thus if a cell was wrongly added to segmentation, this could lower the accuracy of the classifier.
        """

        cinac_predictor = CinacPredictor()

        """
        Args:

            removed_cells_mapping: integers array of length the original numbers of 
                cells (such as defined in CinacRecording)
                and as value either of positive int representing the new index of 
                the cell or -1 if the cell has been removed
        """

        cinac_predictor.add_recording(cinac_recording=self.cinac_recording,
                                      removed_cells_mapping=None,
                                      model_files_dict=model_files_dict)

        """
        Finally, we run the prediction.

        The output format could be either a matlab file(.mat) and/or numpy one (.npy).

        If matlab is chosen, the predictions will be available under the key "predictions".

        The predictions are a 2d float array (n_cells * n_frames) with value between 0 and 1, representing the prediction of our classifier for each frame. 1 means the cell is 100% sure active at that time, 0 is 100% sure not active.

        A cell is considered active during the rising time of the calcium transient.

        We use a threshold of 0.5 to binarize the predictions array and make it a raster.
        """

        # you could decomment this line to make sure the GPU is used
        # with tf.device('/device:GPU:0'):

        # predictions are saved in the results_path and return as a dict,
        predictions_dict = cinac_predictor.predict(results_path=None,
                                                   overlap_value=0, cell_type_classifier_mode=True,
                                                   n_segments_to_use_for_prediction=4,
                                                   cell_type_pred_fct=np.mean)
        # mean of the different predictions is already in the dict
        prediction_values = predictions_dict[list(predictions_dict.keys())[0]][cell]

        for index_pred, prediction_value in enumerate(prediction_values):
            if index_pred not in self.cell_type_from_code_dict:
                continue
            cell_type = self.cell_type_from_code_dict[index_pred]
            self.cell_type_classifier_predictions[cell][cell_type] = prediction_value

    def cell_type_classifier_button_action(self):
        """
        Method called when pushing cell type classification button
        Returns:

        """

        # if the prediction is already know, then no computation will happen
        self.set_cell_type_classifier_prediction_for_cell(cell=self.current_neuron)

        self.display_cell_type_predictions()

    def display_cell_type_predictions(self):
        """
        Display in the cell type labels the predictions for the current_neuron
        Returns:

        """
        if self.current_neuron not in self.cell_type_classifier_predictions:
            # then we erase the labels
            for cell_type, cell_type_label in self.cell_type_predictions_label_dict.items():
                cell_type_label["text"] = ""
            return

        for cell_type, cell_type_label in self.cell_type_predictions_label_dict.items():
            if cell_type not in self.cell_type_classifier_predictions[self.current_neuron]:
                continue
            cell_type_label["text"] = str(np.round(self.cell_type_classifier_predictions[self.current_neuron]
                                                   [cell_type], 2))

    def correlation_check_box_action(self, from_std_treshold=False):
        if self.display_threshold and not from_std_treshold:
            self.threshold_check_box_action(from_correlation=True)

        self.display_correlations = not self.display_correlations
        if not from_std_treshold:
            if self.display_correlations:
                if self.display_background_img is False:
                    self.display_background_img = True
                    self.update_plot_map_img()
                start_time = time.time()
                # computing correlations between source and transients profile for this cell and the overlaping ones
                self.compute_source_and_transients_correlation(main_cell=self.current_neuron)
                stop_time = time.time()
                # print(f"Time for computing source and transients correlation for cell {self.current_neuron}: "
                #       f"{np.round(stop_time - start_time, 3)} s")
                if self.display_background_img is True:
                    self.display_background_img = False
                    self.update_plot_map_img(after_michou=True)

            if self.display_correlations:
                self.remove_peaks_under_threshold_button['state'] = 'normal'
            else:
                self.remove_peaks_under_threshold_button['state'] = DISABLED

            self.update_plot()
        else:
            self.correlation_check_box.deselect()

    def threshold_check_box_action(self, from_correlation=False):
        if self.display_correlations and not from_correlation:
            self.correlation_check_box_action(from_std_treshold=True)

        self.display_threshold = not self.display_threshold
        if not from_correlation:
            if self.display_threshold:
                self.remove_peaks_under_threshold_button['state'] = 'normal'
            else:
                self.remove_peaks_under_threshold_button['state'] = DISABLED

            self.update_plot()
        else:
            self.threshold_check_box.deselect()

    def spin_box_pixels_around_cell_update(self):
        self.segment_window_in_pixels = int(self.spin_box_pixels_around_cell.get())
        if self.display_classifier_frame_around_cell:
            self.update_plot_map_img()

    def spin_box_transient_classifier_update(self):
        self.transient_classifier_threshold = float(self.spin_box_transient_classifier.get())
        self.print_transients_predictions_stat = True
        if self.show_transient_classifier:
            self.update_plot()

    def spin_box_threshold_update(self):
        self.nb_std_thresold = float(self.spin_box_threshold.get())
        if self.display_threshold:
            self.update_plot()

    def spin_box_correlation_update(self):
        self.correlation_thresold = float(self.spin_box_correlation.get())
        if self.display_correlations:
            self.update_plot()

    def unsaved(self):
        """
        means a changed has been done, and the actual plot is not saved """
        # not used anymore
        pass
        # self.is_saved = False
        # self.save_button['state'] = 'normal'

    def update_doubtful_frames_periods(self, cell):
        if np.sum(self.doubtful_frames_nums[cell]) == 0:
            self.doubtful_frames_periods[cell] = []
            return

        self.doubtful_frames_periods[cell] = get_continous_time_periods(self.doubtful_frames_nums[cell])

    def update_mvt_frames_periods(self, cell):
        if np.sum(self.mvt_frames_nums[cell]) == 0:
            self.mvt_frames_periods[cell] = []
            return

        self.mvt_frames_periods[cell] = get_continous_time_periods(self.mvt_frames_nums[cell])

    def normalize_traces(self):
        """
        Normalize the fluorescence signal using z-score and change the value of smooth smooth_traces so there are displayed
        under the raw smooth_traces
        Returns:

        """
        # z_score smooth_traces
        for i in np.arange(self.nb_neurons):
            # -2 so smooth smooth_traces will be displayed under the raw smooth_traces
            self.smooth_traces[i, :] = ((self.smooth_traces[i, :] - np.mean(self.smooth_traces[i, :])) / np.std(
                self.smooth_traces[i, :])) - 2
            if self.raw_traces is not None:
                self.raw_traces[i, :] = (self.raw_traces[i, :] - np.mean(self.raw_traces[i, :])) \
                                        / np.std(self.raw_traces[i, :])

    def add_onset(self, at_time):
        if self.onset_times[self.current_neuron, at_time] > 0:
            return

        self.onset_times[self.current_neuron, at_time] = 1
        self.spike_nums[self.current_neuron, at_time] = 1

        # Detecting peak
        add_peak_index = -1
        if self.add_onset_with_peak:
            limit_index_search = min((at_time + (self.decay * self.decay_factor)), self.nb_times_traces - 1)
            if at_time != limit_index_search:
                max_index = np.argmax(self.raw_traces[self.current_neuron, at_time:limit_index_search])
                max_index += at_time
                if np.size(max_index) == 1:  # or isinstance(max_index, int)
                    add_peak_index = max_index
                else:
                    add_peak_index = max_index[0]
                # adding a peak only if there is no peak already detected
                if self.peak_nums[self.current_neuron, add_peak_index] > 0:
                    add_peak_index = -1

        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        bottom_limit, top_limit = self.axe_plot.get_ylim()

        add_peak_action = None
        if add_peak_index > 0:
            self.peak_nums[self.current_neuron, add_peak_index] = self.raw_traces[self.current_neuron, add_peak_index]
            add_peak_action = AddPeakAction(added_time=add_peak_index,
                                            amplitude=self.raw_traces[self.current_neuron, add_peak_index],
                                            session_frame=self,
                                            neuron=self.current_neuron, is_saved=self.is_saved,
                                            x_limits=(left_x_limit, right_x_limit),
                                            y_limits=(bottom_limit, top_limit))

        self.update_last_action(AddOnsetAction(added_time=at_time, session_frame=self,
                                               add_peak_action=add_peak_action,
                                               neuron=self.current_neuron, is_saved=self.is_saved,
                                               x_limits=(left_x_limit, right_x_limit),
                                               y_limits=(bottom_limit, top_limit)))

        self.update_after_onset_change()

    def add_peak(self, at_time, amplitude=0):
        # print("add_peak")
        if self.peak_nums[self.current_neuron, at_time] > 0:
            return

        # print(f"add_peak {at_time}")
        # using the amplitude from self.raw_traces, the amplitude as argument is where the click was made
        self.peak_nums[self.current_neuron, at_time] = 1

        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        bottom_limit, top_limit = self.axe_plot.get_ylim()
        self.update_last_action(AddPeakAction(added_time=at_time,
                                              amplitude=self.raw_traces[self.current_neuron, at_time],
                                              session_frame=self,
                                              neuron=self.current_neuron, is_saved=self.is_saved,
                                              x_limits=(left_x_limit, right_x_limit),
                                              y_limits=(bottom_limit, top_limit)))

        self.update_after_onset_change()

    def update_last_action(self, new_action, from_redo_action=False):
        """
        Keep the size of the last_actions up to five actions
        :param new_action:
        :return:
        """
        self.last_actions.append(new_action)
        if len(self.last_actions) > 5:
            self.last_actions = self.last_actions[1:]

        if from_redo_action:
            return

        # no more undone_actions
        self.undone_actions = []
        self.redo_button['state'] = DISABLED

        self.unsaved()
        self.undo_button['state'] = 'normal'

    def add_peak_switch_mode(self, from_add_peak_button=True):
        """

        :param from_add_peak_button: indicate the user click on the add_peak button, otherwise it means the
        function has been called after another button has been clicked
        :return:
        """
        if from_add_peak_button and (not self.add_peak_mode):
            self.swith_all_click_actions(initiator="add_peak_switch_mode")
        self.add_peak_mode = not self.add_peak_mode
        if self.add_peak_mode:
            self.add_peak_button["fg"] = 'green'
            self.add_peak_button["text"] = ' + PEAK ON  '
        else:
            self.add_peak_button["fg"] = 'red'
            self.add_peak_button["text"] = ' + PEAK OFF '

    def remove_doubtful_frames(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not removing any onset
        modification_done = (np.sum(self.doubtful_frames_nums[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            removed_times = np.where(self.doubtful_frames_nums[self.current_neuron, x_from:x_to] > 0)[0] + x_from
            self.doubtful_frames_nums[self.current_neuron, x_from:x_to] = 0
            self.update_doubtful_frames_periods(cell=self.current_neuron)
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()
            self.update_last_action(RemoveDoubtfulFramesAction(removed_times=removed_times,
                                                               session_frame=self,
                                                               neuron=self.current_neuron, is_saved=self.is_saved,
                                                               x_limits=(left_x_limit, right_x_limit),
                                                               y_limits=(bottom_limit, top_limit)))
        # update to remove the cross of the first click at least
        self.update_after_onset_change()

    def add_doubtful_frames(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value

        backup_values = np.copy(self.doubtful_frames_nums[self.current_neuron, x_from:x_to])
        # print(f"add corrupt frames from {x_from} to {x_to}")
        self.doubtful_frames_nums[self.current_neuron, x_from:(x_to + 1)] = 1
        self.update_doubtful_frames_periods(cell=self.current_neuron)

        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        bottom_limit, top_limit = self.axe_plot.get_ylim()
        self.update_last_action(AddDoubtfulFramesAction(x_from=x_from, x_to=x_to,
                                                        backup_values=backup_values,
                                                        session_frame=self,
                                                        neuron=self.current_neuron, is_saved=self.is_saved,
                                                        x_limits=(left_x_limit, right_x_limit),
                                                        y_limits=(bottom_limit, top_limit)))

        self.update_after_onset_change()

    def remove_mvt_frames(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value
        # if the sum is zero, then we're not removing any onset
        modification_done = (np.sum(self.mvt_frames_nums[self.current_neuron, x_from:x_to]) > 0)
        if modification_done:
            removed_times = np.where(self.mvt_frames_nums[self.current_neuron, x_from:x_to] > 0)[0] + x_from
            self.mvt_frames_nums[self.current_neuron, x_from:x_to] = 0
            self.update_mvt_frames_periods(cell=self.current_neuron)
            left_x_limit, right_x_limit = self.axe_plot.get_xlim()
            bottom_limit, top_limit = self.axe_plot.get_ylim()
            self.update_last_action(RemoveMvtFramesAction(removed_times=removed_times,
                                                          session_frame=self,
                                                          neuron=self.current_neuron, is_saved=self.is_saved,
                                                          x_limits=(left_x_limit, right_x_limit),
                                                          y_limits=(bottom_limit, top_limit)))
        # update to remove the cross of the first click at least
        self.update_after_onset_change()

    def add_mvt_frames(self, x_from, x_to):
        # taking in consideration the case where the click is outside the graph border
        if x_from < 0:
            x_from = 0
        elif x_from > (self.nb_times_traces - 1):
            x_from = (self.nb_times_traces - 1)

        if x_to < 0:
            x_to = 0
        elif x_to > (self.nb_times_traces - 1):
            x_to = (self.nb_times_traces - 1)

        if x_from == x_to:
            return

        self.first_click_to_remove = None

        # in case x_from is after x_to
        min_value = min(x_from, x_to)
        max_value = max(x_from, x_to)
        x_from = min_value
        x_to = max_value

        backup_values = np.copy(self.mvt_frames_nums[self.current_neuron, x_from:x_to])
        # print(f"add corrupt frames from {x_from} to {x_to}")
        self.mvt_frames_nums[self.current_neuron, x_from:(x_to + 1)] = 1
        self.update_mvt_frames_periods(cell=self.current_neuron)

        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        bottom_limit, top_limit = self.axe_plot.get_ylim()
        self.update_last_action(AddMvtFramesAction(x_from=x_from, x_to=x_to,
                                                   backup_values=backup_values,
                                                   session_frame=self,
                                                   neuron=self.current_neuron, is_saved=self.is_saved,
                                                   x_limits=(left_x_limit, right_x_limit),
                                                   y_limits=(bottom_limit, top_limit)))

        self.update_after_onset_change()

    def validation_before_closing(self):
        # if not self.is_saved:
        #     self.save_as_spike_nums()
        self.root.destroy()

    def redo_action(self):
        last_undone_action = self.undone_actions[-1]
        self.undone_actions = self.undone_actions[:-1]
        last_undone_action.redo()
        self.update_last_action(last_undone_action, from_redo_action=True)

        if last_undone_action.is_saved and (not self.is_saved):
            self.save_button['state'] = DISABLED
            self.is_saved = True
        elif self.is_saved:
            self.unsaved()
            # and we put the rest of the last action as not saved as the plot has been saved meanwhile
            for a in self.undone_actions:
                a.is_saved = False

        self.undo_button['state'] = "normal"

        if len(self.undone_actions) == 0:
            self.redo_button['state'] = DISABLED

        # if different neuron, display the other neuron
        if last_undone_action.neuron == self.current_neuron:
            self.update_after_onset_change(new_x_limit=last_undone_action.x_limits,
                                           new_y_limit=last_undone_action.y_limits)
        else:
            self.update_after_onset_change(new_neuron=last_undone_action.neuron,
                                           new_x_limit=last_undone_action.x_limits,
                                           new_y_limit=last_undone_action.y_limits)

    def undo_action(self):
        """
        Revoke the last action
        :return:
        """

        last_action = self.last_actions[-1]
        self.last_actions = self.last_actions[:-1]
        last_action.undo()

        # if self.last_action.onset_added:
        #     # an onset was added
        #     self.onset_times[self.last_action.neuron, self.last_action.added_time] = 0
        #     self.spike_nums[self.last_action.neuron, self.last_action.added_time*2] = 0
        # else:
        #     # an or several onsets were removed
        #     self.onset_times[self.last_action.neuron, self.last_action.removed_times] = 1
        #     self.spike_nums[self.last_action.neuron, self.last_action.removed_times * 2] = 1

        # if it was saved before last modification and was not saved since, then it is still saved with uptodate version
        if last_action.is_saved and (not self.is_saved):
            self.save_button['state'] = DISABLED
            self.is_saved = True
        elif self.is_saved:
            self.unsaved()
            # and we put the rest of the last action as not saved as the plot has been saved meanwhile
            for a in self.last_actions:
                a.is_saved = False

        self.undone_actions.append(last_action)
        self.redo_button['state'] = "normal"

        if len(self.last_actions) == 0:
            self.undo_button['state'] = DISABLED

        # if different neuron, display the other neuron
        if last_action.neuron == self.current_neuron:
            self.update_after_onset_change(new_x_limit=last_action.x_limits, new_y_limit=last_action.y_limits)
        else:
            self.update_after_onset_change(new_neuron=last_action.neuron,
                                           new_x_limit=last_action.x_limits, new_y_limit=last_action.y_limits)

        # self.last_action = None

    def save_sources_profile_map(self, key_cmap=None):
        # c_map = plt.get_cmap('gray')
        # if key_cmap is not None:
        #     if key_cmap is "P":
        #         c_map = self.parula_map
        #     if key_cmap is "B":
        #         c_map = plt.get_cmap('Blues')
        c_map = self.parula_map
        # removed cells in cmap Gray, other cells in Parula
        # decide threshold  and if CNN model available, red border is real cell, green border if false
        # displaying value in the righ bottom border
        n_cells = len(self.raw_traces)
        n_cells_by_row = 20
        n_pixels_by_cell_x = 20
        n_pixels_by_cell_y = 20
        len_x = n_cells_by_row * n_pixels_by_cell_x
        len_y = math.ceil(n_cells / n_cells_by_row) * n_pixels_by_cell_y
        # sources_profile_map = np.zeros((len_y, len_x), dtype="int16")

        sources_profile_fig = plt.figure(figsize=(20, 20),
                                         subplotpars=SubplotParams(hspace=0, wspace=0))
        fig_patch = sources_profile_fig.patch
        rgba = c_map(0)
        fig_patch.set_facecolor(rgba)

        # sources_profile_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 0.1, 'h_pad': 0.1})

        # looking at how many overlapping cell current_neuron has
        intersect_cells = self.overlapping_cells[self.current_neuron]
        # print(f"len(intersect_cells) {len(intersect_cells)}")
        cells_color = dict()
        for index, cell_inter in enumerate(np.arange(n_cells)):
            cells_color[cell_inter] = cm.nipy_spectral(float(index + 1) / (len(intersect_cells) + 1))

        # now adding as many suplots as need, depending on how many overlap has the cell
        n_columns = n_cells_by_row
        width_ratios = [100 // n_columns] * n_columns
        n_lines = (((n_cells - 1) // n_columns) + 1) * 2
        height_ratios = [100 // n_lines] * n_lines
        grid_spec = gridspec.GridSpec(n_lines, n_columns, width_ratios=width_ratios,
                                      height_ratios=height_ratios,
                                      figure=sources_profile_fig, wspace=0, hspace=0)

        # building the subplots to displays the sources and transients
        ax_source_profile_by_cell = dict()

        max_len_x = None
        max_len_y = None
        for cell_to_display in np.arange(n_cells):
            poly_gon = self.data_and_param.coord_obj.cells_polygon[cell_to_display]

            if max_len_x is None:
                tmp_minx, tmp_miny, tmp_maxx, tmp_maxy = np.array(list(poly_gon.bounds)).astype(int)
                max_len_x = tmp_maxx - tmp_minx
                max_len_y = tmp_maxy - tmp_miny
            else:
                tmp_minx, tmp_miny, tmp_maxx, tmp_maxy = np.array(list(poly_gon.bounds)).astype(int)
                max_len_x = max(max_len_x, tmp_maxx - tmp_minx)
                max_len_y = max(max_len_y, tmp_maxy - tmp_miny)
        bounds = (0, 0, max_len_x, max_len_y)

        for cell_index, cell_to_display in enumerate(np.arange(n_cells)):
            line_gs = (cell_index // n_columns) * 2
            col_gs = cell_index % n_columns

            ax_source_profile_by_cell[cell_to_display] = sources_profile_fig.add_subplot(grid_spec[line_gs, col_gs])
            ax = ax_source_profile_by_cell[cell_to_display]
            # ax_source_profile_by_cell[cell_to_display].set_facecolor(self.background_color)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            if predictions is None:
                ax.set_frame_on(False)
            else:
                # 3 range of color
                if predictions[cell_index] > 0.6:
                    frame_color = "green"
                elif predictions[cell_index] < 0.3:
                    frame_color = "red"
                else:
                    frame_color = "black"
                for spine in ax.spines.values():
                    spine.set_edgecolor(frame_color)
                    spine.set_linewidth(1.5)
                # ax.spines['bottom'].set_color(frame_color)
                # ax.spines['top'].set_color(frame_color)
                # ax.spines['right'].set_color(frame_color)
                # ax.spines['left'].set_color(frame_color)
        # saving source profile with full frame for SEUDO in a matlab file
        bounds = None
        seudo_source_profiles = None
        for cell_index, cell_to_display in enumerate(np.arange(n_cells)):
            if cell_to_display not in self.source_profile_dict_for_map_of_all_cells:
                source_profile, minx, miny, mask_source_profile = self.get_source_profile(cell=cell_to_display,
                                                                                          pixels_around=3,
                                                                                          bounds=bounds,
                                                                                          with_full_frame=True)
                source_profile[mask_source_profile] = 0
                if seudo_source_profiles is None:
                    seudo_source_profiles = np.zeros((n_cells, source_profile.shape[0], source_profile.shape[1]))
                seudo_source_profiles[cell_index] = source_profile

        bounds = None
        for cell_index, cell_to_display in enumerate(np.arange(n_cells)):
            if cell_to_display not in self.source_profile_dict_for_map_of_all_cells:
                source_profile, minx, miny, mask_source_profile = self.get_source_profile(cell=cell_to_display,
                                                                                          pixels_around=3,
                                                                                          bounds=bounds)
                xy_source = self.get_cell_new_coord_in_source(cell=cell_to_display, minx=minx, miny=miny)
                self.source_profile_dict_for_map_of_all_cells[cell_to_display] = [source_profile, minx, miny,
                                                                                  mask_source_profile,
                                                                                  xy_source]
            else:
                source_profile, minx, miny, mask_source_profile, xy_source = \
                    self.source_profile_dict_for_map_of_all_cells[cell_to_display]
            if self.cells_to_remove[cell_to_display] == 1:
                c_map = plt.get_cmap('gray')
            else:
                c_map = self.parula_map
            img_src_profile = ax_source_profile_by_cell[cell_to_display].imshow(source_profile,
                                                                                cmap=c_map)
            with_mask = False
            if with_mask:
                source_profile[mask_source_profile] = 0
                img_src_profile.set_array(source_profile)

            lw = 0.2
            contour_cell = patches.Polygon(xy=xy_source,
                                           fill=False,
                                           edgecolor="red",
                                           zorder=15, lw=lw)
            ax_source_profile_by_cell[cell_to_display].add_patch(contour_cell)

            # if key_cmap in ["B", "P"]:
            #     color_text = "red"
            # else:
            #     color_text = "blue"
            if self.cells_to_remove[cell_to_display] == 1:
                color_text = "blue"
            else:
                color_text = "red"
            ax_source_profile_by_cell[cell_to_display].text(x=1.5, y=1,
                                                            s=f"{cell_to_display}", color=color_text, zorder=20,
                                                            ha='center', va="center", fontsize=3, fontweight='bold')

        # plt.show()
        # TODO: open a file_dialog to choose the file to save it
        save_formats = ["pdf"]
        path_results = self.data_and_param.time_str
        if not os.path.isdir(path_results):
            os.mkdir(path_results)

        sio.savemat(f"{path_results}/" + f"seudo_source_profiles.mat",
                    {'seudo_source_profiles': seudo_source_profiles})

        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            sources_profile_fig.savefig(f'{path_results}/'
                                        f'source_profiles_map_cmap_{key_cmap}'
                                        f'_{self.data_and_param.time_str}.{save_format}',
                                        format=f"{save_format}",
                                        facecolor=sources_profile_fig.get_facecolor(), edgecolor='none')

    # def load_checked_predictions(self):
    #     options = {}
    #     options['initialdir'] = self.data_and_param.path_data
    #     if self.save_checked_predictions_dir is not None:
    #         options['initialdir'] = self.save_checked_predictions_dir
    #     options['title'] = "Choose a directory to open files"
    #     options['mustexist'] = False
    #     path_for_files = filedialog.askdirectory(**options)
    #     if path_for_files == "":
    #         return None
    #     file_names_to_load = []
    #     for (dirpath, dirnames, local_filenames) in os.walk(path_for_files):
    #         for file_name in local_filenames:
    #             if file_name.endswith(".npy"):
    #                 file_names_to_load.append(file_name)
    #         break
    #
    #     self.save_checked_predictions_dir = path_for_files
    #
    #     for file_name in file_names_to_load:
    #         underscores_pos = [pos for pos, char in enumerate(file_name) if char == "_"]
    #         if len(underscores_pos) < 4:
    #             continue
    #         # the last 4 indicates how to get cell number and frames
    #         middle_frame = int(file_name[underscores_pos[-1] + 1:-4])
    #         last_frame = int(file_name[underscores_pos[-2] + 1:underscores_pos[-1]])
    #         first_frame = int(file_name[underscores_pos[-3] + 1:underscores_pos[-2]])
    #         cell = int(file_name[underscores_pos[-4] + 1:underscores_pos[-3]])
    #         self.update_transient_prediction_periods_to_check()
    #         predictions = self.transient_prediction[cell]
    #         max_pred = np.max(predictions[max(0, middle_frame - 2):min(middle_frame + 2, len(predictions) + 1), 0])
    #         max_pred = np.round(max_pred, 2)
    #         new_pred_period = (cell, first_frame, last_frame, max_pred, middle_frame)
    #         raster_dur = np.load(os.path.join(path_for_files, file_name))
    #         # print(f"raster_dur.shape {raster_dur.shape}")
    #         periods = get_continous_time_periods(raster_dur)
    #
    #         # tabula rasa
    #         self.onset_times[cell, first_frame:last_frame] = 0
    #         self.spike_nums[cell, first_frame:last_frame] = 0
    #         self.peak_nums[cell, first_frame:last_frame] = 0
    #
    #         for period in periods:
    #             if period[0] > 0:
    #                 self.onset_times[cell, first_frame + period[0]] = 1
    #                 self.spike_nums[cell, first_frame + period[0]] = 1
    #             if first_frame + period[1] != (last_frame - 1):
    #                 self.peak_nums[cell, first_frame + period[1]] = 1
    #
    #         self.segments_to_save_list.append(new_pred_period)
    #         # then we change the foreground of the predictions_list_boxs
    #         if new_pred_period in self.segments_to_save_list:
    #             if new_pred_period in self.transient_prediction_periods_to_check:
    #                 index_predictions_list_box = self.transient_prediction_periods_to_check.index(new_pred_period)
    #                 self.predictions_list_box.itemconfig(index_predictions_list_box,
    #                                                      bg=self.color_bg_predicted_transient_list_box)
    #
    #     self.update_segments_to_save_list_box()
    #     self.update_after_onset_change()

    def get_square_coord_around_cell(self, cell, x_len_max, y_len_max, square_size):
        """

        Args:
            cell:
            x_len_max: max x value (border of the movie)
            y_len_max: max y value (border of the movie)
            square_size: number of pixels that compose the border of the square

        Returns: Two int representing the minx and miny of the square that will be used to train the classifier

        """
        if square_size in self.square_coord_around_cell_dict:
            if cell in self.square_coord_around_cell_dict[square_size]:
                return self.square_coord_around_cell_dict[square_size][cell]
        if min(self.tiff_movie.shape[2], self.tiff_movie.shape[1]) > square_size:

            # determining the size of the square surrounding the cell so it includes all overlapping cells around
            if cell in self.data_and_param.coord_obj.intersect_cells:
                overlapping_cells = self.data_and_param.coord_obj.intersect_cells[cell]
            else:
                overlapping_cells = []
            cells = [cell]
            cells.extend(overlapping_cells)

            use_old_version = True
            # calculating the bound that will surround all the cells
            if use_old_version:
                # calculating the bound that will surround all the cells
                minx = None
                maxx = None
                miny = None
                maxy = None

                centroid_cell = self.data_and_param.coord_obj.center_coord[cell]
                min_x_centroid = centroid_cell[0] - int(square_size // 2)
                max_x_centroid = min_x_centroid + square_size - 1
                min_y_centroid = centroid_cell[1] - int(square_size // 2)
                max_y_centroid = min_y_centroid + square_size - 1

                # TODO: we check if the cell diameter is not bigger than the window, if it is we
                # center the square around the frame
                poly_gon_cell = self.data_and_param.coord_obj.cells_polygon[cell]
                minx_cell, miny_cell, maxx_cell, maxy_cell = np.array(list(poly_gon_cell.bounds)).astype(int)

                # if the cell is bigger than the square, then we just put its centroid in the middle of it
                if ((maxx_cell - minx_cell + 1) >= square_size) or \
                        ((maxy_cell - miny_cell + 1) >= square_size):
                    minx = min_x_centroid
                    miny = min_y_centroid

                    # then we make sure we don't over go the border
                    if minx + square_size >= x_len_max:
                        minx = x_len_max - square_size - 1
                    if miny + square_size >= y_len_max:
                        miny = y_len_max - square_size - 1
                else:

                    for cell_in in cells:
                        poly_gon = self.data_and_param.coord_obj.cells_polygon[cell_in]

                        if minx is None:
                            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
                        else:
                            tmp_minx, tmp_miny, tmp_maxx, tmp_maxy = np.array(list(poly_gon.bounds)).astype(int)
                            minx = min(minx, tmp_minx)
                            miny = min(miny, tmp_miny)
                            maxx = max(maxx, tmp_maxx)
                            maxy = max(maxy, tmp_maxy)

                    # centering the window on the cell
                    # then we want the cell to be in the window
                    # if (min_x_centroid <= minx) and \
                    #         ((min_x_centroid + square_size) >= maxx):
                    #     minx = min_x_centroid
                    #
                    # if (min_y_centroid <= miny) and \
                    #         ((min_y_centroid + square_size) >= maxy):
                    #     miny = min_y_centroid

                    # trying to put the cell in, first by centering the frame around the centroid if necessary
                    # then if some part of the cell still are out, we use the min of the cell
                    if min_x_centroid < minx:
                        minx = min_x_centroid
                    if minx_cell < minx:
                        minx = minx_cell
                    if min_y_centroid < miny:
                        miny = min_y_centroid
                    if miny_cell < miny:
                        miny = miny_cell

                    if (minx + square_size - 1) < max_x_centroid:
                        minx = max_x_centroid - square_size + 1
                    if (minx + square_size - 1) < maxx_cell:
                        minx = maxx_cell - square_size + 1
                    if (maxy + square_size - 1) < max_y_centroid:
                        miny = max_y_centroid - square_size + 1
                    if (miny + square_size - 1) < maxy_cell:
                        miny = maxy_cell - square_size + 1

                    # then we make sure we don't over go the border
                    minx = max(0, minx)
                    miny = max(0, miny)
                    if minx + square_size >= x_len_max:
                        minx = x_len_max - square_size - 1
                    if miny + square_size >= y_len_max:
                        miny = y_len_max - square_size - 1

                    maxx = minx + square_size - 1
                    maxy = miny + square_size - 1
                    len_x = square_size
                    len_y = square_size
            else:
                centroid_cell = self.data_and_param.coord_obj.center_coord[cell]
                min_x_centroid = centroid_cell[0] - int(square_size // 2)
                min_y_centroid = centroid_cell[1] - int(square_size // 2)

                # TODO: Try the old version
                # we keep it simple and center the window around the centroid of the cell
                minx = min_x_centroid
                miny = min_y_centroid

                # then we make sure we don't over go the border
                if minx + square_size >= x_len_max:
                    minx = x_len_max - square_size - 1
                if miny + square_size >= y_len_max:
                    miny = y_len_max - square_size - 1
        else:
            minx = 0
            miny = 0

        # pixels_around is set at 0
        # minx = max(0, minx - pixels_around)
        # miny = max(0, miny - pixels_around)

        if square_size not in self.square_coord_around_cell_dict:
            self.square_coord_around_cell_dict[square_size] = dict()
        self.square_coord_around_cell_dict[square_size][cell] = (max(0, minx), max(0, miny))

        return self.square_coord_around_cell_dict[square_size][cell]

    def save_segments(self, and_close=False):
        if self.save_file_name is None:
            self.save_segments_as(and_close=and_close)
            return

        # self.save_segments_button['state'] = DISABLED
        # so far save button is activated after the first save as
        self.save_segments_button['state'] = 'normal'
        self.is_saved = True

        with_full_data_info = True
        # means we either save the ci movie file_name or the raw data
        save_ci_movie_info = True
        # if False, then save the full movie in the h5 file
        save_only_movie_ref = True
        # TODO: Add a message box so that the user confirms he wants to update this cinac file

        # ## new Version using CinacFileWriter
        cinac_writer = CinacFileWriter(file_name=os.path.join(self.save_path, self.save_file_name))

        # full data information is not supposed to change if the file is already registered
        if (not cinac_writer.file_already_exists) and with_full_data_info:
            # means we put information regarding the full movie with all cells,
            # original cells coordinates
            tiff_movie_to_save = self.data_and_param.non_norm_tiff_movie
            cinac_writer.create_full_data_group(save_only_movie_ref=save_only_movie_ref,
                                                save_ci_movie_info=save_ci_movie_info,
                                                n_cells=len(self.data_and_param.coord_obj.coords),
                                                n_frames=self.n_frames,
                                                smooth_traces=self.smooth_traces,
                                                raw_traces=self.raw_traces,
                                                cells_contour=self.data_and_param.coord_obj.coords,
                                                ci_movie_file_name=self.data_and_param.ci_movie_file_name,
                                                ci_movie=tiff_movie_to_save, invalid_cells=self.cells_to_remove)
        else:
            n_cells_in_file = cinac_writer.get_n_cells()
            if n_cells_in_file is not None:
                if n_cells_in_file != len(self.data_and_param.coord_obj.coords):
                    print(f"Not the same number of cells with {self.save_file_name}")
                    # TODO: See to display a message box instead
                    return

        # represents the groups present in the h5 file
        # we keep the original list, so the ones not present in the menu will be deleted
        original_groups = set(cinac_writer.get_group_names())
        # remove full_data
        original_groups.discard("full_data")
        # key is an int representing the cell index, and the value a 1d array representing the raster dur for this
        # cell. Dict is used just to avoid unecessary computation if raster_dur for a cell has already been
        # computed
        raster_dur_dict = dict()
        # to avoid unecessary computation
        source_profiles_dict = dict()
        pixels_around_for_source_profile = 0
        buffer_for_source_profile = 1

        for segment in self.segments_to_save_list:
            # we will have a list of cell and frames
            # looping over them
            # for each we need to determine which cells are in the window we want to save, their new coordinates
            # in this window and reindexing cells accordingly, 0 being our cell of interest
            # data is identified by the cell index, the first and last frame index of the window
            cell = segment[0]
            first_frame = segment[1]
            # last_frame is included
            last_frame = segment[2]
            if first_frame < 0:
                print(f"first_frame {first_frame} < 0")
                first_frame = 0
            if last_frame >= self.n_frames:
                print(f"last_frame {last_frame} > {self.n_frames}")
                last_frame = self.n_frames - 1

            if cell in raster_dur_dict:
                raster_dur = raster_dur_dict[cell]
            else:
                raster_dur = np.zeros(self.nb_times, dtype="int8")
                peaks_index = np.where(self.peak_nums[cell, :] > 0)[0]
                onsets_index = np.where(self.onset_times[cell, :] > 0)[0]
                if len(onsets_index) != len(peaks_index):
                    messagebox.showwarning("Careful", f"The number of onsets ({len(onsets_index)}) "
                                                      f"and peaks ({len(peaks_index)}) doesn't match for cell {cell}")
                for onset_index in onsets_index:
                    # >= because transient may be only 1 frame
                    peaks_after = np.where(peaks_index >= onset_index)[0]
                    if len(peaks_after) == 0:
                        continue
                    peaks_after = peaks_index[peaks_after]
                    peak_after = peaks_after[0]
                    raster_dur[onset_index:peak_after + 1] = 1
                raster_dur_dict[cell] = raster_dur
            raster_dur_to_save = raster_dur[first_frame:last_frame + 1]

            # has been normalize using z-score in normalize_traces() method
            smooth_traces_to_save = self.smooth_traces[cell, first_frame:last_frame + 1]
            raw_traces_to_save = self.raw_traces[cell, first_frame:last_frame + 1]

            # now getting the movie patch surroung the cell so we save in the file only the pixels
            # surrounding the cell for the given frames
            if cell in source_profiles_dict:
                mask_source_profiles, coords = source_profiles_dict[cell]
            else:
                mask_source_profiles, coords = \
                    get_source_profile_param(cell=cell,
                                             movie_dimensions=self.tiff_movie.shape[1:],
                                             coord_obj=self.data_and_param.coord_obj,
                                             pixels_around=pixels_around_for_source_profile,
                                             buffer=buffer_for_source_profile,
                                             max_width=self.segment_window_in_pixels,
                                             max_height=self.segment_window_in_pixels,
                                             with_all_masks=True)
                source_profiles_dict[cell] = [mask_source_profiles, coords]
            # we save the normalized movie version, as normalizing movie won't be possible without the full movie
            # later on
            frames = np.arange(first_frame, last_frame + 1)
            minx, maxx, miny, maxy = coords
            # frames that contains all the pixels surrounding our cell and the overlapping one
            # with a max size of self.segment_window_in_pixels
            source_profile_frames = self.tiff_movie[frames, miny:maxy + 1, minx:maxx + 1]

            # then we fit it the frame use by the network, padding the surrounding by zero if necessary
            profile_fit = np.zeros((len(frames), self.segment_window_in_pixels, self.segment_window_in_pixels))
            # we center the source profile
            y_coord = (profile_fit.shape[1] - source_profile_frames.shape[1]) // 2
            x_coord = (profile_fit.shape[2] - source_profile_frames.shape[2]) // 2
            profile_fit[:, y_coord:source_profile_frames.shape[1] + y_coord,
            x_coord:source_profile_frames.shape[2] + x_coord] = \
                source_profile_frames

            # changing the corner coordinates, used to scale the scale coordinates of cells contour
            minx = minx - x_coord
            miny = miny - y_coord

            # now we want to compute the new cells coordinates in this window and see if some of the overlapping
            # cells are invalid
            if cell in self.data_and_param.coord_obj.intersect_cells:
                overlapping_cells = self.data_and_param.coord_obj.intersect_cells[cell]
            else:
                overlapping_cells = []
            coords_to_register = []
            cells_to_register = [cell]
            cells_to_register.extend(overlapping_cells)
            # binary array of the same length as the number of cells, 1 if invalid
            invalid_cells = self.cells_to_remove[np.array(cells_to_register)]
            for cell_to_register_index, cell_to_register in enumerate(cells_to_register):
                polygon = self.data_and_param.coord_obj.cells_polygon[cell_to_register]
                scaled_polygon = scale_polygon_to_source(polygon=polygon, minx=minx, miny=miny)
                if isinstance(scaled_polygon, geometry.LineString):
                    coord_shapely = list(scaled_polygon.coords)
                else:
                    coord_shapely = list(scaled_polygon.exterior.coords)
                # changing the format of coordinates so it matches the usual one
                coords_to_register.append(np.array(coord_shapely).transpose())

            # registering invalid cells among the overlaping cells
            # the cell registered can't be invalid
            invalid_cells[0] = 0

            doubtful_frames = self.doubtful_frames_nums[cell, first_frame:last_frame + 1]
            group_name = cinac_writer.add_segment_group(cell=cell, first_frame=first_frame,
                                                        last_frame=last_frame, raster_dur=raster_dur_to_save,
                                                        doubtful_frames=doubtful_frames, ci_movie=profile_fit,
                                                        pixels_around=pixels_around_for_source_profile,
                                                        buffer=buffer_for_source_profile,
                                                        cells_contour=coords_to_register,
                                                        smooth_traces=smooth_traces_to_save,
                                                        raw_traces=raw_traces_to_save,
                                                        cell_type=self.cell_type_dict.get(cell, None),
                                                        invalid_cells=invalid_cells)
            original_groups.discard(group_name)

        cinac_writer.delete_groups(group_names=original_groups)
        cinac_writer.close_file()

        # means that the method has been called when closing the GUI
        if and_close:
            self.root.destroy()

    def save_segments_as(self, and_close=False):
        """
        Open a filedialog to save the data in a .cinac extension (hdf5 format).
        The data saved correspond to the onset and peak for the cells and frames displayed over the smooth_traces.
        Returns: None

        """
        initialdir = "/"
        if self.save_path is not None:
            initialdir = self.save_path

        # print(f"save_segments_as")
        file_name = filedialog.asksaveasfilename(initialdir=initialdir,
                                                 title="Select file",
                                                 filetypes=[("CINAC files", "*.cinac")])
        if (file_name is None) or (file_name == "") or (not isinstance(file_name, str)):
            return

        if not file_name.endswith(".cinac"):
            file_name = file_name + ".cinac"

        # to get real index, remove 1
        self.save_path, self.save_file_name = get_file_name_and_path(file_name)

        if self.save_path is None:
            return

        self.save_segments(and_close=and_close)

    def get_threshold(self):
        trace = self.raw_traces[self.current_neuron, :]
        threshold = (self.nb_std_thresold * np.std(trace)) + np.min(self.raw_traces[self.current_neuron, :])
        # + abs(np.min(self.raw_traces[self.current_neuron, :]))
        return threshold

    def plot_magnifier(self, first_time=False, mouse_x_position=None, mouse_y_position=None):
        """
        Plot the magnifier
        :param first_time: if True, means the function is called for the first time,
        allow sto initialize some variables.
        :param mouse_x_position: indicate the x position of the mouse cursor
        :param mouse_y_position: indicate the y position of the mouse cursor
        :return: None
        """
        if first_time:
            self.axe_plot_magnifier = self.magnifier_fig.add_subplot(111)
            self.axe_plot_magnifier.get_xaxis().set_visible(False)
            self.axe_plot_magnifier.get_yaxis().set_visible(False)
            self.axe_plot_magnifier.set_facecolor(self.background_color)
            self.magnifier_fig.patch.set_facecolor(self.background_color)

        if self.x_center_magnified is not None:
            pos_beg_x = int(np.max((0, self.x_center_magnified - self.magnifier_range)))
            pos_end_x = int(np.min((self.nb_times, self.x_center_magnified + self.magnifier_range + 1)))

            max_value = np.max(self.raw_traces[self.current_neuron, pos_beg_x:pos_end_x])
            min_value = np.min(self.raw_traces[self.current_neuron, pos_beg_x:pos_end_x])

            nb_times_to_display = pos_end_x - pos_beg_x

            color_trace = self.color_trace

            self.axe_plot_magnifier.plot(np.arange(nb_times_to_display),
                                         self.raw_traces[self.current_neuron, pos_beg_x:pos_end_x],
                                         color=self.color_raw_trace, alpha=0.6, zorder=9)

            onsets = np.where(self.onset_times[self.current_neuron, pos_beg_x:pos_end_x] > 0)[0]
            # plotting onsets
            self.axe_plot_magnifier.vlines(onsets, min_value, max_value,
                                           color=self.color_onset, linewidth=1,
                                           linestyles="dashed")

            peaks = np.where(self.peak_nums[self.current_neuron, pos_beg_x:pos_end_x] > 0)[0]
            if len(peaks) > 0:
                reduced_traces = self.raw_traces[self.current_neuron, pos_beg_x:pos_end_x]
                y_peaks = reduced_traces[peaks]
                self.axe_plot_magnifier.scatter(peaks, y_peaks,
                                                marker='o', c=self.color_peak,
                                                edgecolors=self.color_edge_peak, s=30,
                                                zorder=10)
            self.draw_magnifier_marker(mouse_x_position=mouse_x_position, mouse_y_position=mouse_y_position)
            self.axe_plot_magnifier.set_ylim(min_value, max_value + 1)

        if self.x_center_magnified is None:
            main_plot_bottom_y, main_plot_top_y = self.axe_plot.get_ylim()
            self.axe_plot_magnifier.set_ylim(main_plot_bottom_y, main_plot_top_y)

        self.axe_plot_magnifier.spines['right'].set_visible(False)
        self.axe_plot_magnifier.spines['top'].set_visible(False)
        self.axe_plot_magnifier.spines['left'].set_visible(False)
        self.axe_plot_magnifier.spines['bottom'].set_visible(False)
        # if first_time:
        #     self.magnifier_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 0.2, 'h_pad': 0.2})
        self.magnifier_fig.tight_layout()

    def draw_magnifier_marker(self, mouse_x_position=None, mouse_y_position=None):
        if (mouse_x_position is None) or (mouse_y_position is None):
            return

        pos_beg_x = int(np.max((0, self.x_center_magnified - self.magnifier_range)))
        pos_end_x = int(np.min((self.nb_times, self.x_center_magnified + self.magnifier_range + 1)))

        max_value = np.max(self.raw_traces[self.current_neuron, pos_beg_x:pos_end_x])
        min_value = np.min(self.raw_traces[self.current_neuron, pos_beg_x:pos_end_x])

        corrected_mouse_y_position = np.min((mouse_y_position, max_value))

        corrected_mouse_x_position = None
        corrected_mouse_y_position = None

        corrected_mouse_x_position = mouse_x_position - pos_beg_x

        if self.magnifier_marker is not None:
            self.magnifier_marker.set_visible(False)

        if self.magnifier_line is not None:
            self.magnifier_line.set_visible(False)

        self.magnifier_marker = self.axe_plot_magnifier.scatter(corrected_mouse_x_position,
                                                                corrected_mouse_y_position,
                                                                marker='x',
                                                                c="#737373", s=20)
        self.magnifier_line = self.axe_plot_magnifier.vlines(corrected_mouse_x_position, min_value, max_value,
                                                             color="red",
                                                             linewidth=1,
                                                             linestyles=":")

    def corr_between_source_and_transient(self, cell, transient, pixels_around=1, redo_computation=False):
        """

        :param cell: int
        :param transient: (int, int) first_frame and last_frame
        :param pixels_around:
        :param redo_computation: if True, means that even if the correlation has been done before for the peak,
        it will be redo (useful if the onset has changed for exemple
        :return:
        """
        # if cell not in self.corr_source_transient:
        #     self.corr_source_transient[cell] = dict()
        #
        # elif transient in self.corr_source_transient[cell]:
        #     return self.corr_source_transient[cell][transient]

        if (redo_computation is False) and (self.peaks_correlation[cell, transient[1]] >= -1):
            return self.peaks_correlation[cell, transient[1]]

        poly_gon = self.data_and_param.coord_obj.cells_polygon[cell]

        # Correlation test
        bounds_corr = np.array(list(poly_gon.bounds)).astype(int)

        # looking if this source has been computed before
        if cell in self.source_profile_correlation_dict:
            source_profile_corr, mask_source_profile = self.source_profile_correlation_dict[cell]
        else:
            source_profile_corr, minx_corr, \
            miny_corr, mask_source_profile = self.get_source_profile(cell=cell,
                                                                     pixels_around=pixels_around,
                                                                     bounds=bounds_corr, buffer=1)
            # normalizing
            source_profile_corr = source_profile_corr - np.mean(source_profile_corr)
            # we want the mask to be at ones over the cell
            mask_source_profile = (1 - mask_source_profile).astype(bool)
            self.source_profile_correlation_dict[cell] = (source_profile_corr, mask_source_profile)

        transient_profile_corr, minx_corr, miny_corr = self.get_transient_profile(cell=cell,
                                                                                  transient=transient,
                                                                                  pixels_around=pixels_around,
                                                                                  bounds=bounds_corr)
        transient_profile_corr = transient_profile_corr - np.mean(transient_profile_corr)

        pearson_corr, pearson_p_value = stats.pearsonr(source_profile_corr[mask_source_profile],
                                                       transient_profile_corr[mask_source_profile])

        self.peaks_correlation[cell, transient[1]] = pearson_corr

        return pearson_corr

    def compute_source_and_transients_correlation(self, main_cell, redo_computation=False, with_overlapping_cells=True):
        """
        Compute the source and transient profiles of a given cell. Should be call for each new neuron displayed
        :param cell:
        :param redo_computation: if True, means that even if the correlation has been done before for this cell,
        it will be redo (useful if the onsets or peaks has changed for exemple)
        :return:
        """
        # the tiff_movie is necessary to compute the source and transient profile
        if self.tiff_movie is None:
            return

        cells = [main_cell]
        if with_overlapping_cells:
            overlapping_cells = self.overlapping_cells[self.current_neuron]
            cells += list(overlapping_cells)

        for cell in cells:
            peaks_frames = np.where(self.peak_nums[self.current_neuron, :] > 0)[0]
            if len(peaks_frames) == 0:
                return
            if redo_computation is False:
                # it means all peaks correlation are knoww
                if np.min(self.peaks_correlation[cell, peaks_frames]) > -2:
                    # means correlation has been computed before
                    continue

            # first computing the list of transients based on peaks and onsets preceeding the

            onsets_frames = np.where(self.onset_times[self.current_neuron, :] > 0)[0]
            for peak_frame in peaks_frames:
                onsets_before_peak = np.where(onsets_frames < peak_frame)[0]
                if len(onsets_before_peak) == 0:
                    continue
                first_onset_before_peak = onsets_frames[onsets_before_peak[-1]]
                transient = (first_onset_before_peak, peak_frame)
                # the correlation will be saved in the array  elf.peaks_correlation
                self.corr_between_source_and_transient(cell=cell, transient=transient)

    def plot_source_transient(self, transient):
        # transient is a tuple of int, reprensenting the frame of the onset and the frame of the peak
        # using the magnifier figure
        self.magnifier_fig.clear()
        plt.close(self.magnifier_fig)
        self.magnifier_canvas.get_tk_widget().destroy()
        if (self.screen_width < 2000) or (self.screen_height < 1200):
            self.magnifier_fig = plt.figure(figsize=(3, 3))
        else:
            self.magnifier_fig = plt.figure(figsize=(4, 4))
        self.magnifier_fig.patch.set_facecolor(self.background_color)
        self.magnifier_canvas = FigureCanvasTkAgg(self.magnifier_fig, self.magnifier_frame)
        # fig = plt.figure(figsize=size_fig)
        # self.magnifier_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 0.1, 'h_pad': 0.1})

        # looking at how many overlapping cell current_neuron has
        if self.current_neuron in self.overlapping_cells:
            intersect_cells = self.overlapping_cells[self.current_neuron]
        else:
            intersect_cells = []
        # print(f"len(intersect_cells) {len(intersect_cells)}")
        cells_color = dict()
        cells_color[self.current_neuron] = "red"
        cells_to_display = [self.current_neuron]
        for index, cell_inter in enumerate(intersect_cells):
            cells_color[cell_inter] = cm.nipy_spectral(float(index + 1) / (len(intersect_cells) + 1))

        cells_to_display.extend(intersect_cells)
        n_cells_to_display = len(cells_to_display)
        # now adding as many suplots as need, depending on how many overlap has the cell
        # TODO: to adapt depending on the resolution and the size of the main figure
        n_columns = 8
        width_ratios = [100 // n_columns] * n_columns
        n_lines = (((n_cells_to_display - 1) // n_columns) + 1) * 2
        height_ratios = [100 // n_lines] * n_lines
        grid_spec = gridspec.GridSpec(n_lines, n_columns, width_ratios=width_ratios,
                                      height_ratios=height_ratios,
                                      figure=self.magnifier_fig, hspace=0.025, wspace=0.05)

        # building the subplots to displays the sources and transients
        ax_source_profile_by_cell = dict()
        # ax_top_source_profile_by_cell = dict()
        ax_source_transient_by_cell = dict()
        for cell_index, cell_to_display in enumerate(cells_to_display):
            line_gs = (cell_index // n_columns) * 2
            col_gs = cell_index % n_columns
            ax_source_profile_by_cell[cell_to_display] = self.magnifier_fig.add_subplot(grid_spec[line_gs, col_gs])
            ax_source_profile_by_cell[cell_to_display].get_yaxis().set_visible(False)
            ax_source_profile_by_cell[cell_to_display].set_facecolor(self.background_color)
            # ax_top_source_profile_by_cell[cell_to_display] = ax_source_profile_by_cell[cell_to_display].twiny()
            for spine in ax_source_profile_by_cell[cell_to_display].spines.values():
                spine.set_edgecolor(cells_color[cell_to_display])
                spine.set_linewidth(2)
            ax_source_transient_by_cell[cell_to_display] = \
                self.magnifier_fig.add_subplot(grid_spec[line_gs + 1, col_gs])
            ax_source_transient_by_cell[cell_to_display].get_xaxis().set_visible(False)
            ax_source_transient_by_cell[cell_to_display].get_yaxis().set_visible(False)
            ax_source_transient_by_cell[cell_to_display].set_facecolor(self.background_color)
            for spine in ax_source_transient_by_cell[cell_to_display].spines.values():
                spine.set_edgecolor(cells_color[cell_to_display])
                spine.set_linewidth(2)

        # should be a np.array with x, y len equal
        source_profile_by_cell = dict()
        transient_profile_by_cell = dict()

        size_square = 40
        frame_tiff = self.tiff_movie[transient[-1]]
        len_x = frame_tiff.shape[1]
        len_y = frame_tiff.shape[0]
        # calculating the bound that will surround all the cells
        minx = None
        maxx = None
        miny = None
        maxy = None
        corr_by_cell = dict()
        for cell_to_display in cells_to_display:
            poly_gon = self.data_and_param.coord_obj.cells_polygon[cell_to_display]

            if minx is None:
                minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
            else:
                tmp_minx, tmp_miny, tmp_maxx, tmp_maxy = np.array(list(poly_gon.bounds)).astype(int)
                minx = min(minx, tmp_minx)
                miny = min(miny, tmp_miny)
                maxx = max(maxx, tmp_maxx)
                maxy = max(maxy, tmp_maxy)
        bounds = (minx, miny, maxx, maxy)
        # show the extents of all the cells that overlap with the main cell
        # print(f"maxx-minx {maxx-minx}, maxy-miny {maxy-miny}")

        for cell_index, cell_to_display in enumerate(cells_to_display):
            # self.x_beg_movie, self.x_end_movie, self.y_beg_movie, self.y_end_movie = \
            #     self.square_coord_around_cell(cell=cell_to_display, size_square=size_square,
            #                                   x_len_max=len_x, y_len_max=len_y)
            # tiff_array = frame_tiff[self.y_beg_movie:self.y_end_movie,
            #              self.x_beg_movie:self.x_end_movie]
            # ax_source_profile_by_cell[cell_to_display].imshow(tiff_array, cmap=plt.get_cmap('gray'))
            first_time = False
            if cell_to_display not in self.source_profile_dict:
                source_profile, minx, miny, mask_source_profile = self.get_source_profile(cell=cell_to_display,
                                                                                          pixels_around=3,
                                                                                          bounds=bounds)
                xy_source = self.get_cell_new_coord_in_source(cell=cell_to_display, minx=minx, miny=miny)
                self.source_profile_dict[cell_to_display] = [source_profile, minx, miny, mask_source_profile,
                                                             xy_source]
            else:
                source_profile, minx, miny, mask_source_profile, xy_source = \
                    self.source_profile_dict[cell_to_display]

            img_src_profile = ax_source_profile_by_cell[cell_to_display].imshow(source_profile,
                                                                                cmap=plt.get_cmap('gray'))
            with_mask = False
            if with_mask:
                source_profile[mask_source_profile] = 0
                img_src_profile.set_array(source_profile)

            lw = 1
            contour_cell = patches.Polygon(xy=xy_source,
                                           fill=False,
                                           edgecolor=cells_color[cell_to_display],
                                           zorder=15, lw=lw)
            ax_source_profile_by_cell[cell_to_display].add_patch(contour_cell)

            pearson_corr = self.corr_between_source_and_transient(cell=cell_to_display,
                                                                  transient=transient,
                                                                  pixels_around=1)

            pearson_corr = np.round(pearson_corr, 2)
            # ax_source_profile_by_cell[cell_to_display].text(x=3, y=3,
            #                                                 s=f"{cell_to_display}", color="blue", zorder=20,
            #                                                 ha='center', va="center", fontsize=7, fontweight='bold')
            # displaying correlation between source and transient profile
            min_x_axis, max_x_axis = ax_source_profile_by_cell[cell_to_display].get_xlim()
            ax_source_profile_by_cell[cell_to_display].set_xticks([max_x_axis / 2])
            # ax_source_profile_by_cell[cell_to_display].set_xticklabels([f"{pearson_corr} / {percentage_high_corr}%"])
            ax_source_profile_by_cell[cell_to_display].set_xticklabels([f"{cell_to_display} -> {pearson_corr}"])
            # if pearson_p_value < 0.05:
            #     label_color = "red"
            # else:
            #     label_color = "black"
            # padding between axis and xticks labels
            ax_source_profile_by_cell[cell_to_display].xaxis.set_tick_params(labelsize=8, pad=2,
                                                                             labelcolor="white")
            ax_source_profile_by_cell[cell_to_display].xaxis.set_ticks_position('none')
            # displaying cell number
            # min_x_axis, max_x_axis = ax_top_source_profile_by_cell[cell_to_display].get_xlim()
            # # ax_top_source_profile_by_cell[cell_to_display].set_xlim(left=min_x_axis, right=max_x_axis, auto=None)
            # ax_top_source_profile_by_cell[cell_to_display].set_xticks([max_x_axis / 2])
            # ax_top_source_profile_by_cell[cell_to_display].set_xticklabels([cell_to_display])
            # ax_top_source_profile_by_cell[cell_to_display].xaxis.set_tick_params(labelsize=8, pad=0.1,
            #                                                                  labelcolor=cells_color[cell_to_display])
            # ax_top_source_profile_by_cell[cell_to_display].xaxis.set_ticks_position('none')

            transient_profile, minx, miny = self.get_transient_profile(cell=cell_to_display, transient=transient,
                                                                       pixels_around=3, bounds=bounds)
            ax_source_transient_by_cell[cell_to_display].imshow(transient_profile, cmap=plt.get_cmap('gray'))
            for cell_to_contour in cells_to_display:
                # the new coordinates of the cell
                xy = self.get_cell_new_coord_in_source(cell=cell_to_contour, minx=minx, miny=miny)
                lw = 0.5
                if cell_to_display == cell_to_contour:
                    lw = 1
                contour_cell = patches.Polygon(xy=xy,
                                               fill=False,
                                               edgecolor=cells_color[cell_to_contour],
                                               zorder=15, lw=lw)
                ax_source_transient_by_cell[cell_to_display].add_patch(contour_cell)

        self.magnifier_canvas.draw()
        self.magnifier_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)

    def get_source_profile(self, cell, pixels_around=0, bounds=None, buffer=None, with_full_frame=False):
        """

        :param cell:
        :param pixels_around:
        :param bounds:
        :param buffer:
        :param with_full_frame:  Average the full frame
        :return:
        """
        # print("get_source_profile")
        len_frame_x = self.tiff_movie[0].shape[1]
        len_frame_y = self.tiff_movie[0].shape[0]

        # determining the size of the square surrounding the cell
        poly_gon = self.data_and_param.coord_obj.cells_polygon[cell]
        if bounds is None:
            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
        else:
            minx, miny, maxx, maxy = bounds

        if with_full_frame:
            minx = 0
            miny = 0
            maxx = len_frame_x - 1
            maxy = len_frame_y - 1
        else:
            minx = max(0, minx - pixels_around)
            miny = max(0, miny - pixels_around)
            maxx = min(len_frame_x - 1, maxx + pixels_around)
            maxy = min(len_frame_y - 1, maxy + pixels_around)

        len_x = maxx - minx + 1
        len_y = maxy - miny + 1

        # mask used in order to keep only the cells pixel
        # the mask put all pixels in the polygon, including the pixels on the exterior line to zero
        scaled_poly_gon = scale_polygon_to_source(polygon=poly_gon, minx=minx, miny=miny)
        img = PIL.Image.new('1', (len_x, len_y), 1)
        if buffer is not None:
            scaled_poly_gon = scaled_poly_gon.buffer(buffer)
        ImageDraw.Draw(img).polygon(list(scaled_poly_gon.exterior.coords), outline=0, fill=0)
        mask = np.array(img)
        # mask = np.ones((len_x, len_y))
        # cv2.fillPoly(mask, scaled_poly_gon, 0)
        # mask = mask.astype(bool)

        source_profile = np.zeros((len_y, len_x))

        # selectionning the best peak to produce the source_profile
        peaks = np.where(self.peak_nums[cell, :] > 0)[0]
        n_peaks_original = len(peaks)
        if len(peaks) <= 5:
            # if less than 5 peaks, then we measure the source profile on the potential peaks from automtic detection
            peaks = np.where(self.data_and_param.all_potential_peaks[cell, :] > 0)[0]
        threshold = np.percentile(self.raw_traces[cell, peaks], 95)
        selected_peaks = peaks[np.where(self.raw_traces[cell, peaks] > threshold)[0]]
        # max 10 peaks, min 5 peaks
        if len(selected_peaks) > 10:
            p = 10 / len(peaks)
            threshold = np.percentile(self.raw_traces[cell, peaks], (1 - p) * 100)
            selected_peaks = peaks[np.where(self.raw_traces[cell, peaks] > threshold)[0]]
        elif (len(selected_peaks) < 5) and (len(peaks) > 5):
            p = 5 / len(peaks)
            threshold = np.percentile(self.raw_traces[cell, peaks], (1 - p) * 100)
            selected_peaks = peaks[np.where(self.raw_traces[cell, peaks] > threshold)[0]]

        # print(f"threshold {threshold}")
        # print(f"n peaks: {len(selected_peaks)}")
        if n_peaks_original <= 5:
            onsets_frames = np.where(self.data_and_param.all_potential_onsets[cell, :] > 0)[0]
        else:
            onsets_frames = np.where(self.onset_times[cell, :] > 0)[0]

        raw_traces = np.copy(self.raw_traces)
        # so the lowest value is zero
        raw_traces += abs(np.min(raw_traces))

        for peak in selected_peaks:
            tmp_source_profile = np.zeros((len_y, len_x))
            onsets_before_peak = np.where(onsets_frames <= peak)[0]
            if len(onsets_before_peak) == 0:
                # shouldn't arrive
                continue
            onset = onsets_frames[onsets_before_peak[-1]]
            frames_tiff = self.tiff_movie[onset:peak + 1]
            for frame_index, frame_tiff in enumerate(frames_tiff):
                tmp_source_profile += (frame_tiff[miny:maxy + 1, minx:maxx + 1] * raw_traces[cell, onset + frame_index])
            # averaging
            tmp_source_profile = tmp_source_profile / (np.sum(raw_traces[cell, onset:peak + 1]))
            source_profile += tmp_source_profile

        source_profile = source_profile / len(selected_peaks)

        return source_profile, minx, miny, mask

    def get_transient_profile(self, cell, transient, pixels_around=0, bounds=None):
        len_frame_x = self.tiff_movie[0].shape[1]
        len_frame_y = self.tiff_movie[0].shape[0]

        # determining the size of the square surrounding the cell
        if bounds is None:
            poly_gon = self.data_and_param.coord_obj.cells_polygon[cell]
            minx, miny, maxx, maxy = np.array(list(poly_gon.bounds)).astype(int)
        else:
            minx, miny, maxx, maxy = bounds

        minx = max(0, minx - pixels_around)
        miny = max(0, miny - pixels_around)
        maxx = min(len_frame_x - 1, maxx + pixels_around)
        maxy = min(len_frame_y - 1, maxy + pixels_around)

        len_x = maxx - minx + 1
        len_y = maxy - miny + 1

        transient_profile = np.zeros((len_y, len_x))
        frames_tiff = self.tiff_movie[transient[0]:transient[-1] + 1]
        # now we do the weighted average
        raw_traces = np.copy(self.raw_traces)
        # so the lowest value is zero
        raw_traces += abs(np.min(raw_traces))

        for frame_index, frame_tiff in enumerate(frames_tiff):
            # print(f"frame_index {frame_index}")
            transient_profile += (
                    frame_tiff[miny:maxy + 1, minx:maxx + 1] * raw_traces[cell, transient[0] + frame_index])
        # averaging
        transient_profile = transient_profile / (np.sum(raw_traces[cell, transient[0]:transient[-1] + 1]))

        return transient_profile, minx, miny

    # def scale_polygon_to_source(self, poly_gon, minx, miny):
    #     coords = list(poly_gon.exterior.coords)
    #     scaled_coords = []
    #     for coord in coords:
    #         scaled_coords.append((coord[0] - minx, coord[1] - miny))
    #     # print(f"scaled_coords {scaled_coords}")
    #     return geometry.Polygon(scaled_coords)

    def get_cell_new_coord_in_source(self, cell, minx, miny):
        coord = self.data_and_param.coord_obj.coords[cell]
        # coord = coord - 1
        coord = coord.astype(int)
        n_coord = len(coord[0, :])
        xy = np.zeros((n_coord, 2))
        for n in np.arange(n_coord):
            # shifting the coordinates in the square size_square+1
            xy[n, 0] = coord[0, n] - minx
            xy[n, 1] = coord[1, n] - miny
        return xy

    def update_plot_magnifier(self, mouse_x_position, mouse_y_position, change_frame_ref):
        if change_frame_ref:
            self.magnifier_fig.clear()
            plt.close(self.magnifier_fig)
            self.magnifier_canvas.get_tk_widget().destroy()
            if (self.screen_width < 2000) or (self.screen_height < 1200):
                self.magnifier_fig = plt.figure(figsize=(3, 3))
            else:
                self.magnifier_fig = plt.figure(figsize=(4, 4))
            self.magnifier_canvas = FigureCanvasTkAgg(self.magnifier_fig, self.magnifier_frame)

            self.plot_magnifier(first_time=True, mouse_x_position=mouse_x_position,
                                mouse_y_position=mouse_y_position)

            self.magnifier_canvas.draw()
            self.magnifier_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)
            # self.axe_plot_magnifier.clear()
            # self.plot_magnifier(first_time=False, mouse_x_position=mouse_x_position,
            #                     mouse_y_position=mouse_y_position)
        else:
            self.draw_magnifier_marker(mouse_x_position=mouse_x_position, mouse_y_position=mouse_y_position)

            self.magnifier_fig.canvas.draw()
            self.magnifier_fig.canvas.flush_events()

    def start_playing_movie(self, x_from, x_to):
        self.play_movie = True
        self.first_frame_movie = min(x_from, x_to)
        self.last_frame_movie = max(x_to, x_from)
        self.n_frames_movie = np.abs(x_to - x_from)
        if self.n_frames_movie < 3:
            self.play_movie = False
            self.update_plot()
            return
        self.cell_contour_movie = None
        self.movie_frames = cycle((frame_tiff, frame_index + self.first_frame_movie)
                                  for frame_index, frame_tiff in
                                  enumerate(self.tiff_movie[self.first_frame_movie:self.last_frame_movie + 1]))

        self.update_plot_map_img()

    def square_coord_around_cell(self, cell, size_square, x_len_max, y_len_max):
        """
        For a given cell, give the coordinates of the square surrounding the cell.

        :param cell:
        :param size_square:
        :param x_len_max:
        :param y_len_max:
        :return: (x_beg, x_end, y_beg, y_end)
        """
        c_x, c_y = self.center_coord[cell]
        # c_y correspond to
        c_y = int(c_y)
        c_x = int(c_x)
        # print(f"len_x {len_x} len_y {len_y}")
        # print(f"c_x {c_x} c_y {c_y}")
        # limit of the new frame, should make a square
        x_beg_movie = max(0, c_x - (size_square // 2))
        x_end_movie = min(x_len_max - 1, c_x + (size_square // 2) + 1)
        # means the cell is near a border
        if (x_end_movie - x_beg_movie) < (size_square + 1):
            if (c_x - x_beg_movie) < (x_end_movie - c_x - 1):
                x_end_movie += ((size_square + 1) - (x_end_movie - x_beg_movie))
            else:
                x_beg_movie -= ((size_square + 1) - (x_end_movie - x_beg_movie))

        y_beg_movie = max(0, c_y - (size_square // 2))
        y_end_movie = min(y_len_max - 1, c_y + (size_square // 2) + 1)
        if (y_end_movie - y_beg_movie) < (size_square + 1):
            if (c_y - y_beg_movie) < (y_end_movie - c_y - 1):
                y_end_movie += ((size_square + 1) - (y_end_movie - y_beg_movie))
            else:
                y_beg_movie -= ((size_square + 1) - (y_end_movie - y_beg_movie))

        return x_beg_movie, x_end_movie, y_beg_movie, y_end_movie

    def animate_movie(self, i):
        zoom_mode = self.movie_zoom_mode
        # if self.current_neuron not in self.center_coord:
        #     zoom_mode = False
        if not self.play_movie:
            return []
        result = next(self.movie_frames, None)
        if result is None:
            return
        frame_tiff, frame_index = result
        # for zoom purpose
        len_x = frame_tiff.shape[1]
        len_y = frame_tiff.shape[0]
        if zoom_mode and ((i == -1) or (self.cell_contour_movie is None)):
            # zoom around the cell
            self.x_beg_movie, self.x_end_movie, self.y_beg_movie, self.y_end_movie = \
                self.square_coord_around_cell(cell=self.current_neuron, size_square=self.size_zoom_pixels,
                                              x_len_max=len_x, y_len_max=len_y)
            # used to change the coord of the polygon
            # x_shift = self.x_beg_movie - c_x
            # y_shift = self.y_beg_movie - c_y

            # cell contour
            coord = self.data_and_param.coord_obj.coords[self.current_neuron]
            # coord = coord - 1
            coord = coord.astype(int)
            n_coord = len(coord[0, :])
            xy = np.zeros((n_coord, 2))
            for n in np.arange(n_coord):
                # shifting the coordinates in the square size_square+1
                xy[n, 0] = coord[0, n] - self.x_beg_movie
                xy[n, 1] = coord[1, n] - self.y_beg_movie
                # then multiplying to fit it to the len of the original image
                xy[n, 0] = (xy[n, 0] * len_x) / (self.size_zoom_pixels + 1)
                xy[n, 1] = (xy[n, 1] * len_y) / (self.size_zoom_pixels + 1)
            self.cell_contour_movie = patches.Polygon(xy=xy,
                                                      fill=False, linewidth=0, facecolor="red",
                                                      edgecolor="red",
                                                      zorder=15, lw=0.6)

        # if zoom_mode:
        #     img_to_display = frame_tiff[self.y_beg_movie:self.y_end_movie,
        #                  self.x_beg_movie:self.x_end_movie]
        #
        #     # if we do imshow, then the size of the image will be the one of the square, with no zoom
        #     if i == -1:
        #         high_contrast = True
        #         if high_contrast:
        #             img = PIL.Image.new('1', img_to_display.shape, 1)
        #             xy_coords = self.cell_contour_movie.get_xy()
        #             xy_coords = [(xy_coords[pixel, 0], xy_coords[pixel, 1]) for pixel in np.arange(len(xy_coords))]
        #             ImageDraw.Draw(img).polygon(xy_coords, outline=0, fill=0)
        #             mask = np.array(img)
        #             max_value = np.max(img_to_display[mask])
        #             # max_value = np.mean(frame_tiff) + np.std(frame_tiff)*4
        #             self.last_img_displayed = self.axe_plot_map_img.imshow(frame_tiff,
        #                                                                    cmap=plt.get_cmap('gray'),
        #                                                                    vmax=max_value)
        #         else:
        #             self.last_img_displayed = self.axe_plot_map_img.imshow(frame_tiff,
        #                                                                    cmap=plt.get_cmap('gray'))
        #         self.last_img_displayed.set_array(img_to_display)
        #     else:
        #         self.last_img_displayed.set_array(img_to_display)
        # else:
        #     if i == -1:
        #         self.last_img_displayed = self.axe_plot_map_img.imshow(frame_tiff,
        #                                                                cmap=plt.get_cmap('gray'))
        #     else:
        #         self.last_img_displayed.set_array(frame_tiff)
        if zoom_mode:
            img_to_display = frame_tiff[self.y_beg_movie:self.y_end_movie,
                             self.x_beg_movie:self.x_end_movie]
        else:
            img_to_display = frame_tiff

        if i == -1:
            high_contrast = True
            if high_contrast:
                # img = PIL.Image.new('1', (img_to_display.shape[1], img_to_display.shape[0]), 0)
                # if zoom_mode:
                #     xy_coords = self.cell_contour_movie.get_xy()
                # else:
                #     xy_coords = self.cell_contour.get_xy()
                # xy_coords = [(xy_coords[pixel, 1], xy_coords[pixel, 0]) for pixel in np.arange(len(xy_coords))]
                # ImageDraw.Draw(img).polygon(xy_coords, outline=1, fill=1)
                # mask = np.array(img)
                # max_value = np.max(img_to_display[mask])
                max_value = np.max(img_to_display)
                # max_value = np.mean(frame_tiff) + np.std(frame_tiff)*4
                self.last_img_displayed = self.axe_plot_map_img.imshow(frame_tiff,
                                                                       cmap=plt.get_cmap('gray'),
                                                                       vmax=max_value)
            else:
                self.last_img_displayed = self.axe_plot_map_img.imshow(frame_tiff,
                                                                       cmap=plt.get_cmap('gray'))
            self.last_img_displayed.set_array(img_to_display)
        else:
            self.last_img_displayed.set_array(img_to_display)

        if self.last_frame_label is not None:
            self.last_frame_label.set_visible(False)

        x_text = max(1, int(frame_tiff.shape[1] // 10))
        y_text = max(1, int(frame_tiff.shape[0] // 20))
        self.last_frame_label = self.axe_plot_map_img.text(x=x_text, y=y_text,
                                                           s=f"{frame_index}", color="red", zorder=20,
                                                           ha='center', va="center", fontsize=10, fontweight='bold')
        if self.trace_movie_p1 is not None:
            self.trace_movie_p1[0].set_visible(False)
        if self.trace_movie_p2 is not None:
            self.trace_movie_p2[0].set_visible(False)

        first_frame = self.first_frame_movie
        last_frame = self.last_frame_movie

        if self.n_frames_movie > len_x:
            new_x_values = np.linspace(0, len_x - 1, self.n_frames_movie)
        else:
            new_x_values = np.arange(self.n_frames_movie) + ((len_x - self.n_frames_movie) / 2)

        # we want the fluorescence signal to stay inside the frame of the cell
        if zoom_mode and (self.current_neuron in self.traces_for_movie_with_zoom_dict):
            traces_to_display = self.traces_for_movie_with_zoom_dict[self.current_neuron]
        elif (not zoom_mode) and (self.current_neuron in self.traces_for_movie_dict):
            traces_to_display = self.traces_for_movie_dict[self.current_neuron]
        else:
            traces_to_display = self.raw_traces
            traces_to_display = traces_to_display[self.current_neuron]
            min_trace_value = np.min(traces_to_display)
            new_max_trace_value = int(frame_tiff.shape[0] // 1.5)
            # first we put the min to zero
            traces_to_display = traces_to_display - min_trace_value
            max_trace_value = np.max(traces_to_display)
            traces_to_display = (traces_to_display / max_trace_value) * new_max_trace_value
            # then flipup the fluorescence signal as imshow will do it when displayed
            traces_to_display = frame_tiff.shape[0] - traces_to_display - 1
            if zoom_mode:
                self.traces_for_movie_with_zoom_dict[self.current_neuron] = traces_to_display
            else:
                self.traces_for_movie_dict[self.current_neuron] = traces_to_display

        trace_lw = 1
        # 2 parts, one in red, the other in white
        if first_frame < frame_index:
            self.trace_movie_p1 = self.axe_plot_map_img.plot(new_x_values[:frame_index - first_frame],
                                                             traces_to_display[first_frame:frame_index],
                                                             color="red", alpha=1, zorder=10, lw=trace_lw)
        if last_frame > frame_index:
            self.trace_movie_p2 = self.axe_plot_map_img.plot(new_x_values[frame_index - first_frame:],
                                                             traces_to_display[frame_index:last_frame],
                                                             color="white", alpha=1, zorder=10, lw=trace_lw)
        self.draw_cell_contour()
        if zoom_mode:
            artists = [self.last_img_displayed, self.last_frame_label, self.cell_contour_movie]
        else:
            artists = [self.last_img_displayed, self.last_frame_label, self.cell_contour]
        if self.trace_movie_p1 is not None:
            artists.append(self.trace_movie_p1[0])
        if self.trace_movie_p2 is not None:
            artists.append(self.trace_movie_p2[0])
        return artists

    def plot_map_img(self, first_time=True, after_movie=False):
        if (self.data_and_param.avg_cell_map_img is None) and (not self.display_background_img):
            return

        # if first_time:
        if self.axe_plot_map_img is None:
            self.axe_plot_map_img = self.map_img_fig.add_subplot(111)
            self.axe_plot_map_img.set_facecolor(self.map_img_bg_color)
        # if self.last_img_displayed is not None:
        #     self.last_img_displayed.set_visible(False)

        if self.display_background_img:
            if len(self.background_imgs) > 0:
                if first_time:
                    self.last_img_displayed = self.axe_plot_map_img.imshow(
                        self.background_imgs[self.background_img_to_display])
                else:
                    self.last_img_displayed.set_array(self.background_imgs[self.background_img_to_display])
        else:
            if self.play_movie:
                if self.square_classifier_patch is not None:
                    self.square_classifier_patch.set_visible(False)
                if self.square_zoom_patch is not None:
                    self.square_zoom_patch.set_visible(False)
                self.animate_movie(i=-1)
                # # frame_tiff is numpy array of 2D
                # frame_tiff, frame_index = next(self.movie_frames)
                # self.last_img_displayed = self.axe_plot_map_img.imshow(frame_tiff, cmap=plt.get_cmap('gray'))
                # if self.last_frame_label is not None:
                #     self.last_frame_label.set_visible(False)
                # self.last_frame_label = self.axe_plot_map_img.text(x=10, y=10,
                #                                                    s=f"{frame_index}", color="red", zorder=20,
                #                                                    ha='center', va="center", fontsize=10,
                #                                                    fontweight='bold')
            else:
                if self.last_frame_label is not None:
                    self.last_frame_label.set_visible(False)
                    self.last_frame_label = None
                if first_time or after_movie:
                    # after that the size of the image will stay this one
                    self.last_img_displayed = self.axe_plot_map_img.imshow(self.data_and_param.avg_cell_map_img,
                                                                           cmap=plt.get_cmap('gray'))
                else:
                    self.last_img_displayed.set_array(self.data_and_param.avg_cell_map_img)
                self.last_img_displayed.set_zorder(1)
                # self.last_img_displayed.set_visible(True)
                self.draw_cell_contour()
                if self.display_classifier_frame_around_cell:
                    len_x = self.tiff_movie.shape[2]
                    len_y = self.tiff_movie.shape[1]
                    min_x, min_y = self.get_square_coord_around_cell(self.current_neuron,
                                                                     x_len_max=len_x, y_len_max=len_y,
                                                                     square_size=self.segment_window_in_pixels)
                    dimensions_movie = self.tiff_movie.shape[1:]
                    square_coords = list()
                    square_coords.append((min_x, min_y))
                    square_coords.append((min(min_x + self.segment_window_in_pixels - 1, dimensions_movie[0]), min_y))
                    square_coords.append((min(min_x + self.segment_window_in_pixels - 1, dimensions_movie[0]),
                                          min(dimensions_movie[1], min_y + self.segment_window_in_pixels - 1)))
                    square_coords.append((min_x, min(dimensions_movie[1], min_y + self.segment_window_in_pixels - 1)))

                    if self.square_classifier_patch is not None:
                        self.square_classifier_patch.set_visible(False)
                    self.square_classifier_patch = patches.Polygon(xy=square_coords,
                                                                   fill=False, linewidth=0, facecolor="red",
                                                                   edgecolor="red",
                                                                   zorder=15, lw=0.5)
                    self.square_classifier_patch.set_visible(True)
                    self.axe_plot_map_img.add_patch(self.square_classifier_patch)
                if self.display_zoom_frame_around_cell and self.movie_zoom_mode:
                    len_x = self.tiff_movie.shape[2]
                    len_y = self.tiff_movie.shape[1]
                    # zoom around the cell
                    x_beg, x_end, y_beg, y_end = \
                        self.square_coord_around_cell(cell=self.current_neuron, size_square=self.size_zoom_pixels,
                                                      x_len_max=len_x, y_len_max=len_y)
                    square_coords = list()
                    square_coords.append((x_beg, y_beg))
                    square_coords.append((x_beg, y_end))
                    square_coords.append((x_end, y_end))
                    square_coords.append((x_end, y_beg))

                    if self.square_zoom_patch is not None:
                        self.square_zoom_patch.set_visible(False)
                    self.square_zoom_patch = patches.Polygon(xy=square_coords,
                                                             fill=False, linewidth=0, facecolor="white",
                                                             linestyle="dashed",
                                                             edgecolor="white",
                                                             zorder=15, lw=0.5)
                    self.square_zoom_patch.set_visible(True)
                    self.axe_plot_map_img.add_patch(self.square_zoom_patch)

        if first_time:
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)

            self.map_img_fig.tight_layout()
            # self.map_img_fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 0.2, 'h_pad': 0.2})

    def draw_cell_contour(self):
        if self.cell_contour is not None:
            self.cell_contour.set_visible(False)
        if self.play_movie and (self.cell_contour_movie is not None) and self.movie_zoom_mode:
            self.axe_plot_map_img.add_patch(self.cell_contour_movie)
        else:
            self.cell_contour = self.cell_contours[self.current_neuron]
            self.cell_contour.set_visible(True)
            self.axe_plot_map_img.add_patch(self.cell_contour)

    def update_plot_map_img(self, after_michou=False, after_movie=False):
        if self.display_background_img and (not self.play_movie):
            self.axe_plot_map_img.clear()
            self.plot_map_img()
        elif self.play_movie:
            # self.axe_plot_map_img.clear()
            self.plot_map_img()
            self.map_img_fig.canvas.draw()
            self.map_img_fig.canvas.flush_events()
            self.anim_movie = animation.FuncAnimation(self.map_img_fig, func=self.animate_movie,
                                                      frames=self.n_frames_movie,
                                                      blit=True, interval=100, repeat=True)  # repeat=True,
            return
            # self.after(self.movie_delay, self.update_plot_map_img)
        else:
            if after_michou or after_movie or self.display_zoom_frame_around_cell or \
                    self.display_classifier_frame_around_cell:
                self.axe_plot_map_img.clear()
                self.plot_map_img(after_movie=after_movie)
            else:
                self.draw_cell_contour()

        self.map_img_fig.canvas.draw()
        self.map_img_fig.canvas.flush_events()

    def plot_graph(self, first_time=False):
        """

        :param first_time:
        :return:
        """

        if first_time:
            gs_index = 0
            self.axe_plot = self.fig.add_subplot(self.gs[gs_index])
            gs_index += 1

        if self.cells_to_remove[self.current_neuron] == 1:
            self.axe_plot.set_facecolor("gray")
        else:
            self.axe_plot.set_facecolor(self.background_color)

        traces_to_plot = []
        color_traces = []
        for trace_str in self.actual_traces_str:
            traces_to_plot.append(self.traces_dict[trace_str])
            color_traces.append(self.traces_color_dict[trace_str])
        # #################### TRANSIENT CLASSIFIER VALUES ####################

        if self.show_transient_classifier:
            if self.current_neuron in self.transient_prediction:
                # TODO: work on the shape of predictions, should be (n_celles, n_class)
                predictions = self.transient_prediction[self.current_neuron]
                # print(f"predictions > 1: {predictions[predictions > 1]}")
                if len(predictions.shape) == 1:
                    pass
                if (len(predictions.shape) == 1) or predictions.shape[1] == 1:
                    predictions_color = "red"
                else:
                    predictions_color = "dimgrey"
                if len(predictions.shape) == 1:
                    self.axe_plot.plot(np.arange(self.nb_times_traces),
                                       predictions / 2,
                                       color=predictions_color, zorder=20)
                else:
                    for index_pred in np.arange(predictions.shape[1]):
                        self.axe_plot.plot(np.arange(self.nb_times_traces),
                                           (predictions[:, index_pred] / 2) - (0.75 * index_pred),
                                           color=predictions_color, zorder=20)
                # displaying prediction improvement if available
                if self.prediction_improvement_mode and self.current_neuron in self.prediction_improvement_dict:
                    improvement_values = self.prediction_improvement_dict[self.current_neuron]
                    self.axe_plot.plot(np.arange(self.nb_times_traces),
                                       improvement_values / 2, linewidth=1.2,
                                       color="black", linestyle="dashed", zorder=21, alpha=0.7)

                threshold_tc = self.transient_classifier_threshold
                self.axe_plot.hlines(threshold_tc / 2, 0, self.nb_times_traces - 1, color="red",
                                     linewidth=0.5,
                                     linestyles="dashed")
                self.axe_plot.hlines(1 / 2, 0, self.nb_times_traces - 1, color="red",
                                     linewidth=0.5)
                if threshold_tc not in self.transient_prediction_periods[self.current_neuron]:
                    if len(predictions.shape) == 1:
                        predicted_raster_dur = np.zeros(len(predictions), dtype="int8")
                    else:
                        predicted_raster_dur = np.zeros(predictions.shape[0], dtype="int8")

                    if len(predictions.shape) == 1:
                        real_transient_frames = predictions >= threshold_tc
                    elif predictions.shape[1] == 1:
                        real_transient_frames = predictions[:, 0] >= threshold_tc
                    elif predictions.shape[1] == 3:
                        # real transient, fake ones, other (neuropil, decay etc...)
                        # keeping predictions about real transient when superior
                        # to other prediction on the same frame
                        max_pred_by_frame = np.max(predictions, axis=1)
                        real_transient_frames = (predictions[:, 0] == max_pred_by_frame)
                        for class_index in np.arange(predictions.shape[1]):
                            frames_index = (predictions[:, class_index] == max_pred_by_frame)
                            tmp_raster_dur = np.zeros(predictions.shape[0], dtype="int8")
                            tmp_raster_dur[frames_index] = 1
                            periods = get_continous_time_periods(tmp_raster_dur)
                            for period in periods:
                                frames = np.arange(period[0], period[1] + 1)
                                self.axe_plot.plot(frames,
                                                   (predictions[frames, class_index] / 2) -
                                                   (0.75 * class_index), lw=2,
                                                   color="red", zorder=21)
                    elif predictions.shape[1] == 2:
                        # real transient, fake ones
                        # keeping predictions about real transient superior to the threshold
                        # and superior to other prediction on the same frame
                        max_pred_by_frame = np.max(predictions, axis=1)
                        real_transient_frames = np.logical_and((predictions[:, 0] >= threshold_tc),
                                                               (predictions[:, 0] == max_pred_by_frame))
                    predicted_raster_dur[real_transient_frames] = 1
                    active_periods = get_continous_time_periods(predicted_raster_dur)
                    self.transient_prediction_periods[self.current_neuron][threshold_tc] = active_periods
                else:
                    active_periods = self.transient_prediction_periods[self.current_neuron][threshold_tc]
                    if (len(predictions.shape) > 1) and (predictions.shape[1] == 3):
                        # real transient, fake ones, other (neuropil, decay etc...)
                        # keeping predictions about real transient when superior
                        # to other prediction on the same frame
                        max_pred_by_frame = np.max(predictions, axis=1)
                        real_transient_frames = (predictions[:, 0] == max_pred_by_frame)
                        for class_index in np.arange(predictions.shape[1]):
                            frames_index = (predictions[:, class_index] == max_pred_by_frame)
                            tmp_raster_dur = np.zeros(predictions.shape[0], dtype="int8")
                            tmp_raster_dur[frames_index] = 1
                            periods = get_continous_time_periods(tmp_raster_dur)
                            for period in periods:
                                frames = np.arange(period[0], period[1] + 1)
                                self.axe_plot.plot(frames,
                                                   (predictions[frames, class_index] / 2) -
                                                   (0.75 * class_index), lw=2,
                                                   color="red", zorder=21)

                for i_ap, active_period in enumerate(active_periods):
                    period = np.arange(active_period[0], active_period[1] + 1)
                    # using the first trace
                    min_traces = np.min(traces_to_plot[0][self.current_neuron, period])  # - 0.1
                    y2 = np.repeat(min_traces, len(period))
                    self.axe_plot.fill_between(x=period, y1=traces_to_plot[0][self.current_neuron, period], y2=y2,
                                               color=self.classifier_filling_color)

        for trace_index, trace in enumerate(traces_to_plot):
            self.axe_plot.plot(np.arange(self.nb_times_traces),
                               trace[self.current_neuron, :],
                               color=color_traces[trace_index], alpha=0.8, zorder=9)

        # #################### MIN & MAX VALUE ####################

        max_value = np.max(traces_to_plot[0][self.current_neuron, :])
        min_value = np.min(traces_to_plot[0][self.current_neuron, :])
        if len(traces_to_plot) > 1:
            for trace in traces_to_plot[1:]:
                max_value = max(max_value, np.max(trace[self.current_neuron, :]))
                min_value = min(min_value, np.min(trace[self.current_neuron, :]))

        # we substract 0.5 for each raster we have to display
        if self.other_rasters is not None:
            to_substract = 0.5 * len(self.other_rasters)
            min_value -= to_substract

        # #################### transient predicted to look at ###########
        # used when we want to look at some specific predicted transients
        if (self.last_predicted_transient_selected is not None) and \
                (self.last_predicted_transient_selected[0] == self.current_neuron):
            self.axe_plot.vlines(self.last_predicted_transient_selected[1], min_value, max_value,
                                 color=self.color_transient_predicted_to_look_at, linewidth=1)

        # #################### ONSETS ####################

        onsets = np.where(self.onset_times[self.current_neuron, :] > 0)[0]
        self.axe_plot.vlines(onsets, min_value, max_value, color=self.color_onset, linewidth=1,
                             linestyles="dashed")

        # #################### TO AGREE ONSETS ####################

        if self.to_agree_spike_nums is not None:
            to_agree_onsets = np.where(self.to_agree_spike_nums[self.current_neuron, :])[0]
            self.axe_plot.vlines(to_agree_onsets, min_value, max_value, color="red",
                                 linewidth=self.to_agree_spike_nums[self.current_neuron, to_agree_onsets],
                                 linestyles="dashed")

        # #################### DOUBTFUL FRAMES ####################

        if (self.current_neuron in self.doubtful_frames_periods) and \
                (len(self.doubtful_frames_periods[self.current_neuron]) > 0):
            for doubtful_frames_period in self.doubtful_frames_periods[self.current_neuron]:
                self.axe_plot.axvspan(doubtful_frames_period[0], doubtful_frames_period[1], ymax=1,
                                      alpha=0.5, facecolor="red", zorder=15)

        # #################### Inferred neuronal activity from other sources ####################

        # if self.caiman_spike_nums is not None:
        #     self.axe_plot.vlines(np.where(self.caiman_spike_nums[self.current_neuron])[0],
        #                          min_value, min_value + 0.5,
        #                          color="green", linewidth=2, zorder=7)

        if (self.other_rasters is not None) and len(self.other_rasters) > 0:
            for raster_index, raster in enumerate(self.other_rasters):
                other_color_raster = self.other_rasters_colors[raster_index % len(self.other_rasters_colors)]
                if len(np.unique(raster)) > 2:
                    # value are ranging from 0 to 1, so we multiply by 0.5
                    self.axe_plot.plot(np.arange(self.nb_times_traces),
                                       (min_value + (0.5 * raster_index)) + (raster[self.current_neuron, :]*0.5),
                                       color=other_color_raster,
                                       alpha=0.8, zorder=7)
                    self.axe_plot.fill_between(x=np.arange(self.nb_times_traces),
                                               y1=(min_value + (0.5 * raster_index)) + (raster[self.current_neuron, :]*0.5),
                                               y2=[(min_value + (0.5 * raster_index))]*self.nb_times_traces,
                                               color=other_color_raster)
                else:
                    self.axe_plot.vlines(np.where(raster[self.current_neuron])[0],
                                         min_value + (0.5 * raster_index), min_value + (0.5 * (raster_index + 1)),
                                         color=other_color_raster,
                                         linewidth=2, zorder=7)

        # #################### PEAKS ####################

        size_peak_scatter = 50
        peaks = np.where(self.peak_nums[self.current_neuron, :] > 0)[0]
        for trace in traces_to_plot:
            if self.display_threshold:
                threshold = self.get_threshold()
                peaks_under_threshold = np.where(trace[self.current_neuron, peaks] < threshold)[0]
                if len(peaks_under_threshold) == 0:
                    peaks_under_threshold_index = []
                    peaks_under_threshold_value_raw = []
                    self.peaks_under_threshold_index = []
                else:
                    peaks_under_threshold_index = peaks[peaks_under_threshold]
                    self.peaks_under_threshold_index = peaks_under_threshold_index
                    # to display the peaks on the raw trace as well
                    peaks_under_threshold_value_raw = trace[self.current_neuron, peaks][peaks_under_threshold]
                peaks_over_threshold = np.where(trace[self.current_neuron, peaks] >= threshold)[0]
                if len(peaks_over_threshold) == 0:
                    peaks_over_threshold_index = []
                else:
                    peaks_over_threshold_index = peaks[peaks_over_threshold]
                    peaks_over_threshold_value_raw = trace[self.current_neuron, peaks][peaks_over_threshold]

                # plotting peaks
                # z_order=10 indicate that the scatter will be on top
                if len(peaks_over_threshold_index) > 0:
                    # on raw_trace
                    self.ax1_bottom_scatter = self.axe_plot.scatter(peaks_over_threshold_index,
                                                                    peaks_over_threshold_value_raw,
                                                                    marker='o', c=self.color_peak,
                                                                    edgecolors=self.color_edge_peak, s=30, zorder=10)
                if len(peaks_over_threshold_index) > 0:
                    # on raw_trace
                    self.ax1_bottom_scatter = self.axe_plot.scatter(peaks_under_threshold_index,
                                                                    peaks_under_threshold_value_raw,
                                                                    marker='o', c=self.color_peak_under_threshold,
                                                                    edgecolors=self.color_edge_peak, s=30, zorder=10)

                self.axe_plot.hlines(threshold, 0, self.nb_times_traces - 1, color=self.color_threshold_line, linewidth=1,
                                     linestyles="dashed")
            elif self.display_correlations:
                if self.correlation_for_each_peak_option and (self.peaks_correlation is not None):
                    color_over_threshold = self.color_peak
                    color_under_threshold = self.color_peak_under_threshold
                    color_undetermined = "cornflowerblue"
                    threshold = self.correlation_thresold

                    peaks_over_threshold = np.where(self.peaks_correlation[self.current_neuron, peaks] >= threshold)[0]
                    peaks_over_threshold_index = peaks[peaks_over_threshold]
                    if len(peaks_over_threshold_index) == 0:
                        peaks_over_threshold_value_raw = []
                    else:
                        peaks_over_threshold_value_raw = trace[self.current_neuron, peaks_over_threshold_index]

                    # among peaks under treshold we need to find the ones with not overlaping cell over the tresholds
                    # using self.peaks_correlation and the self.overlaping_cells dict
                    peaks_left = np.where(self.peaks_correlation[self.current_neuron, peaks] < threshold)[0]
                    peaks_left_index = peaks[peaks_left]

                    overlapping_cells = self.overlapping_cells[self.current_neuron]
                    if len(overlapping_cells) == 0:
                        peaks_under_threshold_index = peaks_left_index
                        peaks_under_threshold_value_raw = trace[self.current_neuron, peaks_under_threshold_index]
                        peaks_undetermined_index = []
                        peaks_undetermined_value_raw = []
                    else:
                        overlapping_cells = np.array(list(overlapping_cells))
                        peaks_under_threshold_index = []
                        peaks_undetermined_index = []
                        # print(f"overlapping_cells {overlapping_cells}, peaks_left_index {peaks_left_index}")
                        for peak in peaks_left_index:
                            cells_over_threshold = np.where(self.peaks_correlation[overlapping_cells, peak] >= threshold)[0]
                            if len(cells_over_threshold) > 0:
                                # means at least an overlapping cell is correlated to its source for this peak transient
                                peaks_under_threshold_index.append(peak)
                            else:
                                # means the peak is not due to an overlapping cell, movement might have happened
                                peaks_undetermined_index.append(peak)
                        peaks_under_threshold_index = np.array(peaks_under_threshold_index)
                        if len(peaks_under_threshold_index) == 0:
                            peaks_under_threshold_value_raw = []
                        else:
                            peaks_under_threshold_value_raw = trace[
                                self.current_neuron, peaks_under_threshold_index]
                        peaks_undetermined_index = np.array(peaks_undetermined_index)
                        if len(peaks_undetermined_index) == 0:
                            peaks_undetermined_value_raw = []
                        else:
                            peaks_undetermined_value_raw = trace[self.current_neuron, peaks_undetermined_index]
                    # use to remove them
                    self.peaks_under_threshold_index = peaks_under_threshold_index

                    if len(peaks_over_threshold_index) > 0:
                        self.ax1_bottom_scatter = self.axe_plot.scatter(peaks_over_threshold_index,
                                                                        peaks_over_threshold_value_raw,
                                                                        marker='o', c=color_over_threshold,
                                                                        edgecolors=self.color_edge_peak,
                                                                        s=size_peak_scatter, zorder=10)

                    if len(peaks_under_threshold_index) > 0:
                        self.ax1_bottom_scatter = self.axe_plot.scatter(peaks_under_threshold_index,
                                                                        peaks_under_threshold_value_raw,
                                                                        marker='o', c=color_under_threshold,
                                                                        edgecolors=self.color_edge_peak,
                                                                        s=size_peak_scatter, zorder=10)
                    if len(peaks_undetermined_index) > 0:
                        self.ax1_bottom_scatter = self.axe_plot.scatter(peaks_undetermined_index,
                                                                        peaks_undetermined_value_raw,
                                                                        marker='o', c=color_undetermined,
                                                                        edgecolors=self.color_edge_peak,
                                                                        s=size_peak_scatter, zorder=10)

            else:
                # plotting peaks
                # z_order=10 indicate that the scatter will be on top
                self.ax1_bottom_scatter = self.axe_plot.scatter(peaks, trace[self.current_neuron, peaks],
                                                                marker='o', c=self.color_peak,
                                                                edgecolors=self.color_edge_peak, s=30, zorder=10)

        # #################### TO AGREE PEAKS ####################

        if self.to_agree_peak_nums is not None:
            to_agree_peaks = np.where(self.to_agree_peak_nums[self.current_neuron, :])[0]
            peaks_amplitude = traces_to_plot[0][self.current_neuron, to_agree_peaks]
            self.ax1_bottom_scatter = self.axe_plot.scatter(to_agree_peaks,
                                                            peaks_amplitude,
                                                            linewidths=self.to_agree_peak_nums[self.current_neuron,
                                                                                               to_agree_peaks],
                                                            marker='o', c="black",
                                                            edgecolors="red",
                                                            s=size_peak_scatter * 1.2, zorder=10)

        # #################### CLICK SCATTER ####################

        if self.first_click_to_remove is not None:
            self.axe_plot.scatter(self.first_click_to_remove["x"], self.first_click_to_remove["y"], marker='x',
                                  c=self.color_mark_to_remove, s=30)
        if self.click_corr_coord:
            self.axe_plot.scatter(self.click_corr_coord["x"], self.click_corr_coord["y"], marker='x',
                                  c="red", s=30)
        if self.center_segment_coord is not None:
            self.axe_plot.scatter(self.center_segment_coord[0], self.center_segment_coord[1], marker='x',
                                  c="cornflowerblue", s=30)

        if (self.mvt_frames_periods is not None) and self.display_mvt:
            for mvt_frames_period in self.mvt_frames_periods:
                # print(f"mvt_frames_period[0], mvt_frames_period[1] {mvt_frames_period[0]} {mvt_frames_period[1]}")
                self.axe_plot.axvspan(mvt_frames_period[0], mvt_frames_period[1], ymax=1,
                                      alpha=0.8, facecolor="red", zorder=1)

        self.axe_plot.set_ylim(min_value,
                               math.ceil(max_value))

        # removing first x_axis
        axes_to_clean = [self.axe_plot]
        for ax in axes_to_clean:
            # ax.axes.get_xaxis().set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
        self.axe_plot.yaxis.label.set_color("white")
        self.axe_plot.tick_params(axis='y', colors="white")
        self.axe_plot.xaxis.label.set_color("white")
        self.axe_plot.tick_params(axis='x', colors="white")
        self.axe_plot.margins(0)
        self.fig.tight_layout()
        # tight_layout is posing issue on Ubuntu
        # self.fig.set_tight_layout({'rect': [0, 0, 1, 1], 'pad': 0.1, 'h_pad': 0.1})

    def current_max_amplitude(self):
        """
        Ceiling value
        :return:
        """
        return math.ceil(np.max(self.raw_traces[self.current_neuron, :]))

    def move_zoom(self, to_the_left):
        # the plot is zoom out to the max, so no moving
        left_x_limit_1, right_x_limit_1 = self.axe_plot.get_xlim()
        # print(f"left_x_limit_1 {left_x_limit_1}, right_x_limit_1 {right_x_limit_1}, "
        #       f"self.nb_times_traces {self.nb_times_traces}")
        if (left_x_limit_1 <= 0) and (right_x_limit_1 >= (self.nb_times_traces - 1)):
            return

        # moving the windown to the right direction keeping 10% of the window in the new one
        length_window = right_x_limit_1 - left_x_limit_1
        if to_the_left:
            if left_x_limit_1 <= 0:
                return
            new_right_x_limit = int(left_x_limit_1 + (0.1 * length_window))
            new_left_x_limit = new_right_x_limit - length_window
            new_left_x_limit = int(max(new_left_x_limit, 0))
            if new_right_x_limit <= new_left_x_limit:
                return
        else:
            if right_x_limit_1 >= (self.nb_times_traces - 1):
                return
            new_left_x_limit = int(right_x_limit_1 - (0.1 * length_window))
            new_right_x_limit = new_left_x_limit + length_window
            new_right_x_limit = int(min(new_right_x_limit, self.nb_times_traces - 1))
            if new_left_x_limit >= new_right_x_limit:
                return

        new_top_y_limit = np.max(self.raw_traces[self.current_neuron, new_left_x_limit:new_right_x_limit + 1]) + 0.5
        new_bottom_y_limit = np.min(self.raw_traces[self.current_neuron,
                                    new_left_x_limit:new_right_x_limit + 1]) - 0.5

        new_x_limit = (new_left_x_limit, new_right_x_limit)
        new_y_limit = (new_bottom_y_limit, new_top_y_limit)

        self.update_plot(new_x_limit=new_x_limit, new_y_limit=new_y_limit, amplitude_zoom_fit=False)

    def add_them_all(self):
        """
        Add all possible onset and peaks based on change of derivative in the smooth trace
        Returns:

        """
        left_x_limit, right_x_limit = self.axe_plot.get_xlim()
        first_frame = int(left_x_limit)
        last_frame = int(right_x_limit)

        # we want to get all onset and peaks on this window based on the smooth fluorescence signal (self.smooth_traces)
        old_peak_values = np.copy(self.peak_nums[self.current_neuron, first_frame:last_frame + 1])
        self.peak_nums[self.current_neuron, first_frame:last_frame + 1] = 0
        # TODO: Only use onset_times or spike_nums and not both
        old_onset_values = np.copy(self.onset_times[self.current_neuron, first_frame:last_frame + 1])
        self.onset_times[self.current_neuron, first_frame:last_frame + 1] = 0
        self.spike_nums[self.current_neuron, first_frame:last_frame + 1] = 0

        smooth_traces = self.smooth_traces[self.current_neuron, first_frame:last_frame + 1]
        n_frames = last_frame - first_frame + 1
        # computing all potential peaks and onset from smooth_trace
        all_potential_peaks = np.zeros(n_frames, dtype="int8")
        all_potential_onsets = np.zeros(n_frames, dtype="int8")
        # then we do an automatic detection
        peaks, properties = signal.find_peaks(x=smooth_traces, distance=2)
        all_potential_peaks[peaks] = 1

        onsets = []
        diff_values = np.diff(smooth_traces)
        for index, value in enumerate(diff_values):
            if index == (len(diff_values) - 1):
                continue
            if value < 0:
                if diff_values[index + 1] >= 0:
                    onsets.append(index + 1)
        all_potential_onsets[np.array(onsets)] = 1

        self.peak_nums[self.current_neuron, first_frame:last_frame + 1] = all_potential_peaks
        self.onset_times[self.current_neuron, first_frame:last_frame + 1] = all_potential_onsets
        self.spike_nums[self.current_neuron, first_frame:last_frame + 1] = all_potential_onsets

        bottom_limit, top_limit = self.axe_plot.get_ylim()
        self.update_last_action(AddThemAllAction(first_frame=first_frame, last_frame=last_frame,
                                                 old_peak_values=old_peak_values,
                                                 new_peak_values=all_potential_peaks,
                                                 old_onset_values=old_onset_values,
                                                 new_onset_values=all_potential_onsets,
                                                 session_frame=self,
                                                 neuron=self.current_neuron, is_saved=self.is_saved,
                                                 x_limits=(left_x_limit, right_x_limit),
                                                 y_limits=(bottom_limit, top_limit)))

        self.update_after_onset_change()

    def update_plot(self, new_neuron=False, amplitude_zoom_fit=True,
                    new_x_limit=None, new_y_limit=None, changing_face_color=False,
                    new_trace=False,
                    raw_trace_display_action=False):
        """

        Args:
            new_neuron:
            amplitude_zoom_fit:
            new_x_limit:
            new_y_limit:
            changing_face_color:
            new_trace: if True, means the trace has changed, and so we want to adapt the y-axis limit
            raw_trace_display_action:

        Returns:

        """
        # used to keep the same zoom after updating the plot
        # if we change neuron, then back to no zoom mode
        left_x_limit_1, right_x_limit_1 = self.axe_plot.get_xlim()
        bottom_limit_1, top_limit_1 = self.axe_plot.get_ylim()
        self.axe_plot.clear()

        self.plot_graph()

        # to keep the same zoom
        if not new_neuron:
            self.axe_plot.set_xlim(left=left_x_limit_1, right=right_x_limit_1, auto=None)
            if new_trace:
                left_x = max(0, math.floor(left_x_limit_1))
                right_x = min(self.n_frames-1, math.ceil(right_x_limit_1))
                traces_to_plot = [self.traces_dict[trace_str] for trace_str in self.actual_traces_str]
                bottom_limit = math.floor(np.min(traces_to_plot[0][self.current_neuron, left_x:right_x+1]))
                top_limit = math.ceil(np.max(traces_to_plot[0][self.current_neuron, left_x:right_x+1]))
                if len(traces_to_plot) > 1:
                    for trace in traces_to_plot[1:]:
                        bottom_limit = min(bottom_limit,
                                           math.floor(np.min(trace[self.current_neuron, left_x:right_x+1])))
                        top_limit = max(top_limit,
                                        math.ceil(np.max(trace[self.current_neuron, left_x:right_x+1])))
                self.axe_plot.set_ylim(bottom=bottom_limit, top=top_limit, auto=None)
                pass
            else:
                self.axe_plot.set_ylim(bottom=bottom_limit_1, top=top_limit_1, auto=None)
        if new_x_limit is not None:
            self.axe_plot.set_xlim(left=new_x_limit[0], right=new_x_limit[1], auto=None)
        if (new_y_limit is not None) and (not amplitude_zoom_fit):
            self.axe_plot.set_ylim(new_y_limit[0], new_y_limit[1])
        if new_neuron or changing_face_color:
            self.plot_canvas.draw()
            self.plot_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)
        else:
            self.fig.canvas.draw()
            # self.fig.canvas.flush_events()

    # def spin_box_update(self):
    #     content = int(self.spin_box_button.get())
    #     if content != self.current_neuron:
    #         self.current_neuron = content
    #         self.update_plot()

    def update_to_agree_label(self):
        if self.to_agree_label is not None:
            self.to_agree_label["text"] = f"{self.numbers_of_onset_to_agree()}/{self.numbers_of_peak_to_agree()}"

    # if an onset has been removed or added to smooth_traces and spike_nums for current_neuron
    def update_after_onset_change(self, new_neuron=-1,
                                  new_x_limit=None, new_y_limit=None):
        """
        Update the frame if an onset change has been made
        :param new_neuron: if -1, then the neuron hasn't changed, neuron might change if undo or redo are done.
        :return:
        """
        if new_neuron > -1:
            self.current_neuron = new_neuron
        self.onset_numbers_label["text"] = f" {self.numbers_of_onset()} "
        self.peak_numbers_label["text"] = f" {self.numbers_of_peak()} "
        if new_neuron > -1:
            self.update_neuron(new_neuron=new_neuron,
                               new_x_limit=new_x_limit, new_y_limit=new_y_limit)
        else:
            self.update_plot(new_x_limit=new_x_limit, new_y_limit=new_y_limit)

    def select_previous_neuron(self):
        if self.current_neuron == 0:
            return

        if (self.current_neuron - 1) == 0:
            self.prev_button['state'] = DISABLED

        self.update_neuron(new_neuron=(self.current_neuron - 1))

        self.next_button['state'] = 'normal'

        # self.spin_box_button.invoke("buttondown")

    def select_next_neuron(self):
        if self.current_neuron == (self.nb_neurons - 1):
            return
        self.prev_button['state'] = 'normal'
        if (self.current_neuron + 1) == (self.nb_neurons - 1):
            self.next_button['state'] = DISABLED
        self.update_neuron(new_neuron=(self.current_neuron + 1))

    def go_to_next_cell_with_same_type(self):
        """
        If cell typeis know, allows to display the next cell from the cell type as the cell actualy displayed
        Returns:

        """
        if not self.display_cell_type_classifier_field:
            return

        if self.current_neuron == (self.nb_neurons - 1):
            return

        if self.current_neuron not in self.cell_type_classifier_predictions:
            return

        # self.cell_type_classifier_predictions
        #  # dict with key being the cell id, and value being a dict with key the cell_type and value the prediction
        cell_type_dict = self.cell_type_classifier_predictions[self.current_neuron]
        max_prob = 0
        actual_cell_type = None
        for cell_type, prob in cell_type_dict.items():
            if prob > max_prob:
                max_prob = prob
                actual_cell_type = cell_type
        if actual_cell_type is None:
            return

        for cell in np.arange(self.current_neuron+1, self.nb_neurons):
            max_prob = 0
            next_cell_type = None
            cell_type_dict = self.cell_type_classifier_predictions[cell]
            for cell_type, prob in cell_type_dict.items():
                if prob > max_prob:
                    max_prob = prob
                    next_cell_type = cell_type
            if (next_cell_type is None) or (next_cell_type != actual_cell_type):
                continue

            self.update_neuron(new_neuron=cell)
            return

    def update_neuron(self, new_neuron,
                      new_x_limit=None, new_y_limit=None, amplitude_zoom_fit=True):
        """
        Call when the neuron number has changed
        :return:
        """
        self.current_neuron = new_neuron

        # TEMPORARY
        # raw_trace = self.raw_traces[self.current_neuron]
        # smooth_trace = self.smooth_traces[self.current_neuron]
        # n_frames = self.raw_traces.shape[1]
        # # computing all potential peaks and onset from smooth_trace
        # all_potential_peaks = np.zeros(n_frames, dtype="int8")
        # all_potential_onsets = np.zeros(n_frames, dtype="int8")
        # # then we do an automatic detection
        # peaks, properties = signal.find_peaks(x=raw_trace, distance=2)
        # all_potential_peaks[peaks] = 1
        #
        # onsets = []
        # diff_values = np.diff(raw_trace)
        # for index, value in enumerate(diff_values):
        #     if index == (len(diff_values) - 1):
        #         continue
        #     if value < 0:
        #         if diff_values[index + 1] >= 0:
        #             onsets.append(index + 1)
        # all_potential_onsets[np.array(onsets)] = 1
        #
        # signal_variation = 0
        # for onset_index in all_potential_onsets:
        #     peaks_after = np.where(all_potential_peaks > onset_index)[0]
        #     if len(peaks_after) == 0:
        #         continue
        #     peaks_after = all_potential_peaks[peaks_after]
        #     peak_after = peaks_after[0]
        #     if self.raw_traces[new_neuron, peak_after] < 3:
        #         signal_variation += np.abs(self.raw_traces[new_neuron, onset_index] -
        #                                    self.raw_traces[new_neuron, peak_after])
        # print(f"signal variation for cell {new_neuron}: {int(signal_variation)}")

        # TEMPORARY

        # for predictions improvement
        if self.prediction_improvement_mode and new_neuron not in self.prediction_improvement_dict:
            self.compute_prediction_improvement_for_cell(cell=new_neuron)

        # removing the cross representing the center_segment_coord
        self.center_segment_coord = None

        # so we scroll to predictions concerning this neuron
        self.update_predictions_list_box(keep_same_selected_index=True)
        if self.show_transient_classifier:
            # if predictions are not already loaded, then when we change cell
            # we removed the predictions. The user has to click again on the check box to launch
            # prediction thus avoiding a potentially long (on CPU) computation that might not have been
            # wanted
            if self.current_neuron in self.transient_prediction:
                self.set_transient_classifier_prediction_for_cell(cell=self.current_neuron)
                self.print_transients_predictions_stat = True
            else:
                self.show_transient_classifier = False
                self.print_transients_predictions_stat = False
                # print("self.transient_classifier_var.set(0)")
                self.transient_classifier_var.set(0)
                self.transient_classifier_check_box.deselect()
        # cell type classifier
        if self.display_cell_type_classifier_field:
            self.display_cell_type_predictions()
        if self.correlation_for_each_peak_option:
            if self.display_correlations:
                self.correlation_check_box_action(from_std_treshold=True)
                # start_time = time.time()
                # self.compute_source_and_transients_correlation(main_cell=self.current_neuron)
                # stop_time = time.time()
                # print(f"Time for computing source and transients correlation for cell {self.current_neuron}: "
                #       f"{np.round(stop_time-start_time, 3)} s")

        self.neuron_label["text"] = f"{self.current_neuron} / {self.nb_neurons - 1}"
        # self.spin_box_button.icursor(new_neuron)
        self.clear_and_update_entry_neuron_widget()
        self.clear_and_update_entry_cell_type_widget()
        self.onset_numbers_label["text"] = f" {self.numbers_of_onset()} "
        self.peak_numbers_label["text"] = f" {self.numbers_of_peak()} "
        self.update_to_agree_label()

        if (self.current_neuron + 1) == self.nb_neurons:
            self.next_button['state'] = DISABLED
        else:
            self.next_button['state'] = "normal"

        if self.current_neuron == 0:
            self.prev_button['state'] = DISABLED
        else:
            self.prev_button['state'] = "normal"

        # if self.inter_neurons[self.current_neuron] == 0:
        #     self.inter_neuron_button["text"] = ' not IN '
        #     self.inter_neuron_button["fg"] = "black"
        # else:
        #
        #     self.inter_neuron_button["text"] = ' IN '
        #     self.inter_neuron_button["fg"] = "red"

        if self.cells_to_remove[self.current_neuron] == 0:
            self.remove_cell_button["text"] = ' valid cell '
            self.remove_cell_button["fg"] = "black"
        else:
            self.remove_cell_button["text"] = ' invalid cell '
            self.remove_cell_button["fg"] = "red"

        self.first_click_to_remove = None
        self.click_corr_coord = None
        self.update_plot(new_neuron=True,
                         new_x_limit=new_x_limit, new_y_limit=new_y_limit,
                         amplitude_zoom_fit=amplitude_zoom_fit)
        self.update_plot_map_img()


def print_save(text, file, to_write, no_print=False):
    if not no_print:
        print(text)
    if to_write:
        file.write(text + '\n')


def merge_close_values(raster, raster_to_fill, cell, merging_threshold):
    """

    :param raster: Raster is a 2d binary array, lines represents cells, columns binary values
    :param cell: which cell to merge
    :param merging_threshold: times separation between two values under which to merge them
    :return:
    """
    values = raster[cell]
    indices = np.where(values)[0]
    peaks_diff = np.diff(indices)
    to_merge_indices = np.where(peaks_diff < merging_threshold)[0]
    for index_to_merge in to_merge_indices:
        value_1 = indices[index_to_merge]
        if raster[cell, value_1] == 0:
            # could be the case if more than 2 peaks were closes, then the first 2 would be already merge
            # then the next loop in n_gound_truther will do the job
            continue
        value_2 = indices[index_to_merge + 1]
        new_peak_index = (value_1 + value_2) // 2
        raster[cell, value_1] = 0
        raster[cell, value_2] = 0
        raster_to_fill[cell, new_peak_index] = 1
        # raster[cell, new_peak_index] = 1


# TODO: to update to new CINAC format file
def fusion_gui_selection(path_data):
    rep_fusion = "for_fusion"
    file_names = []
    txt_to_read = None
    # merge close ones
    # if True merge spikes or peaks that are less then merging_threshold, taking the average value
    merge_close_ones = False
    merging_threshold = 7
    # how many people did ground truth, useulf to merge close ones
    # should be superior to 1
    n_ground_truther = 2

    # look for filenames in the fisrst directory, if we don't break, it will go through all directories
    for (dirpath, dirnames, local_filenames) in os.walk(os.path.join(path_data, rep_fusion)):
        file_names.extend(local_filenames)
        break

    if len(file_names) == 0:
        return

    for file_name in file_names:
        if file_name.endswith(".txt"):
            txt_to_read = file_name

    data_files = []
    cells_by_file = []
    n_cells = None
    n_times = None
    with open(os.path.join(path_data, rep_fusion, txt_to_read), "r", encoding='UTF-8') as file:
        for nb_line, line in enumerate(file):
            line_list = line.split(':')
            data_file_name = line_list[0]
            # finding the file
            for file_name in file_names:
                if (data_file_name + ".mat").lower() in file_name.lower():
                    print(f"data_file_name {data_file_name}")
                    data_file = hdf5storage.loadmat(os.path.join(path_data, rep_fusion, file_name))
                    data_files.append(data_file)
                    if n_cells is None:
                        peak_nums = data_file['LocPeakMatrix_Python'].astype(int)
                        n_cells = peak_nums.shape[0]
                        n_times = peak_nums.shape[1]

                    cells_str_split = line_list[1].split()
                    cells = []
                    for cells_str in cells_str_split:
                        if "-" in cells_str:
                            limits = cells_str.split('-')
                            cells.extend(list(range(int(limits[0]), int(limits[1]) + 1)))
                        else:
                            cells.append(int(cells_str))
                    cells_by_file.append(cells)
                    continue

    peak_nums = np.zeros((n_cells, n_times), dtype="int8")
    spike_nums = np.zeros((n_cells, n_times), dtype="int8")
    to_agree_peak_nums = np.zeros((n_cells, n_times), dtype="int8")
    to_agree_spike_nums = np.zeros((n_cells, n_times), dtype="int8")
    doubtful_frames_nums = np.zeros((n_cells, n_times), dtype="int8")
    mvt_frames_nums = np.zeros((n_cells, n_times), dtype="int8")
    inter_neurons = np.zeros(0, dtype="int16")
    cells_to_remove = np.zeros(0, dtype="int16")
    cells_fusioned = []

    # in case if one of the file is a fusion file
    for index_data, data_file in enumerate(data_files):
        cells_array = np.array(cells_by_file[index_data])
        if "to_agree_peak_nums" in data_file:
            to_agree_peak_nums[cells_array] = data_file['to_agree_peak_nums'].astype(int)[cells_array]
        if "to_agree_spike_nums" in data_file:
            to_agree_spike_nums[cells_array] = data_file['to_agree_spike_nums'].astype(int)[cells_array]

    for index_data, data_file in enumerate(data_files):
        if "inter_neurons" in data_file:
            inter_neurons_data = data_file['inter_neurons'].astype(int)
            if len(inter_neurons_data) > 0:
                inter_neurons = np.union1d(inter_neurons, inter_neurons_data[0])
        if "cells_to_remove" in data_file:
            cells_to_remove_data = data_file['cells_to_remove'].astype(int)
            if len(cells_to_remove_data) > 0:
                cells_to_remove = np.union1d(cells_to_remove, cells_to_remove_data[0])

        peak_nums_data = data_file['LocPeakMatrix_Python'].astype(int)
        spike_nums_data = data_file['Bin100ms_spikedigital_Python'].astype(int)
        cells_fusioned.extend(list(cells_by_file[index_data]))
        for cell in cells_by_file[index_data]:
            # to_agree_peaks = np.where(to_agree_peak_nums[cell])[0]
            # to_agree_onsets = np.where(to_agree_spike_nums[cell])[0]

            # checking if we have added some peaks before
            if np.sum(peak_nums[cell]) == 0:
                peak_nums[cell] = peak_nums_data[cell]
            else:
                peaks_index_data = np.where(peak_nums_data[cell])[0]
                peaks_index = np.where(peak_nums[cell])[0]
                peaks_index_to_agree = np.setxor1d(peaks_index_data, peaks_index, assume_unique=True)
                peaks_index_agreed = np.intersect1d(peaks_index_data, peaks_index, assume_unique=True)
                to_agree_peak_nums[cell, peaks_index_to_agree] = to_agree_peak_nums[cell, peaks_index_to_agree] + 1
                peak_nums[cell, peaks_index_to_agree] = 0
                peak_nums[cell, peaks_index_agreed] = 1

            if np.sum(spike_nums[cell]) == 0:
                spike_nums[cell] = spike_nums_data[cell]
            else:
                onsets_index_data = np.where(spike_nums_data[cell])[0]
                onsets_index = np.where(spike_nums[cell])[0]
                onsets_index_to_agree = np.setxor1d(onsets_index_data, onsets_index, assume_unique=True)
                onsets_index_agreed = np.intersect1d(onsets_index_data, onsets_index, assume_unique=True)
                to_agree_spike_nums[cell, onsets_index_to_agree] = to_agree_spike_nums[cell, onsets_index_to_agree] + 1
                spike_nums[cell, onsets_index_to_agree] = 0
                spike_nums[cell, onsets_index_agreed] = 1

        if "doubtful_frames_nums" in data_file:
            doubtful_frames_nums_data = data_file['doubtful_frames_nums'].astype(int)
            for cell in np.arange(n_cells):
                if np.sum(doubtful_frames_nums_data[cell]) > 0:
                    doubtful_frames_nums[cell, doubtful_frames_nums_data[cell] > 0] = 1

        if "mvt_frames_nums" in data_file:
            mvt_frames_nums_data = data_file['mvt_frames_nums'].astype(int)
            for cell in np.arange(n_cells):
                if np.sum(mvt_frames_nums_data[cell]) > 0:
                    mvt_frames_nums[cell, mvt_frames_nums_data[cell] > 0] = 1

    cells_fusioned = np.unique(cells_fusioned)
    if merge_close_ones:
        for n in np.arange(n_ground_truther - 1):
            for cell in cells_fusioned:
                merge_close_values(raster=to_agree_peak_nums, raster_to_fill=peak_nums,
                                   cell=cell, merging_threshold=merging_threshold)
                merge_close_values(raster=to_agree_spike_nums, raster_to_fill=spike_nums,
                                   cell=cell, merging_threshold=merging_threshold)

    # now we want to fill the cells that didn't have to be fusionned, using one the data file
    cells_to_fill = np.setxor1d(cells_fusioned, np.arange(n_cells), assume_unique=True)

    for cell in cells_to_fill:
        peak_nums_data = data_files[0]['LocPeakMatrix_Python'].astype(int)
        spike_nums_data = data_files[0]['Bin100ms_spikedigital_Python'].astype(int)
        peak_nums[cell] = peak_nums_data[cell]
        spike_nums[cell] = spike_nums_data[cell]

    sio.savemat(os.path.join(path_data, rep_fusion, "fusion.mat"), {'Bin100ms_spikedigital_Python': spike_nums,
                                                                    'LocPeakMatrix_Python': peak_nums,
                                                                    'cells_to_remove': cells_to_remove,
                                                                    'inter_neurons': inter_neurons,
                                                                    "doubtful_frames_nums": doubtful_frames_nums,
                                                                    "mvt_frames_nums": mvt_frames_nums,
                                                                    "to_agree_peak_nums": to_agree_peak_nums,
                                                                    "to_agree_spike_nums": to_agree_spike_nums})


def launch_cinac_gui():
    # print(f'platform: {platform}')
    root = Tk()
    root.title(f"Options")

    app = ChoiceFormatFrame(master=root, default_path=None)
    app.mainloop()
    # root.destroy()


if __name__ == '__main__':
    launch_cinac_gui()
