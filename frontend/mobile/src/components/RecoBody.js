import { REACT_APP_BACKEND_URL } from '@env';
import { Picker } from '@react-native-picker/picker';
import { getRecommendations } from 'shared';
import { postVocab } from 'shared';
import React, { useEffect, useRef, useState } from 'react';
import { Button, StyleSheet, Text, TextInput, View, ToastAndroid } from 'react-native';
import axios from 'axios'

const FACTS_LIST = [ // TODO dynamically pull from backend
    'spoken_to_definition',
    'definition_to_spoken',
    'word_to_definition',
    'definition_to_word',
    'written_to_definition',
]

DEFAULT_STATS_DICTS = { // TODO hacking this together, add checks for adding vocab stats to UI
    'polish': {
        'word_to_definition': {},
        'definition_to_word': {}
    },
    'chinese': {
        'spoken_to_definition': {},
        'definition_to_spoken': {},
        'written_to_definition': {}
    }
}

const RecoBody = () => {
    const userId = "62a57d5bfa96028f59ac1d75"
    const [recc_language, setRecc_language] = useState("chinese") // TODO setting to a stupid name because I think there's a global name collision?
    const [recommendations, setRecommendations] = useState({})

    const getReccs = async (e) => {
        // e.preventDefault()
        getRecommendations(
            REACT_APP_BACKEND_URL,
            userId,
            recc_language
        ).then(response => {
            setRecommendations(response.data)
        }).catch( error => {    
            console.log(error)
        })
    }

    /**
     * Add a recommended term to the user's vocab set
     * @param {*} lexeme_id
     */
    const addToVocab = async (lexeme_id) => {
        let stats = DEFAULT_STATS_DICTS[recc_language]
        console.log(recc_language)
        postVocab(
            REACT_APP_BACKEND_URL,
            userId,
            recc_language,
            lexeme_id,
            stats
        ).then(response => {
            let recsCopy = { ...recommendations }
            delete recsCopy[lexeme_id]
            setRecommendations(recsCopy)
        }).catch(error => {
            ToastAndroid.show(`intermittent error - ${error}`, ToastAndroid.SHORT);
            console.log(error)
        })
    }

    return (
        <>
            <Text style={{ display: 'flex', justifyContent: 'center' }}>Reccs View</Text>
                <Picker
                    selectedValue={recc_language}
                    onValueChange={(lang) => setRecc_language(lang)}>
                    <Picker.Item label="chinese" value="chinese" />
                    <Picker.Item label="polish" value="polish" />
                </Picker>
                <Button title="Pull Entries" onPress={getReccs} />
                <>
                {
                    Object.keys(recommendations).map((i) => {
                        return <Button key={`reco${i}`} value={i} title={`${recommendations[i].lemma} - ${recommendations[i].definitions[0]}`} onPress={() => { addToVocab(i) }} />
                    })
                }
                </>
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

export default RecoBody