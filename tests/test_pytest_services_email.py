import pytest

from src.database import db, models

data = ("oleh", "my@email.com")

@pytest.fixture
def new_user():
    user = models.User(first_name=data[0], email=data[1])
    return user

def test_create_user(new_user):
    db.add(new_user)
    db.commit()
    assert new_user.id > 0
    assert new_user.first_name == data[0]
    assert new_user.email == data[1]
    db.delete(new_user)
    
    




