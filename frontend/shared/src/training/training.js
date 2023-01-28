import axios from 'axios'

/**
   * Gets a list of study terms from the backend, given some constraints
   * @param {!backendUrl} str the URL of the backend
   * @param {!userId} int the unique identifier of the user that's studying
   * @param {!language} str the language for which we want to get study terms
   * @param {!fact} str the study fact for which we want to get flashcards
   * @param {!count} int the number of study items we want to get
   * @returns {list} a list of terms for studying
   */
export const getStudySession = async (backendUrl, userId, language, facts, count) => {
    // TODO I don't love using the backend URL as a parameter,
    // but I can't find a way for all of these node frameworks to use env vars the same
    return axios({
        method: 'GET',
        url: `${backendUrl}/training/study_set`,
        headers: { 'Content-Type': 'application/json' },
        params: {
            user_id: userId,
            count: count,
            language: language,
            facts: facts
        }
    })
}

/**
   * PUT a list of study terms to the backend
   * @param {!backendUrl} str the URL of the backend
   * @param {!userId} int the unique identifier of the user that's studying
   * @param {!entryies} list a list of terms that were studied
   * @returns {list} a list of terms for studying
   */
export const putStudySession = async (backendUrl, userId, language, entries) => {
    return axios({
        method: 'PUT',
        url: `${backendUrl}/training/study_set`,
        headers: { 'Content-Type': 'application/json' },
        data: {
            user_id: userId,
            language: language,
            entries: entries
        }
    })
}