# condig=utf


class Calculator(object):
    def eval(self, text):
        tree = self._parse(text)
        return self._eval_tree(tree)

    def _parse(self, text):
        # parse_tree = ExprParser.parse(text)
        return None
        # return parse_tree

    def _repr_tree(self, text):
        return ExprParser.repr_parse_tree(self._parse(text))

    def _eval_tree(self, tree):
        pass
