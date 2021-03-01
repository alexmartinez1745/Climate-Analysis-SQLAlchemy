from flask import Flask

app = Flask(__name__)

# Flask routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

if __name__ == "__main__":
    app.run(debug=True)