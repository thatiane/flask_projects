from flask import Flask
from string import Template
import requests

def is_url_ok(url):
    return 200 == requests.head(url).status_code

HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<head>
   <title>My Video App</title>
   <style>
      body{
          text-align: center;
          background-color: #FFF;
      }
      h2{
          margin: 14px auto;
      }

      iframe{
          width: 80%;
          height: 600px;
      }
   </style>
</head>
<body>
    <h2>${headline}</h2>
    <iframe src="https://www.youtube.com/embed/${youtube_id}" frameborder="1" allowfullscreen></iframe>
</body>""")

app = Flask(__name__)
@app.route('/')
def homepage():
    youtube_url = 'https://www.youtube.com/watch?v=%s' % ('YQHsXMglC9A')
    headline_html = """<a href="{url}">YouTube video: ADELE-HELLO</a>&emsp;<a href="/videos/">videos&#8811;</a>""".format(url=youtube_url)
    all_html = HTML_TEMPLATE.substitute(headline=headline_html, youtube_id='YQHsXMglC9A')
    return all_html

@app.route('/videos/<vid>')
def videos(vid):
    youtube_url = 'https://www.youtube.com/watch?v=' + vid
    if True == is_url_ok(youtube_url):
        headline_html = """<a href="{url}">YouTube video: {id}</a>""".format(url=youtube_url, id=vid)
        all_html = HTML_TEMPLATE.substitute(headline=headline_html, youtube_id=vid)
        return all_html
    else:
        headline_html = """<title>My Video App</title><h2 style="text-align: center;">YouTube video <u>{id}</u> does not exist</h2>""".format(id=vid)
        return headline_html

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)