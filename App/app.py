from flask import Flask, render_template, request
from generate import search_similar_chunks, generate_answer  

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    context = ""
    if request.method == "POST":
        user_prompt = request.form["prompt"]
        context = search_similar_chunks(user_prompt)
        answer = generate_answer(context, user_prompt, max_tokens=300)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)

