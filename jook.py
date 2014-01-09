from flask import Flask, session, render_template, url_for, redirect, request
import json
import dropbox

app = Flask(__name__)

app_key = 'cl4r9w05dblwqhx'
app_secret = '53br9rm0jljhire'
flow = ''
client = ''

@app.route('/')
def main():
    global flow

    redir_uri = url_for('authenticated', _external=True)
    flow = dropbox.client.DropboxOAuth2Flow(app_key, app_secret, redir_uri, session, 'access_token')
    authorize_url = flow.start()
    return render_template('index.html', auth=authorize_url)

@app.route('/authenticated/')
def authenticated():
    global client

    try:
        access_token, user_id, url_state = flow.finish(request.args)
    except:
        return redirect(url_for('main'))

    client = dropbox.client.DropboxClient(access_token)
    return redirect(url_for('player'))    

def getLinks(m):
    songList = []
    contents = m["contents"]

    for entry in contents:
        song = entry["path"]
        song = song.lower()
        if (song.endswith('.mp3') or song.endswith('.m4a') \
            or song.endswith('.wav') or song.endswith('.ogg')):
            songList.append(song)

    return songList

@app.route('/player/')
def player():
    try:
        client.file_create_folder('/jook')
    except:
        pass

    folder_metadata = client.metadata('/jook/')
    songList = getLinks(folder_metadata)
    links = []

    for song in songList:
        link = client.share(song, short_url=False)["url"]
        link = link.replace('www.dropbox.com', 'dl.dropboxusercontent.com', 1)
        links.append(link)

    return render_template('player.html', songs=links, jquery=url_for('static', filename='jquery-1.10.2.js'), styles=url_for('static', filename='styles.css'))

app.secret_key = ''

if __name__ == '__main__':
    app.run(debug=True)