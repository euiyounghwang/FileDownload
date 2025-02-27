import pytest

# https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/

@pytest.mark.skip(reason="no way of currently testing this")
def test_skip():
    assert 1 != 1
    
    
def test_api(mock_client):
    response = mock_client.get("/")
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {"message": "This API allow us to download any files"}
    