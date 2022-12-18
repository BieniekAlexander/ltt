import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthProvider';
import { stats_update, stats_session_init, push_study_entry } from '../training/sm2_anki/sm2_anki_utils'
const url = require('url');

const RECALL_OPTIONS = ['0','1','2','3']

export default function VocabularyBody() {
    const { userId } = useAuth()
    const [entryCount, setEntryCount] = useState(10)
    const [language, setLanguage] = useState("polish")
    const [currentEntry, setCurrentEntry] = useState(null)
    const [showHint, setShowHint] = useState(false)

    let state = useRef({
        entries: null,
        vocabulary: null
    });

    useEffect(() => {
        const keyDownHandler = event => {
            if (event.key === ' ') {
                event.preventDefault()
                setShowHint(!showHint)
            } else if (event.key in RECALL_OPTIONS) {
                handleStudyTerm(parseInt(event.key))
                setShowHint(false)
            }
        };

        document.addEventListener('keydown', keyDownHandler);

        return () => {
            document.removeEventListener('keydown', keyDownHandler);
        };
    }, [showHint, currentEntry]);

    const getStudySession = async (e) => {
        e.preventDefault();
        axios({
            method: 'GET',
            url: `${process.env.REACT_APP_BACKEND_URL}/training/study_set`,
            headers: { 'Content-Type': 'application/json' },
            params: {
                user_id: userId,
                count: entryCount,
                language: language
            }
        }).then(response => {
            state.current.vocabulary = response.data.entries
            state.current.entries = [...state.current.vocabulary]
            for (let i = 0; i < state.current.entries.length; i++) {
                stats_session_init(state.current.entries[i].stats.definition)
            }

            consumeStudyTerm()
        }).catch(error => { console.error(error) })
    }

    const consumeStudyTerm = () => {
        if (state.current.entries.length > 0) {
            setCurrentEntry(state.current.entries.shift())
        } else {
            console.log(state.current.vocabulary)
            // TODO terms are getting consumed, something here is failing with the PUT
            axios({
                method: 'PUT',
                url: `${process.env.REACT_APP_BACKEND_URL}/training/study_set`,
                headers: { 'Content-Type': 'application/json' },
                data: {
                    user_id: userId,
                    language: language,
                    entries: state.current.vocabulary // naming here is confusing
                }
            }).then(response => {
                console.log('persisted studied terms')
                setCurrentEntry(null)
                state.current.entries = null
                state.current.vocabulary = null
            }).catch(error => { console.error(error) })
        }
    }

    const handleStudyTerm = (recall) => {
        let entry = currentEntry
        stats_update(entry.stats.definition, recall)
        push_study_entry(state.current.entries, entry)
        consumeStudyTerm()
    }

    return (
        <>
            <h2 style={{ display: 'flex', justifyContent: 'center' }}>Vocabulary Training Session Thing</h2>
            {
                currentEntry
                    ?
                    <>
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '30vh' }}>
                            <div>
                                {
                                    [...Array(RECALL_OPTIONS.length).keys()].map((i) => {
                                        return <button key={`recall${i}`} value={i} onClick={() => { handleStudyTerm(i) }}>{i}</button>
                                    })
                                }
                            </div>
                            <button onClick={() => { setShowHint(!showHint) }}>Show Hint (space)</button>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <h3>{currentEntry.lexeme.lemma}</h3><br />
                        </div>
                        {
                            showHint &&
                            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                                <p>{currentEntry.lexeme.definitions[0]}</p><br />
                            </div>
                        }
                    </>
                    :
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '90vh' }}>
                        <form onSubmit={getStudySession}>
                            <label>
                                Study session count:<input type="int" value={entryCount} onChange={e => setEntryCount(e.target.value)} />
                            </label>
                            <label>
                                Study language:
                                <select id="language" name="language" value={language} onChange={e => setLanguage(e.target.value)}>
                                    <option value="polish">Polish</option>
                                    <option value="spanish">Spanish</option>
                                </select>
                            </label>
                            <input type="submit" value="Submit" />
                        </form>
                    </div>
            }

        </>
    )
}