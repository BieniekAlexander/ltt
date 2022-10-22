import React, { useState } from 'react';
import axios from 'axios';

export default function VocabularyBody() {
    const [entryCount, setEntryCount] = useState(100);

    // TODO make the vocabulary study session thing
    const getStudySession = async e => {
        e.preventDefault();
        // TODO
        axios({
            method: 'post',
            url: `${process.env.REACT_APP_BACKEND_URL}/training`,
            headers: { 'Content-Type': 'application/json' },
            data: {
                // ...
            }
        }).then(response => {
            // ...
        }).catch(error => { console.error(error) })
    }

    return (
        <>
            <h2 style={{ display: 'flex', justifyContent: 'center' }}>Vocabulary Training Session Thing</h2>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '90vh' }}>
                <form onSubmit={getStudySession}>
                    <label>
                        Study session size:<input type="int" value={entryCount} onChange={e => setEntryCount(e.target.value)} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        </>
    )
}