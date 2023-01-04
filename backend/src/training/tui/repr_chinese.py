from textwrap import dedent

### WRITTEN ###
def written_hint_repr(entry):
    return dedent(f"""
    {entry['lexeme'].lemma}
    """).strip()

def written_answer_repr(entry):
    # TODO handle words that don't have romanizations right now, they probably should
    return (
    (entry['lexeme'].romanizations['jyutping'] if entry['lexeme'].romanizations != {} else "romanization not found") + '\n'
    + '\n'
    + '\n'.join(entry['lexeme'].definitions)
    )

### SPOKEN ###
def written_hint_repr(entry):
    return dedent(f"""
    {entry['lexeme'].romanizations['jyutping']}
    
    {entry['lexeme'].lemma}
    """).strip()

def written_answer_repr(entry):
    # TODO handle words that don't have romanizations right now, they probably should
    return '\n'.join(entry['lexeme'].definitions)