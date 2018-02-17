from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL = 'https://api.fortnitetracker.com/v1/profile/pc/Twitch_Svennoss'
URL = 'https://api.fortnitetracker.com/v1/profile/pc/{}'
headers = {'TRN-Api-Key': '2db9f19b-1143-4de3-8aa1-b00538ef0185'}
# res = requests.get(URL, headers=headers)
# result = res.json()['lifeTimeStats']
# print(result)


def populate_player_data(api_data):
    temporary_dict = {}
    for res in api_data:
        if res['key'] == 'Wins':
            temporary_dict['Wins'] = res['value']
        if res['key'] == 'Kills':
            temporary_dict['Kills'] = res['value']
        if res['key'] == 'Matches Played':
            temporary_dict['Matches'] = res['value']

    return temporary_dict

# print(populate_player_data(result))


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    player_one = None
    player_two = None
    player_one_stats = {}
    player_two_stats = {}
    if request.method == 'POST':
        player_one = request.form.get('player_one_name')
        if player_one:
            player_two = request.form.get('player_name')
        else:
            player_one = request.form.get('player_name')

        player_one_result = requests.get(URL.format(player_one), headers=headers).json()['lifeTimeStats']
        player_one_stats = populate_player_data(player_one_result)

        if player_two:
            player_two_result = requests.get(URL.format(player_two), headers=headers).json()['lifeTimeStats']
            player_two_stats = populate_player_data(player_two_result)

    return render_template('index.html', player_one=player_one, player_two=player_two,
                           player_one_stats=player_one_stats, player_two_stats=player_two_stats)


if __name__ == '__main__':
    app.run(debug=True)
