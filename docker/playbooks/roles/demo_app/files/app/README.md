Absoltely awful flask app.

I was following the tutorial but there wasn't a referent to the source, so I decided to hack my own.

It is possible to run this locally, the default `config.json` uses sqlite.


```sh
export FLASK_APP=app.py

# Create db and migrate
flask db init
flask db migrate
flask db upgrade

# // OR //
# Run the idempotent db script which is what the ansible tasks run
sh init_db.sh

# Start the server
flask run
```