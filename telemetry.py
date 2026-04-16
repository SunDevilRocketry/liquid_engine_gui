import time
import os
import sys

import sensor_conv
import engineController
import sensor as SDR_sensor

class TelemetryProcessor:
    """Encapsulates the per-loop telemetry pipeline:

        request → format → filter → flow rates → gauge update → valve sync → log

    By accepting all dependencies through the constructor this class has no
    knowledge of Tkinter, serial setup, or application state beyond what it
    needs to do its job.
    """

    def __init__( self,
                  terminal,
                  sensor_buffer,
                  gauges,
                  update_valve_fn,
                  engine_state,
                  engine_state_filenames,
                  output_dir,
                  test_num,
                  start_time,
                  gauge_filter_enabled=True ):
        """
        Parameters
        ----------
        terminal               : sdec.terminalData
        sensor_buffer          : Sensor_Data_Buffer
        gauges                 : list[SDR_gauge.gauge]  — ordered to match gauge layout
        update_valve_fn        : callable(valve_states) — e.g. window.update_valve_states
        engine_state           : Liquid_Engine_State
        engine_state_filenames : dict[str, str]
        output_dir             : str
        test_num               : int
        start_time             : float  — value of time.perf_counter() at app start
        gauge_filter_enabled   : bool
        """
        self._terminal               = terminal
        self._sensor_buffer          = sensor_buffer
        self._gauges                 = gauges
        self._update_valve_fn        = update_valve_fn
        self._engine_state           = engine_state
        self._engine_state_filenames = engine_state_filenames
        self._output_dir             = output_dir
        self._test_num               = test_num
        self._start_time             = start_time
        self._gauge_filter_enabled   = gauge_filter_enabled

    def process( self, show_output=False ):
        """Run one full telemetry cycle for the current engine state."""
        time_sec = time.perf_counter() - self._start_time

        engineController.telreq([], self._terminal, show_output=show_output)
        self._terminal.sensor_readouts["t"] = time_sec

        src, src_fmt = self._get_sensor_source()

        ox_fr, fuel_fr, ox_fr_fmt, fuel_fr_fmt = self._compute_flow_rates(src)

        self._update_gauges(src, src_fmt, ox_fr, fuel_fr, ox_fr_fmt, fuel_fr_fmt)
        self._update_valve_fn(self._terminal.valve_states)
        self._log_data(time_sec)

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _format_readouts( self, readout_dict ):
        return {
            s: SDR_sensor.format_sensor_readout(self._terminal.controller, s, v)
            for s, v in readout_dict.items()
        }

    def _get_sensor_source( self ):
        """Return (source_values, formatted_source_values), applying the
        low-pass filter when enabled."""
        fmt = self._format_readouts(self._terminal.sensor_readouts)

        if self._gauge_filter_enabled:
            self._sensor_buffer.add_data(self._terminal.sensor_readouts)
            filtered = self._sensor_buffer.get_data()
            return filtered, self._format_readouts(filtered)

        return self._terminal.sensor_readouts, fmt

    def _compute_flow_rates( self, src ):
        ox_fr   = sensor_conv.ox_pressure_to_flow(src["pt1"] - src["pt2"])
        fuel_fr = sensor_conv.fuel_pressure_to_flow(src["pt6"] - src["pt5"])
        ox_fr_fmt   = SDR_sensor.format_sensor_readout(
            self._terminal.controller, "oxfr", ox_fr)
        fuel_fr_fmt = SDR_sensor.format_sensor_readout(
            self._terminal.controller, "ffr",  fuel_fr)
        return ox_fr, fuel_fr, ox_fr_fmt, fuel_fr_fmt

    def _update_gauges( self, src, src_fmt, ox_fr, fuel_fr, ox_fr_fmt, fuel_fr_fmt ):
        # Order must match the _GAUGE_CONFIGS table in DashboardWindow
        gauge_updates = [
            (src_fmt["pt7"], "Fuel Tank Pressure", src["pt7"]),
            (fuel_fr_fmt,    "Fuel Flow Rate",     fuel_fr   ),
            ("NaN",          "None",               0         ),
            (src_fmt["lc"],  "Thrust",             src["lc"] ),
            (src_fmt["pt0"], "LOX Pressure",       src["pt0"]),
            (ox_fr_fmt,      "LOX Flow Rate",      ox_fr     ),
            (src_fmt["pt4"], "Engine Pressure",    src["pt4"]),
            (src_fmt["tc"],  "LOX Temperature",    src["tc"] ),
        ]
        for gauge, (text_val, label, angle_val) in zip(self._gauges, gauge_updates):
            gauge.setText(text_val, label)
            gauge.setAngle(angle_val)

    def _log_data( self, time_sec ):
        state_name = self._engine_state.state
        log_path   = os.path.join(
            self._output_dir,
            self._engine_state_filenames[state_name] + str(self._test_num) + ".txt"
        )
        _SENSOR_KEYS = ["pt0","pt1","pt2","pt3","pt4","pt5","pt6","pt7","lc","tc"]
        _VALVE_KEYS  = ["oxPress","oxVent","oxPurge","fuelPress","fuelVent",
                        "fuelPurge","oxMain","fuelMain"]
        with open(log_path, "a") as f:
            f.write(str(time_sec) + " ")
            for s in _SENSOR_KEYS:
                f.write(str(self._terminal.sensor_readouts[s]) + " ")
            for v in _VALVE_KEYS:
                f.write(self._terminal.valve_states[v] + " ")
            f.write("\n")
## TelemetryProcessor ##
