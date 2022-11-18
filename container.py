#!/usr/bin/env python3
import os


def build():
    result = os.system("docker build . -t ps:latest ")
    if result == 0:
        print("Build successful")
    else:
        raise Exception("Build failed")


def build_and_run():
    build()
    run()


def run(cmd="", entrypoint="", port=""):

    if entrypoint:
        entrypoint = f" --entrypoint '{entrypoint}'"

    if port:
        port = f" -p {port}"

    volumes = " ".join(
        [
            " -v $HOME/projects/PythonSearch:/src ",
            " -v $HOME/projects/PySearchEntries/:/entries ",
            " -v $HOME/.PythonSearch:/root/.PythonSearch ",
            " -v $HOME/.PythonSearch/container_cache/:/root/.cache ",
            " -v $HOME/.data:/root/.data" " -v $HOME/.gitconfig:/root/.gitconfig",
        ]
    )

    environment_variables = " ".join(
        [
            " -e 'PS_ENTRIES_HOME=/entries' ",
            " -e ARIZE_API_KEY=$ARIZE_API_KEY ",
            " -e ARIZE_SPACE_KEY=$ARIZE_SPACE_KEY ",
        ]
    )

    LIMIT_CPU = 8
    cmd = f"docker run {port} --expose=8000 --expose 6379 --cpus={LIMIT_CPU} {environment_variables} -it {volumes} {entrypoint} ps {cmd}"
    print("Cmd: " + cmd)
    os.system(cmd)


def sh():
    shell()


def shell():
    run(entrypoint="/bin/bash")


def run_jupyter():
    run(
        cmd="jupyter lab --allow-root --ip '*' --notebook-dir / --NotebookApp.token='' --NotebookApp.password=''",
        port="8888:8888",
    )


def run_mlflow():
    run(
        cmd="mlflow ui --backend-store-uri file:/entries/mlflow --port 5001 --host '0.0.0.0' ",
        port="5001:5001",
    )


def run_webserver():
    run(cmd="python_search_webapi", port="8000:8000")


def run_streamlit():
    run(cmd=" streamlit run python_search/data_ui/main.py --server.address=0.0.0.0  --server.port=8501 ", port="8501:8501")

def main():
    import fire

    fire.Fire()


if __name__ == "__main__":
    main