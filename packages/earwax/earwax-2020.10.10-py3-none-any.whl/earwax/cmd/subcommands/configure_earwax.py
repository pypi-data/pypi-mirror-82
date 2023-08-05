"""Provides the configure_earwax subcommand."""

from argparse import Namespace
from pathlib import Path

from pyglet.window import Window

from ... import ConfigMenu, Game
from ..constants import options_filename


def configure_earwax(args: Namespace) -> None:
    """Configure earwax, using a :class:`earwax.ConfigMenu` instance."""
    path: Path = options_filename.absolute()
    if not path.is_file():
        print('Error: No options file found.')
        print()
        print('Please use the `init` subcommand first.')
        raise SystemExit
    window: Window = Window(caption='Configure Earwax')
    game: Game = Game()
    with path.open('r') as f:
        game.config.load(f)
    menu: ConfigMenu = ConfigMenu(game, 'Configure Earwax', dismissible=False)

    @menu.item('Save and Exit')
    def save_and_exit() -> None:
        """Save the configuration before exiting."""
        with path.open('w') as f:
            game.config.save(f)
        window.close()

    @menu.item('Exit Without Saving')
    def exit_without_saving() -> None:
        """Exit without saving the configuration."""
        window.close()

    game.push_level(menu)
    game.run(window)
