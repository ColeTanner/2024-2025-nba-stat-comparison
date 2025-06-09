from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
namesFile = "players.txt"
load_dotenv()
api_key = os.getenv('API_KEY')



def loadNames():
    playerNames = []
    try:
        with open(namesFile, "r", encoding="utf-8") as names:
            playerNames = [line.strip() for line in names.readlines()]
            
    except Exception as e:
        print(f"There was an error loading the player names: {e}")
    return playerNames


@app.route('/api/players', methods = ["GET"])
def getPlayers():
    input = request.args.get('search').lower()
    names = loadNames()
    viableOption = [player for player in names if input in player[0:len(input)].lower()]
    return jsonify({"players": [{"id": idx + 1, "name": player} for idx, player in enumerate(viableOption)]})



baseurl = 'https://api-nba-v1.p.rapidapi.com'


headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

#player_name = 'Anthony'  #Replace with the name of the player
#player_last = 'edwards'
@app.route('/api/searchPlayerID', methods=['GET'])
def searchPlayerID():

    
    name = request.args.get('name')
    if ' ' in name and name[len(name) - 1] != ' ' and name[0] != ' ':   
        fname, lname = name.split()
    else:
        return jsonify({"playerID": f"notAvailable"})
    
    url = f'https://api-nba-v1.p.rapidapi.com//players?search={lname}'

    try: 
        response = requests.get(url, headers=headers)
    except TypeError:
        return jsonify({"playerID": f"notAvailable"})


    if response.status_code == 200:
        data = response.json()
        if data.get('response'):
            found = False
            player_id = ''
            for item in data.get('response'):
                if item['firstname'].lower() == fname.lower():
                    player = item  # Get the first player in the response
                    player_id = player['id']  # Extract the Player ID
                    found = True
            #print(f"Player ID for {player_name}: {player_id}")
            if found:
                if player_id != '':
                    return jsonify({'playerID': f'{player_id}'})
            else:
                 return jsonify({
                'points': 'N/A',
                'rebounds':'N/A',
                'assists': 'N/A',
                 })
        else:
            print(f"No player found for {fname} {lname}")
            return jsonify({"playerID": -1})
    else:
        print(f"Error fetching player data: {response.status_code}")
        return jsonify({"playerID": -1})


@app.route('/api/fetch_player_stats', methods=['GET'])
def fetch_player_stats():
    player = request.args.get('player')
    season = 2024
    url = f'{baseurl}/players/statistics?id={player}&season={season}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for any HTTP errors
        data = response.json()  # Convert the response to JSON format
        # Check if we got valid data
        if data and data.get('response'):
            points = 0
            assists = 0
            rebounds = 0
            mins = 0
            steals = 0
            turnovers = 0
            blocks = 0
            field_goal_percentage = 0
            for item in data.get('response'): 
                #player = data['response'][0]  # Get the first player in the response
                mins += int(item['min'])
                points += item['points']
                assists += item['assists']
                rebounds += item['totReb']
                steals += item['steals']
                turnovers += item['turnovers']
                blocks += item['blocks']
              #  field_goal_percentage += item['fgp']
            
            mins = float(mins) / (data['results'] - 1)
            points = float(points) / (data['results'] - 1)
            assists = float(assists) / (data['results'] - 1)
            rebounds = float(rebounds) / (data['results'] - 1)
            steals = float(steals) / (data['results'] - 1)
            turnovers = float(turnovers) / (data['results'] - 1)
            blocks = float(blocks) / (data['results'] - 1)



            return jsonify({
                'mins': round(mins,1),
                'points': round(points,1),
                'rebounds': round(rebounds,1),
                'assists': round(assists,1),
                'steals': round(steals,1),
                'turnovers': round(turnovers,1),
                'blocks': round(blocks,1)
            })
  
        else:
             return jsonify({
                'mins' : 'N/A',
                'points': 'N/A',
                'rebounds':'N/A',
                'assists': 'N/A',
                'steals': 'N/A',
                'turnovers': 'N/A',
                'blocks': 'N/A'
            })
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player stats: {e}")
        return jsonify({
                'mins' : 'N/A',
                'points': 'N/A',
                'rebounds':'N/A',
                'assists': 'N/A',
                'steals': 'N/A',
                'turnovers': 'N/A',
                'blocks': 'N/A'
            })
       


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
