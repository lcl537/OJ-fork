.PHONY: all rc rs

all: rc rs

rs:
	uvicorn s:app --host=118.89.82.251 --port=80

rc:
	python3 c.py

clean:
	rm -rf *.pyc __pycache__/ upload
