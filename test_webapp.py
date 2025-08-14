import pytest
from flask_testing import TestCase
from webapp import app, get_db_connection
import re
import sqlite3

class TestFlaskApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.conn = get_db_connection()
        self.conn.execute('CREATE TABLE IF NOT EXISTS urls (short_url TEXT, long_url TEXT)')

    def tearDown(self):
        self.conn.execute('DROP TABLE urls')
        self.conn.close()

    def test_index_get(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('index.html')
    
    def test_index_post(self):
        long_url = 'https://www.example.com'
        response = self.client.post('/', data={'long_url': long_url})
        self.assert200(response)
        html_string = response.data.decode()
        match = re.search(r'href="([^"]*)"', html_string)
        if match:
            short_url = match.group(1).split('/')[-1]
            url_data = self.conn.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
            assert url_data is not None, "No data found in the database for the given short_url"
            assert url_data['long_url'] == long_url
        else:
            assert False, "URL not found in the response"

    def test_redirect_url(self):
        long_url = 'https://www.example.com'
        short_url = 'test_short_url'
        self.conn.execute('INSERT INTO urls (short_url, long_url) VALUES (?, ?)', (short_url, long_url))
        self.conn.commit()
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



### test commit to trigger webook
