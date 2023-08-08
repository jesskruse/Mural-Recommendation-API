# . venv/bin/activate
# export FLASK_APP=recommendation_api.py
#  flask run --host=0.0.0.0 --port=80

# ngrok config add-authtoken 2PcjyMRzigwhxBgv33RRf0ZXqnE_7oscjSKHpkKKXjLaV2SDA
# ngrok http 80

from flask import Flask, jsonify
import csv
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)

def csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Usage example
csv_file_path = 'mural_sticky_notes.csv'
json_file_path = 'sticky_notes_json.json'
csv_to_json(csv_file_path, json_file_path)

# --------------------------------------

with open('sticky_notes_json.json', 'r') as file:
    input_json = json.load(file)

# Read the target JSON structure file
with open('new_information_structure.json', 'r') as file:
    target_json = json.load(file)

# Initialize the stop words
stop_words = set(stopwords.words('english'))

# Extract the required fields from input_json and update target_json
sticky_notes = input_json
for sticky_note in sticky_notes:
    note_id = sticky_note['ID']
    note_text = sticky_note['Text']
    note_topic = sticky_note['Area']
    keywords = [word.lower() for word in word_tokenize(note_text) if word.isalpha() and word.lower() not in stop_words]
    
    if note_text.strip():  # Check if 'Text' field is not empty or only contains whitespace
        target_json[0]['mural']['sticky_note'].append({
            'note_id': note_id,
            'note_text': note_text,
            'note_topic': note_topic,
            'note_keyword': keywords
        })

# Write the updated target JSON structure back to the file
with open('nlp_demo.json', 'w') as file:
    json.dump(target_json, file, indent=4)

# ------------------------------------------------

with open('new_information_structure.json', 'r') as file:
    information_structure = json.load(file)

# Read the new sticky note file
with open('new_keywords.json', 'r') as file:
    sticky_notes = json.load(file)

# Add the sticky notes to the information structure
information_structure[0]['mural']['sticky_note'] = sticky_notes

# Write the updated information structure back to the file
with open('new_information_structure.json', 'w') as file:
    json.dump(information_structure, file, indent=4)


# -----------------------------------------------

def generate_recommended_contents(sticky_notes, content_list):
    recommended_contents = []

    for sticky_note in sticky_notes:
        for content in content_list['content']:
            if sticky_note['note_topic'].lower() == content['content_topic'][0].lower() and any(keyword in sticky_note['note_keyword'] for keyword in content['content_keyword']):
                recommended_content = {
                    'content_id': content['content_id'],
                    'content_title': content['content_title'],
                    'content_url': content['content_url'],
                    'content_keyword': content['content_keyword'],
                    'content_topic': content['content_topic'][0]
                }
                recommended_contents.append(recommended_content)

    return recommended_contents

# Import our content corpus
with open('content_list.json', 'r') as file:
    content_list = json.load(file)

recommended_contents = generate_recommended_contents(sticky_notes, content_list)

# Add recommended_contents to the information structure
information_structure[0]['recommendation'] = recommended_contents

# Write the updated information structure back to the file
with open('new_information_structure.json', 'w') as file:
    json.dump(information_structure, file, indent=4)


# -----------------------------------------------

# Opening Page
@app.route('/')
def info():
    message="""
       <p>Hi, Welcome to the Mentorship Recommendation API!</p>
       
       <p>You can view student's sticky notes input, recommendation based on the input, and matched results for the Eight Dimensions of Wellness by searching for a specific wellness element: 
       <strong>Emotional, Spiritual, Intellectual, Physical, Environmental, Financial, Occupational, 
       and Social</strong> by using <em>'/notes/<u>element</u>'</em>, <em>'/recommendations/<u>element</u>'</em>, and <em>'/match_results/<u>element</u>'</em>.</p>
    """ 
    return message 

# Access sticky notes text with a given topic
@app.route('/notes/<element>')
def notes(element):
    text_items = []
    mural_topics = information_structure[0].get('mural', {}).get('mural_topic', [])
    if element.lower() not in [t.lower() for t in mural_topics]:
        return "This is not one of the topics. Please use one of the following topics: <strong>Emotional, Spiritual, Intellectual, Physical, Environmental, Financial, Occupational, and Social</strong>"

    for sticky_note in information_structure[0]['mural']['sticky_note']:
        if sticky_note['note_topic'].lower() == element.lower():
            text_items.append(sticky_note['note_text'])
            
    if len(text_items) == 0:
            return 'There are no sticky notes for topic ' % element
        
    return text_items

@app.route('/show_structure')
def structure():
    return information_structure


# Access recommendation content title and link with a given topic
@app.route('/recommendations/<element>')
def get_recommendations(element):
    result = []
    mural_topics = information_structure[0].get('mural', {}).get('mural_topic', [])
    if element.lower() not in [t.lower() for t in mural_topics]:
        return "This is not one of the topics. Please use one of the following topics: <strong>Emotional, Spiritual, Intellectual, Physical, Environmental, Financial, Occupational, and Social</strong>"

    for item in information_structure:
        recommendations = item.get('recommendation', [])
        for rec in recommendations:
            if rec['content_topic'].lower() == element.lower():
                title = rec['content_title']
                link = rec['content_url']
                result.append({'Title': title, 'Link': link})
        if len(result) == 0:
            return 'There are no sticky notes for topic ' % element
    return jsonify(result)


# Access matching sticky notes and recommendation contents with a given topic
@app.route('/match_results/<topic>')
def get_content(topic):
    result = []
    for item in information_structure:
        mural_topics = item.get('mural', {}).get('mural_topic', [])
        if topic.lower() not in [t.lower() for t in mural_topics]:
            return "This is not one of the topics. Please use one of the following topics: <strong>Emotional, Spiritual, Intellectual, Physical, Environmental, Financial, Occupational, and Social</strong>"

        sticky_notes = item.get('mural', {}).get('sticky_note', [])
        recommendations = item.get('recommendation', [])
        for sticky_note in sticky_notes:
            if sticky_note['note_topic'].lower() == topic.lower():
                sticky_content = sticky_note['note_text']
                result.append({'Source': 'Sticky Note', 'Content': sticky_content})
        for recommendation in recommendations:
            if recommendation['content_topic'].lower() == topic.lower():
                recommendation_content = recommendation['content_title']
                result.append({'Source': 'Recommendation', 'Content': recommendation_content})
        if len(result) == 0:
            return 'There are no sticky notes for topic ' % topic

    return jsonify(result)
