.PHONY: all rc rs

all: rc rs

rs:
	uvicorn s:app --host=0.0.0.0 --port=8000

rc:
	python3 c.py

clean:
	rm -rf *.pyc __pycache__/ upload
