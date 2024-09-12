from flask import Flask, render_template, request, jsonify
import openai
import numpy as np
from sklearn.neighbors import NearestNeighbors
from transformers import pipeline
import os

app = Flask(__name__)

user_data = np.array([[90, 1], [75, 2], [85, 3]])  # Example: [score, interest]
courses = np.array([[80, 1], [70, 2], [85, 3], [60, 1]])

# Nearest Neighbors model
model = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(courses)

@app.route('/')
def indes():
    return render_template('app.html')

@app.route('/recommend', methods=['POST'])
def recommends():
    try:
        # Get user input from the form
        user_score = int(request.form['score'])
        interests = request.form.getlist('interests')  # Handles multiple selections
        print(interests)
        # Convert interests into numeric format or a suitable format for your model
        interest_map=[]
        interest_vector = [int(i) for i in interests]  # type: ignore # Assuming you map interests to integers
        print(interest_vector)
        user = np.array([[user_score, sum(interest_vector) / len(interest_vector)]])  # Simplified approach
        distances, indices = model.kneighbors(user)
        print(distances,indices)
        recommendations = [
            f"Course {int(i) + 1}: Required Score {courses[i][0]}, Interest {courses[i][1]}"
            for i in indices[0]
        ]
        return jsonify(recommendations=recommendations)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/roadmap/after10th', methods=['POST'])
def roadmap_after_10th():
    try:
        interests = request.form.getlist('interests')  # List of interests from the form
        roadmaps = {
        'Science': {
            'description': 'Explore advanced topics in Physical and Biological sciences. This field includes in-depth studies and research opportunities in various scientific disciplines and their applications.',
        'courses': [
            {'name': 'Physics', 'details': 'Study of matter, energy, and the fundamental forces of nature. Includes classical mechanics, electromagnetism, quantum physics, and relativity.'},
            {'name': 'Chemistry', 'details': 'Study of substances, their properties, reactions, and the use of these reactions to form new substances. Includes organic, inorganic, and physical chemistry.'},
            {'name': 'Biology', 'details': 'Study of living organisms, including their structure, function, growth, and evolution. Covers genetics, microbiology, ecology, and physiology.'},
            {'name': 'Mathematics', 'details': 'Study of numbers, quantities, shapes, and patterns. Includes algebra, calculus, statistics, and differential equations.'},
            {'name': 'Environmental Science', 'details': 'Study of environmental processes and issues. Includes topics on ecology, conservation, environmental policies, and sustainability.'},
            {'name': 'Astronomy', 'details': 'Study of celestial objects and phenomena beyond Earth’s atmosphere. Includes astrophysics, cosmology, and space exploration.'}
        ],
        'career_options': [
            {'field': 'Engineering', 'details': 'Careers in various engineering fields such as Mechanical, Civil, Electrical, Chemical, and Aerospace Engineering.'},
            {'field': 'Medical Sciences', 'details': 'Medical professions including doctors, surgeons, medical researchers, and specialists.'},
            {'field': 'Research', 'details': 'Opportunities in scientific research across disciplines such as physics, chemistry, biology, and environmental science.'},
            {'field': 'Environmental Management', 'details': 'Roles in environmental protection, conservation, and sustainability initiatives.'},
            {'field': 'Astronomy and Space Science', 'details': 'Careers in space agencies, observatories, and research institutions focusing on astrophysics and space exploration.'}
        ]
    },
    'Commerce': {
        'description': 'Focus on business principles, economic theories, and financial management. This stream provides a foundation for careers in business, finance, and management.',
        'courses': [
            {'name': 'Business Studies', 'details': 'Understanding of business management principles including marketing, human resources, and operations management.'},
            {'name': 'Accountancy', 'details': 'Study of financial transactions, bookkeeping, and financial reporting. Includes financial accounting, management accounting, and auditing.'},
            {'name': 'Economics', 'details': 'Study of production, distribution, and consumption of goods and services. Includes microeconomics, macroeconomics, and economic policy.'},
            {'name': 'International Business', 'details': 'Study of global business practices, international trade, and cross-cultural management.'},
            {'name': 'Financial Management', 'details': 'Focuses on financial planning, investment strategies, and risk management in businesses and personal finance.'},
            {'name': 'Marketing Management', 'details': 'Study of market research, consumer behavior, advertising, and sales strategies.'}
        ],
        'career_options': [
            {'field': 'Business Management', 'details': 'Roles in business administration, operations management, and strategic planning in various industries.'},
            {'field': 'Accounting', 'details': 'Careers in accounting, financial auditing, and taxation.'},
            {'field': 'Finance', 'details': 'Opportunities in financial analysis, investment banking, and corporate finance.'},
            {'field': 'International Business', 'details': 'Roles in global trade, international marketing, and export-import management.'},
            {'field': 'Entrepreneurship', 'details': 'Opportunities to start and manage new business ventures or startups.'}
        ]
    },
    'Humanities': {
        'description': 'Explore human society, culture, and history through various disciplines. This field includes studies in arts, social sciences, and public administration.',
        'courses': [
            {'name': 'History', 'details': 'Study of past events, historical processes, and their impact on contemporary society. Includes ancient, medieval, and modern history.'},
            {'name': 'Geography', 'details': 'Study of physical landscapes, human-environment interactions, and spatial phenomena. Includes physical geography, human geography, and geographic information systems (GIS).'},
            {'name': 'Political Science', 'details': 'Study of government systems, political theories, and international relations. Includes comparative politics, political theory, and public policy.'},
            {'name': 'Sociology', 'details': 'Study of social behavior, institutions, and societal issues. Covers topics such as social stratification, social change, and research methods.'},
            {'name': 'Philosophy', 'details': 'Study of fundamental questions about existence, knowledge, and ethics. Includes branches like metaphysics, epistemology, and ethics.'},
            {'name': 'Cultural Studies', 'details': 'Study of cultural practices, identities, and expressions. Includes media studies, gender studies, and cultural theory.'}
        ],
        'career_options': [
            {'field': 'Education', 'details': 'Roles in teaching, curriculum development, and educational administration.'},
            {'field': 'Civil Services', 'details': 'Careers in public administration, policy-making, and governmental roles.'},
            {'field': 'Journalism', 'details': 'Roles in news reporting, media production, and investigative journalism.'},
            {'field': 'Social Work', 'details': 'Opportunities in community service, counseling, and social advocacy.'},
            {'field': 'Cultural Heritage Management', 'details': 'Careers in preserving and promoting cultural and historical heritage, including museum and archival work.'}
        ]
        }
        }
        recommendations = {}
        for interest in interests:
            recommendations[interest] = roadmaps.get(interest, {'description': 'No specific roadmap available', 'courses': [], 'career_options': []})
        return jsonify(roadmaps=recommendations)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/roadmap/after12th', methods=['POST'])
