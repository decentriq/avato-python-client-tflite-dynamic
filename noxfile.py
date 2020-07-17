import os
import nox

@nox.session(python=["python3.6", "python3.7"])
def tests(session):
    env = {
        "TEST_API_TOKEN_1": os.environ["TEST_API_TOKEN_1"],
    }
    session.install("pytest")
    session.run("pip", "install", ".")
    session.run("pytest", "tests/", env=env)
