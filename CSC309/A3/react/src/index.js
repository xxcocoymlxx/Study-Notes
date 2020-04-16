import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import { BrowserRouter, Route } from 'react-router-dom';

const root = document.getElementById('root');

ReactDOM.render(
    <MuiThemeProvider>
        <div>
            <BrowserRouter>
                <div>
                    <Route path ='/' component = {App}></Route>
                </div>
            </BrowserRouter>
        </div>
    </MuiThemeProvider>, root);
serviceWorker.unregister();