#! /bin/bash

# Copyright (c) 2018, Dennis Hedback
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     1. Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in
#        the documentation and/or other materials provided with the
#        distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

pivvy_DIR=$1
REGULAR_NAME=$2
SNAKE_CASE_NAME=$3
DOC_NAME=$4

mkdir $REGULAR_NAME
pushd $REGULAR_NAME

cp -r $pivvy_DIR/project_tpl/* .
mkdir bundle/pivvy
cp $pivvy_DIR/__init__.py bundle/pivvy/

mv _gitignore .gitignore

<plugin/__REGULAR_PLACEHOLDER__.vim sed "s/__SNAKE_CASE_PLACEHOLDER__/${SNAKE_CASE_NAME}/g" >plugin/$REGULAR_NAME.vim
rm plugin/__REGULAR_PLACEHOLDER__.vim

<plugin/bootstrap.py sed "s/__SNAKE_CASE_PLACEHOLDER__/${SNAKE_CASE_NAME}/g" >plugin/tmp.py
rm plugin/bootstrap.py
mv plugin/tmp.py plugin/bootstrap.py

<application/__init__.py sed "s/__SNAKE_CASE_PLACEHOLDER__/${SNAKE_CASE_NAME}/g" >application/tmp.py
rm application/__init__.py
mv application/tmp.py application/__init__.py

echo "# $REGULAR_NAME" > README.md
echo "" >> README.md
echo "There doesn't seem to be anything here yet." >> README.md
echo

<doc/doc.txt sed "s/__PLACEHOLDER__/${DOC_NAME}/g" >doc/$REGULAR_NAME.txt
rm doc/doc.txt

git init
git add .gitignore
git add *
git commit -m "Automatically created by 'pivvy startproject'"

popd
