"""this module implements the gui using flask"""

import flask
import flask_socketio
import app.guis.gui as gui
import app.utils.paths as paths
import app._version as _version


class FlaskGui(gui.Gui):
    """flask implementation of the app gui"""

    def __init__(self, config: dict, locator: paths.ResourceLocator):
        super().__init__()
        templates_dir = locator.path("templates")
        static_dir = locator.path("static")
        self._app = flask.Flask(
            "CampaignChronicle",
            template_folder=str(templates_dir),
            static_folder=str(static_dir),
        )
        self._app.config["SECRET_KEY"] = config["flask_secret_key"]
        self._config = config
        self._socketio = flask_socketio.SocketIO(
            self._app, async_mode="threading"
        )

    def run(self, is_debug_mode):
        self._setup_routes()
        self._socketio.run(
            app=self._app,
            host="0.0.0.0",
            port=self._config["port"],
            debug=is_debug_mode,
            use_reloader=is_debug_mode,
        )

    def emit_object(self, event, data):
        pass

    def _setup_routes(self):
        @self._app.route("/")
        def render_index_page():
            return flask.render_template(
                "index.html", app_version=_version.version
            )
