from geosolver.text.lexer.states import Token
from geosolver.text.semantics.states import SemanticNode, SourceNode, SinkNode

__author__ = 'minjoon'

def semantic_proximity_score(syntax_proximity_score_function, ontology_proximity_score_function,
                             from_node, to_node, arg_idx):
    """
    Combines two score functions (syntax and basic_ontology).
    Can be as simple as the multiplication of the two (which is the case now).

    :param syntax_proximity_score_function:
    :param ontology_proximity_score_function:
    :param from_node:
    :param to_node:
    :return:
    """
    assert isinstance(from_node, SemanticNode)
    assert isinstance(to_node, SemanticNode)

    syntax = from_node.syntax
    basic_ontology = from_node.basic_ontology

    from_token = from_node.token
    to_token = to_node.token
    from_function = from_node.function
    to_function = to_node.function

    assert isinstance(from_token, Token)
    assert isinstance(to_token, Token)

    if isinstance(from_token, Token) and isinstance(to_token, Token):
        syntax_score = syntax_proximity_score_function(syntax, from_token, to_token)
    else:
        syntax_score = 1
    ontology_score = ontology_proximity_score_function(basic_ontology, from_function, to_function, arg_idx)
    return syntax_score * ontology_score


def node_syntax_score(syntax, score_function, from_node, to_node):
    if isinstance(from_node, SourceNode):
        return 1
    elif isinstance(to_node, SinkNode):
        return 1
    else:
        assert isinstance(from_node, SemanticNode)
        assert isinstance(to_node, SemanticNode)
        return score_function(syntax, from_node, to_node)


def node_ontology_score(basic_ontology, score_function, from_node, to_node):
    if isinstance(from_node, SourceNode):
        assert isinstance(to_node, SemanticNode)
        if from_node.type is to_node.function.return_type:
            return 1
        else:
            return 0