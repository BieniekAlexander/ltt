from textwrap import dedent

def definition_hint_repr(entry):
    return dedent(f"""
    {entry['lexeme'].lemma}
    
    {entry['lexeme'].pos.lower()}
    """).strip()

def definition_answer_repr(entry):
    return "\n".join(entry['lexeme'].definitions)