def roadmap_after_12th():
    try:
        stream = request.form['stream']
        roadmaps = {
        'Science': {
            'description': 'Advanced studies in scientific disciplines and engineering. This field includes extensive research and practical applications in various branches of science and technology.',
        'courses': [
            {'name': 'B.Sc Physics', 'details': 'Bachelor of Science in Physics. Focuses on fundamental principles, quantum mechanics, and applied physics.'},
            {'name': 'B.Sc Chemistry', 'details': 'Bachelor of Science in Chemistry. Covers organic, inorganic, and physical chemistry, along with practical laboratory work.'},
            {'name': 'B.Sc Biology', 'details': 'Bachelor of Science in Biology. Emphasizes molecular biology, genetics, and ecological studies.'},
            {'name': 'B.Sc Environmental Science', 'details': 'Bachelor of Science in Environmental Science. Focuses on environmental issues, conservation, and sustainable practices.'},
            {'name': 'Engineering (Various Branches)', 'details': 'Specialized courses in engineering including Mechanical, Civil, Electrical, Computer, and Chemical Engineering.'},
            {'name': 'MBBS', 'details': 'Bachelor of Medicine, Bachelor of Surgery. Comprehensive medical education leading to a career in healthcare.'},
            {'name': 'BDS', 'details': 'Bachelor of Dental Surgery. Focuses on dental care, surgery, and oral health.'},
            {'name': 'B.Sc Nursing', 'details': 'Bachelor of Science in Nursing. Prepares students for careers in nursing with clinical and theoretical training.'},
            {'name': 'B.Sc Biotechnology', 'details': 'Bachelor of Science in Biotechnology. Covers the use of biological processes in technology and medicine.'}
        ],
        'career_options': [
            {'field': 'Engineering', 'details': 'Careers in various branches of engineering such as Mechanical, Civil, and Electrical Engineering.'},
            {'field': 'Medicine', 'details': 'Medical professions including doctors, surgeons, and specialists in various fields.'},
            {'field': 'Research', 'details': 'Opportunities in scientific research, laboratory work, and academic positions.'},
            {'field': 'Environmental Management', 'details': 'Roles in environmental protection, conservation, and sustainable development.'},
            {'field': 'Biotechnology', 'details': 'Careers in biotech firms, pharmaceutical companies, and research institutions.'}
        ]
        },
        'Commerce': {
            'description': 'In-depth knowledge of commerce and business management. This field prepares individuals for various roles in the business world, including management, finance, and accounting.',
        'courses': [
            {'name': 'B.Com General', 'details': 'Bachelor of Commerce with a broad focus on commerce subjects including accounting, economics, and business law.'},
            {'name': 'B.Com Accounting & Finance', 'details': 'Specialized Bachelor of Commerce focusing on accounting principles, financial management, and auditing.'},
            {'name': 'BBA', 'details': 'Bachelor of Business Administration. Covers management principles, business strategies, and organizational behavior.'},
            {'name': 'B.Com International Business', 'details': 'Bachelor of Commerce focusing on global business practices and international trade.'},
            {'name': 'CA (Chartered Accountancy)', 'details': 'Professional qualification in accounting, focusing on financial accounting, auditing, and taxation.'},
            {'name': 'CFA (Chartered Financial Analyst)', 'details': 'Professional qualification in financial analysis, investment management, and portfolio management.'},
            {'name': 'MBA', 'details': 'Master of Business Administration. Advanced studies in management, strategy, and organizational leadership.'}
             ],
        'career_options': [
            {'field': 'Business Management', 'details': 'Roles in management, operations, and strategic planning within businesses and organizations.'},
            {'field': 'Finance', 'details': 'Careers in financial analysis, investment banking, and financial planning.'},
            {'field': 'Accounting', 'details': 'Opportunities in accounting, auditing, and taxation.'},
            {'field': 'International Business', 'details': 'Roles in global trade, international marketing, and export-import management.'},
            {'field': 'Entrepreneurship', 'details': 'Opportunities to start and manage your own business ventures.'}
            ]
        },
        'Humanities': {
            'description': 'Study of arts, social sciences, and humanities. This field focuses on understanding human society, culture, and historical contexts through various disciplines.',
            'courses': [
            {'name': 'BA History', 'details': 'Bachelor of Arts in History. Covers historical events, contexts, and their impact on the present.'},
            {'name': 'BA Geography', 'details': 'Bachelor of Arts in Geography. Focuses on physical landscapes, human geography, and environmental issues.'},
            {'name': 'BA Political Science', 'details': 'Bachelor of Arts in Political Science. Studies government systems, political theories, and international relations.'},
            {'name': 'BA Sociology', 'details': 'Bachelor of Arts in Sociology. Focuses on social behavior, institutions, and societal issues.'},
            {'name': 'B.Ed', 'details': 'Bachelor of Education. Prepares individuals for teaching careers in schools and educational institutions.'},
            {'name': 'Mass Communication', 'details': 'Courses in journalism, media studies, and communication strategies.'},
            {'name': 'BA Philosophy', 'details': 'Bachelor of Arts in Philosophy. Covers fundamental questions about existence, knowledge, and ethics.'},
            {'name': 'BA Literature', 'details': 'Bachelor of Arts in Literature. Studies various genres of literature, critical analysis, and literary history.'}
            ],
        'career_options': [
            {'field': 'Teaching', 'details': 'Educational roles in schools, colleges, and training institutes.'},
            {'field': 'Journalism', 'details': 'Careers in news reporting, media production, and content creation.'},
            {'field': 'Public Administration', 'details': 'Roles in government services, policy-making, and public sector management.'},
            {'field': 'Social Work', 'details': 'Opportunities in community service, counseling, and social advocacy.'},
            {'field': 'Cultural Heritage Management', 'details': 'Careers in preserving and promoting cultural heritage and historical sites.'}
            ]
        }
        }

        recommendations = roadmaps.get(stream, {'description': 'No specific roadmap available', 'courses': [], 'career_options': []})
        return jsonify(roadmaps=recommendations)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
