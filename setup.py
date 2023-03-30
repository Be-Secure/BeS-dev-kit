from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'assessment_report',
    version = '0.0.1',
    # author = 'sudhir Verma',
    # author_email = 'sudhir.verma@wipro.com',
    license = 'MIT',
    description = 'Generate assessment report for Be-Secure',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/Be-Secure/besecure-developer-toolkit',
    py_modules = ['assessment_report', 'src'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        assessment_report=assessment_report:cli
    '''
)