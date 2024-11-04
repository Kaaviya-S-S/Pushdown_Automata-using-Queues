from io import BytesIO
import streamlit as st
import visualize

# Validation function for a^n b^n c^n language
def validate_L1(inputstring):
    queue = []
    enqueue, dequeue = -1, 0  
    phase = 1 

    steps = [("epsilon", list(queue))]  

    for x in inputstring:
        steps.append((x, list(queue)))  

        if phase == 1:
            if x == "a":
                enqueue += 1
                queue.append("a") 
            elif x == "b" and enqueue >= 0:
                enqueue += 1
                queue.append("b")  
                queue.pop(dequeue)  
                enqueue -= 1 
                phase = 2 
            else:
                return "Invalid input string", steps

        elif phase == 2:
            if x == "b" and enqueue >= 0:
                enqueue += 1
                queue.append("b") 
                queue.pop(dequeue)  
                enqueue -= 1  
            elif x == "c" and queue[dequeue] == "b":
                queue.pop(dequeue)  
                enqueue -= 1 
                phase = 3  
            else:
                return "Invalid input string", steps

        elif phase == 3:
            if x == "c" and enqueue >= 0:
                if queue[dequeue] == "b":
                    queue.pop(dequeue) 
                    enqueue -= 1
                else:
                    return "Invalid input string", steps
            else:
                return "Invalid input string", steps

    steps.append(("epsilon", list(queue)))  

    if enqueue == -1 and len(queue) == 0:
        return "Valid input string", steps
    else:
        return "Invalid input string", steps
    
# Validation function for a^n b^m a^n b^m language
def validate_L2(inputstring):
    front = 0
    rear = 0
    queue = []
    phase = 1 
    steps = [] 
    steps.append(("epsilon", list(queue)))
    for x in inputstring:
        steps.append((x, list(queue)))

        if phase == 1:
            if x=="a" and front==rear:
                queue.append("a")
                front += 1
            elif x=="a":
                queue.append("a")
                front += 1
            elif x == "b":
                queue.append("b")
                front += 1
                phase = 2  # state 2
            else:
                return "Invalid input string", steps
            print(front)

        elif phase == 2:
            if x=="b":
                queue.append("b")
                front += 1
            elif x == "a" and queue[rear]=="a":
                queue.pop(rear)
                front -= 1
                phase = 3  # state 3
            else:
                return "Invalid input string", steps
            print(front)

        elif phase == 3:
            if x=="a" and queue[rear] == "a":
                front -= 1
                queue.pop(rear)
            elif x == "b" and queue[rear]=="b":
                front -= 1
                queue.pop(rear)
                phase = 4  # state 4
            else:
                return "Invalid input string", steps
            print(front)
        
        elif phase == 4:
            if x == "b" and queue[rear]=="b":
                front -= 1
                queue.pop(rear)
            else:
                return "Invalid input string", steps
            print(front)
        
    steps.append(("epsilon", list(queue)))
    if front==rear and phase==4:
        return "Valid input string", steps
    else:
        return "Invalid input string", steps

# Validation function for a^m b^(2m+1) language
def validate_L3(inputstring):
    front = 0
    rear = 0
    queue = []
    phase = 1 
    steps = [] 
    steps.append(("", list(queue)))
    for x in inputstring:
        steps.append((x, list(queue)))

        if phase == 1:
            if x=="a" and front==rear:
                queue.append("a")
                front += 1
            elif x=="a":
                queue.append("a")
                front += 1
            elif x == "b":
                phase = 2  # state 2
            else:
                return "Invalid input string", steps
            print(front)

        elif phase == 2:
            if x=="b":
                phase = 3  # state 3
            else:
                return "Invalid input string", steps
            print(front)

        elif phase == 3:
            if x == "b":
                front -= 1
                queue.pop(rear)
                phase = 4  # state 4
            else:
                return "Invalid input string", steps
            print(front)
        
        elif phase == 4:
            if x == "b":
                phase = 3
            else:
                return "Invalid input string", steps
            print(front)
        
    steps.append(("", list(queue)))
    if front==rear and phase==4:
        return "Valid input string", steps
    else:
        return "Invalid input string", steps

# Validation function for a^n b^(n+k) c^m language
def validate_L4(inputstring):
    queue = []
    enqueue, dequeue = -1, 0
    phase = 1 
    
    steps = [("epsilon", list(queue))]
    
    for x in inputstring:
        steps.append((x, list(queue)))
        if phase == 1:
            if x=="a" and enqueue==-1:
                enqueue += 1
                queue.append("a")
            elif x=="a" and queue[enqueue] == "a":
                enqueue += 1
                queue.append("a")
            elif x == "b" and enqueue!=-1 and queue[dequeue] == "a":
                enqueue += 1
                queue.append("0")
                queue.pop(dequeue)
                enqueue -= 1
                phase = 2  # state 2
            else:
                return "Invalid input string", steps

        elif phase == 2:
            if x=="b" and queue[enqueue] == "0" and queue[dequeue] == "a":
                enqueue += 1
                queue.append("0")
                queue.pop(dequeue)
                enqueue -= 1
            elif x == "b" and queue[enqueue] == "0" and queue[dequeue] == "0":
                continue
            elif x=="c"and queue[dequeue] == "0":
                queue.pop(dequeue)
                enqueue -= 1
                phase=3
            else:
                return "Invalid input string", steps

        elif phase == 3:
            if  x == "c" and enqueue!=-1:
                queue.pop(dequeue)
                enqueue -= 1
            else:
                return "Invalid input string", steps

    steps.append(("epsilon", list(queue)))
    if enqueue!=-1 and queue[dequeue]=="0":
        return "Valid input string", steps
    else:
        return "Invalid input string", steps
    

