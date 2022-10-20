import React from 'react';
import { ReactSession } from 'react-client-session';

const AboutBody = () => {
  ReactSession.setStoreType("cookie");
  ReactSession.set("username", "beanyak");

  return (
    <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '90vh'}}>
      <h1>About</h1>
    </div>
  );
};

export default AboutBody;