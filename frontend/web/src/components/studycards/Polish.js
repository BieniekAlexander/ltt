export function getDefinition(entry) { // TODO turn these into cards, not just string things
    return entry.lexeme.definitions[0]
}

export function getLemma(entry) {
    return entry.lexeme.lemma
}

const PolishStudyCardGenerators = {
    word_to_definition: {
        hint: getLemma,
        answer: getDefinition
    },
    definition_to_word: {
        hint: getDefinition,
        answer: getLemma
    }
}

export default PolishStudyCardGenerators