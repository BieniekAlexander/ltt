// File that connects the app to the root folder in index.html
// imports
import React from 'react';
import ReactDOM from 'react-dom';
import AuthProvider from './auth/AuthProvider';


import App from './App';

ReactDOM.render(
    <App/>, 
    document.getElementById('root')
);