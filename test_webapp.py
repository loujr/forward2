import pytest
from flask_testing import TestCase
from webapp import app, shortened_urls, generate_short_url

class TestFlaskApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_get(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')

    def test_index_post(self):
        long_url = 'https://www.example.com'
        response = self.client.post('/', data={'long_url': long_url})
        self.assert200(response)
        short_url = response.data.decode().split('/')[-1]
        assert shortened_urls[short_url] == long_url

    def test_redirect_url(self):
        long_url = 'https://www.example.com'
        short_url = generate_short_url()
        shortened_urls[short_url] = long_url
        response = self.client.get(f'/{short_url}')
        self.assertRedirects(response, long_url)

    def test_redirect_url_not_found(self):
        response = self.client.get('/nonexistent')
        self.assert404(response)

    def test_api_hello_world(self):
        response = self.client.get('/v2')
        self.assert200(response)
        assert response.data.decode() == "this is api \n"

    def test_api_ip_endpoint(self):
        response = self.client.get('/v2/ip')
        self.assert200(response)
        assert 'origin' in response.json

if __name__ == '__main__':
    pytest.main()