def reset_session_state():
    """Resets session variables that should be cleared when language or input string changes."""
    st.session_state.result = "Invalid input string"
    st.session_state.steps = [[None, None]]
    st.session_state.queue_index = 0
    st.session_state.queue = []

# Initialize session variables if not already set
if "language" not in st.session_state:
    st.session_state.language = None
if "inputstring" not in st.session_state:
    st.session_state.inputstring = None
    
# Visualization of Pushdown Automata with Queue
st.title("Pushdown Automata with Queue")

language = st.selectbox("Select Language", ["L = {a^n b^n c^n | n>=1}",
                                            "L = {a^n b^(n+k) c^m where k any integer(>=0) and m<n}",
                                            "L = {a^n b^m a^n b^m | m,n>=1}",
                                            "L = {a^m b^(2m+1) | m>=1}"])
inputstring = st.text_input("Enter the string to validate")

# Check if language or input string has changed
if st.session_state.language != language or st.session_state.inputstring != inputstring:
    reset_session_state()
    st.session_state.language = language
    st.session_state.inputstring = inputstring

# Initialize session variables
if "current_pda" not in st.session_state:
    st.session_state.current_pda = None
if "steps" not in st.session_state:
   st.session_state.steps = [[None, None]]
if "result" not in st.session_state:
    st.session_state.result = "Invalid input string"
if "queue_index" not in st.session_state:
    st.session_state.queue_index = 0
if "queue" not in st.session_state:
    st.session_state.queue = []


if st.button("Validate"):
    if language == "L = {a^n b^n c^n | n>=1}":
        if len(inputstring) != 0:
            st.session_state.result, st.session_state.steps = validate_L1(inputstring)
            st.session_state.current_state = visualize.pda_1["start_state"]
            st.session_state.current_pda = visualize.pda_1 
            #print(st.session_state.steps)
            
    elif language == "L = {a^n b^m a^n b^m | m,n>=1}":
        st.session_state.current_pda = visualize.pda_2
        st.session_state.result, st.session_state.steps = validate_L2(inputstring)
        st.session_state.current_state = visualize.pda_2["start_state"]
        print(st.session_state.steps)
    
    elif language == "L = {a^m b^(2m+1) | m>=1}":
        st.session_state.current_pda = visualize.pda_3
        st.session_state.result, st.session_state.steps = validate_L3(inputstring)
        st.session_state.current_state = visualize.pda_3["start_state"]
        print(st.session_state.steps)
    
    elif language== "L = {a^n b^(n+k) c^m where k any integer(>=0) and m<n}":
        st.session_state.current_pda = visualize.pda_4
        st.session_state.result, st.session_state.steps = validate_L4(inputstring)
        st.session_state.current_state = visualize.pda_4["start_state"]
        print(st.session_state.steps)
        
    st.write(st.session_state.result)
      
# Navigation for steps
if st.session_state.result == "Valid input string":
    # Inside the if st.button("Next Step"): block
    if st.button("Next Step"):
        if st.session_state.queue_index < len(st.session_state.steps) - 1:
            st.session_state.queue_index += 1
        else:
            st.warning("No more steps available!")

    # Get the current step details
    current_step = st.session_state.steps[st.session_state.queue_index]
    input_char = current_step[0]
    current_queue = current_step[1]

    # Update queue visualization
    fig = visualize.visualize_queue(st.session_state.steps, current_queue)
    st.pyplot(fig)

    # Get stack tops
    enqueue_end = current_queue[-1] if current_queue else "epsilon"  # Default to z0 if empty
    dequeue_end = current_queue[0] if len(current_queue) > 0 else "epsilon"  # Default to z0 if empty
    
    # Find next state and stack operations
    def find_next_state(pda, current_state, input_char, enqueue_end, dequeue_end):
        for (from_state, char, stack_ops, stack_symbols), to_state in pda['transitions'].items():
            if (from_state == current_state and 
                (char == input_char or char == "epsilon") and
                stack_ops.split('|')[0] == enqueue_end and
                stack_symbols.split('|')[0] == dequeue_end):
                return to_state, stack_ops, stack_symbols
        return current_state, None, None

    # Get next state and operations
    next_state, stack_ops, stack_symbols = find_next_state(
        st.session_state.current_pda,
        st.session_state.current_state,
        input_char,
        enqueue_end,
        dequeue_end
    )
    print(next_state, stack_ops, stack_symbols)
    # Visualize the transition
    pda_diagram = visualize.visualize_transition(
        st.session_state.current_pda,
        st.session_state.current_state,
        input_char,
        stack_ops,
        stack_symbols
    )
    st.graphviz_chart(pda_diagram.source)

    # Update current state in session state
    st.session_state.current_state = next_state



# Button to generate PDA visualization without validation
if st.button("Generate PDA Visualization"):
    if language == "L = {a^n b^n c^n | n>=1}":
        st.session_state.current_pda = visualize.pda_1  
    elif language == "L = {a^n b^m a^n b^m | m,n>=1}":
        st.session_state.current_pda = visualize.pda_2
    elif language == "L = {a^m b^(2m+1) | m>=1}":
        st.session_state.current_pda = visualize.pda_3
    elif language == "L = {a^n b^(n+k) c^m where k any integer(>=0) and m<n}":
        st.session_state.current_pda = visualize.pda_4

    pda = visualize.generate_pda_visualization(st.session_state.current_pda)
    st.write("*Pushdown Automaton*")
    st.graphviz_chart(pda.source)

