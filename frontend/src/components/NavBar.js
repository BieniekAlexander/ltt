// imports
import React, { useState } from 'react';
// import  {Button} from './Button'; 
import Dropdown from './Dropdown';
import styled from 'styled-components';
import { Link, useNavigate } from 'react-router-dom';
import { useDetectOutsideClick } from '../functions/useDetectOutsideClick';
import './NavBar.css';
import { useAuth } from "../auth/AuthProvider"

// styling
export const NavSpan = styled.span`
  color: #fff;
  display: flex;
  align-items: center;
  text-decoration: none;
  padding: 0 1rem;
  height: 100%;
  cursor: pointer;
  &.active {
    color: #15cdfc;
  }
`;

export const Nav = styled.nav`
  background: #000;
  height: 80px;
  display: flex;
  justify-content: space-between;
  padding: 0.5rem calc((100vw - 1000px) / 2);
  z-index: 10;
  /* Third Nav */
  // justify-content: flex-start;
`;

export const NavLink = styled(Link)`
  color: #fff;
  display: flex;
  align-items: center;
  text-decoration: none;
  padding: 0 1rem;
  height: 100%;
  cursor: pointer;
  &.active {
    color: #15cdfc;
  }
`;

export const SignUpNavLink = styled(NavLink)`
  background-color: red;
`

export const NavMenu = styled.div`
  display: flex;
  align-items: center;
  margin-right: 24px;
  @media screen and (max-width: 768px) {
    display: none;
  }
`;

const Navbar = () => {
    const { username, setJwt } = useAuth();

    const [click, setClick] = useState(false);
    const handleClick = () => setClick(!click);

    const [dropdown, setDropdown] = useState(false);
    const toggleDropdown = () => setDropdown(!dropdown);

    const [isActive, setIsActive] = useDetectOutsideClick(dropdown, false);
    const navigate = useNavigate();

    const handleLogout = () => {
        setJwt(null)
        navigate('/')
    }

    return (
        <>
            <Nav>
                <NavLink to="/">
                    <h1 className='navbar'>Language Trainer</h1>
                </NavLink>

                <NavMenu>
                    <Dropdown />
                    <NavLink to="/vocabulary" className='navbar'>Vocabulary</NavLink>
                    <NavLink to="/about" className='navbar'>About</NavLink>
                    {/* TOOD this section isn't working, I'm trying to handle login and logout and have it reflect in the UI */}
                    {
                        username
                            ?
                            <div>
                                <NavLink to="/profile" className='navbar'><b>{username}</b></NavLink>
                                <NavLink to="/" className='navbar' onClick={handleLogout}>Logout</NavLink>
                            </div>
                            :
                            <div>
                                <NavLink to="/log-in" className='navbar'>Log In</NavLink>
                                <SignUpNavLink to="/sign-up" className='navbar'>Sign Up</SignUpNavLink>
                            </div>
                    }
                </NavMenu>
            </Nav>
        </>
    )
}

export default Navbar;