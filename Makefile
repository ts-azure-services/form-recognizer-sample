install:
	#conda create -n fr python=3.8 -y; conda activate fr
	pip install python-dotenv
	pip install azure-ai-formrecognizer

infra:
	./setup/create-cognitive-resource.sh

sample_workflow:
	python ./scripts/read_model.py

ar_memo:
	python ./scripts/full_memo_generation.py

ocr_from_doc:
	python ./scripts/pdf_model.py --data_input_file "./data/sample.pdf"\
		--output_path "./outputs/ocr_sample_pdf.txt"
