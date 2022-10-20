import React from 'react';
import { ReactSession } from 'react-client-session';

export default function VocabularyBody() {
  var name = ReactSession.get("username");

  return (
    <>
      <h1 className="Vocabulary">VOCABULARY {name} WILL GO HERE</h1>
    </>
  )
}