# FSA_simulator_1
<b>Implement an FSA validator.</b> 
Given an FSA description in the fsa.txt (see input file format) your program should output the result.txt containing an error description (see validation result) or a report, indicating if FSA is complete (or incomplete) and warning (see warning messages) if any. Warnings should be sorted according to their code. <br>
Validation result<br>
Errors:<br>
E1: A state 's' is not in the set of states<br>
E2: Some states are disjoint<br>
E3: A transition 'a' is not represented in the alphabet<br>
E4: Initial state is not defined<br>
E5: Input file is malformed<br>
Report:<br>
FSA is complete/incomplete<br>
Warnings:<br>
W1: Accepting state is not defined<br>
W2: Some states are not reachable from the initial state<br>
W3: FSA is nondeterministic<br>
Input file format<br>
states=[s1,s2,...]	  // s1 , s2, ... ∈ latin letters, words and numbers<br>
alpha=[a1,a2, ...]	  // a1 , a2, ... ∈ latin letters, words, numbers and character '_’(underscore)<br>
init.st=[s]	  // s ∈ states<br>
fin.st=[s1,s2,...]	  // s1, s2 ∈ states<br>
trans=[s1>a>s2,... ]<br>
  // s1,s2,...∈ states; a ∈ alpha<br>
Example 1<br>
fsa.txt<br>
states=[on,off]<br>
alpha=[turn_on,turn_off]    <br>
init.st=[off]<br>
fin.st=[]<br>
trans=[off>turn_on>off,on>turn_off>on]<br>
result.txt<br>
Error:<br>
E2: Some states are disjoint<br>
<br>
Example 2<br>
fsa.txt<br>
states=[on,off]<br>
alpha=[turn_on,turn_off]   <br> 
init.st=[off]<br>
fin.st=[]<br>
trans=[off>turn_on>on,on>turn_off>off]<br>
result.txt<br>
FSA is incomplete<br>
Warning:<br>
W1: Accepting state is not defined<br>
