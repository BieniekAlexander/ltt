import React, { useState } from 'react';
import TextSubmissionForm from '../components/TextSubmissionForm'
import AnnotatedTerm from '../components/AnnotatedTerm';
import styled from 'styled-components';
import './Annotations.css';
import { useAuth } from '../auth/AuthProvider';

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
        ret.push(<AnnotatedTerm key={index} {...annotation} />)
        i = j + annotation.term.length
    });

    ret.push(text.substring(i))
    return (<AnnotatedTextDiv className='annotatedText'>{ret}</AnnotatedTextDiv>)
}

export default function AnnotationsBody() {
    // const [annotated, setIsAnnotated] = useState(false);
    const {userId} = useAuth();
    const [annotations, setAnnotations] = useState(null);
    const [text, setText] = useState(null);

    const getAnnotationRequestBody = (text, language) => {
        console.log(userId)
        return JSON.stringify({
            text: text,
            language: language,
            user_id: userId
        })
    }

    const getAnnotations = (values, handleSubmit) => {
        setText(values.text)
        let requestBody = getAnnotationRequestBody(values.text, values.language)

        fetch(`${process.env.REACT_APP_BACKEND_URL}/annotate`, {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: requestBody}).then(response => response.json()
            ).catch(error => {
                console.error(error)
            }).then(data => {
                setAnnotations(data.annotations);
            }).catch(error => {
                console.error(error)
            })


    }

    return (
        <>
            {!annotations ?
                <div style={{ alignSelf: 'center', justifyContent: 'center', display: 'table', marginLeft: 'auto', marginRight: 'auto' }}>
                    <h2>Submit Text for Annotation :)</h2>
                    <TextSubmissionForm handleClick={getAnnotations.bind(this)} style={{ transform: "translateY(30px)" }} />
                </div>
                :
                getAnnotatedText(text, annotations)
            }
        </>
    )
}