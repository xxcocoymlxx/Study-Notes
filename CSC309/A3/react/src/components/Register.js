import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { AppBar, RadioButton, RadioButtonGroup, RaisedButton, TextField } from 'material-ui';
import $ from 'jquery';

// The registration page
class Register extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '', username_error_text: '',
            password: '', password_error_text: '',
            password_repeat: '', password_repeat_error_text: '',
            firstName: '', firstname_error_text: '',
            email: '',  email_error_text: '',
            gender: '',  gender_error_text: ''
        }

        this.clear = this.clear.bind(this);
    }

    render() {
        return (
            <div align="center">
              <MuiThemeProvider>
                <div>
                  <AppBar title = "Register" style = {style.display} />
                  <TextField 
                  hintText = "username" 
                  floatingLabelText = "Please enter your username"
                  errorText={this.state.username_error_text}
                  value = {this.state.username}
                  onChange = {(event, newValue) => this.setState({username: newValue})}
                  />
                  <br />
                  <TextField
                  type = "password"
                  hintText = "password"
                  floatingLabelText = "Please enter your password"
                  errorText={this.state.password_error_text}
                  value = {this.state.password}
                  onChange = {(event,newValue) => this.setState({password: newValue})}
                  />
                  <br />
                  <TextField
                  type = "password"
                  hintText = "password"
                  floatingLabelText = "Please repeat your password"
                  errorText={this.state.password_repeat_error_text}
                  value = {this.state.password_repeat}
                  onChange = {(event,newValue) => this.setState({password_repeat: newValue})}
                  />
                  <br />
                  <TextField
                  hintText = "first name"
                  floatingLabelText = "Please enter your first name"
                  errorText={this.state.firstname_error_text}
                  value = {this.state.firstName}
                  onChange = {(event, newValue) => this.setState({firstName: newValue})}
                  />
                  <br />
                  <TextField
                  hintText = "email"
                  floatingLabelText = "Please enter your email"
                  errorText={this.state.email_error_text}
                  value = {this.state.email}
                  onChange = {(event, newValue) => this.setState({email: newValue})}
                  />
                  <br /><br />
                  Please choose your gender: <br />
                  <RadioButtonGroup labelPosition = 'left' name = "gender" onChange = {(event, newValue) => this.setState({gender: newValue})}>
                    <RadioButton value = "male" label = "male" style = {style.radioButton}/>
                    <RadioButton value = "female" label = "female" style = {style.radioButton}/>
                    <RadioButton value = "unknown" label = "unknown" style = {style.radioButton}/>
                  </RadioButtonGroup>
                  <div style={style.div} className='error-text'>{this.state.gender_error_text}</div>
                  <br />
                  <RaisedButton  label = "Submit"  primary = {true} style = {style} onClick = {(event) => this.validateUserInput(event)}/>
                  <RaisedButton label = "Clear" primary = {true} style = {style} onClick = {this.clear}/>
                  <RaisedButton label = "Back To Login" primary = {true} style = {style} onClick = {this.props.backToLogin}/>
                </div>
              </MuiThemeProvider>
            </div>
        )
    }

    clear = () => {
      this.setState({
        username: '', password: '',
        password_repeat: '', firstName: '',
        email: '', gender: '',
      });
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
      }else if (!this.state.password_repeat) {
        this.setState({password_repeat_error_text: 'This field is required'});
        return false;
      }  else if (this.state.password.length < 6) {
        this.setState({password_error_text: 'Password is too short. Minimum 6 characters'})
        return false;
      } else if (this.state.password_repeat !== this.state.password){
        this.setState({password_repeat_error_text: 'Password mismatch'})
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
    }

    validateUserInput(event) {
      event.preventDefault();
      if (!this.validateUsername() || !this.validatePassword() || !this.validateFirstName() || !this.validateEmail() || !this.validateGender()) {
        alert("Incomplete form");
      } else {
        this.submit();
      }
    };

    submit() {
      console.log("clicked submit");
      var payload = {
        "username": this.state.username,
        "firstname": this.state.firstName,
        "password": this.state.password,
        "email": this.state.email,
        "gender": this.state.gender,
      }

      $.ajax({
        url: "/api/register",
        method: "POST",
        data: JSON.stringify(payload),
        contentType: "application/json; charset=UTF-8",
    }).done((data, text_status, jqXHR)=> {
        console.log(text_status);
        console.log(jqXHR.status);
        var returned = JSON.stringify(data);
        console.log(returned);
        alert("Registration was Successful!");
        this.props.completeRegistration();
    }).fail((err)=> {
        alert("username already exists");
        console.log(err.status);
        console.log(JSON.stringify(err.responseJSON));
    });
    }

    };

const style = {
  margin: 15,
  radioButton: {
    width: 'auto',
    textAlign: 'center',
    display: 'inline-block'
  },
  div: {
    color: 'red',
    textAlign: 'center',
    fontSize: 12
  }
};

export default Register;