import pytest
from unittest.mock import patch
from main import app  # pastikan path ke file 'main.py' benar
from flask import jsonify


# Fixture untuk membuat test client Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Mocking Supabase
@pytest.fixture
def mock_supabase(mocker):
    return mocker.patch('main.supabase')  # patch Supabase client



#############################################################
# import pytest
# from dotenv import load_dotenv
# from main import app

# @pytest.fixture
# def client():
#     app.config["Testing"] = True
#     with app.test_client() as client:
#         yield client

# @pytest.fixture
# def admin_username():
#     return "admin_user"

# def test_fix(admin_username):
#     assert admin_username == "admin_user"
    
# @pytest.fixture
# def home():
#     return "home_directory"

# def test_sum(home):
#     assert home == "home_directory"

        
# @pytest.fixture
# def admin_username():
#     return "admin"

# @pytest.fixture
# def home():
#     return "malang"
        
# @pytest.fixture
# def appjson() -> dict:
#     return {"Content-Type": "application/json"}

