// src: https://letsbuildui.dev/articles/building-a-dropdown-menu-component-with-react-hooks
import React, { useRef, useState } from "react";
import "./Dropdown.css";
import styled from 'styled-components';
import { useDetectOutsideClick } from "../functions/useDetectOutsideClick";
import { NavLink } from "./NavBar";

// styling
export const DropdownUL = styled.ul`
  margin-right: 24px;
  position: relative;
  menu-placement: bottom;
`;

export const DropdownLI = styled.li`
  background: #000;
  padding: 6px 0px;
  border: 1px solid #FFF;
  list-style: none;
`;

export const DropdownNav = styled.nav`
  position: absolute;
  top: -20px;
  left: 0px;
  transform: translateY(50px);
`;

export const styling = {
    'position': 'relative',
    'display': 'flex'
}

export default function Dropdown() {
    // TODO dropdown gets messed up when I mess around with annotation popups too
    const dropdownRef = useRef(null);
    const [isActive, setIsActive] = useDetectOutsideClick(dropdownRef, false);
    const closeDropdown = () => setIsActive(false);
    const onClick = () => setIsActive(!isActive);

    return (
        <div className="container">
            <div className="menu-container" style={styling}>
                <NavLink to="#" onClick={onClick} className="navbar">
                    Training <i className='fas fa-caret-down' />
                </NavLink>

                {isActive &&
                    <DropdownNav ref={dropdownRef} className="menu">
                        <DropdownUL>
                            <DropdownLI>
                                <NavLink to="/annotations" onClick={closeDropdown} className="navbar">Annotations</NavLink>
                            </DropdownLI>
                            <DropdownLI>
                                <NavLink to="/inflections" onClick={closeDropdown} className="navbar">Inflections</NavLink>
                            </DropdownLI>
                            <DropdownLI>
                                <NavLink to="/vocabulary" onClick={closeDropdown} className="navbar">Vocabulary</NavLink>
                            </DropdownLI>
                        </DropdownUL>
                    </DropdownNav>}
            </div>
        </div>
    );
}
