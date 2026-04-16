class Liquid_Engine_State:
    """Holds and transitions the current engine state string."""

    def __init__( self ):
        self.state = "Initialization State"

    def get_engine_state( self ):
        return self.state

    def set_engine_state( self, new_engine_state ):
        self.state = new_engine_state
## Liquid_Engine_State ##
