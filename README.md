# <span dir="">About</span>

This API uses data exported from Mural boards to make recommendations for relevant content within a mentoring online platform based on keywords. <span dir="">The MURAL board input information will be accessed by both mentees and mentors participating in the online mentoring program, and the final information structure with extracted keywords and recommended content will be available to the same audience and stored in the mentorship system database. Mentees will first respond to the Mural activity called “What’s on your radar” by entering text on sticky notes relevant to each category of wellness. The data inputted by the mentee will be exported to CSV format for data organization and analysis to recommend relevant content and tools in the mentoring system to assist the mentorship experience. The exported CSV data will be cleaned and organized through Python functions and we will use NLP and text technology to match the keywords in the input with mentorship content to create mentorship activity and resource recommendations that will be displayed to both the mentee and the mentor. </span>

# <span dir="">Methodology</span>

* <span dir="">Export the </span>[<span dir="">MURAL board</span>](https://app.mural.co/t/estherhan4738/m/estherhan4738/1683766600872/2b7e849923ec16af977e1559d78fd2c2943cd05e?sender=u51c7066dc5a395f39bbf4188)<span dir=""> as CSV</span>
* <span dir="">Use Python to identify sticky note elements, clean empty data, and use NLP technology to identify and extract verbs and nouns in the sticky note texts. Add the extracted words to a dictionary.</span>
* <span dir="">Use NLP technology and Python to link the works in the student input dictionary to the mentorship article topic dictionary and find the closest match</span>
  * See our [ChatGPT history](https://gitlab.com/imt589_spring23/mural-recommendation-api/-/blob/f16e9daf8083411eafee0d569814c1934de418fb/ChatGPT%20Project%20History) for how we generated a content list with keywords and had Chat GPT match the text to the content keywords.
* <span dir="">Take the output of the list of closest topic match results and present it on the mentorship main page interface for both mentors and students</span>
* <span dir="">Use Python and Flask to create a simple API endpoint to host an information structure for the recommended topics and sticky note input information </span>

# <span dir="">Access</span>

* <span dir="">The student completes the “What’s on my radar” MURAL activity which is linked in the to-do section of their student dashboard in the mentorship system.</span>
* <span dir="">After completing the activity, they navigate back to the mentorship system and click “recommend content” which is listed below the embedded MURAL activity.</span>
* <span dir="">Recommended content based on their MURAL will be listed under “recommended” on their student dashboard in the mentorship system.</span>
* <span dir="">Students can make changes to their “What’s on my radar” and click “recommend content” again to update the recommendations based on their changes to the MURAL board.</span>

# <span dir="">Structure</span>

```plaintext
[
    {
        "session": {
            "id": "10001",
            "call_time": "05/31/2023 3:30:00 PM",
            "url": "/session/10001",
            "tool": "Natural Language Toolkit (NLTK)"
        },
        "mural": {
            "mural_id": "MURAL05202023000001",
            "mural_url": "https://app.mural.co/invitation/mural/estherhan4738/1683766600872?sender=u51c7066dc5a395f39bbf4188&key=9ef3e1aa-bdc6-4ca0-baa9-95caa3c5fdcd",
            "sticky_note": [],
            "export": {
                "export_id": "202300520120000",
                "export_format": "json"
            }
        },
        "recommendation": []
    }
]
```

# Example

* <span dir="">Student adds the sticky note “How do I save up for a car?” in the MURAL board under the category “Financial” </span>
* ![image.png](uploads/61a19656cd50c11267a18d7db374c382/image.png)
* <span dir="">Export sticky notes into CSV files, the files show useful properties such as text, area, and tags that can be used to analyze in further steps.</span>
* ![image.png](uploads/d87b950c2d509529b81a81ad2e63e888/image.png)
* <span dir="">Use python code to evaluate the text string data for keywords and compare to keywords in a file/database containing keywords and related content.</span>
* <span dir="">Output on student dashboard “Recommended content” with a link to the article “How to buy a car” and “How to start a savings account”</span>
* ![image.png](uploads/e1a8ce7d316c21b89f64502dbd71809d/image.png)
