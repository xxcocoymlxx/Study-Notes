#!/bin/bash
# -------------------------------------------------------------------------
# Here is what we did to set this all up...
rm package*
rm -fr node_modules

npm init
# npm init creates a package.json
# http://browsenpm.org/package.json
# https://docs.npmjs.com/files/package.json

npm install --save express
npm install --save cookie-parser
npm install --save url
npm install --save http
npm install --save body-parser
npm install --save sqlite3

#JWT for authentication 
npm install --save jsonwebtoken
#contains our secret token for JWT
npm install --save dotenv

sqlite3 ./db/database.db < ./db/schema.sql 

# check out the package.json now
# check out node_modules

#nodejs ftd.js PORT_NUMBER
# http://142.1.200.148:PORT_NUMBER

