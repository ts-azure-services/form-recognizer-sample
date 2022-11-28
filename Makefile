install:
	#conda create -n fr python=3.8 -y; conda activate fr
	pip install python-dotenv
	pip install azure-ai-formrecognizer

infra:
	./setup/create-cognitive-resource.sh

workflow:
	python read_model.py
