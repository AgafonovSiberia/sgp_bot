
build:
	docker build -t sgp_bot .

run:
	docker run --env-file=.env_dev sgp_bot

build_hub:
	docker build -t 811022626/sgp_bot .

run_hub:
	docker run --env-file=.env_dev 811022626/sgp_bot
