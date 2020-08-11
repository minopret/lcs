# Created: August 2020
# Author: Aaron Mansheim <aaron.mansheim@gmail.com>

from flask import Flask
from flask import request
from flask import make_response
import json
import jsonschema
import suffix_trees.STree

class MySTree(suffix_trees.STree.STree):

    # Overrides library code with changes, in order to
    # return every lcs, not only the first one.
    # The changes can be sent to the library's GitHub project as pull requests.

    def lcs(self, stringIdxs=-1):
        """Returns the Largest Common Substrings of Strings provided in stringIdxs.
        If stringIdxs is not provided, the LCS's of all strings are returned.

        ::param stringIdxs: Optional: List of indexes of strings.
        """
        if stringIdxs == -1 or not isinstance(stringIdxs, list):
            stringIdxs = set(range(len(self.word_starts)))
        else:
            stringIdxs = set(stringIdxs)

        deepestNodes = self._find_lcs(self.root, stringIdxs)
        return [self.word[n.idx:n.idx + n.depth]
                for n in deepestNodes]

    # Overrides library code with changes, in order to
    # return every lcs, not only the first one.
    # The changes can be sent to the library's GitHub project as pull requests.

    def _find_lcs(self, node, stringIdxs):
        """Helper method that finds LCS's by traversing the labeled GST."""
        nodes = [deepestNode 
                 for n in node.transition_links.values()
                 if n.generalized_idxs.issuperset(stringIdxs)
                 for deepestNode in self._find_lcs(n, stringIdxs)]

        if nodes == []:
            return [node]

        deepestNode = max(nodes, key=lambda n: n.depth)
        deepestNodes = [n for n in nodes if n.depth == deepestNode.depth]
        return deepestNodes

# The library's version 0.3.0 is limited to this many strings.
content_length_limit = 137465

app = Flask(__name__)
@app.route('/lcs', methods=['POST'])
def lcs():
    BAD_FORMAT = 'The format of the request was not acceptable. '
    if content_length_limit <= request.content_length:
        return make_response(
                BAD_FORMAT + 'Too much content.',
                413)
    elif request.content_length <= 0:
        return make_response(
                BAD_FORMAT + 'No content.',
                400)

    data = request.get_data()
    try:
        request_json = json.loads(data)
    except json.JSONDecodeError:
        return make_response(
                BAD_FORMAT + 'Not understood as JSON.',
                400)

    try:
        jsonschema.validate(
                instance=request_json,
                schema={
                    'type': 'object',
                    'properties': {
                        'setOfStrings': {
                            'type': 'array',
                            # 'minItems': 1,
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'value': {
                                        'type': 'string'
                                        }
                                    }
                                }
                            }
                        }
                    }
                )
    except ValidationError:
        return make_response(
                BAD_FORMAT + 'Not in the correct format.',
                400)

    values = [item['value'] for item in request_json['setOfStrings']]
    if not values:
        return make_response(
                BAD_FORMAT + 'setOfStrings should not be empty.',
                400)
    
    if len(set(values)) < len(values):
        return make_response(
                BAD_FORMAT + 'setOfStrings must be a Set.',
                400)

    tree = MySTree(values)
    result = sorted(tree.lcs())
    response_json = json.dumps(
            {
                'lcs': [{'value': value} for value in result]
            },
            separators=(',', ':'))
    response = make_response(response_json)
    response.mimetype = 'application/json'
    return response
