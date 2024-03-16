import subprocess
import sys
from time import sleep

import yaml


def create_service(name, host, path, port, routes):
    subprocess.run(
        [
            "curl",
            "-i",
            "-X",
            "POST",
            "http://kong:8001/services/",
            "--data",
            "name=" + name,
            "--data",
            "url=http://" + host + ":" + str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("=" * 40)
    print(f"Service '{name}' has been successfully created.")
    sleep(1.2)

    for route in routes:
        paths = [["--data", f"paths[]={path}"] for path in route["paths"]]
        subprocess.run(
            [
                "curl",
                "-i",
                "-X",
                "POST",
                "http://kong:8001/services/" + name + "/routes",
                "--data", 
                "name=" + route["name"],
                "--data",
                "strip_path=" + str(route["strip_path"]).lower()
            ]
            + sum(paths, []),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"--- Route '{route['name']}' has been successfully created.")

    print("=" * 40)


def main(config_file):
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        for service in config["services"]:
            create_service(
                service["name"],
                service["host"],
                service["path"],
                service["port"],
                service["routes"],
            )
    except yaml.YAMLError as e:
        print(f"Error occurred while parsing YAML file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 create_services.py <config_file>")
        sys.exit(1)
    main(sys.argv[1])
