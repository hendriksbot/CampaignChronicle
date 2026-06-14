"""main file of app"""

import typer
import webbrowser
from threading import Timer
import app.utils.paths as paths
import app.guis.flask_gui as flask_gui
import app.controller as ctr
import app.interactor as iactr

app = typer.Typer()


def make_locator() -> paths.ResourceLocator:
    locator = paths.ResourceLocator.from_package(
        "app", contents_dir="CampaignChronicle"
    )
    locator.register(
        "templates",
        dev_rel="templates",
        frozen_rel_candidates=("CampaignChronicle/templates",),
    )
    locator.register(
        "static",
        dev_rel="static",
        frozen_rel_candidates=("CampaignChronicle/static",),
    )

    return locator


def open_browser(port: int):
    webbrowser.open_new(f"http://127.0.0.1:{str(port)}/")


@app.command()
def main(
    is_debug_mode: bool = typer.Option(
        False, "--debug", "-d", help="enable debug mode"
    )
):
    locator = make_locator()
    gui_config = {"flask_secret_key": "to_be_replaced", "port": 5001}
    gui = flask_gui.FlaskGui(config=gui_config, locator=locator)
    controller = ctr.Controller(gui=gui, interactor=iactr.Interactor())
    gui.bind_event_handler(controller)

    Timer(1, lambda: open_browser(port=gui_config["port"])).start()
    controller.start_app(is_debug_mode=is_debug_mode)


if __name__ == "__main__":
    app()
