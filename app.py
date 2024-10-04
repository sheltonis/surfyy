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
