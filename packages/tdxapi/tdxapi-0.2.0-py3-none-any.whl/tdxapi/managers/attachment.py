from typing import Any

import attr

from tdxapi.managers.bases import TdxManager, tdx_method
from tdxapi.models.attachment import Attachment


@attr.s
class AttachmentManager(TdxManager):
    __tdx_section__ = "Attachments"

    @tdx_method("GET", "/api/attachments/{id}")
    def get(self, attachment_id: str) -> Attachment:
        """Gets an attachment."""
        return self.dispatcher.send(
            self.get.method,
            self.get.url.format(id=attachment_id),
            rclass=Attachment,
            rlist=False,
            rpartial=False,
        )

    @tdx_method("GET", "/api/attachments/{id}/content")
    def get_content(self, attachment_id: str) -> Any:
        """Gets the contents of an attachment."""
        return self.dispatcher.send(
            self.get_content.method, self.get_content.url.format(id=attachment_id)
        )

    @tdx_method("DELETE", "/api/attachments/{id}")
    def delete(self, attachment_id: str) -> None:
        """Deletes an attachment."""
        self.dispatcher.send(
            self.delete.method, self.delete.url.format(id=attachment_id),
        )
