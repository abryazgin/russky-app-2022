#!/usr/bin/env bash

broken_files=`grep -UIlr --exclude-dir=.git --binary-files=without-match $(printf '\r\n') $1`

if [ ! -z "$broken_files" ]
then
  printf 'Fix CRLF line endings in files:\n%s\n' "$broken_files" >&2
  exit 1
fi
