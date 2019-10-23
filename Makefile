all: upgrade

update:
	docker pull kukker/lightnovel-crawler:latest

upgrade: update
	docker service update --force --image kukker/lightnovel-crawler:latest lightnovel-crawler_crawler

deploy: delete
	docker stack deploy --compose-file docker-compose.yml lightnovel-crawler

delete:
	-docker stack rm lightnovel-crawler_crawler
