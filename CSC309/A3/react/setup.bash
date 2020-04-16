# DO NOT run this file
# Please see README.txt in order to run our application
# -------------------------------------------------------------------------
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
npm install --save jquery
npm i react --save
npm install react react-dom --save
npm install concurrently --save

npm install --save create-react-app
npm install --save nodemon
npm install node-env-run --save
npm install npm-run-all --save-dev
curl -o- -L https://yarnpkg.com/install.sh | bash

npm i cors

npm install material-ui@latest
npm install react-router-dom
npm install --save react-scripts
npm install @material-ui/core --save

#JWT for authentication 
npm install --save jsonwebtoken
#contains our secret token for JWT
npm install --save dotenv

sqlite3 ./db/database.db < ./db/schema.sql 


#nodejs ftd.js PORT_NUMBER
# http://142.1.200.148:PORT_NUMBER

