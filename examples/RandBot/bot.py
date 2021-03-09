import sys
# ==============================================================================
# ROBOT
# Los robots definidos deben heredar de esta clase.
# ==============================================================================

class Bot(object):
    """Bot base. Este bot no hace nada (pasa todos los turnos)."""
    NAME = "NullBot"

    # ==========================================================================
    # Comportamiento del bot
    # Metodos a implementar / sobreescribir (opcionalmente)
    # ==========================================================================

    def __init__(self, init_state):
        """Inicializar el bot: llamado al comienzo del juego."""
        self.player_num = init_state["player_num"]
        self.player_count = init_state["player_count"]
        self.init_pos = init_state["position"]
        self.map = init_state["map"]
        self.lighthouses = map(tuple, init_state["lighthouses"])

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una accion (jugada).

        state: estado actual del juego.
        """
        return self.nop()

    def success(self):
        """Exito: llamado cuando la jugada previa es valida."""
        pass

    def error(self, message, last_move):
        """Error: llamado cuando la jugada previa no es valida."""
        self.log("Recibido error: %s", message)
        self.log("Jugada previa: %r", last_move)

    # ==========================================================================
    # Utilidades
    # No es necesario sobreescribir estos metodos.
    # ==========================================================================

    def log(self, message, *args):
        """Mostrar mensaje de registro por stderr"""
        print("[%s] %s" % (self.NAME, (message % args)), file=sys.stderr)

    # ==========================================================================
    # Jugadas posibles
    # No es necesario sobreescribir estos metodos.
    # ==========================================================================

    def nop(self):
        """Pasar el turno"""
        return {
            "command": "pass",
        }

    def move(self, x, y):
        """Mover a una casilla adyacente

        x: delta x (0, -1, 1)
        y: delta y (0, -1, 1)
        """
        return {
            "command": "move",
            "x": x,
            "y": y
        }

    def attack(self, energy):
        """Atacar a un faro

        energy: energia (entero positivo)
        """
        return {
            "command": "attack",
            "energy": energy
        }

    def connect(self, destination):
        """Conectar a un faro remoto

        destination: tupla o lista (x,y): coordenadas del faro remoto
        """
        return {
            "command": "connect",
            "destination": destination
        }
