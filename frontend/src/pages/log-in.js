import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { useAuth } from '../auth/AuthProvider';
import axios from 'axios';


const LogInBody = () => {
    const { setJwt } = useAuth();
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async e => {
        e.preventDefault();

        axios({
            method: 'post',
            url: `${process.env.REACT_APP_BACKEND_URL}/auth/login`,
            headers: { 'Content-Type': 'application/json' },
            data: {
                username: username,
                password: password
            }
        }).then(response => {
            setJwt(response.data.access_token)
            navigate('/')
        }).catch(error => { console.error(error) })
    }

    return (
        <div>
            <h2 style={{ display: 'flex', justifyContent: 'center' }}>Sign In</h2>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '90vh' }}>
                <form onSubmit={handleLogin}>
                    <label>
                        Username:<input type="text" onChange={e => setUsername(e.target.value)} />
                    </label>
                    <label>
                        Password:<input type="text" onChange={e => setPassword(e.target.value)} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        </div>
    );
};

export default LogInBody;