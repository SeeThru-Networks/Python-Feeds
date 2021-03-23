from setuptools import setup, find_packages

# setup()

setup(
    name="seethrufeeds",
    version="0.1.4",
    author="SeeThru Networks",
    author_email="aidan@seethrunetworks.com",
    description="The SeeThruNetworks feed framework",
    license="MIT",
    url="https://github.com/SeeThru-Networks/Python-Feeds",
    project_urls={
        "Website": "https://www.seethrunetworks.com/"
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only"
    ],
    packages=find_packages(),
    install_requires=['requests', "python-dotenv", "toml", "mysql-connector-python", "py-zabbix", "pydantic"],
    python_requires=">=3.9",
    keywords=["seethru", "seethrunetworks", "feed"],
    entry_points={
        "console_scripts": [
                "SeeThru_Feeds=SeeThru_Feeds.Core.SeeThruFeed:exec",
                "seethrufeeds=SeeThru_Feeds.Core.SeeThruFeed:exec"
            ]
    }


)
