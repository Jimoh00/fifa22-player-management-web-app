import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "API is running"})

def get_db():
    conn = sqlite3.connect('players.db')
    conn.row_factory = sqlite3.Row

    return conn 

@app.route("/players")
def get_players():
    filter_club = request.args.get("club_name")
    filter_nationality = request.args.get("nationality_name")
    filter_position = request.args.get("player_positions")
    filter_name = request.args.get("short_name")
    conn = get_db()

    query = "SELECT * FROM players WHERE 1=1"
    params = []

    if filter_name:
        query += " AND short_name LIKE ?"
        params.append(f"%{filter_name}%")
    if filter_club:
        query += " AND club_name=?"
        params.append(filter_club)
    if filter_nationality:
        query += " AND nationality_name=?"
        params.append(filter_nationality)
    if filter_position:
        query += " AND player_positions LIKE ?"
        params.append(f"%{filter_position}%")

    query += " LIMIT 60"

    players = conn.execute(query,params).fetchall()
    conn.close()
    
    return jsonify([dict(p) for p in players ])
        
@app.route("/players/<int:id>")
def get_player(id):
    conn = get_db()
    player = conn.execute("SELECT * FROM players WHERE id = ?", (id,)).fetchone()
    conn.close()
    if player is None:
        return jsonify({"message": "Player not found"}), 404
    return jsonify(dict(player))

@app.route("/players/top")
def get_top_player():
    conn = get_db()
    players = conn.execute("""
        SELECT short_name, club_name, nationality_name, overall, player_positions
        FROM players
        ORDER BY overall DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return jsonify([dict(p) for p in players])


@app.route("/players/hidden-gems")
def get_hidden_gems():
    conn = get_db()
    players = conn.execute("""
        SELECT * FROM players
        WHERE (potential - overall) >= 10
        AND age <= 23
        ORDER BY potential DESC
        LIMIT 20
    """).fetchall()
    conn.close() 
    return jsonify([dict(p) for p in players])

@app.route("/players/compare")
def compare_players():
    p1 = request.args.get("p1")
    p2 = request.args.get("p2")
    conn = get_db()
    player1 = conn.execute("SELECT * FROM players WHERE short_name LIKE ?", (f"%{p1}%",)).fetchone()
    player2 = conn.execute("SELECT * FROM players WHERE short_name LIKE ?", (f"%{p2}%",)).fetchone()
    conn.close()
    return jsonify({
        "player1": dict(player1) if player1 else None,
        "player2": dict(player2) if player2 else None
    })

@app.route("/nationalities")
def get_nationalities():
    conn = get_db()
    result = conn.execute("SELECT DISTINCT nationality_name FROM players ORDER BY nationality_name").fetchall()
    conn.close()

    return jsonify([row["nationality_name"] for row in result])

@app.route("/clubs")
def get_clubs():
    conn = get_db()
    result = conn.execute("SELECT DISTINCT club_name FROM players ORDER BY club_name").fetchall()
    conn.close()

    return jsonify([row["club_name"] for row in result])

@app.route("/player_name")
def get_players_name():
    conn = get_db()
    result = conn.execute("SELECT DISTINCT short_name FROM players ORDER BY short_name").fetchall()
    conn.close
    return jsonify([row["short_name"] for row in result])

@app.route("/positions")
def get_positions():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT player_positions FROM players ORDER BY player_positions").fetchall()
    conn.close()
    
    positions = set()
    for row in rows:
        if row["player_positions"]:
            for pos in row["player_positions"].split(","):
                positions.add(pos.strip())
    
    return jsonify(sorted(list(positions)))


port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
