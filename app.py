# importing Flask
from flask import Flask, jsonify

# Creating an app
app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    return (
        f"Welcome to my Hawaii weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"




if __name__ == "__main__":
    app.run(debug=True)