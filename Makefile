build::
	docker build -t test-redirect .

run::
	docker stop test-redirect || true && docker rm test-redirect || true
	docker run -it -d  --name test-redirect -p 8080:80 --mount type=bind,source="$(CURDIR)",target=/code/src test-redirect

test::
	docker exec -it test-redirect pytest -vv

shell::
	docker exec -it test-redirect bash

all: build run test