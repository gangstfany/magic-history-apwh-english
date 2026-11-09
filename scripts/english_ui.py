"""Normalize translated interface labels without changing historical prose or IDs."""
import re

def normalize_ui_copy(text):
    # Dynamic counters are UI templates; static prose and identifier strings stay intact.
    text=re.sub(r'Step (\$\{[^}]+\})( / \$\{[^}]+\})? stops?\b',lambda m:'Stop '+m[1]+(m[2] or ''),text)
    text=re.sub(r'Step (\$\{[^}]+\})(?:(?: / | of )(\$\{[^}]+\}))? steps?\b',lambda m:'Step '+m[1]+(' / '+m[2] if m[2] else ''),text)
    text=re.sub(r'Stop (\$\{[^}]+\})(?:(?: / | of )(\$\{[^}]+\}))? stops?\b',lambda m:'Stop '+m[1]+(' / '+m[2] if m[2] else ''),text)
    text=re.sub(r'Return to stop (\$\{chainRouteContext\.step\+1\}) step\b',r'Return to step \1',text)
    text=re.sub(r'(" · Step "\s*\+\s*\((?:i|target\.step)\s*\+\s*1\))\s*\+\s*" step"',r'\1',text)
    text=re.sub(r'Full chain · (\$\{route\.stops\.length\}) step\b',r'Full chain · \1 steps',text)
    text=text.replace('>Comparison theme<','>Theme<').replace('>Comparison group<','>Case pair<')
    text=text.replace('EVENT IN FOCUS / Event image','EVENT IN FOCUS')
    for label in ['Trade routes and exchange','Trade Routes and Exchange']:
        text=text.replace('>'+label+'</button>','>Trade & exchange</button>')
    text=text.replace('>Main Chain</span>','>Main</span>').replace('>Supplementary Chain</span>','>Extra</span>')
    text=text.replace('Click a region to expand its content; click again to collapse. Click “Comparison and explanation” below to view it in a map popup.','Select a case to read more.')
    text=re.sub(r'>(\s*)Practice quiz(<span class="rc-count">)',r'>\1Start quiz\2',text)
    text=text.replace('10 questions per set','Up to 10 questions')
    text=text.replace('Practiced: ${st.practiced} items · To review: ${st.review} items','Practiced: ${st.practiced} · To review: ${st.review}')
    text=text.replace('data-quiz-action="exit">Back</button>','data-quiz-action="exit">Back to practice</button>')
    text=text.replace('data-quiz-action="exit">Exit practice</button>','data-quiz-action="exit">Back to practice</button>')
    return text
