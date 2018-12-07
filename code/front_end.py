from flask import *
from model import model
import time


app = Flask(__name__)
db = model()


@app.route('/')
@app.route('/index.html')
def index():
    """
    Page that displays the actions of the bot
    """
    actions = [dict(post_id=row[0], action=row[1], time=row[2], link=row[4]) for row in db.select()]
    
    for i in actions[::-1]:
        i['time'] = time.gmtime(i['time'])
        timeString = time.strftime('%m/%d/%Y -- %H:%M:%S', i['time'] )
        i['time'] = timeString
    return render_template('index.html', actions=actions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
