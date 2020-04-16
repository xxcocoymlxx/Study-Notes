import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import { AppBar, RadioButton, RadioButtonGroup, RaisedButton, TextField } from 'material-ui';
import $ from 'jquery';

// The profile component 
// pre-fills user's information
// Users are able to update their profile and delete their account here
class Profile extends Component {
    constructor(props) {
        super(props);

       this.getUserData();

       this.state = {
        username: '', username_error_text: '',
        password: '', password_error_text: '',
        password_repeat: '', password_repeat_error_text: '',
        firstName: '', firstname_error_text: '',
        email: '', email_error_text: '',
        gender: '', gender_error_text: '' 
    }
  }

    render() {
        return (
            <div align="center">
              <MuiThemeProvider>
                  <div>
                      <AppBar title = "Profile" style = {style.display} />
                        Username
                        <br />
                        <TextField required defaultValue = {this.state.username} disabled = { true }/>
                        <br />
                        Password<br />
                        <TextField
                        required
                        type = "password"
                        errorText={this.state.password_error_text}
                        defaultValue = {this.state.password}
                        onChange = {(event,newValue) => this.setState({password: newValue})}
                        />
                        <br />
                        Repeat Password<br />
                        <TextField
                        required
                        type = "password"
                        errorText={this.state.password_repeat_error_text}
                        defaultValue = {this.state.password_repeat}
                        onChange = {(event,newValue) => this.setState({password_repeat: newValue})}
                        />
                        <br />
                        First Name<br />
                        <TextField
                        required
                        errorText={this.state.firstname_error_text}
                        defaultValue = {this.state.firstName}
                        onChange = {(event, newValue) => this.setState({firstName: newValue})}
                        />
                        <br />
                        Email<br />
                        <TextField
                        required
                        errorText={this.state.email_error_text}
                        defaultValue = {this.state.email}
                        onChange = {(event, newValue) => this.setState({email: newValue})}
                        />
                        <br /><br />
                        Please choose your gender: <br />
                        <RadioButtonGroup labelPosition = 'left' name = "gender"  valueSelected= {this.state.gender} onChange = {(event, newValue) => this.setState({gender: newValue})}>
                            <RadioButton value = "male" label = "male" style = {style.radioButton}/>
                            <RadioButton value = "female" label = "female" style = {style.radioButton}/>
                            <RadioButton value = "no" label = "unknown" style = {style.radioButton}/>
                        </RadioButtonGroup>
                        <div style={style.div} className='error-text'>{this.state.gender_error_text}</div>
                        <br />
                        <RaisedButton label = "Update" primary = {true} style = {style} onClick = {(event) => this.validateUserInput(event)}/>
                        <RaisedButton label = "Delete Account" primary = {true} style = {style} onClick = {(event) => this.deleteUser(event)}/>
                    </div>
              </MuiThemeProvider>
            </div>
        )
    }

    validateUsername() {
        if (!this.state.username) {
          this.setState({username_error_text: 'This field is required'});
          return false;
        } else {
          this.setState({username_error_text: ''});
          return true;
        }
    };
  
    validatePassword() {
        if (!this.state.password) {
          this.setState({password_error_text: 'This field is required'});
          return false;
        } else if (!this.state.password_repeat){
            this.setState({password_repeat_error_text: 'This field is required'});
            return false;
        }else if (this.state.password.length < 6) {
          this.setState({password_error_text: 'Password is too short. Minimum 6 characters'})
          return false;
        } else if (this.state.password !== this.state.password_repeat) {
            this.setState({password_repeat_error_text: 'Password mismatch'})
            return false;
        }else {
          this.setState({password_error_text: ''});
          return true;
        }
    };
  
    validateFirstName() {
        if (!this.state.firstName) {
          this.setState({firstname_error_text: 'This field is required'});
          return false;
        } else {
          this.setState({firstname_error_text: ''});
          return true;
        }
    };
  

    validateEmail() {
        if (!this.state.email) {
          this.setState({email_error_text: 'This field is required'});
          return false;
        } else if (!this.state.email.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i)) {
          this.setState({email_error_text: 'Incorrect email format'});
          return false;
        } else {
          this.setState({email_error_text: ''});
          return true;
        }
    };
  
    validateGender() {
        if (!this.state.gender) {
          this.setState({gender_error_text: 'This field is required'});
          return false;
        } else {
          this.setState({gender_error_text: ''});
          return true;
        }
    };
  
    validateUserInput(event) {
        event.preventDefault();
        if (!this.validateUsername() || !this.validatePassword() || !this.validateFirstName() || !this.validateEmail() || !this.validateGender()) {
          alert("Incomplete form");
        } else {
          this.submit();
        }
    };

    submit() {
        console.log("clicked update");
        var username = this.props.userName;
        var payload = {
            "firstname": this.state.firstName,
            "password": this.state.password,
            "email": this.state.email,
            "gender": this.state.gender,
        }
        $.ajax({
            headers: {'Authorization': "Bearer "+ this.props.userToken},
            url: "/api/user/"+username+"/update",
            method: "PUT",
            data: JSON.stringify(payload),
            contentType: "application/json; charset=UTF-8",
        }).done((data, text_status, jqXHR)=> {
            console.log(text_status);
            console.log(jqXHR.status);
            var returned = JSON.stringify(data);
            console.log(returned);
            alert("profile successfully updated");
        }).fail((err)=> {
            alert("profile update failed");
            console.log(err.status);
            console.log(JSON.stringify(err.responseJSON));
        });
    };

    deleteUser(event) {
        event.preventDefault();
        console.log("clicked delete");
        var username = this.props.userName;
        $.ajax({
            headers: {'Authorization': "Bearer " + this.props.userToken},
                    url: "/api/user/"+username+"/deleteAccount",
                    method: "DELETE",
                    contentType: "application/json; charset=UTF-8",
                }).done((data, text_status, jqXHR)=> {
                    console.log(text_status);
                    console.log(jqXHR.status);
                    this.props.deleteUser();
                    alert("Your account has been deleted");
                }).fail((err)=> {
                    console.log(err.status);
                    alert(JSON.stringify(err.responseJSON));
                    console.log(JSON.stringify(err.responseJSON));
                });
    };

    getUserData() {
        var username = this.props.userName;

        $.ajax({
            headers: {'Authorization': "Bearer " + this.props.userToken},
            url: "/api/user/"+username,
            method: "GET",
            contentType: "application/json; charset=UTF-8"
        }).done((data, text_status, jqXHR)=> {
            console.log(text_status);
            console.log(jqXHR.status);
            var returned = JSON.stringify(data);
            console.log(returned);
            this.setState({
                username: data['username'],
                password: data['password'],
                password_repeat: data['password'],
                firstName: data['firstname'],
                email: data['email'],
                gender: data['gender'],
            });
        }).fail((err)=> {
            if (err){
                alert("Failed Autofill");
            }
            alert(JSON.stringify(err.responseJSON));
            console.log(JSON.stringify(err.responseJSON));
        });
    };
}

const style = {
    margin: 15, labelColor: 'white',
    radioButton: {
      width: 'auto',
      textAlign: 'center',
      display: 'inline-block'
    },
    div: {color: 'red', textAlign: 'center', fontSize: 12
    }
  };
  
export default Profile;