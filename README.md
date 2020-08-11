# Longest Common Substring (LCS) Server

## Description

This server provides the longest common substrings of specified strings.

It produces a JSON document in response to an HTTP POST request.

This project was created in August 2020 by [Aaron Mansheim](mailto:aaron.mansheim@gmail.com).

It was created as an exercise to be evaluated by Todd Ricker, Senior Manager of Applications Engineering at Comcast.

## System Requirements

The project requires Python 3 and expects Linux or macOS.

The project does not modify the host Python environment.

When the project needs Python packages that are not present, the project modifies the project's own, lightweight Python environment. It adds the packages by using the package installer `pip` that comes with Python.

The project's lightweight Python environment is stored in the project's directory. The project creates that environment by using the package `venv` that comes with Python.

## Running

The project is ready to run when it is delivered.

Run the project using its script: `lcs.sh`

The script accepts optional arguments: `lcs.sh [<hostname>] [<port>]`

- `hostname`: The DNS name or IP number to use when contacting the server. Default: `localhost`
- `port`: The TCP/IP port number where the server should run. Default: `53792`

The project does not provide a configuration for deployment to production. The following tutorial explains deploying a project like this one to production: https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/

## Example Session

The program `curl` is one way to produce a request to the server.

```sh
curl -d '{"setOfStrings":[
    {"value":"comcast"},
    {"value":"comcastic"},
    {"value":"broadcaster"}]}' \
http://localhost:53792/lcs
```

That request gets a response with the following content.

```sh
{"lcs":[{"value":"cast"}]}
```

## Files

<dl>
    <dt><code>README.md</code></dt>
    <dd>This document.</dd>
    <dt><code>app.py</code></dt>
    <dd>The server, implemented in the Python programming language.</dd>
    <dt><code>lcs.sh</code></dt>
    <dd>The script that runs the server in Linux or macOS using Python 3.</dd>
    <dt><code>src/test/script/test1.py</code></dt>
    <dd>An example in the Python programming language, making requests to the server and interpreting the resulting JSON data.</dd>
</dl>
