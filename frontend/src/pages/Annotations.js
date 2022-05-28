import React, { useState } from 'react';
import TextSubmissionForm from '../components/TextSubmissionForm'
import AnnotatedTerm from  '../components/AnnotatedTerm';
import styled from 'styled-components';
import './Annotations.css';

// styling
export const AnnotatedTextDiv = styled.div`
  margin: auto;
  margin-top: 50px;
  margin-bottom: 50px;
  width: 60%;
  padding: 10px;
  white-space: pre-wrap; // maintains whitespace behavior from non-html strings
`;

const getAnnotatedText = (text, annotations) => {
  let ret = []
  let i = 0

  annotations.forEach((annotation, index) => {
    let j = text.indexOf(annotation.term, i)
    let punctuation = text.slice(i, j)
    ret.push(punctuation)
    ret.push(<AnnotatedTerm key={index} {...annotation}/>)
    i = j+annotation.term.length
  });

  ret.push(text.substring(i))
  return (<AnnotatedTextDiv className='annotatedText'>{ret}</AnnotatedTextDiv>)
}

export default function AnnotationsBody() {
  // const [annotated, setIsAnnotated] = useState(false);
  const [annotations, setAnnotations] = useState(null);
  const [text, setText] = useState(null); 

  const getAnotationRequestBody = (text, language) => {
    return {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        language: language
      })
    }
  }

  const getAnnotations = (values, handleSubmit) => {
    setText(values.text)
    let requestBody = getAnotationRequestBody(values.text, values.language)
    fetch('http://localhost:8000/annotate', requestBody)
          .then(response => response.json())
          .catch(error => {
            console.error(error)}
          )
          .then(data => {
            console.log(data)
            setAnnotations(data.annotations);
          })
          .catch(error => {console.error(error)})

          
  }

  return (
    <>
    {!annotations ?
      <div style={{alignSelf: 'center', justifyContent:'center', display: 'table', marginLeft: 'auto', marginRight: 'auto'}}>
        <h2>Submit Text for Annotation :)</h2>
        <TextSubmissionForm handleClick={getAnnotations.bind(this)} style={{transform: "translateY(30px)"}}/>
      </div>
      :
      getAnnotatedText(text, annotations)
    }
      {/* // <AnnotatedTextDiv>
      // {annotations.annotations.map((d, idx) => {
          return (<AnnotatedTerm key={idx} {...d}/>)
        })}
      </AnnotatedTextDiv> */}

    </>
  )
}