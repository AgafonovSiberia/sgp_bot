build:
	docker build -t sgp_bot .
	docker tag sgp_bot 811022626/sgp_bot:latest
	docker push 811022626/sgp_bot:latest
	docker tag sgp_bot cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:latest
	docker push cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:latest

run:
	docker run --env-file=./.env_dev

push:
	docker tag sgp_bot 811022626/sgp_bot:latest
	docker push 811022626/sgp_bot:latest
	docker tag sgp_bot cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:latest
	docker push cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:latest

run_prod:
	docker run -rm --env-file=./config/.env_prod cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:latest


build_kaniko:
	docker run -v $(PWD):/workspace \
			-v ~/.docker/config.json:/kaniko/.docker/config.json \
			gcr.io/kaniko-project/executor:latest \
			--dockerfile /workspace/Dockerfile\
			--context /workspace/ \
			--cache=true \
			--destination=811022626/gp_bot_kaniko:latest

run_kaniko:
	docker run --env-file=./.env_dev 811022626/gp_bot_channel:latest


docker_clean:
	docker images purge
	docker image prune -a
	docker system prune -a --volumes