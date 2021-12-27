// imports
import React, { useState } from 'react';
// import  {Button} from './Button'; 
import Dropdown from './Dropdown';
import styled from 'styled-components';
import { Link } from 'react-router-dom';


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

export const NavBtn = styled.nav`
  display: flex;
  align-items: center;
  margin-right: 24px;
  /* Third Nav */
  /* justify-content: flex-end;
  width: 100vw; */
  @media screen and (max-width: 768px) {
    display: none;
  }
`;

export const NavBtnLink = styled(Link)`
  border-radius: 4px;
  background: #256ce1;
  padding: 10px 22px;
  color: #fff;
  outline: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  margin-left: 24px;

  &:hover {
    transition: all 0.2s ease-in-out;
    background: #fff;
    color: #010606;
  }
`;

const Navbar = () => {
  const [click, setClick] = useState(false);
  const [dropdown, setDropdown] = useState(false);

  const handleClick = () => setClick(!click);
  const toggleDropdown = () => setDropdown(!dropdown);

  return (
    <>
      <Nav className='navbar'>
        <NavLink to="/">
          <h1>Language Trainer</h1>
        </NavLink>
        <div className='menu-icon' onClick={handleClick}>
          <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
        </div>
        <ul className={click ? 'nav-menu active' : 'nav-menu'}>
        </ul>
        <NavMenu>
          <NavSpan className='nav-links' onClick={toggleDropdown}>
              Training <i className='fas fa-caret-down' />
          </NavSpan>
          {dropdown && <Dropdown />}
          <NavLink to="/sign-up" activeStyle>
            Vocabulary
          </NavLink>
          <NavLink to="/about" activeStyle>About</NavLink>
          <NavBtnLink to='/signin'>Sign In</NavBtnLink>
        </NavMenu>
      </Nav>
    </>
  )
}

export default Navbar;