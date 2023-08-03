from flask import Flask, jsonify
from routes.users import users_blueprint

app = Flask(__name__)

# Register the users_blueprint with the app
app.register_blueprint(users_blueprint)


@app.route('/',methods=['GET'])
def home():
    return jsonify({'success':'true'})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)