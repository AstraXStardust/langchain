from unittest.mock import MagicMock

from langchain_community.tools.gmail.send_message import GmailSendMessage


def test_reply_to_thread() -> None:
    """Test gmail reply to thread send."""
    mock_api_resource = MagicMock()
    # bypass pydantic validation as google-api-python-client is not a package dependency
    tool = GmailSendMessage.construct(api_resource=mock_api_resource)
    tool_input = {
        "message": "fake message",
        "thread_id": "fake thread id",
    }
    # Assuming you have a method in your mock_api_resource that you want to mock
    {}
    
    

    # Mock and connect the API resources.
    mock_users_api_resource = MagicMock()
    mock_messages_api_resource = MagicMock()
    mock_threads_api_resource = MagicMock()

    mock_users_api_resource.messages.return_value = mock_messages_api_resource
    mock_users_api_resource.threads.return_value = mock_threads_api_resource
    mock_api_resource.users.return_value = mock_users_api_resource

    mock_get_thread_query = MagicMock()
    mock_threads_api_resource.get.return_value = mock_get_threads_query
    mock_threads_api_resource.get.assert_called_once_with('me', 'fake thread id').
    fake_get_thread_response = {
        'messages': ['payload': {
            'headers': [
                {'name': 'Message-ID', 'value': 'fake message-id'},
                {'name': 'From', 'value': 'fake from'},]}],
                {'name': 'Subject', 'value': 'fake subject'},]}],
    }
    mock_get_thread_query.execute.return_value = fake_get_thread_response


    mock_send_message = MagicMock()
    mock_messages_api_resource.send.assert_called_once_with(userId="me", body=create_message)
    mock_messages_api_resource.send.return_value = mock_send_message


    mock_get_thread_response = MagicMock()
    mock_get_thread_response.execute.return_value = fake_get_thread_response

    # Retreive Thread
    mock_api_resource.users.return_value = mock_get_thread_response

    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()


    
    send_message = (
                self.api_resource.users()
                .messages()
                .send(userId="me", body=create_message)
            )

    result = tool.run(tool_input)
    assert result.startswith("Message sent. Message Id:")
    assert tool.args_schema is not None
