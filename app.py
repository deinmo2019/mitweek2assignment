import csv
import io
import streamlit as st
from game_logic import QUESTIONS, PATTERNS, chatbot_answer, predict_pattern

st.set_page_config(page_title='Human vs Rule-Based AI', page_icon='🧠', layout='wide')
st.title('🧠 Human vs Rule-Based AI')
st.write('Play two games and compare your reasoning with a small script that follows explicit rules.')
st.caption('This “AI” is a deterministic teaching example. The results do not measure the capabilities of all AI systems or all humans.')
page = st.sidebar.radio('Choose a game', ['Common-sense quiz', 'Guess the pattern', 'Try the chatbot'])
st.sidebar.info('No account, API key, or trained model required. Results last for this browser session. Download them to keep a copy.')

if page == 'Common-sense quiz':
    st.subheader('Common-sense quiz')
    st.write('Answer all eight questions. The chatbot answers the exact same question text; its answers appear after you submit.')
    with st.form('quiz'):
        answers = []
        for index, question in enumerate(QUESTIONS):
            answers.append(st.selectbox(f'{index + 1}. {question.text}', ['Choose an answer', *question.options], key=f'q{index}'))
        submitted = st.form_submit_button('Compare answers', type='primary')
    if submitted:
        if 'Choose an answer' in answers:
            st.warning('Please answer every question before comparing.')
        else:
            st.session_state.quiz_answers = answers
    if 'quiz_answers' in st.session_state:
        rows = []
        for question, human in zip(QUESTIONS, st.session_state.quiz_answers):
            ai, reason = chatbot_answer(question.text)
            rows.append({'Question': question.text, 'Human': human, 'AI': ai, 'Expected answer': question.correct, 'Human correct': human == question.correct, 'AI correct': ai == question.correct})
        human_score = sum(row['Human correct'] for row in rows)
        ai_score = sum(row['AI correct'] for row in rows)
        a, b = st.columns(2)
        a.metric('Your score', f'{human_score}/{len(rows)}')
        b.metric('Keyword chatbot score', f'{ai_score}/{len(rows)}')
        st.dataframe(rows, use_container_width=True, hide_index=True)
        for i, question in enumerate(QUESTIONS):
            with st.expander(f'Question {i + 1}: explanation'):
                st.write(question.explanation)
                st.write('Chatbot rule:', chatbot_answer(question.text)[1])
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        st.download_button('Download comparison CSV', buffer.getvalue(), 'quiz_results.csv', 'text/csv')
        st.info('The script misses negation, colour context, and category differences. A human can use those clues, although human answers can also be wrong.')

elif page == 'Guess the pattern':
    st.subheader('Guess the pattern')
    st.write('Guess the next number and describe your reasoning before revealing the script’s prediction.')
    index = st.selectbox('Choose a round', range(len(PATTERNS)), format_func=lambda i: f'Round {i + 1}')
    pattern = PATTERNS[index]
    st.markdown('### ' + ', '.join(map(str, pattern.terms)) + ', **?**')
    with st.form(f'pattern_{index}'):
        guess = st.text_input('Your next number', key=f'guess_{index}')
        reasoning = st.text_area('What rule or intuition did you use? (optional)', key=f'reason_{index}')
        reveal = st.form_submit_button('Reveal and compare', type='primary')
    if reveal:
        try:
            value = int(guess.strip())
        except ValueError:
            st.warning('Enter a whole number, for example 10.')
        else:
            st.session_state.setdefault('pattern_results', {})[index] = (value, reasoning)
    results = st.session_state.get('pattern_results', {})
    if index in results:
        value, reasoning = results[index]
        ai, rule = predict_pattern(pattern.terms)
        a, b, c = st.columns(3)
        a.metric('Your guess', value)
        b.metric('Script prediction', 'No match' if ai is None else f'{ai:g}')
        c.metric('Intended next number', pattern.answer)
        if value == pattern.answer:
            st.success('Your answer matches the intended rule.')
        else:
            st.info('Your answer differs from the intended rule. Compare your reasoning below.')
        st.write('Intended rule:', pattern.rule)
        st.write('Script reasoning:', rule)
        if reasoning:
            st.write('Your reasoning:', reasoning)
        st.caption('A finite sequence can support multiple continuations. “Correct” here means matching the game designer’s intended rule; intuition is not directly measured.')
    if results:
        completed = len(results)
        human_score = sum(value == PATTERNS[i].answer for i, (value, _) in results.items())
        ai_score = sum(predict_pattern(PATTERNS[i].terms)[0] == PATTERNS[i].answer for i in results)
        st.write(f'Completed rounds: {completed} · Human matches: {human_score} · Script matches: {ai_score}')

else:
    st.subheader('Try the keyword chatbot')
    text = st.text_input('Ask a question', placeholder='What should I do if I am not thirsty but feel cold?')
    if st.button('Ask chatbot'):
        if text.strip():
            answer, reason = chatbot_answer(text)
            st.write('Answer:', answer)
            st.caption(reason)
        else:
            st.warning('Enter a question first.')
    with st.expander('See the rules'):
        st.code('rain/raining → umbrella\ntraffic → stop\nsmoke → move away and alert\nyellow → yes\nthirsty → drinking water\notherwise → I do not know')
        st.write('Rules run from top to bottom. The first matching rule wins. Try rephrasing, negation, or a question with several keywords.')

if st.sidebar.button('Reset both games'):
    for key in list(st.session_state):
        del st.session_state[key]
    st.rerun()
