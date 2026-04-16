import tkinter as tk
from PIL import Image, ImageTk

import gauge          as SDR_gauge
import sensor         as SDR_sensor
import engine_display as SDR_engine_display
from button_factory import ButtonFactory

# Valve state constants
VALVE_OPEN   = True
VALVE_CLOSED = False

# Layout constant
_GRID_LEN = 85


class DashboardWindow:
    """Encapsulates all Tkinter details for the engine dashboard.

    The rest of the application never imports tkinter directly; it interacts
    with the GUI exclusively through this class's public interface:

        update_valve_states(valve_states)  — sync valve button visuals
        update()                           — tick the GUI event loop
        close()                            — destroy both windows

    Widget collections are exposed as plain attributes:
        gauges        : list of SDR_gauge.gauge, in _GAUGE_CONFIGS order
        valve_buttons : dict[str, SDR_valve.Buttons], keyed by valve-state key
    """

    def __init__( self, callbacks, valve_buttons ):
        """
        Parameters
        ----------
        callbacks     : CallbackHandler — provides all button callbacks
        valve_buttons : dict            — shared mutable dict; populated here
                                          so external code (TelemetryProcessor,
                                          CallbackHandler closures) can reference it
        """
        self._callbacks    = callbacks
        self.valve_buttons = valve_buttons   # populated during _build_widgets
        self.gauges        = []

        self._root     = self._build_root()
        self._frames   = self._build_frames()
        self.plumbing  = SDR_engine_display.Engine_Display(_GRID_LEN)
        self._build_widgets()
        self._layout()

    # -------------------------------------------------------------------------
    # Public interface
    # -------------------------------------------------------------------------

    def update_valve_states( self, valve_states ):
        """Sync every valve button's visual state with the latest telemetry."""
        for key, btn in self.valve_buttons.items():
            state_str = valve_states.get(key)
            if state_str == "OPEN":
                btn.symbol.setState(VALVE_OPEN);  btn.state = VALVE_OPEN
            elif state_str == "CLOSED":
                btn.symbol.setState(VALVE_CLOSED); btn.state = VALVE_CLOSED
            btn.updateText()
            btn.updateColor()
            btn.configButton()

    def update( self ):
        """Advance the Tkinter and P&ID event loops by one tick."""
        self.plumbing.updatePipeStatus()
        self._root.update()
        self.plumbing.getWindow().update()

    def close( self ):
        """Destroy both the dashboard window and the P&ID window."""
        self._root.destroy()
        self.plumbing.win.destroy()

    # -------------------------------------------------------------------------
    # Private construction helpers
    # -------------------------------------------------------------------------

    def _build_root( self ):
        root = tk.Tk()
        root.title("Engine Dashboard")
        root.configure( background="black", borderwidth=10 )
        root.geometry("900x1000")
        root.protocol( "WM_DELETE_WINDOW", self._callbacks.close_window )

        # Load logo images (kept on self to prevent garbage collection)
        self._sdr_logo  = tk.PhotoImage(file='images/SDRLogo5.png')
        sdr_img         = Image.open("images/SDRlogont2.png")
        sdr_img         = sdr_img.resize(
            (int(0.8*140), int(0.8*125)), Image.Resampling.LANCZOS
        )
        self._sdr_photo = ImageTk.PhotoImage(sdr_img)
        return root

    def _build_frames( self ):
        r           = self._root
        valve_frame = tk.Label( r, bg='black' )
        frames = {
            "main_title"    : tk.Label( r,           bg='black' ),
            "valve_button"  : valve_frame,
            "valve_col1"    : tk.Label( valve_frame, bg='black' ),
            "valve_col2"    : tk.Label( valve_frame, bg='black' ),
            "valve_col3"    : tk.Label( valve_frame, bg='black' ),
            "valve_col4"    : tk.Label( valve_frame, bg='black' ),
            "sequence_row1" : tk.Label( r,           bg='black' ),
            "sequence_row2" : tk.Label( r,           bg='black' ),
            "gauge_row1"    : tk.Label( r,           bg='black' ),
            "gauge_row2"    : tk.Label( r,           bg='black' ),
        }
        return frames

    def _build_widgets( self ):
        f = self._frames
        cb = self._callbacks

        # --- Valve buttons ---------------------------------------------------
        # (valve_state_key, label, col_frame_key, plumbing_sym, seq_fn_name)
        _VALVE_CONFIGS = [
            ("oxPress",   "LOX Pressure (1)",  "valve_col1", self.plumbing.one,   "manual_lox_press" ),
            ("oxVent",    "LOX Vent (2)",       "valve_col1", self.plumbing.two,   "manual_lox_vent"  ),
            ("oxPurge",   "LOX Purge (5)",      "valve_col1", self.plumbing.five,  "manual_lox_purge" ),
            ("oxMain",    "LOX Main",           "valve_col1", self.plumbing.s2,    "manual_lox_main"  ),
            ("fuelPress", "Fuel Pressure (3)",  "valve_col2", self.plumbing.three, "manual_fuel_press"),
            ("fuelVent",  "Fuel Vent (4)",      "valve_col2", self.plumbing.four,  "manual_fuel_vent" ),
            ("fuelPurge", "Fuel Purge (6)",     "valve_col2", self.plumbing.six,   "manual_fuel_purge"),
            ("fuelMain",  "Fuel Main Valve",    "valve_col2", self.plumbing.s1,    "manual_fuel_main" ),
        ]
        for key, label, col_key, sym, seq_fn in _VALVE_CONFIGS:
            self.valve_buttons[key] = ButtonFactory.valve_button(
                f[col_key], label, sym, cb.make_valve_callback(key, seq_fn)
            )

        # --- Sequence / control buttons --------------------------------------
        # (dict_key, label, frame_key, callback, fg, outline, text_color)
        _BUTTON_CONFIGS = [
            ("pre_fire_purge", "Pre-Fire Purge", "sequence_row1", cb.pre_fire_purge, 'white', 'white', 'white'),
            ("fill_chill",     "Fill/Chill",     "sequence_row1", cb.fill_and_chill, 'white', 'white', 'white'),
            ("standby",        "Standby",        "sequence_row1", cb.standby,        'white', 'white', 'white'),
            ("ignite",         "Ignite",         "sequence_row1", cb.fire_engine,    'white', 'white', 'white'),
            ("stop_hotfire",   "Stop Hotfire",   "sequence_row2", cb.stop_hotfire,   'white', 'white', 'white'),
            ("stop_purge",     "Disarm",         "sequence_row2", cb.stop_purge,     'white', 'white', 'white'),
            ("lox_purge",      "LOX Purge",      "sequence_row2", cb.lox_purge,      'white', 'white', 'white'),
            ("kbottle_close",  "KBottle Close",  "sequence_row2", cb.kbottle_close,  'white', 'white', 'white'),
            ("getstate",       "Get State",      "valve_col3",    cb.get_state,      'white', 'white', 'white'),
            ("manual",         "Manual",         "valve_col3",    cb.manual_mode,    'white', 'white', 'white'),
            ("abort",          "ABORT",          "valve_col4",    cb.hotfire_abort,  'red',   'red',   'red'  ),
            ("reset",          "Reset",          "valve_col4",    cb.reset,          'white', 'white', 'white'),
        ]
        self._sequence_buttons = {}
        for name, label, frame_key, callback, fg, outline, text in _BUTTON_CONFIGS:
            self._sequence_buttons[name] = ButtonFactory.sequence_button(
                f[frame_key], label, callback,
                fg_color=fg, outline_color=outline, text_color=text
            )

        # --- Sensor gauges ---------------------------------------------------
        # (sensor_key, display_label, row_frame_key)
        _GAUGE_CONFIGS = [
            ("pt7",  "Fuel Tank Pressure", "gauge_row1"),
            ("ffr",  "Fuel Flow Rate",     "gauge_row1"),
            ("pt2",  "None",               "gauge_row1"),
            ("lc",   "Thrust",             "gauge_row1"),
            ("pt0",  "LOX Pressure",       "gauge_row2"),
            ("oxfr", "LOX Flow Rate",      "gauge_row2"),
            ("pt4",  "Engine Pressure",    "gauge_row2"),
            ("tc",   "LOX Temperature",    "gauge_row2"),
        ]
        for sensor_key, label, row_key in _GAUGE_CONFIGS:
            g = SDR_gauge.gauge(
                f[row_key],
                background     = 'black',
                max_sensor_val = SDR_sensor.max_sensor_vals[sensor_key]
            )
            g.setText("Nan", label)
            self.gauges.append(g)

    def _layout( self ):
        f  = self._frames
        sb = self._sequence_buttons

        f["main_title"].pack()

        f["valve_col1"].pack( side='left' )
        f["valve_col2"].pack( side='left' )
        f["valve_col3"].pack( side='left' )
        f["valve_col4"].pack( side='left' )
        f["valve_button"].pack()

        f["sequence_row1"].pack()
        f["sequence_row2"].pack()

        sb["pre_fire_purge"].pack( side="left", padx=30 )
        sb["fill_chill"    ].pack( side="left", padx=30 )
        sb["standby"       ].pack( side="left", padx=30 )
        sb["ignite"        ].pack( side="left", padx=30 )
        sb["getstate"      ].pack( side="top",  padx=30 )
        sb["manual"        ].pack( side="top",  padx=30 )
        sb["abort"         ].pack( side="top",  padx=30 )
        sb["stop_hotfire"  ].pack( side="left", padx=30 )
        sb["stop_purge"    ].pack( side="left", padx=30 )
        sb["lox_purge"     ].pack( side="left", padx=30 )
        sb["kbottle_close" ].pack( side="left", padx=30 )
        sb["reset"         ].pack( side="top",  padx=30 )

        f["gauge_row1"].pack()
        f["gauge_row2"].pack()
        for g in self.gauges:
            g.getWidget().pack(side='left')
## DashboardWindow ##
