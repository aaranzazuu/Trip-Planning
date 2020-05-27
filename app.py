from flask import Flask

# Flask Setup
app = Flask(__name__)

# Def Home
@app.route("/")
def home():
    return (
        f"Welcome to the Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


if __name__ == "__main__":
    app.run(debug=True)
