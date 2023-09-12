import axios from 'axios'

/**
   * Gets a list of study terms from the backend, given some constraints
   * @param {!backendUrl} str the URL of the backend
   * @param {!userId} int the unique identifier of the user that's studying
   * @param {!language} str the language for which we want to get study terms
   */
export const postVocab = async (backendUrl, userId, language, lexeme_id, stats) => {
    // TODO I don't love using the backend URL as a parameter,
    // but I can't find a way for all of these node frameworks to use env vars the same
    return axios({ // TODO outdated call
        method: "POST",
        url: `${process.env.REACT_APP_BACKEND_URL}/vocabulary`,
        headers: { 'Content-Type': 'application/json' },
        data: JSON.stringify({
            lexeme_id: lexeme_id,
            user_id: userId,
            language: language,
            stats: stats // don't hardcode
        })
    })
}