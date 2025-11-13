# main.py
from www import app

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=7435, debug=True, use_reloader=False)