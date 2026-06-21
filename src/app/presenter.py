"""presenter module"""

import markdown as md

import app.domain.people as ppl
import app.view_models.vm_people as vm_ppl


class Presenter:
    """presenter class"""

    def show_person(
        self, person: ppl.Person, file_content: str
    ) -> vm_ppl.VMPerson:
        return vm_ppl.VMPerson(
            id=person.id,
            markdown_rendered=self.render_markdown(file_content),
            markdown_raw=file_content,
        )

    def render_markdown(self, raw_str: str) -> str:
        return md.markdown(raw_str, extensions=["nl2br", "tables"])
