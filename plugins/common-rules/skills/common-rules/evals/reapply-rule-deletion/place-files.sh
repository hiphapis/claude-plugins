#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm init
