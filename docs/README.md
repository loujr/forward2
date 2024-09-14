# Forward 2

## Setup 

This repository operates based on two services an API and a UI component. The AI components contain the framework for creating the URL and serving the short link. The UI component does not currently contain any buttons for user interaction but rather a framework for those to be created later. This is displayed on a website template that contains a simple splash page but also acts as the redirect that takes the user to the final website. 

The framework of this application is built on flask. The service configuration files create two sockets for each of the services that then utilize Gunicorn workers to handle the task of generating a short link and redirection. The database is currently SQL lite that creates and reads from a urls.db file.

To begin start by installing `requirements.txt` and setting up the configuration files for the two python services. I placed my files in the `/etc/systemd/system` directory but you can modify this location to fit your needs.

```
pip install -r requirements.txt 
```

### API 

Location: `webapp.py`

To setup this service. Start by creating a service configuration file. This is an example of my testing environment but you can modify this to fit the needs of your server. 


```
[Unit]
Description=API Configuration File
After=network.target

[Service]
User=fwd2
Group=www-data
WorkingDirectory=/home/USER/api
Environment="PATH=/home/USER/api/venv/bin"
ExecStart=/usr/local/bin/gunicorn --workers 5 --bind unix:fwd2.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

### UI

Location: `website/website.py`

To setup this service. Start by creating a service configuration file. This is an example of my current testing environment but you can modify this to fit the needs of your server.

```
[Unit]
Description=Website Configuration File
After=network.target

[Service]
User=fwd2
Group=www-data
WorkingDirectory=/home/USER/api/website
Environment="PATH=/home/USER/api/venv/bin"
ExecStart=/usr/local/bin/gunicorn --workers 5 --bind unix:fwd2.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

## Running the application

After the configuration files are created you can start the services by running the following commands. You can name the services whatever you would like.

```
sudo systemctl start api.service
sudo systemctl start ui.service
```

Webapp.py will create a websocket called `fwd2.sock` and a database file `urls.db`. This is a key value pair containing a six letter string and the origional URL eg. `('QrEFYy':'example.com')`. This is pair is read from `website.py` and then the user is redirected to the origional URL.


## Testing

To test the application you can use the following curl commands. 

``` 
test_webapp.py
```

This is a series of unit tests that test the API endpoints and verify that the correct response is returned. 

**Note:** There is a known issue where running these tests inside your local environment will cause the database to be locked. This is because the tests are running in parallel and the database is not able to handle the requests. This is a known issue and will be fixed in the future. For best results run the tests in a CI/CD pipeline.