import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../auth/AuthProvider';
import { stats_update, stats_session_init, push_study_entry, getStudySession, putStudySession, Recall, getArrayToggleValue } from 'shared'
import StudyCardGenerators from '../components/studycards/StudyCardGenerators'

const RECALL_OPTIONS = ['0', '1', '2', '3']
const FACTS_LIST = [ // TODO dynamically pull from backend
    'spoken_to_definition',
    'definition_to_spoken',
    'word_to_definition',
    'definition_to_word',
    'written_to_definition',
]

export function VocabularyCard({ hint, answer, showHint }) {
    return (
        // TODO I messed up the naming of hint and answer here - showHint doesn't make sense, should be show answer
        <>
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <h3>{hint}</h3><br />
            </div>
            {
                showHint &&
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <p>{answer}</p><br />
                </div>
            }
        </>
    )
}

export default function VocabularyBody() {
    const { userId } = useAuth()
    const [count, setCount] = useState(10)
    const [language, setLanguage] = useState("polish")
    const [facts, setFacts] = useState([])
    const [currentEntry, setCurrentEntry] = useState(null)
    const [showHint, setShowHint] = useState(false)
    const [getHint, setGetHint] = useState(() => { })
    const [getAnswer, setGetAnswer] = useState(() => { })

    let state = useRef({
        entries: null,
        vocabulary: null,
        entry_fact_map: {}  // used to specify which fact of the vocabulary term is being used for studying,
        // given that we might pull multiple facts into the session
    });

    useEffect(() => {
        // update the hint and answer generators according to the entry we're studying
        setShowHint(false)

        if (currentEntry) {
            let fact = state.current.entry_fact_map[currentEntry.lexeme_id]
            setGetHint(() => StudyCardGenerators[language][fact].hint)
            setGetAnswer(() => StudyCardGenerators[language][fact].answer)
        } else {
            setGetHint(() => () => { })
            setGetAnswer(() => () => { })
        }
    }, [currentEntry])

    useEffect(() => {
        // handle key events
        const keyDownHandler = event => {
            if (currentEntry != null) { // ignore keypresses when they're not during a study session
                // TODO I should probably add sme code to make it so that the keypresses are also ignored in certain contexts,
                // i.e. a textfield is selected
                if (event.key === ' ') {
                    event.preventDefault()
                    setShowHint(!showHint)
                } else if (event.key === 'f') { // forget the study term
                    forgetStudyTerm()
                } else if (event.key === 's') { // suspend the term
                    handleStudyTerm(Recall.toValue(Recall.SUSPEND))
                } else if (event.key in RECALL_OPTIONS) { // study the term
                    handleStudyTerm(parseInt(event.key))
                }
            }
        };

        document.addEventListener('keydown', keyDownHandler);

        return () => {
            document.removeEventListener('keydown', keyDownHandler);
        };
    }, [showHint, currentEntry]);

    const consumeStudyTerm = async () => {
        if (state.current.entries.length > 0) {
            setCurrentEntry(state.current.entries.shift())
        } else {
            putStudySession(
                process.env.REACT_APP_BACKEND_URL,
                userId,
                language,
                state.current.vocabulary
            ).then(response => {
                setCurrentEntry(null)
                state.current.entries = null
                state.current.vocabulary = null
                state.current.entry_fact_map = {}
            }).catch((error) => {
                console.log(error)
            })
        }
    }

    /**
     * Update the term that was just studied according to the fact we're studying and the recall we gave it
     * @param {*} recallValue
     */
    const handleStudyTerm = (recallValue) => {
        let recall = Recall.fromValue(recallValue)
        let entry = currentEntry
        let fact = state.current.entry_fact_map[entry.lexeme_id]
        stats_update(entry.stats[fact], recall)
        push_study_entry(state.current.entries, fact, entry)
        consumeStudyTerm()
    }

    /**
     * Remove the fact from the term being studied
     * Note that the entry is not pushed back into the study entry queue
     */
    const forgetStudyTerm = () => {
        let entry = currentEntry
        let fact = state.current.entry_fact_map[entry.lexeme_id]
        delete entry.stats[fact]
        consumeStudyTerm()
    }

    /**
     * TODO
     * this function takes form data to collect vocabulary data from the backend and preprocess it for studying
     * @param {*} e the event that is instantiating the study session
     */
    const loadStudySession = async (e) => {
        e.preventDefault()
        getStudySession(
            process.env.REACT_APP_BACKEND_URL, userId, language, facts, count
        ).then(response => {
            if (response.data.entries.length == 0) {
                alert(`Got no study entries for language=${language}, facts=${facts}`)
            } else {
                state.current.vocabulary = response.data.entries
                state.current.entries = [...state.current.vocabulary]
                for (let i = 0; i < state.current.entries.length; i++) {
                    let entry = state.current.entries[i]
                    let stats = entry.stats
                    Object.entries(stats).forEach(([k, v]) => {
                        stats_session_init(v)
                    });

                    // set the thing being studied for the term to be the first stats entry (stats entries are sorted in the backend)
                    let study_fact = Object.keys(stats)[0]
                    state.current.entry_fact_map[entry.lexeme_id] = study_fact
                }
                consumeStudyTerm()
            }
        }).catch(error => { console.error(error) })
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
                            <button onClick={() => { forgetStudyTerm() }}>Forget ('f')</button>
                            <button onClick={() => { handleStudyTerm(Recall.toValue(Recall.SUSPEND)) }}>Suspend ('s')</button>
                        </div>

                        {
                            currentEntry &&
                            <VocabularyCard hint={getHint(currentEntry)} answer={getAnswer(currentEntry)} showHint={showHint} />
                        }
                    </>
                    :
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '90vh' }}>
                        <form onSubmit={loadStudySession}>
                            <label>
                                Study session count:<input type="int" value={count} onChange={e => setCount(e.target.value)} />
                            </label>

                            <label>
                                Study language:
                                <select id="language" name="language" value={language} onChange={e => setLanguage(e.target.value)}>
                                    <option value="polish">Polish</option>
                                    <option value="spanish">Spanish</option>
                                    <option value="chinese">Chinese</option>
                                </select>
                            </label>

                            {/* Fact checklist */}
                            {
                                [...Array(FACTS_LIST.length).keys()].map((i) => {
                                    let id = `fact${i}`
                                    let fact = FACTS_LIST[i]
                                    return <div key={`fact${i}`}>
                                        <label htmlFor={id} style={{ display: "inline-block" }} key={`factLabel${i}`}>{fact}</label>
                                        <input type="checkbox" id={id} name={id} value={fact} key={`factCheckbox${i}`}
                                            onChange={e => setFacts(getArrayToggleValue(facts, e.target.value, e.target.checked))}
                                        />
                                    </div>
                                })
                            }

                            <input type="submit" value="Submit" />
                        </form>
                    </div>
            }

        </>
    )
}