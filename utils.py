def stripBrackets(content):
    start = content.find('(')+1
    end = content.rfind(')')
    return content[start:end]

def findRefs(brackets):
    refs = []
    ends = [i for i, x in enumerate(brackets) if x in [',',')']]
    begings = [i for i, x in enumerate(brackets) if x in ['#']]
    for b in begings:
        end = [e for e in ends if e > b][0]
        refs.append(brackets[b:end][1:])
    return refs
