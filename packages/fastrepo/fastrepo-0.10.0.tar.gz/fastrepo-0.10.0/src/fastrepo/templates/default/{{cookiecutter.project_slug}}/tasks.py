# type: ignore
""" Tasks for {{ cookiecutter.project_slug }} project. """

from pathlib import Path
from shutil import rmtree

from invoke import task

PROJECT_DIR = Path(__file__).parent

SRC_DIR = PROJECT_DIR / "src"
TESTS_DIR = PROJECT_DIR / "tests"
DIST_DIR = PROJECT_DIR / "dist"
DOCS_DIR = PROJECT_DIR / "docs"
DOCS_DIST_DIR = DIST_DIR / "docs"

SRC_FILES = " ".join([str(path) for path in SRC_DIR.glob("**/*.py")])
TEST_FILES = " ".join([str(path) for path in TESTS_DIR.glob("**/*.py")])


@task
def lint(c):
    """Lint the code sources."""
    c.run(f"flake8 {SRC_FILES} {TEST_FILES} tasks.py")


@task
def format(c):
    """Format the code sources."""
    c.run(f"black {SRC_FILES} {TEST_FILES} tasks.py")
    c.run(f"isort {SRC_FILES} {TEST_FILES} tasks.py")


@task
def test(c):
    """Run the unit tests."""
    c.run("pytest")


@task
def typecheck(c):
    """Run type checking using mypy."""
    c.run(f"mypy {SRC_DIR}")


@task
def build(c, package=True, docs=True, coverage=True):
    """Build the user documentation."""
    if docs:
        c.run(f"mkdocs build -d {DOCS_DIST_DIR}")
        if coverage:
            if not Path(DOCS_DIR / "coverage-report" / "index.html").is_file():
                print("Running tests to generate coverage report.")
                c.run("pytest")
    if package:
        c.run("poetry build")


@task
def docs(c, coverage=True):
    """Serve the documentation."""
    if coverage:
        if not Path(DOCS_DIR / "coverage-report" / "index.html").is_file():
            print("Running tests to generate coverage report.")
            c.run("pytest")
    c.run("mkdocs serve")


@task
def publish(c, username=None, password=None):
    """Publish the package."""
    if (username is None) and (password is None):
        c.run("poetry publish")
    else:
        c.run(f"poetry publish -u {username} -p {password}")


@task
def clean(c):
    """Clean the build artefacts."""
    try:
        rmtree(PROJECT_DIR / "dist")
    except FileNotFoundError:
        pass


@task
def build_ci_image(c, image="{{ cookiecutter.ci_docker_image }}"):
    """Build the Docker image for Continuous Integration."""
    c.run(f"docker build -t {image} -f ci/Dockerfile .")


@task
def nb_kernel(c, name="{{ cookiecutter.project_slug }}", display_name="{{ cookiecutter.project_name }}"):
    """Register IPython kernel to use in jupyter notebooks."""
    try:
        import ipykernel as _  # noqa: F401
    except ModuleNotFoundError:
        c.run("poetry add --dev ipykernel")
    c.run(
        "python -m ipykernel install --user"
        f' --name "{name}"'
        f' --display-name "{display_name}"'
    )


@task
def notebooks(c):
    """Start jupyter notebook."""
    c.run("jupyter notebook notebooks")
