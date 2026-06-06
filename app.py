from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dataset")
def dataset():
    return render_template("dataset.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/visualizations")
def visualizations():
    return render_template("visualizations.html")


@app.route("/alerts")
def alerts():
    return render_template("alerts.html")


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
