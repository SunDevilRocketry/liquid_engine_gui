import valve   as SDR_valve
import buttons as SDR_buttons


class ButtonFactory:
    """Abstract factory that centralises construction of valve and sequence buttons.

    Having widget constructor details in one place means a single edit propagates
    to every button rather than hunting through the initialisation block."""

    @staticmethod
    def valve_button(parent, label, plumbing_sym, callback):
        """Create an SDR_valve.Buttons widget."""
        return SDR_valve.Buttons(parent, label, 'top', plumbing_sym,
                                 f_callback=callback)

    @staticmethod
    def sequence_button(parent, label, callback,
                        fg_color='white', outline_color='white',
                        text_color='white', size=(135, 45)):
        """Create an SDR_buttons.Button widget with the dashboard's default styling."""
        return SDR_buttons.Button(
            parent,
            text          = label,
            bg_color      = 'black',
            fg_color      = fg_color,
            outline_color = outline_color,
            text_color    = text_color,
            size          = size,
            f_callback    = callback,
        )
## ButtonFactory ##
