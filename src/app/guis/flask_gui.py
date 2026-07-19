"""this module implements the gui using flask"""

import flask
from dataclasses import dataclass
from functools import singledispatchmethod
import flask_socketio
import app.guis.gui as gui
import app.utils.paths as paths
import app._version as _version


@dataclass
class NavigationItemViewModel:
    display_name: str
    endpoint: str


@dataclass
class BasePageDefinition:
    """defines a page"""

    id: str
    template: str
    endpoint: str = ""
    route: str = ""

    def __post_init__(self):
        if not self.endpoint:
            self.endpoint = self.id
        if not self.route:
            self.route = f"/{self.id}"


@dataclass
class PageDefinition(BasePageDefinition):
    pass


@dataclass
class RessourcePageDefinition(BasePageDefinition):
    resource_name_str: str = "obj_id"

    def __post_init__(self):
        if not self.route:
            self.route = f"/{self.id}/<{self.resource_name_str}>"
        super().__post_init__()


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
        self._pages = [
            PageDefinition("index", "index.html", route="/"),
            PageDefinition("relations", "relations.html"),
            PageDefinition("people", "people.html"),
            RessourcePageDefinition(
                "person", "person.html", resource_name_str="person_id"
            ),
            PageDefinition("events", "people.html"),
            RessourcePageDefinition("event", "person.html"),
        ]
        self._ui_config = {
            "app_version": _version.version,
            "app_navigation": [
                NavigationItemViewModel("Personen", "people"),
                NavigationItemViewModel("Ereignisse", "events"),
            ],
        }

    def run(self, is_debug_mode):
        self._setup_routes()
        for rule in self._app.url_map.iter_rules():
            print(rule.endpoint, rule.rule)
        self._socketio.run(
            app=self._app,
            host="0.0.0.0",
            port=self._config["port"],
            debug=is_debug_mode,
            use_reloader=is_debug_mode,
        )

    def emit_dict(self, event: str, data: dict):
        self._socketio.emit(event, data)

    @singledispatchmethod
    def _register_page(self, page):
        raise NotImplementedError(f"{type(page)} is not implemented.")

    @_register_page.register
    def _(self, page: PageDefinition):
        @self._app.route(page.route, endpoint=page.endpoint)
        def render_page():
            return flask.render_template(page.template, **self._ui_config)

    @_register_page.register
    def _(self, page: RessourcePageDefinition):
        @self._app.route(page.route, endpoint=page.endpoint)
        def render_page(**kwargs):
            obj_id = kwargs[page.resource_name_str]
            obj = {page.resource_name_str: obj_id}
            return flask.render_template(
                page.template, **obj, **self._ui_config
            )

    def _setup_routes(self):
        for page in self._pages:
            self._register_page(page)

        @self._app.route("/api/render-markdown", methods=["POST"])
        def render_markdown():
            data = flask.request.get_json()
            return {"html": self._evh.render_markdown(data["markdown"])}

        @self._socketio.on("request_set_campaign_folder")
        def request_set_campaign_folder():
            self._evh.request_set_campaign_folder()

        @self._socketio.on("request_reload_index")
        def request_reload_index():
            self._evh.request_reload_index()

        @self._socketio.on("request_init_relations_data")
        def request_initial_relations_data():
            self._evh.request_initial_relations_data()

        @self._socketio.on("request_create_relation")
        def request_create_relation(data):
            self._evh.request_create_relation(data)

        @self._socketio.on("request_delete_relation")
        def request_delete_relation(data):
            self._evh.request_delete_relation(data["id"])

        @self._socketio.on("request_people_list")
        def request_people_list():
            self._evh.request_people_list()

        @self._socketio.on("request_create_person")
        def request_create_person(data):
            self._evh.request_create_person(data)

        @self._socketio.on("request_person")
        def request_person(data):
            self._evh.request_person(data)

        @self._socketio.on("save_markdown")
        def save_markdown(data):
            self._evh.save_markdown(data["type"], data["id"], data["content"])
