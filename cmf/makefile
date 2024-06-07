.PHONY: all client server

all: client server

server:
	uvicorn s:app --host 0.0.0.0 --port 8000

client:
	python3 c.py

clean:
	rm -rf *.pyc __pycache__/ upload
