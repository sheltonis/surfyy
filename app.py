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
        <title>Surfyy</title>
    </head>
    <body>
        <h1>Surfyy</h1>
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
        print(f"Fetching URL: {url}")  # Debugging line
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Log the response content type
        print(f"Response content type: {response.headers['Content-Type']}")  # Debugging line

        # Update all relative URLs in <a>, <img>, <link>, and <script> tags
        for tag in soup.find_all(['a', 'img', 'link', 'script']):
            if tag.name == 'a':
                tag['href'] = urljoin(url, tag.get('href'))
            elif tag.name == 'img':
                tag['src'] = urljoin(url, tag.get('src'))
            elif tag.name == 'link' and tag.get('href'):
                tag['href'] = urljoin(url, tag.get('href'))
            elif tag.name == 'script' and tag.get('src'):
                tag['src'] = urljoin(url, tag.get('src'))

        # Add a Content Security Policy to allow scripts to load
        headers = {
            'Content-Security-Policy': "default-src 'self'; script-src 'unsafe-inline' 'unsafe-eval';"
        }

        return Response(str(soup), content_type=response.headers['Content-Type'], headers=headers)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log to console for debugging
        return f"HTTP error occurred: {http_err}", 400
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")  # Log to console for debugging
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
