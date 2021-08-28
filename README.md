# CSV-to-JSON
Simple Flask API with single endpoint that receive CSV file of products and return JSON response of the top product

### Installing Dependencies for the project

1. **Python** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, run:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

4. **Installing the RabbitMQ Server** - RabbitMQ is open source message broker software (sometimes called message-oriented middleware) that implements the Advanced Message Queuing Protocol (AMQP).
You can downdload it from [RabbitMQ](https://www.rabbitmq.com/download.html), or you can use [community Docker image](https://registry.hub.docker.com/_/rabbitmq/).

If you want to run it on Docker execute this:
```bash
docker run -d -p 5672:5672 rabbitmq
```
5. **Running the Celery worker server**

You can now run the worker by executing our program with the worker argument:
```bash
celery -A app.celery worker --loglevel=INFO
```