# Tibber Challenge (Cleaning Robot)

Author: [Jakob Schmitt](https://www.linkedin.com/in/jakob-schmitt/), June 2022.

In this README, you will learn how to set up a development environment and
run tests. The file also contains some pointers to important parts of the code.

## Usage

### Requirements:
* [Docker](https://docs.docker.com/get-docker/) (installed and running)

### Installation:
1. **Clone the respository:**
```zsh
git clone https://github.com/JokusPokus/tibber-challenge.git
cd ./tibber_challenge
```

2. **Set the necessary environment variables** in an `.env` file at `tibber_challenge/tibber_challenge/.env`.
You can find the required environment variables in the `.env.dist` file.

    If you would like to use the `docker-compose` script, you need to specify
some environment variables to create the database. Do so by adding a file
at `tibber_challenge/tibber_challenge/.env.db`, based on the requirements 
in `tibber_challenge/tibber_challenge/.env.db.dist`.


3. **Run the `docker-compose` script** to spin up the containers:
```zsh
docker-compose up -d --build
```

Note that a `docker-compose.prod.yml` file suited for deployment to production is
also provided and can be used as such:
```zsh
docker-compose -f docker-compose.prod.yml up -d --build
```


4. **Run the test suite:**
```zsh
docker-compose exec web pytest
```


## Techstack
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [pytest](https://docs.pytest.org/en/6.2.x/) (for development and testing)


## Pointers
This section will help you find the most relevant parts of the code.

* `tibber_challenge/robot/`: This is a Django app containing all the business logic.
  * `models.py`: Defines the `executions` database table
  * `views.py`: Handles requests to the API endpoint
  * `serializers.py`: Serialization of `Execution` instances
  * `tests.py`: API (end-to-end) tests
  * `cleanbot/`: A package to calculate the robot's cleaning success

Please note that I implemented two different algorithms to find the number
of unique vertices cleaned by the robot. The first one (implemented
via `trackers.SimpleRobotTracker`) is a 'naive' approach and performs
poorly for large problem sizes. The optimized one (implemented via 
`trackers.RobotTracker`) takes advantage of representing cleaned vertices as
ranges rather than single points in the grid.


## Refactored version
I refactored the code to make it more extensible by enabling dependency
inversion. For example, I defined an abstract base class (Python's way of specifying
shared interfaces for inheriting classes) for office representations. This 
makes it easier to implement an office with different specifications (e.g., 
with a different kind of grid or constraints).

However, this feels a bit over-engineered for the current challenge. Hence, 
I kept the changes in a separate branch `refac`.