from typing import List
from requests import Response, post


class Mailgun:
    # Constants
    MAILGUN_DOMAIN = "sandboxcc439ff7cbdc492a9c46699fcb61ef04.mailgun.org"
    MAILGUN_API_KEY = "pubkey-52ec5444ce137f0de733eee1dc96689f"

    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "faiqueali017@sandboxcc439ff7cbdc492a9c46699fcb61ef04.mailgun.org"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        return post(
            f"https://api.mailgun.net/v4/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
