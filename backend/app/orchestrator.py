import docker

client = docker.from_env()

def execute_engine(image_name, command, file_path):
    # Standardizing the path for Docker volumes
    abs_path = os.path.abspath(file_path)
    work_dir = os.path.dirname(abs_path)

    try:
        # We use 'logs=True' to capture output
        # We use 'environment' to pass any needed variables
        container = client.containers.run(
            image=image_name,
            command=command,
            volumes={work_dir: {'bind': '/src', 'mode': 'rw'}},
            working_dir='/src',
            detach=False,
            remove=True,
            environment={"AIGIS_CONTEXT": "local_test"}
        )
        return container.decode('utf-8')
    except docker.errors.ImageNotFound:
        return f"Error: The engine image '{image_name}' has not been built by Member 3 yet."
    except Exception as e:
        return f"Critical Runtime Error: {str(e)}"