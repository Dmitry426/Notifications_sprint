from app import app


@app.route("/")
def home():
    return "И снова здравствуйте!"
