# To create Azure infrastructure
sub-init:
	echo "SUB_ID=<input subscription_id>" > sub.env

venv_setup:
	rm -rf .venv
	python3.11 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	# .venv/bin/python -m pip install -r ./requirements.txt
	# source .tutorial_venv/bin/activate # not possible with Makefile

infra:
	./setup/create-cognitive-resource.sh

sample_workflow:
	.venv/bin/python ./scripts/read_model.py

ar_memo:
	.venv/bin/python ./scripts/full_memo_generation.py

ocr_from_doc:
	.venv/bin/python ./scripts/pdf_model.py --data_input_file "./data/sample.pdf"\
		--output_path "./outputs/ocr_sample_pdf.txt"

# Commit local branch changes
branch=$(shell git symbolic-ref --short HEAD)
now=$(shell date '+%F_%H:%M:%S' )
git-push:
	git add . && git commit -m "Changes as of $(now)" && git push -u origin $(branch)

git-pull:
	git pull origin $(branch)
