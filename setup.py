from setuptools import setup
from pathlib import Path

project_dir_path = Path(__file__).parent

requirements_file = str(project_dir_path.joinpath("requirements.txt").absolute())
readme_file = str(project_dir_path.joinpath("README.md").absolute())


def filter_comment_lines(input_lines):
    non_empty_lines = (line.strip() for line in input_lines if len(line) > 0)
    return [line.split("#")[0].strip() for line in non_empty_lines if not line.startswith("#")]


if __name__ == '__main__':
    with open(requirements_file, "r") as file:
        requirements_list = filter_comment_lines(file.readlines())

    with open(readme_file, "r") as f:
        long_description = f.read()

    setup(
        install_requires=requirements_list,
        long_description=long_description,
        long_description_content_type="text/markdown"
    )
