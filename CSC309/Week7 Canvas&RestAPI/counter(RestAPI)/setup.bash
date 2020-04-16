#!/bin/bash
# -------------------------------------------------------------------------
# Here is what we did to set this all up...
rm package*
npm init
# npm init creates a package.json
# http://browsenpm.org/package.json
# https://docs.npmjs.com/files/package.json
# Take the defaults here

# We are adding libraries, they will be in our local node_modules

npm install --save express

# for post https://scotch.io/tutorials/use-expressjs-to-get-url-and-post-parameters
npm install --save body-parser 

# http://www.sqlitetutorial.net/sqlite-nodejs/
npm install --save sqlite3

# check out the package.json now
# check out node_modules

