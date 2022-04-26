build:
	docker build -t sgp_bot .

run:
	docker run --env-file=.env_dev sgp_bot

push:
	docker push 811022626/sgp_bot:latest

run_prod:
	docker run -rm --env-file=/home/agafonov/dev/env/.env_prod sgp_bot


build_kaniko:
	docker run -v /home/agafonov/dev/sgp_bot:/workspace \
			-v /home/agafonov/.docker/config.json:/kaniko/.docker/config.json \
			gcr.io/kaniko-project/executor:latest \
			--dockerfile /workspace/Dockerfile\
			--context /workspace/ \
			--cache=true \
			--destination=811022626/sgp_bot:kaniko

run_kaniko:
	docker run -rm --env-file=.env_dev 811022626/sgp_bot:kaniko



