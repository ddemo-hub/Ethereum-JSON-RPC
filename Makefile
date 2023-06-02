install: 
	sudo apt-get update
	sudo apt-get install python3

init:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

clean:
	rm -rf public/src/containers/__pycache__
	rm -rf public/src/services/__pycache__
	rm -rf public/src/utils/__pycache__
	rm -rf public/tasks/__pycache__
	rm -rf public/__pycache__
	
	rm -rf artifacts
	rm -rf .venv