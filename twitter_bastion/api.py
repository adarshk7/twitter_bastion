from twitter_bastion import app


@app.route('/')
def root():
    return "Hello World!"
