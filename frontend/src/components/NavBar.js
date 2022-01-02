// imports
import React, { useState } from 'react';
// import  {Button} from './Button'; 
import Dropdown from './Dropdown';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { useDetectOutsideClick } from '../functions/useDetectOutsideClick';
import './NavBar.css';

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

export const NavMenu = styled.div`
  display: flex;
  align-items: center;
  margin-right: 24px;
  @media screen and (max-width: 768px) {
    display: none;
  }
`;

const Navbar = () => {
  const [click, setClick] = useState(false);
  const [dropdown, setDropdown] = useState(false);

  const handleClick = () => setClick(!click);
  const toggleDropdown = () => setDropdown(!dropdown);

  // const [isActive, setIsActive] = useDetectOutsideClick(dropdownRef, false);
  const [isActive, setIsActive] = useDetectOutsideClick(dropdown, false);

  return (
    <>
      <Nav>
        <NavLink to="/">
          <h1 className='navbar'>Language Trainer</h1>
        </NavLink>
        
        <NavMenu>
          <Dropdown/>
          <NavLink to="/vocabulary" className='navbar'>Vocabulary</NavLink>
          <NavLink to="/about" className='navbar'>About</NavLink>
          <NavLink to="/sign-up" className='navbar'>Sign Up</NavLink>
        </NavMenu>
      </Nav>
    </>
  )
}

export default Navbar;