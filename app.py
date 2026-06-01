import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open('results_data.json') as f:
    records = json.load(f)

# Build lookup dict
lookup = {str(r['roll']): r for r in records}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    roll = request.args.get('roll', '').strip()
    if not roll:
        return jsonify({'error': 'Please enter a roll number'})
    
    # Try partial match
    results = [r for r in records if roll in str(r['roll'])]
    
    if not results:
        return jsonify({'error': f'No student found with roll number "{roll}"'})
    
    results.sort(key=lambda x: x['rank'])
    return jsonify(results[:20])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
