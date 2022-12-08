run:
	docker-compose up --build

stop:
	docker-compose stop

clear_data:
	docker-compose down -v

run_dev:
	python -m app
