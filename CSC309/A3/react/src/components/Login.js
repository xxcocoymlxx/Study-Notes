import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Link from '@material-ui/core/Link';
import { AppBar, RaisedButton, TextField } from 'material-ui';
import $ from 'jquery';

class Login extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '',
            password: '',
            username_error_text: '',
            password_error_text: '',
        }

        this.submit = this.submit.bind(this);
    }


    render() {
        return (
          
            <div align="center">
              <MuiThemeProvider>
                <div>
                <AppBar title = "Login" className={style} />
                  <TextField 
                  label="Helper text"
                  hintText = "Please enter your username" 
                  errorText={this.state.username_error_text}
                  variant="outlined"
                  margin="normal"
                  required
                  value = {this.state.username}
                  onChange = {(event, newValue) => this.setState({username: newValue})}
                  />
                  <br />
                  <TextField
                  type = "password"
                  hintText = "Please enter your password"
                  variant="outlined"
                  margin="normal"
                  required
                  floatingLabelText = "Please enter your password"
                  errorText={this.state.password_error_text}
                  value = {this.state.password}
                  onChange = {(event,newValue) => this.setState({password: newValue})}
                  />
                  <br />
                  <RaisedButton 
                  label = "Login" 
                  secondary = {true} 
                  style = {style} 
                  onClick = {(event) => this.validateUserInput(event)}
                  />
                  <br />
                  <Link href="#" variant="body2">
                {"Don't have an account?"}
                </Link>
                  <RaisedButton 
                  label = "Register" 
                  secondary = {true} 
                  style = {style} 
                  onClick = {this.props.register}
                  />
                 
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
      } else if (this.state.password.length < 6) {
        this.setState({password_error_text: 'Password is too short. Minimum 6 characters'})
        return false;
      } else {
        this.setState({password_error_text: ''});
        return true;
      }
    };

    validateUserInput(event) {
      event.preventDefault();
      if (!this.validateUsername() || !this.validatePassword()) {
        alert("Invalid Login");
      } else {
        this.submit();
      }
    };


    submit = () =>{
        console.log("clicked login");
        var payload = {
            "username": this.state.username,
            "password": this.state.password
        }

        $.ajax({
          url: "/api/login",
          method: "POST",
          data: JSON.stringify(payload),
          contentType: "application/json; charset=UTF-8",

          success: function (data) {
        },
        error: function (xhr, err) {
          console.log(err);
            alert("invalid username or password. please try again.");
        }
        }).done((data, text_status, jqXHR)=>{
          //if in this case means login successful, otherwise there's gonna be an error
          var returned = JSON.stringify(data);
          console.log(returned);
          alert("login was successful!");
          this.props.loginFunc(data['accessToken'], this.state.username);		
  
        }).fail((err)=>{
          if (err){
            console.log(err);
          }
          console.log(JSON.stringify(err.responseJSON));
        });
    }   
    };


const style = {
  margin: 15,
  background : '#2E3B55'
};

export default Login;