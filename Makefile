setup:
# sudo apt -y install python3.8-venv
# python3 -m venv ~/.ncaa_mvp_env
	virtualenv -p python3 env
	# source env/bin/activate

install:
	python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt


deploy:
	# gcloud auth login --cred-file="/home/yunuo6/Deployment/key.json" --quiet
	export PROJECT_ID=prod-dev-env
	gcloud projects add-iam-policy-binding ${PROJECT_ID} \
	--member serviceAccount:testaccount@${PROJECT_ID}.iam.gserviceaccount.com \
	--role roles/owner
	
	gcloud iam service-accounts keys create ~/key.json \
	--iam-account testaccount@${PROJECT_ID}.iam.gserviceaccount.com

	gcloud app deploy --project=prod-dev-env --version=dev 



all: install deploy 
