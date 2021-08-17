from invoke import task

@task
def format(c):
    c.run("black rest_api_with_cdk/* src/* tests/*")