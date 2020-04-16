import React, { Component } from 'react';
import Navigation from './components/Navigation';
import Profile from './components/Profile';
import Login from './components/Login';
import Play from './components/Play';
import Register from './components/Register';
import GameStats from './components/GameStats';

//the root "component"
class App extends Component {
	constructor(){
		super()
		this.state = {currentPage: 'LOGIN', token: null, name: null}
  }

  //passing the JWT authenticate token and user name
  goToProfile(token, name){
		this.setState({currentPage: 'PROFILE', token: token, name: name});
  }

  goToLogin(){
		this.setState({currentPage: 'LOGIN', token: null, name: null});
  }
  
  goToPlay(token,name) {
		this.setState({currentPage: 'GAME', token: token, name: name})
	}

  logout(token,name) {
		this.setState({currentPage: 'LOGIN', token: token, name: name})
  }
  
  goToRegister() {
		this.setState({currentPage: 'REGISTER', token: null, name: null})
  }
  
  goToGameStats(token,name) {
		this.setState({currentPage: 'GAMESTATS', token: token, name: name})
	}
  
  render() {
		const state = this.state.currentPage;
		//conditional rendering different components
		if (state === 'LOGIN') {
				return (<Login
          					loginFunc = {(token, name) => this.goToPlay(token, name)}
          					register = {()=>this.goToRegister()}
						/>);
		}else if (state === 'REGISTER'){
				return (<Register 
							completeRegistration = {() => this.goToLogin()}
							backToLogin = {()=>this.goToLogin()}
						  />);
		}else if (state === 'PROFILE'){
			//return a react "fragment" containing 2 components
				return (
				<>
					<Navigation 
					logoutFunc = {() => this.logout()} 
					playFunc = {() => this.setState({currentPage:'GAME'})}
					goToProfile = {() => this.setState({currentPage:'PROFILE'})}
					goToGameStats = {() => this.setState({currentPage:'GAMESTATS'})}
				/>
				<Profile 
					userToken = {this.state.token} 
					userName = {this.state.name} 
					deleteUser = {() => this.logout()}
				/>
				</>);
		}else if (state === 'GAMESTATS'){
				//return a react "fragment" containing 2 components
				return (
				<>
				<Navigation 
					logoutFunc = {() => this.logout()} 
					playFunc = {() => this.setState({currentPage:'GAME'})}
					goToProfile = {() => this.setState({currentPage:'PROFILE'})}
					goToGameStats = {() => this.setState({currentPage:'GAMESTATS'})}
				/>
				<GameStats
					userName = {this.state.name}
					userToken = {this.state.token}
				/>
				</>);
		}else if (state === 'GAME'){
			//return a react "fragment" containing 2 components
				return (
				<>
				<Navigation 
				logoutFunc = {() => this.logout()} 
				playFunc = {() => this.setState({currentPage:'GAME'})}
				goToProfile = {() => this.setState({currentPage:'PROFILE'})}
				goToGameStats = {() => this.setState({currentPage:'GAMESTATS'})}
				/>
				<Play
					userName = {this.state.name}
					userToken = {this.state.token}
					submitScoreFunc = {() => this.goToPlay()} 
				/>
				</>)
			}
	};
}

export default App;
