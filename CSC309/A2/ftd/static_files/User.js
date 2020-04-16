class User {
    constructor() {
        this.info = {
            username: null,
            firstname: null,
            password: null,
            gender: null,
            email: null
        };
        this.achievement = {
            kill: 0,
            damage: 0
        }
    }

    setInfo(data) {
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                this.info[key] = data[key];
            }
        }
    }

    setAchievement(data) {
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                this.achievement[key] = data[key];
            }
        }
    }

    setUsername(username) {
        this.info.username = username;
    }

    setFirstname(firstname) {
        this.info.firstname = firstname;
    }

    setEmail(email) {
        this.info.email = email;
    }

    setPassword(password) {
        this.info.password = password;
    }

    setGender(gender) {
        this.info.gender = gender;
    }

    toString(){
        return "username: " + this.info.username + 
                " email: " + this.info.email +
                " gender: " + this.info.gender
    }

    clear() {
        this.info = {
            username: null,
            firstname: null,
            password: null,
            gender: null,
            email: null
        };
        this.achievement = {
            kill: 0,
            damage: 0
        }
    }
}

module.exports = User;