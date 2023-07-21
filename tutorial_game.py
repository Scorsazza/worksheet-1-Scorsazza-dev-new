import random
import pyasge
import self as self

from gamedata import GameData


def isInside(sprite, mouse_x, mouse_y) -> bool:
    # grab the sprite's bounding box. the box has 4 vertices
    bounds = sprite.getWorldBounds()

    # check to see if the mouse position falls within the x and y bounds
    if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
        return True

    return False


class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        # This is a comment
        self.data.background = pyasge.Sprite()
        self.initBackground()

        #
        self.menu_text = None
        self.initMenu()

        #
        self.scoreboard = None
        self.initScoreboard()

        # This is a comment
        self.fish = pyasge.Sprite()
        self.initFish()

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):
            # Loaded, remember to render this.
            self.data.background.z_order = -100
            return True
        else:
            return False

    def initFish(self) -> bool:
        if self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_073.png"):
            self.fish.z_order = 1
            self.fish.scale = 1
            self.fish.x = 300
            self.fish.y = 300
            self.spawn()
            return True

        return False

    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.x = 1300
        self.scoreboard.y = 75
        self.scoreboard.string = str(self.data.score).zfill(6)
        self.scoreboard.colour = pyasge.COLOURS.INDIGO

    def initMenu(self) -> bool:
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/AlloyInk.ttf", 64)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "The Fish Game"
        self.menu_text.position = [100, 100]
        self.menu_text.colour = pyasge.COLOURS.INDIGO
        #start
        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = ">START"
        self.play_option.position = [100, 400]
        self.play_option.colour = pyasge.COLOURS.INDIGO

        #End
        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = ">QUIT TO DESKTOP"
        self.exit_option.position = [500, 400]
        self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
        return True

        return True

    def clickHandler(self, event: pyasge.ClickEvent) -> None:
        # look to see if mouse button 1 pressed
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and \
                event.button == pyasge.MOUSE.MOUSE_BTN1:

            # is the mouse position within the sprite's bounding box?
            if isInside(self.fish, event.x, event.y):
                self.data.score += 1  # here we add 1 to the score
                self.scoreboard.string = str(self.data.score).zfill(6)
                self.spawn()  # now we respawn the fish to keep the game going

    def keyHandler(self, event: pyasge.KeyEvent) -> None:

        # only act when the key is pressed and not released
        if event.action == pyasge.KEYS.KEY_PRESSED:

            # use both the right and left keys to select the play/exit options
            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option
                if self.menu_option == 0:
                    self.play_option.string = ">START"
                    self.play_option.colour = pyasge.COLOURS.INDIGO
                    self.exit_option.string = " QUIT TO DESKTOP"
                    self.exit_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                else:
                    self.play_option.string = " START"
                    self.play_option.colour = pyasge.COLOURS.LIGHTSLATEGRAY
                    self.exit_option.string = " >QUIT TO DESKTOP"
                    self.exit_option.colour = pyasge.COLOURS.INDIGO

            # if the enter key is pressed, action the menu option
            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.menu_option == 0:
                    self.menu = False
                else:
                    self.signalExit()

    def spawn(self) -> None:
        fish = pyasge.Sprite()
        fishtexture = ''

        fish.z_order = 1
        fish.scale = 1
        # generate random {x,y} but don't let the fish spawn on edges
        x = random.randint(0, self.data.game_res[0] - self.fish.width)
        y = random.randint(0, self.data.game_res[1] - self.fish.height)

        self.fish.x = x
        self.fish.y = y

    def update(self, game_time: pyasge.GameTime) -> None:

        if self.menu:
            # update the menu here
            pass
        else:
            # update the game here
            self.fish.x+=100*game_time.fixed_timestep
            if self.fish.x > self.data.game_res[1]:
                self.fish.x = 0-self.fish.width
            pass

    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the gam    e-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """
        self.data.renderer.render(self.data.background)
        if self.menu:
            # render the menu here
            self.data.renderer.render(self.data.background)
            self.data.renderer.render(self.menu_text)

            self.data.renderer.render(self.play_option)
            self.data.renderer.render(self.exit_option)
        else:
            # render the game here
            self.data.renderer.render(self.fish)
            self.data.renderer.render(self.scoreboard)





def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()

class fish():
    def initFish(self) -> bool:
        if self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_073.png"):
            self.fish.z_order = 1
            self.fish.scale = 1
            self.fish.x = 300
            self.fish.y = 300
            self.spawn()

