#!/bin/bash
# workaround script to quickly run the operation of rebuilding local node dependencies - handling local packages is very bad for React
pushd ../shared
yalc publish
popd
yalc add shared
npm install
