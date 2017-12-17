from lxml import etree
import jamm.exception
import numbers


def parse(s, file='<console>', **kwargs):
    """
    Parse a string of Jam Code
    :param s: string
    :param file: file path to use in exceptions. defaults to <console>
    :param kwargs: initial variables to pass to parser
    :return:
    """
    try:
        root = etree.fromstring(s)
    except etree.XMLSyntaxError as e:
        raise jamm.exception.Syntax(e)
    if root.tag != 'code':
        raise jamm.exception.Syntax('Invalid root tag "{root}" in file "{file}"'.format(root=root.tag, file=file))
    _parse(root, file, kwargs)


# noinspection PyShadowingBuiltins
def _parse(root, file, vars):
    for tag in root:
        if tag.tag == 'if':
            if 'type' not in tag.attrib.keys():
                raise jamm.exception.Syntax('No condition type specified for condition on line {line}'.format(
                    line=tag.sourceline))
            condition_type = tag.get('type')
            # type of if statement - variable, key state, window exist/active
            if condition_type in ('eq', 'lt', 'gt', 'lte', 'gte', 'neq'):  # var if statement
                if 'variable' not in tag.attrib.keys() or not tag.get('variable'):  # variable not specified
                    raise jamm.exception.Syntax('No variable specified for condition on line {line}'.format(
                        line=tag.sourceline))
                elif tag.get('variable') not in vars.keys():  # variable doesn't exist
                    raise jamm.exception.Name('Variable {var} not found in condition on line {line}'.format(
                        line=tag.sourceline, var=tag.get('variable')))
                elif tag.get('value') not in tag.attrib.keys():  # value not specified
                    raise jamm.exception.Syntax('No value specified for condition on line {line}'.format(
                        line=tag.sourceline))
                if condition_type in ('lt', 'gt', 'lte', 'gt'):  # numeric only conditionals
                    if not isinstance(vars.get(tag.get('variable')), numbers.Number):  # not a number
                        raise jamm.exception.Type('Invalid target for operator {op}'  # can't use this operator
                                                  ' in condition on line {line}'.format(op=condition_type,
                                                                                        line=tag.sourceline))
                if (condition_type == 'eq' and   # == != < <= > >= true
                        evaluate(tag.get('value'), vars, tag.sourceline) == tag.get('value')) or (
                    condition_type == 'neq' and
                        evaluate(tag.get('value'), vars, tag.sourceline) != tag.get('value')) or (
                    condition_type == 'lt' and
                        evaluate(tag.get('value'), vars, tag.sourceline) < tag.get('value')) or (
                    condition_type == 'lte' and
                        evaluate(tag.get('value'), vars, tag.sourceline) <= tag.get('value')) or (
                    condition_type == 'gt' and
                        evaluate(tag.get('value'), vars, tag.sourceline) > tag.get('value')) or (
                    condition_type == 'gte' and
                        evaluate(tag.get('value'), vars, tag.sourceline) >= tag.get('value')) or (
                    condition_type == 'true'
                ):
                    _parse(tag, file, vars)
            elif condition_type == 'false':  # always false - pass so doesn't get caught by else and error thrown
                pass
            else:
                raise jamm.exception.Syntax('Invalid type attribute "{type}" for condition on line {line}'.format(
                    type=condition_type, line=tag.sourceline))


# noinspection PyShadowingBuiltins
def evaluate(s, vars, line):
    # TODO: implement functions, maths etc.
    escape = False
    close = False
    for char, index in enumerate(s):
        if escape:
            escape = False
            continue
        if char == '%':
            if s[index+1] == '%':  # escaped percent sign
                escape = True
            elif close:  # expecting closing percent
                # `close` will only ever be true when i'm a starting percent sign
                # in which case var_start will have been defined.
                # noinspection PyUnboundLocalVariable
                var_name = s[var_start:index-1]
                if var_name not in vars.keys():
                    raise jamm.exception.Name('Variable {variable} not found on line {line}'.format(variable=var_name,
                                                                                                    line=line))
                return vars[var_name]
            else:
                close = True
                var_start = index + 1
