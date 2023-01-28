export function getDefinition(entry) { // TODO turn these into cards, not just string things
    return entry.lexeme.definitions[0]
}

export function getRomanization(entry) {
    return entry.lexeme.romanizations.jyutping
}

export function getLemma(entry) {
    return entry.lexeme.lemma
}

const ChineseStudyCardGenerators = {
    spoken_to_definition: {
        hint: getRomanization,
        answer: getDefinition
    },
    definition_to_spoken: {
        hint: getDefinition,
        answer: getRomanization
    },
    written_to_definition: {
        hint: getLemma,
        answer: getDefinition
    }
}

export default ChineseStudyCardGenerators