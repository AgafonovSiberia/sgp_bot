build:
	docker build -t sgp_bot .

run:
	docker run --env-file=./config/.env_dev sgp_bot

push:
	docker push 811022626/sgp_bot:latest

run_prod:
	docker run -rm --env-file=./config/.env_prod sgp_bot


build_kaniko:
	docker run -v $(PWD):/workspace \
			-v ~/.docker/config.json:/kaniko/.docker/config.json \
			gcr.io/kaniko-project/executor:latest \
			--dockerfile /workspace/Dockerfile\
			--context /workspace/ \
			--cache=true \
			--destination=811022626/sgp_bot:kaniko
run_kaniko:
	docker run --env-file=./config/.env_dev 811022626/sgp_bot:kaniko



