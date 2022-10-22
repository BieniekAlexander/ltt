import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthProvider';
const url = require('url');

export default function VocabularyBody() {
    const { userId } = useAuth();
    const [entryCount, setEntryCount] = useState(100);
    const [language, setLanguage] = useState("polish")
    const [studySet, setStudySet] = useState(null)

    // TODO make the vocabulary study session thing
    const getStudySession = async e => {
        e.preventDefault();
        axios({
            method: 'GET',
            url: `${process.env.REACT_APP_BACKEND_URL}/training`,
            headers: { 'Content-Type': 'application/json' },
            params: {user_id: userId,
                count: entryCount,
                language: language
            }
        }).then(response => {
            setStudySet(response.data.entries)
            console.log(studySet)
        }).catch(error => { console.error(error) })
    }

    return (
        <>
            <h2 style={{ display: 'flex', justifyContent: 'center' }}>Vocabulary Training Session Thing</h2>
            {
                studySet
                ?
                // TODO I have the study set being rendered and brought to the UI, now I have to make sure a user can study the stuff
                <ul>
                    {studySet.map((item, i) => {
                        return <li>{JSON.stringify(item.lexeme)}</li>
                    })}
                </ul>
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