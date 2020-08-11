#!/bin/sh
#
# Created: August 2020
# Author: Aaron Mansheim <aaron.mansheim@gmail.com>

function require_program {
    local program=$0
    if ! which -s "${program}"; then
        >&2 echo "Did not find '${program}'. This project will not run without that."
        exit 1
    fi
}

function activate_venv {
    local name=$1

    if [ ! -d "${name}" ]; then
        python3 -m venv "${name}"
    fi

    local is_activated=True

    if [ -z "$VIRTUAL_ENV" ]; then
        is_activated=False
    elif [ `basename "$VIRTUAL_ENV"` != "${name}" ]; then
        is_activated=False
    else
        local have_inode=`ls -id "$VIRTUAL_ENV" | cut -d' ' -f1`
        local want_inode=`ls -id "${name}" | cut -d' ' -f1`
        if [ "$have_inode" -ne "$want_inode" ]; then
            is_activated=False
        fi
    fi

    if [ x"$is_activated" != x"True" ]; then
        source "${name}/bin/activate"
    fi
}

function check_pip {
    python3 -m pip install --upgrade -q pip
}

function check_python_package {
    local name=$1

    if ! pip show -qq "${name}"; then
        pip install "${name}"
    fi
}

function try_ending_flask_if_port_busy {
    local hostname=$1
    local port=$2
    if which -s nc && nc -z "${hostname}" "${port:-80}" 2> /dev/null; then
        pkill -f flask
        if nc -z "${hostname}" "${port:-80}" 2> /dev/null; then

            >&2 echo "Not starting flask. Port ${port:-80} is in use."
            >&2 echo "Even tried killing existing flask processes."
            exit 1
        fi
    fi
}

function start_flask {
    local hostname=$1
    local port=$2
    if [ -n "${port}" ]; then
        FLASK_APP=app.py flask run -p "${port}" &
    else
        FLASK_APP=app.py flask run &
    fi
    local flask_pid=$!
    sleep 3
    echo
    echo "> Flask is now background process ${flask_pid}. (Not CTRL+C; 'kill ${flask_pid}' to quit)"
    echo "> Server: http://${hostname}:${port}/lcs"
}



hostname="${1:-localhost}"
port="${2:-53792}"

cd `dirname -- "$0"`

require_program python3
activate_venv venv
check_pip

check_python_package Flask
check_python_package jsonschema
check_python_package suffix_trees

try_ending_flask_if_port_busy "${hostname}" "${port}"
start_flask "${hostname}" "${port}"
