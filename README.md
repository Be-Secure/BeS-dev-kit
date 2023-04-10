# Be-Secure Developer Toolkit (bes-dev-kit)

bes-dev-kit is a cli tool for generating metadata and assessment report for [BeSLighthouse](https://github.com/Be-Secure/BeSLighthouse).

`Note: The code is still in testing phase`

# Pre-requisites

1. [Poetry](https://python-poetry.org/)
2. Python 3.x
3. pip
4. Github personal access token

# Setting env variables

`Note: Should be done before testing`

1. Creating a json file in your user home dir under the name `bes-dev-kit.json`.
2. Copy the below contents and paste it inside the file.
   
        {
        "GITHUB_ORG": "Be-Secure",
        "OSSPOI_DIR": "<user-home>/besecure-osspoi-datastore",
        "ASSESSMENT_DIR": "<user-home>/besecure-assessment-datastore",
        "GITHUB_AUTH_TOKEN": "<token>"
        }
3. Update `OSSPOI_DIR` and `ASSESSMENT_DIR` with complete path to your `assessment datastore` and `osspoi datastore`  dirs.
4. Add your github personal access token

# Testing

1. Install [poetry](https://python-poetry.org/). Use the [link](https://python-poetry.org/docs/) to install Poetry.
2. Clone the repo.
3. Move into the cloned directory.
4. Create a new virtual env using Poetry - `$ poetry shell`
5. Run the command to install the tool- `$ poetry install`
6. Check installation - `$ bes-dev-kit --help`
