from flask import Flask, request, render_template
from plant_counter import Plant_Counter
from cfbmatchup import Analyzer
import StatBuilder


app = Flask(__name__)

cfb_analyzer = Analyzer()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/plant-counter')
def plant_counter():
    return render_template('plant-counter.html')


@app.route('/plant-counter', methods=['POST'])
def plant_counter_post():
    input = request.form["text"].split('\n')
    pc = Plant_Counter()
    pc.makePlantList(input)
    output = pc.getCountText()
    return render_template('plant-counter.html', results=output)

@app.route('/matchup-analyzer')
def matchup_analyzer():
    return render_template('matchup-analyzer.html', teams=StatBuilder.getTeams())

@app.route('/matchup-analyzer', methods=['POST'])
def fetchByPostedTeam():
    stats, keys, niceKeys = matchup_analyzer_post(request.form.get('teamA'))
    return render_template('matchup-analyzer.html', teamStats=stats, keys=keys, niceKeys=niceKeys)

def matchup_analyzer_post(team):

    stats = StatBuilder.buildStats(team)
    keys = list(stats.keys())
    keys.sort()
    keys.remove('date')

    niceKeys = StatBuilder.getNiceKeys()

    return stats, keys, niceKeys

if __name__ == '__main__':
    app.run()