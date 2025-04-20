import pytest
import requests_mock
from app import app as flask_app

# Minimal mock brewery item containing only checked keys
MOCK_BREWERY_ITEM = {
    "id": "5128df48-79fc-4f0f-8b52-d06be54d0cec",
    "name": "(405) Brewing Co",
    "brewery_type": "micro"
}

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_get_breweries(client):
    """Test the /breweries endpoint."""
    # Mock the external API call
    with requests_mock.Mocker() as m:
        mock_url = "https://api.openbrewerydb.org/v1/breweries"
        mock_response_data = [MOCK_BREWERY_ITEM]
        m.get(mock_url, json=mock_response_data)

        # Make a request to the /breweries endpoint
        response = client.get('/breweries')

        # Assertions
        assert response.status_code == 200
        response_data = response.get_json()
        assert isinstance(response_data, list)
        assert len(response_data) > 0
        assert response_data[0]['brewery_type'] == MOCK_BREWERY_ITEM['brewery_type']
        assert 'id' in response_data[0]
        assert 'name' in response_data[0]
        assert 'brewery_type' in response_data[0]
