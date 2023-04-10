import os
import re
import jieba
import stanza

def load_stanza_model():
    nlp = stanza.Pipeline(lang='zh', processors='tokenize,pos,lemma')
    return nlp

def parse_cases(file_path):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    return re.split(r'\n\s*\n', content)

def extract_symptoms_and_causes(cases, nlp):
    symptoms_and_causes = set()
    non_symptoms_and_causes = set(['经过', '给予', '缓解', '老年', '上', '不详', '中', '为', '主要', '主诉', '乏力', '休息', '位', '体格', '体检', '保暖', '充血', '先生', '冠','冲洗','减弱','出现','出院','刺激','加强','包括','医生','发现','口服','口腔','名','吸入','呼吸','咳','年','年轻','年龄'])

    for case in cases:
        doc = nlp(case)
        for sentence in doc.sentences:
            for token in sentence.tokens:
                if token.words[0].upos in ['NOUN', 'VERB', 'ADJ']:
                    word = token.words[0].lemma
                    if not re.match(r'\d+', word) and word not in non_symptoms_and_causes:
                        symptoms_and_causes.add(word)

    return sorted(list(symptoms_and_causes))

def generate_binary_representation(cases, symptoms_and_causes):
    binary_repr = []

    for case in cases:
        case_repr = ''
        for symptom_or_cause in symptoms_and_causes:
            if symptom_or_cause in case:
                case_repr += '1'
            else:
                case_repr += '0'
        binary_repr.append(case_repr)

    return binary_repr

def write_to_files(symptoms_and_causes, binary_repr):
    with open('static/symptoms_and_causes.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(symptoms_and_causes))

    with open('static/binary_repr.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(binary_repr))

def main(file_path):
    nlp = load_stanza_model()
    cases = parse_cases(file_path)
    symptoms_and_causes = extract_symptoms_and_causes(cases, nlp)
    binary_repr = generate_binary_representation(cases, symptoms_and_causes)
    write_to_files(symptoms_and_causes, binary_repr)

if __name__ == '__main__':
    input_path = 'static/input.txt'
    file_path = input_path.strip()
    main(file_path)
