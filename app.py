from flask import Flask, request

app = Flask(__name__)

post_counter = 0

@app.route('/', methods=['GET', 'POST'])
def count_posts():
    global post_counter
    if request.method == 'POST':
        post_counter += 1
        return f"POST request received. Count: {post_counter}"
    else:
        return f"POST request count: {post_counter}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
