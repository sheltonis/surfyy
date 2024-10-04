from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Surfyy</h1>
    <form method="POST" action="/proxy">
        <input type="text" name="url" placeholder="Enter URL to browse">
        <input type="submit" value="Go">
    </form>
    '''

@app.route('/proxy', methods=['POST'])
def proxy():
    url = request.form.get('url')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    try:
        response = requests.get(url)
        return Response(response.content, content_type=response.headers['Content-Type'])
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/styles.css">
        <title>My Awesome Proxy</title>
    </head>
    <body>
        <h1>My Awesome Proxy</h1>
        <form method="POST" action="/proxy">
            <input type="text" name="url" placeholder="Enter URL to browse" required>
            <input type="submit" value="Go">
        </form>
    </body>
    </html>
    '''

@app.route('/proxy', methods=['POST'])
def proxy():
    url = request.form.get('url')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Update all relative URLs in <a> and <img> tags
        for tag in soup.find_all(['a', 'img']):
            if tag.name == 'a':
                tag['href'] = urljoin(url, tag.get('href'))
            elif tag.name == 'img':
                tag['src'] = urljoin(url, tag.get('src'))

        return Response(str(soup), content_type=response.headers['Content-Type'])

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}", 400
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
