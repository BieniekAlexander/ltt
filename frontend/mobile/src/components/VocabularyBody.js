import { REACT_APP_BACKEND_URL } from '@env';
import { Picker } from '@react-native-picker/picker';
import axios from 'axios';
import { push_study_entry, stats_update, getArrayToggleValue, putStudySession, Recall, stats_session_init } from 'shared';
import { getStudySession } from 'shared';
import React, { useEffect, useRef, useState } from 'react';
import { Button, StyleSheet, Text, TextInput, View } from 'react-native';
import CheckBox from '@react-native-community/checkbox';
import NumericInput from 'react-native-numeric-input';
import StudyCardGenerators from '../components/studycards/StudyCardGenerators'

const RECALL_OPTIONS = ['0', '1', '2', '3']

const FACTS_LIST = [ // TODO dynamically pull from backend
    'spoken_to_definition',
    'definition_to_spoken',
    'word_to_definition',
    'definition_to_word',
    'written_to_definition',
]

const VocabularyBody = () => {
    // const { userId } = useAuth() TODO use useAuth to do auth with tokens and such
    const userId = "62a57d5bfa96028f59ac1d75"
    const [entryCount, setEntryCount] = useState(10)
    const [language, setLanguage] = useState("chinese")
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

    const consumeStudyTerm = async () => { // TODO resused in web and mobile, pull to common?
        if (state.current.entries.length > 0) {
            setCurrentEntry(state.current.entries.shift())
        } else {
            putStudySession(
                REACT_APP_BACKEND_URL,
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
    const handleStudyTerm = async (recallValue) => {
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
            REACT_APP_BACKEND_URL, userId, language, facts, entryCount
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
            <Text style={{ display: 'flex', justifyContent: 'center' }}>Vocabulary Training Session Thing</Text>
            {
                currentEntry
                    ?
                    <>
                        <>
                            {
                                [...Array(RECALL_OPTIONS.length).keys()].map((i) => {
                                    return <Button key={`recall${i}`} value={i} title={String(i)} onPress={() => { handleStudyTerm(i) }} />
                                })
                            }
                            <Button title="Suspend" onPress={() => { handleStudyTerm(Recall.SUSPEND) }} />
                            <Button title="Forget" onPress={ forgetStudyTerm } />
                            {/* TODO for testing, remove */}
                            <Button title="Abort" onPress={ () => {setCurrentEntry(null); state.current.entries=[]} } />
                        </>
                        <Button onPress={() => { setShowHint(!showHint) }} title="Show Hint" />
                        {/* // TODO I messed up the naming of hint and answer here - showHint doesn't make sense, should be show answer */}
                        <Text>{getHint(currentEntry)}</Text>
                        {
                            showHint &&
                            <Text>{getAnswer(currentEntry)}</Text>
                        }
                    </>
                    :
                    <View>
                        <Text>Language</Text>
                        <Picker
                            selectedValue={language}
                            onValueChange={(lang) => setLanguage(lang)}>
                            <Picker.Item label="chinese" value="chinese" />
                            <Picker.Item label="polish" value="polish" />
                        </Picker>

                        {/* Fact checklist */}
                        <View>
                        {
                            [...Array(FACTS_LIST.length).keys()].map((i) => {
                                let id = `fact${i}`
                                let fact = FACTS_LIST[i]
                                return <View key={`fact${i}`}>
                                    <Text>{fact}</Text>
                                    <View style={styles.container}>
                                        <CheckBox
                                            value={facts.includes(fact)}
                                            onValueChange={(newValue) => {setFacts(getArrayToggleValue(facts, fact, newValue))}}
                                        />
                                    </View>
                                </View>
                            })
                        }
                        </View>


                        <Text>Study session count</Text>
                        <NumericInput initValue={entryCount} onChange={(value) => setEntryCount(value)} />

                        <Button onPress={loadStudySession} title="Study!" />
                    </View>
            }

        </>
    )
}

const styles = StyleSheet.create({
    container: {
      flex: .3,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#F5FCFF',
    }
})

export default VocabularyBody