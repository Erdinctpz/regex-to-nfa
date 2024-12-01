class State:
    id_counter = 0
    def __init__(self):
        self.id = State.id_counter
        State.id_counter += 1
        
    def __repr__(self) -> str:
        return f'q{self.id}'
    
class SubNFA:
    def __init__(self, start_state, final_states=[]):
        self.start_state = start_state
        self.final_states = final_states
        
    def __repr__(self) -> str:
        return f'({self.start_state}, {self.final_states})'
    
class NFA:
    def __init__(self, transitions, start_state, final_state):
        self.transitions = transitions
        self.start_state = start_state
        self.final_state = final_state

class RegexToNFA:
    def __init__(self,regex) -> None:
        self.regex = infixToPostfix(regex)
        self.stack = [] #holds the sub NFAs
        self.transitions = {}
    
    def convert(self):
        for symbol in self.regex:
            if symbol.isalnum():
                start_state = State()
                final_state = State()
                sub_nfa = SubNFA(start_state=start_state, final_states=final_state)
                if start_state not in self.transitions:
                    self.transitions[f'{start_state}'] = {symbol: [f'{final_state}']}
                else:
                    self.transitions[f'{start_state}'].append({symbol: [f'{final_state}']})
                self.stack.append(sub_nfa)
            elif symbol == '+':
                prev_nfa2 = self.stack.pop()
                prev_nfa1 = self.stack.pop()
                start_state = State()
                final_state = State()
                if f'{start_state}' not in self.transitions:
                    self.transitions[f'{start_state}'] = {'ε': [f'{prev_nfa1.start_state}']}
                    self.transitions[f'{start_state}']['ε'].append(f'{prev_nfa2.start_state}')
                else:
                    self.transitions[f'{start_state}'].append({'ε': [f'{prev_nfa1.start_state}']})
                    self.transitions[f'{start_state}']['ε'].append(f'{prev_nfa2.start_state}')
                self.transitions[f'{prev_nfa1.final_states}'] = {'ε': [f'{final_state}']}
                self.transitions[f'{prev_nfa2.final_states}'] = {'ε': [f'{final_state}']}
                
                sub_nfa = SubNFA(start_state=start_state, final_states=final_state)
                self.stack.append(sub_nfa)
            elif symbol == '*':
                prev_nfa = self.stack.pop()
                start_state = State()
                final_state = State()
                self.transitions[f'{prev_nfa.final_states}'] = {'ε': [f'{prev_nfa.start_state}']}
                self.transitions[f'{start_state}'] = {'ε': [f'{prev_nfa.start_state}']}
                self.transitions[f'{prev_nfa.final_states}']['ε'].append(f'{final_state}')
                self.transitions[f'{start_state}']['ε'].append(f'{final_state}')
                sub_nfa = SubNFA(start_state=start_state, final_states=final_state)
                self.stack.append(sub_nfa)
            elif symbol == '.':
                prev_nfa2 = self.stack.pop()
                prev_nfa1 = self.stack.pop()
                if f'{prev_nfa1.final_states}' not in self.transitions:
                    self.transitions[f'{prev_nfa1.final_states}'] = {'ε': [f'{prev_nfa2.start_state}']}
                else:
                    self.transitions[f'{prev_nfa1.final_states}']['ε'].append(f'{prev_nfa2.start_state}')
                sub_nfa = SubNFA(start_state=prev_nfa1.start_state, final_states=prev_nfa2.final_states)
                self.stack.append(sub_nfa)
        
        lastSubNFA = self.stack.pop() # The last remaining subNFA on the stack
        nfa = NFA(self.transitions, lastSubNFA.start_state, lastSubNFA.final_states)
        
        return nfa
    
def infixToPostfix(regex):
    operators = []
    postfix = ""
    
    PRIORITY = {
        '+': 1,
        '.': 2,
        '*': 3
    }
    
    for symbol in regex:
        if symbol.isalnum():
            postfix += symbol
        elif symbol in ['+', '.', '*']:
            if (len(operators) != 0) and (operators[-1] != '(') and (PRIORITY[operators[-1]] >= PRIORITY[symbol]):
                while (len(operators) != 0) and operators[-1] != '(' and (PRIORITY[operators[-1]] >= PRIORITY[symbol]):
                    postfix += operators.pop()
                operators.append(symbol)
            else:
                operators.append(symbol)
        elif symbol == '(':
            operators.append(symbol)
        elif symbol == ')':
            while len(operators) != 0 and operators[-1] != '(':
                postfix += operators.pop()
            operators.pop()
            
    while operators:
        postfix += operators.pop()
    
    return postfix
    
    
if __name__ == '__main__':
    regex = input("Enter a regular expression:")
    converter = RegexToNFA(regex)
    nfa = converter.convert()
    
    for state, transition in sorted(nfa.transitions.items(), key=lambda tpl: int(tpl[0][1:])):
        print(f"{state}: {transition}")
        
    print("\nstart_state:", nfa.start_state)
    print("final_state:", nfa.final_state)