import React, {useState} from 'react';
import Popover from '@mui/material/Popover';
import { Button } from '@mui/material';
import styled from 'styled-components';
import './AnnotatedTerm.css';

// styling
export const AnnotationPopover = styled(Popover)`
  max-height: 150px;
  max-width: 750px;
`;

const paper={
  style: { 
    minHeight: "50px",
    maxHeight: "150px",
    minWidth: "100px",
    maxWidth: "500px" }
}

export default function AnnotatedTerm(props) {
  // rendering
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [marked, setHighlighted] = React.useState(true);
  
  // data
  /*
  - lexeme, lexemeId, term will be populated
  - vocabularyId, rating will only be defined if text was annotated with a user account, and they will be null if the lexeme isn't in the user's vocabulary
  */
  const [lexeme, setLexeme] = useState(props.lexeme);
  const [lexemeId, setLexemeId] = useState(props.lexeme_id);
  const [term, setTerm] = useState(props.term);
  const [vocabularyId, setVocabularyId] = useState(props.vocabulary_id);
  const [rating, setRating] = useState(props.rating);
  const [user, setUser] = useState('aaaaaaaaaaaaaaaaaaaaaaaa');

  const annotatedTermOnClick = (event) => {
    if (event.ctrlKey) {
      if (lexemeId) { 
        addVocabularyTerm(lexemeId, user)
        // TODO add popup to make it obvious
      }
    } else {
      setAnchorEl(event.currentTarget);
    }
  };

  const closePopover = () => {
    setAnchorEl(null);
  };

  const getAddVocabularyBody = (lexemeId, userId) => {
    return {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lexeme_id: lexemeId,
        rating: 1.0,
        user_id: userId
      })
    }
  }

  const addVocabularyTerm = (lexemeId, userId) => {
    let requestBody = getAddVocabularyBody(lexemeId, userId)
    fetch('http://localhost:8000/vocabulary/addTerm', requestBody)
          .then(response => response.json())
          .then(data => {
            setVocabularyId(data.vocabulary_id);
          })
  }

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  const annotation = lexeme ? ( 
    <div style={{ padding: '10px 10px 10px 10px'}}>
      <h3>{lexeme.lemma}</h3>
      <ul>
        {lexeme.definitions.map((definition, i) => {
          // TODO maintain formatting and punctuation from input
          return (<li key={i}>{definition}</li>)
        })}
        {(vocabularyId === null) && // if the term is not in the user's vocab
          <Button onClick={(event, value) => addVocabularyTerm(props.lexeme_id, user)}>Add to Vocab</Button>
        }
      </ul>
    </div>
  ) : (
    <div style={{ padding: '10px 10px 10px 10px'}}>
      <span>Data not found...</span>
    </div>
  )

  return (
    <span>
      <span onClick={annotatedTermOnClick} className={`annotatedText ${marked ? "marked" : ""} ${!lexeme ? "missing" : ""} ${vocabularyId!==undefined ? (vocabularyId!==null ? "known" : "unknown") : ""}`}>
      {/* <span onClick={annotatedTermOnClick} className={`annotatedText ${vocabularyId!==undefined ? (vocabularyId!==null ? "known" : "unknown") : ""}`}> */}
        {props.term}
      </span>
      <Popover
        PaperProps={paper}
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={closePopover}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
      >
        {annotation}
      </Popover>
    {/* </OverlayTrigger> */}
    </span>
  )
}
