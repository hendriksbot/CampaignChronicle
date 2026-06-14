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

    def emit_dict(self, event: str, data: dict):
        self._socketio.emit(event, data)

    def _setup_routes(self):
        @self._app.route("/")
        def render_index_page():
            return flask.render_template(
                "index.html", app_version=_version.version
            )

        @self._app.route("/people")
        def render_people_page():
            return flask.render_template(
                "people.html", app_version=_version.version
            )

        @self._app.route("/people/<person_id>")
        def render_person_page(person_id):
            return flask.render_template(
                "person.html", app_version=_version.version, person_id=person_id
            )

        @self._socketio.on("request_set_campaign_folder")
        def request_set_campaign_folder():
            self._evh.request_set_campaign_folder()

        @self._socketio.on("request_reload_index")
        def request_reload_index():
            self._evh.request_reload_index()

        @self._socketio.on("request_people_list")
        def request_people_list():
            self._evh.request_people_list()

        @self._socketio.on("request_create_person")
        def request_create_person(data):
            self._evh.request_create_person(data)

        @self._socketio.on("request_person")
        def request_person(data):
            self._evh.request_person(data)
