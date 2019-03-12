# Web Scraper microservice

Simple web scraper microservice. Collect clean texts and images from web pages and store it in database.

##### DONE:
* REST API created with Flask + Flask-RESTPlus and Swagger UI.
* Asynchronous tasks running with Celery + Redis
* Data storage SQLAlchemy + PostgreSQL
* Tests written with Unittest framework

##### TODO:
* More tests...
* Frontend app

## API

API url `http://localhost:5000/api/v1`

Method | Endpoint | Params | Description |
|---|---|---|---|
| POST | /tasks/collect_text | \<string:url> | Delegate task to collect text from page
| POST | /tasks/collect_images | \<string:url> | Delegate task to collect images from page
| GET | /tasks/status/\<string:task_id> | - | Get status of given task
| GET | /resources/texts | - | Get all collected texts
| GET | /resources/texts/\<string:url> | - | Get text collected from one page
| GET | /resources/images | - | Get all collected images (only urls)
| GET | /resources/images/\<string:url> | - | Get images collected from one page (download a .zip)

API docs [localhost:5000/api/v1/docs](http://localhost:5000/api/v1/docs)

## Getting Started

### Prerequisites

Project is running in docker containers, so you only need docker and docker-compose installed.

```
docker
docker-compose
```

### Installing

```
git clone https://github.com/lewyg/web-scraper-microservice
cd web-scraper-microservice
docker-compose build
```

## Running

```
docker-compose up
```

After start you can test api via
[localhost:5000/api/v1/docs](http://localhost:5000/api/v1/docs)

## Running the tests

Tests are running by command inside docker container

```
python manage.py test --verbosity VERBOSITY
```

To run tests and environment

```
docker-compose -p webscrapermicroservice_test up -d db redis && 
docker-compose -p webscrapermicroservice_test run --entrypoint "python manage.py test -v 3" app && 
docker-compose -p webscrapermicroservice_test down -v
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
