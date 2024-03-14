.PHONY: all clean run

PYTHON = python3
SRC_FILE = carbonifer/carbonifer.py

all: run

run:
	$(PYTHON) $(SRC_FILE)

clean:
	# No cleanup needed for this example

dockerbuild:
    docker build -t my_flask_app .

rundocker
	docker run -p 80:80 my_flask_app

