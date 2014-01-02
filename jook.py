from flask import Flask, render_template, url_for, redirect, request
import json

app = Flask(__name__)

import dropbox
app_key = 'cl4r9w05dblwqhx'
app_secret = '53br9rm0jljhire'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

userInfo = ''
client = ''

@app.route('/')
def main():
    authorize_url = flow.start()
    return render_template('index.html', url=authorize_url)

def getLinks(m):
    songList = []
    contents = m["contents"]
    print contents

    for entry in contents:
        song = entry["path"]
        if (song.endswith('.mp3')):
            songList.append(song)

    return songList

@app.route('/player/')
def player():
    folder_metadata = client.metadata('/jook/')
    songList = getLinks(folder_metadata)
    links = []

    for song in songList:
        link = client.share(song, short_url=False)["url"]
        link = link.replace('www.dropbox.com', 'dl.dropboxusercontent.com', 1)
        links.append(link)

    return render_template('player.html', songs=links, jquery=url_for('static', filename='jquery-1.10.2.js'), styles=url_for('static', filename='styles.css'))


def auth(key):
    access_token, user_id = flow.finish(key)
    global client
    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()
    global userInfo 
    userInfo = client.account_info()
    return redirect(url_for('.player'))

@app.route('/', methods=['POST'])
def req():
    key = request.form['key']
    return auth(key)

if __name__ == '__main__':
    app.run(debug = True)

