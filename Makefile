build:
	docker build -t sgp_bot .
	docker tag sgp_bot 811022626/sgp_bot:latest
	docker push 811022626/sgp_bot:latest
	docker tag sgp_bot cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:docker
	docker push cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:docker

run:
	docker run --env-file=./.env_dev

push:
	docker tag sgp_bot 811022626/sgp_bot:docker
	docker push 811022626/sgp_bot:docker
	docker tag sgp_bot cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:docker
	docker push cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:docker

run_prod:
	docker run -rm --env-file=./config/.env_prod cr.yandex/crpfhht4qar8fp15gkte/sgp_bot:docker


docker_clean:
	docker images purge
	docker image prune -a
	docker system prune -a --volumes