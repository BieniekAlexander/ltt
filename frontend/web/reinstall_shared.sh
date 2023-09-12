#!/bin/bash
# workaround script to quickly run the operation of rebuilding local node dependencies - handling local packages is very bad for React Native
pushd ../shared
npm run build
popd
npm install ../shared
