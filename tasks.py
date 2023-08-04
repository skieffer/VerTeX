from invoke import task


@task
def clean(c):
    c.run("rm -rf *.egg-info build dist")


@task
def build(c):
    c.run("python -m build")


@task
def dist(c):
    c.run("python -m twine upload dist/*")


@task
def testdist(c):
    c.run("python -m twine upload --repository testpypi dist/*")
