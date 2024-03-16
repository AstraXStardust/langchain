"""Reply to Gmail threads."""

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional, Type, Union

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_community.tools.gmail.base import GmailBaseTool


class ReplyToThreadSchema(BaseModel):
    """Input for ReplyToThread tool."""

    message: str = Field(
        ...,
        description="The message to send.",
    )
    # From https://support.google.com/mail/answer/7190?hl=en
    thread_id: str = Field(
        ...,
        description="The thread ID.",
    )


class GmailReplyToThread(GmailBaseTool):
    """Tool that replies to a Gmail thread."""

    name: str = "reply_to_gmail_thread"
    description: str = (
        "Use this tool to reply to email messages on a thread."
        " The input is the thread_id and message."
    )
    args_schema: Type[ReplyToThreadSchema] = ReplyToThreadSchema

    def _prepare_message(
        self,
        message: str,
        to: Union[str, List[str]],
        subject: str,
        gmail_thread_id: str,
        rfc_compliant_thread_id: str,
    ) -> Dict[str, Any]:
        """Create a message for an email."""
        mime_message = MIMEMultipart()
        mime_message.attach(MIMEText(message, "html"))

        mime_message["To"] = ", ".join(to if isinstance(to, list) else [to])
        mime_message["Subject"] = subject
        mime_message["In-Reply-To"] = rfc_compliant_thread_id
        mime_message["References"] = rfc_compliant_thread_id
        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        return {"raw": encoded_message, "threadId": gmail_thread_id}

    def _run(
        self,
        message: str,
        thread_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Run the tool."""
        query = self.api_resource.users().threads().get(userId="me", id=thread_id)
        thread_data = query.execute()
        if not isinstance(thread_data, dict):
            raise ValueError("The output of the query must be a list.")
        if not len(thread_data["messages"]) > 0:
            raise ValueError("The thread must have at least one message.")
        last_message = thread_data["messages"][-1]
        for header in last_message["payload"]["headers"]:
            if header["name"] == "Message-ID":
                rfc_compliant_thread_id = header["value"]
            if header["name"] == "From":
                to = header["value"]
            if header["name"] == "Subject":
                subject = header["value"]
        if not rfc_compliant_thread_id:
            raise ValueError(
                f"The thread_id found [{rfc_compliant_thread_id}] is not RFC compliant."
            )
        create_message = self._prepare_message(
            message, to, subject, thread_id, rfc_compliant_thread_id
        )
        try:
            send_message = (
                self.api_resource.users()
                .messages()
                .send(userId="me", body=create_message)
            )
            sent_message = send_message.execute()
            return f'Message sent. Message Id: {sent_message["id"]}'
        except Exception as error:
            raise Exception(f"An error occurred: {error}")
