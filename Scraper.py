from bs4 import BeautifulSoup
import requests

# Edited to work with python 3 from https://github.com/loisaidasam/stravalib-scraper
VERSION = '0.1.0'


class StravaScraper(object):
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    USER_AGENT = "Mozilla/5.0"

    HEADERS = {'User-Agent': USER_AGENT}

    BASE_URL = "https://www.strava.com"

    URL_LOGIN = "%s/login" % BASE_URL
    URL_SESSION = "%s/session" % BASE_URL
    URL_DASHBOARD = "%s/dashboard" % BASE_URL

    is_authed = False

    # The content from the /dashboard request post-login (if you'd like to
    # reference it at some point)
    dashboard_content = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()

    def get_page(self, url):
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def login(self):
        response = self.get_page(StravaScraper.URL_LOGIN)
        soup = BeautifulSoup(response.content, 'html.parser')
        utf8 = soup.find_all('input',
                             {'name': 'utf8'})[0].get('value').encode('utf-8')
        token = soup.find_all('input',
                              {'name': 'authenticity_token'})[0].get('value')
        data = {
            'utf8': utf8,
            'authenticity_token': token,
            'plan': "",
            'email': self.email,
            'password': self.password,
        }
        response = self.session.post(StravaScraper.URL_SESSION,
                                     data=data,
                                     headers=StravaScraper.HEADERS)
        response.raise_for_status()
        # Simulate that redirect here:
        response = self.get_page(StravaScraper.URL_DASHBOARD)
        #assert("<h2>Activity Feed</h2>".encode('utf-8') in response.content)
        self.is_authed = True
        # Save this in case someone wants it later...
        self.dashboard_content = response.content