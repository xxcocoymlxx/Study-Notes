<?php

class User {
    public $username;
	public $password;
	public $gender;
    public $birthday;
    public $gift;
    public $subscribe;

    //male:0 female:1 unknown:3
    public $genderflag;

    //nogift:1 giftcard:2 3sub:3 secret:4
    public $giftflag;

    //yes:1 no:0
    public $subflag;

    public function __construct($name, $psw,$sex,$bday, $g,$sub) {
        $this->username = $name;
        $this->password = $psw;
        $this->gender = $sex;
        $this->birthday = $bday;
        $this->gift = $g;
        $this->subscribe = $sub;
    }

    public function updatePassword($psw) {
        $this->password = $psw;
    }

    public function updateGender($sex) {
        $this->gender = $sex;
    }

    public function updateBirthday($bday) {
        $this->birthday = $bday;
    }

    public function updateSubscribe($sub) {
        $this->subscribe = $sub;
    }

    public function updateGenderFlag($flag) {
        $this->genderflag = $flag;
    }

    public function updateSubFlag($flag) {
        $this->subflag = $flag;
    }

}

?>