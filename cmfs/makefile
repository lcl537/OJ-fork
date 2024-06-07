.PHONY: all rc rs

all: rc rs

rs:
	uvicorn s:app --reload

rc:
	python3 c.py

clean:
	rm -rf *.pyc __pycache__/ upload
