from flask import Flask, render_template, url_for, redirect, request, flash
from soc_graph import SocialGraph


app = Flask(__name__)
app.secret_key = "smth secret"


@app.route('/',  methods=['POST', 'GET'])
def graph():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        graph = SocialGraph(nickname)
        if not graph.build_graph():
            flash("No such user.")
            return redirect(url_for('graph'))
        else:
            graph.draw()
            graph.save(f"static/data/{nickname}.png")
            return redirect(url_for('show_graph', nickname=nickname))
    return render_template("home.html")


@app.route('/path',  methods=['POST', 'GET'])
def path():
    if request.method == 'POST':
        nickname_1 = request.form.get('nickname_1')
        nickname_2 = request.form.get('nickname_2')

        graph = SocialGraph(nickname_1, nickname_2)
        if not graph.social_path():
            flash("No path between users.")
            return redirect(url_for('path'))
        else:
            graph.draw()
            graph.save(f"static/data/from_{nickname_1}_to_{nickname_2}.png")
            return redirect(url_for('show_graph', nickname=f"from_{nickname_1}_to_{nickname_2}"))
    return render_template("path.html")


@app.route('/<nickname>')
def show_graph(nickname):
    return render_template("soc_graph.html", path=f"../static/data/{nickname}.png")


if __name__ == '__main__':
    app.run()
