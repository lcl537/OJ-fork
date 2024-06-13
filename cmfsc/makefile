.PHONY: all rc rs

all: rc rs

rs:
	uvicorn s:app

rc:
	python3 c.py

re:
	uvicorn e:app

clean:
	rm -rf *.pyc __pycache__/ upload
