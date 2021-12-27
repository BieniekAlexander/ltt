import React, {useState} from 'react';
import {MenuItems} from './MenuItems';
import {Link} from 'react-router-dom';
import './Dropdown.css';

function Dropdown() {
  const [click, setClick] = useState(false);
  const handleClick = () => setClick(!click);

  return <>
    <ul onClock={handleClick} className={click  ? 'dropdown-menu clicked' : 'dropdown-menu'}>
      {MenuItems.map((item, index) => {
        return (
          <li key={index}>
            <Link className={item.cName} to={item.path} onCLick={() => 
            setClick(false)}>
              {item.title}
            </Link>
          </li>
        )
      })}
    </ul>
  </>;
}

export default Dropdown;