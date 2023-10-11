"""
Languages module.
"""

from dataclasses import dataclass

from .. import modules as mod
from .. import contexts


@dataclass
class Address:
    """The address"""

    street: str
    zipcode: str | int
    city: str
    country: str
    link: str = None


@dataclass
class Contact(mod.Data):
    email: str | list[str] = None
    website: str = None
    github: str = None
    orcid: str = None
    linkedin: str = None
    address: Address = None
    pdf: str = None

    def __post_init__(self) -> None:
        # Conversion of dictionary to Address
        if isinstance(self.address, dict):
            self.address = Address(**self.address)
        if isinstance(self.email, str):
            self.email = [self.email]

    def to_latex(self, context: contexts.latex.LaTeXContext) -> str:
        latex = ""
        for mail in self.email:
            latex += context.format_variable("email", mail)
        latex += context.format_variable("website", self.website)
        latex += context.format_variable("github", self.github)
        latex += context.format_variable("orcid", self.orcid)
        latex += context.format_variable("linkedIn", self.linkedin)
        if self.address is not None:
            latex += context.format_variable("street", self.address.street)
            latex += context.format_variable("zipcode", self.address.zipcode)
            latex += context.format_variable("city", self.address.city)
            latex += context.format_variable("country", self.address.country)

        return latex

    def to_html(self, context: contexts.html.HTMLContext) -> str:
        html = context.open_list(False, "contact-list")

        for email in self.email:
            html += context.list_item(
                "mail",
                context.idiomatic_block("contact-icon iconoir-mail", "")
                + context.link_block("mail-link", f"mailto:{email}", email, ""),
            )

        if self.address is not None:
            html += context.list_item(
                "address",
                context.idiomatic_block("contact-icon iconoir-pin-alt", "")
                + context.link_block(
                    "address-link",
                    self.address.link,
                    self.address.street
                    + ", "
                    + str(self.address.zipcode)
                    + ", "
                    + self.address.city
                    + ", "
                    + self.address.country,
                    "",
                ),
            )

        if self.pdf is not None:
            html += context.list_item(
                "pdf",
                context.idiomatic_block("contact-icon iconoir-user", "")
                + context.link_block("pdf-link", self.pdf, "Curriculum vitae", ""),
            )

        if self.github is not None:
            html += context.list_item(
                "github",
                context.idiomatic_block("contact-icon iconoir-github", "")
                + context.link_block(
                    "github-link",
                    f"https://github.com/{self.github}",
                    self.github,
                    "",
                ),
            )

        if self.orcid is not None:
            html += context.list_item(
                "orcid",
                context.img_block(
                    "contact-icon orcid",
                    "https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png",
                    "",
                )
                + context.link_block(
                    "orcid-link",
                    f"https://orcid.org/{self.orcid}",
                    self.orcid,
                    "",
                ),
            )

        if self.linkedin is not None:
            html += context.list_item(
                "linkedin",
                context.idiomatic_block("contact-icon iconoir-linkedin", "")
                + context.link_block(
                    "linkedin-link",
                    f"https://linkedin.com/in/{self.linkedin}",
                    self.linkedin,
                    "",
                ),
            )

        html += context.close_block()  # list

        return html


class ContactModule(mod.Module):
    def __init__(
        self,
        level: int = 1,
        section: str = "Contact",
        icon: str = "iconoir-hand-card",
    ):
        super().__init__(level, section, icon)

    def to_latex(self, context: "contexts.latex.LaTeXContext") -> str:
        latex = ""
        for _, data_list in self.data:
            for data in data_list:
                latex += data.to_latex(context)

        return latex

    def load(self, json_value) -> None:
        contact = Contact(**json_value)
        self.data.append((None, [contact]))

    def _get_class_name(self) -> str:
        return "contact"
