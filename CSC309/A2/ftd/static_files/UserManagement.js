/**database class warped by promise*/
class UserManagement {

    constructor(database) {
        //Enable Delete cascade
        this.db = database;
        this.run('PRAGMA foreign_keys = ON', []).then(() => {}, (err) => {
            throw err.message;
        });
    }

    //all the queries are executed through these 3 functions
    //not directly through db.run() / db.get() / db.all()
    run(sql, params = []) {
        return new Promise((resolve, reject) => {
            //all the queries are being prepared here
            this.db.prepare(sql).run(params, (err) => {
                if (err) {
                    console.log('Error running sql ' + sql);
                    console.log(err);
                    reject(err)
                } else {
                    console.log('Success running sql ' + sql);
                    resolve();
                }
            });
        });
    }

    get(sql, params = []) {
        return new Promise((resolve, reject) => {
            //all the queries are being prepared here
            this.db.prepare(sql).get(params, (err, row) => {
                if (err) {
                    console.log('Error running sql: ' + sql);
                    console.log(err);
                    reject(err)
                } else {
                    resolve(row);
                }
            })
        })
    }

    all(sql, params = []) {
        return new Promise((resolve, reject) => {
            //all the queries are being prepared here
            this.db.prepare(sql).all(params, (err, rows) => {
                if (err) {
                    console.log('Error running sql: ' + sql);
                    console.log(err);
                    reject(err)
                } else {
                    resolve(rows);
                }
            });
        });
    }

    //the query is being prepared in the get() function defined above
    getUserByUsername(username) {
        let sql = "SELECT * FROM user WHERE username=?;";
        return this.get(sql, [username]);
    }

    //the query is being prepared in the get() function defined above
    //two cases: 1. user name does not exists 2. user name exists, but password does not match
    verification(username, password) {
        return this.getUserByUsername(username).then(
            (row) => {
                if (row) {
                    let sql = 'SELECT * FROM user WHERE username=? and password=?;';
                    return this.get(sql, [username, password]);//return a new promise
                } else {
                    //user name does not exists
                    // there won't be an error if the username does not exist, so it shouldn't be in catch block
                    return new Promise((resolve, reject) => {
                    reject("User does not exist");
                    });
                }
            }).catch(
            (err) => {
                console.log(err);
                return new Promise((resolve, reject) => {
                    reject(err);
                });
            });
    }

    //the query is being prepared in the run() function defined above
    deleteUserByid(username) {
        let sql = "DELETE FROM user WHERE username = ?";
        return this.run(sql, [username]);
    }

    //the query is being prepared in the run() function defined above
    insertUser(username, password, firstname, gender, email) {
        let sql = 'INSERT INTO user(username, password, firstname, gender, email) VALUES (?,?,?,?,?);';
        return this.run(sql, [username, password, firstname, gender, email]);
    }

    //the query is being prepared in the run() function defined above
    insertAchievement(username, kill, damage) {
        var scoreid = username + (Math.floor(Math.random() * 100000000));
        let sql = 'INSERT INTO achievement(scoreid, username, kill, damage) VALUES (?,?,?,?);';
        return this.run(sql, [scoreid, username, kill, damage]);
    }

    //the query is being prepared in the run() function defined above
    updateUser(firstname, password, email, gender, username) {
        let sql = 'UPDATE user SET firstname = ?, email = ? , gender = ? , password = ? WHERE username=?;';
        return this.run(sql, [firstname, email, gender, password, username]);
    }

    //the query is being prepared in the get() function defined above
    getAchievementByid(username) {
        let sql = 'SELECT * FROM achievement WHERE username= ?;';
        return this.get(sql, [username]);
    }

    //the query is being prepared in the all() function defined above
    getTop10Score() {
        let sql = 'SELECT username, MAX(kill) as kill FROM achievement GROUP BY username ORDER BY kill DESC LIMIT 10;';
        return this.all(sql);
    }
}

module.exports = UserManagement;