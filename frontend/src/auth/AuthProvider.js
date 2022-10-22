// reference: https://stackoverflow.com/questions/71960194/update-navbar-after-success-login-or-logout-redirection
import { createContext, useContext, useEffect, useState } from 'react';
import jwt_decode from "jwt-decode";


const AuthContext = createContext({
    jwt: null,
    userId: null,
    username: null,
    setJwt: () => { }

});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [jwt, setJwt] = useState(null);
    const [username, setUsername] = useState(null);
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        if (jwt) {
            let jwt_contents = jwt_decode(jwt);
            console.log(jwt_contents)
            setUsername(jwt_contents.sub.username)
            setUserId(jwt_contents.sub.user_id)
        } else {
            setUsername(null)
            setUserId(null)
        }
    }, [jwt]);

    return (
        <AuthContext.Provider value={{ jwt, userId, username, setJwt }}>
            {children}
        </AuthContext.Provider>
    );
};