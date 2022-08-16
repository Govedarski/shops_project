from config import create_app
from db import db

app = create_app()


@app.after_request
def return_response(response):
    db.session.commit()
    return response


if __name__ == '__main__':
    app.run()
