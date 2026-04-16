import sequence as SDR_sequence


class CallbackHandler:
    """Owns every button callback in the dashboard.

    Dependencies are injected at construction so callbacks are not coupled to
    module-level globals.  The window reference is set separately via
    set_window() to break the initialization cycle:
        callbacks → window (needs callbacks to build buttons)
        window → callbacks (needs window reference to close it)
    """

    def __init__( self, engine_state, terminal, valve_buttons, exit_flag ):
        """
        Parameters
        ----------
        engine_state  : Liquid_Engine_State
        terminal      : sdec.terminalData
        valve_buttons : dict  — shared mutable dict populated by DashboardWindow
        exit_flag     : list  — single-element mutable bool, e.g. [False]
        """
        self._engine_state  = engine_state
        self._terminal      = terminal
        self._valve_buttons = valve_buttons
        self._exit_flag     = exit_flag
        self._window        = None

    def set_window( self, window ):
        """Late-bind the window reference after DashboardWindow is created."""
        self._window = window

    # -------------------------------------------------------------------------
    # Window lifecycle
    # -------------------------------------------------------------------------

    def close_window( self ):
        self._window.close()
        self._exit_flag[0] = True

    # -------------------------------------------------------------------------
    # Sequence / control callbacks
    # -------------------------------------------------------------------------

    def pre_fire_purge( self ):
        SDR_sequence.pre_fire_purge( self._engine_state, self._terminal )

    def fill_and_chill( self ):
        SDR_sequence.fill_and_chill( self._engine_state, self._terminal )

    def standby( self ):
        SDR_sequence.standby       ( self._engine_state, self._terminal )

    def fire_engine( self ):
        SDR_sequence.fire_engine   ( self._engine_state, self._terminal )

    def hotfire_abort( self ):
        SDR_sequence.hotfire_abort ( self._engine_state, self._terminal )

    def get_state( self ):
        SDR_sequence.get_state     ( self._engine_state, self._terminal )

    def stop_hotfire( self ):
        SDR_sequence.stop_hotfire  ( self._engine_state, self._terminal )

    def stop_purge( self ):
        SDR_sequence.stop_purge    ( self._engine_state, self._terminal )

    def lox_purge( self ):
        SDR_sequence.lox_purge     ( self._engine_state, self._terminal )

    def kbottle_close( self ):
        SDR_sequence.kbottle_close ( self._engine_state, self._terminal )

    def manual_mode( self ):
        SDR_sequence.manual        ( self._engine_state, self._terminal )

    def reset( self ):
        pass

    # -------------------------------------------------------------------------
    # Valve callback factory
    # -------------------------------------------------------------------------

    def make_valve_callback( self, valve_key, seq_fn_name ):
        """Return a closure that toggles a valve button and fires the matching
        sequence function.  Captured variables are resolved at click-time so
        valve_buttons can be populated after the closure is created."""
        def callback():
            btn = self._valve_buttons[valve_key]
            getattr(SDR_sequence, seq_fn_name)(
                self._engine_state, self._terminal, btn.state
            )
            if btn.symbol is not None and self._engine_state.state == "Manual State":
                btn.state = not btn.state
                btn.symbol.setState(btn.state)
                btn.updateText()
                btn.updateColor()
                btn.configButton()
        return callback
## CallbackHandler ##
