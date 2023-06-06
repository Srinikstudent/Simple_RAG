from flask import Flask, request
import json
import sqlite3
import nlp

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    target_id = request.headers.get('ID')
    
    # web.py
    conn = sqlite3.connect('storage/db/nocobase.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if ('compliance',) in tables:

        cursor.execute("SELECT * FROM compliance;")
        columns = [column[0] for column in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for row in data:
            json_row = dict(zip(columns, row))
            json_data.append(json_row)

        json_output = json.dumps(json_data, indent=4)

        for item in json_data:
            if item.get('id') == int(target_id):
                nlp_output = nlp.extract_rules(item['input_regulations'])
                output = ', '.join(nlp_output)
                print(output)
                cursor.execute(
                    "UPDATE compliance SET output = ? WHERE id = ?", (output, target_id))
                conn.commit()
                
        return "NLP output finish"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
