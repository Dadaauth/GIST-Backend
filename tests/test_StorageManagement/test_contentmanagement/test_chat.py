import os

import pytest



@pytest.fixture
def setup():
    yield

def test_create_message(setup):
    from StorageManagement.contentmanagement.chat import create_message
    
    # Should raise a ValueError if no arguments are passed
    with pytest.raises(ValueError):
        create_message()
    
    # Checks if the sender is present in the conversation
    new_message = create_message(
        sender_id="123",
        conversation_id="123"
    )
    assert new_message[0] is False

    # Here, test if it returns true when all credentials are correct

def test_create_conversation(setup):
    from StorageManagement.contentmanagement.chat import create_conversation
    with pytest.raises(TypeError):
        create_conversation()