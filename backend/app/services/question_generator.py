from openai import OpenAI
import random
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class QuestionGenerator:
    """
    Service to generate interview questions using OpenAI
    """

    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key)

        logger.info("QuestionGenerator initialized")

    def generate_questions(
        self,
        role: str,
        retrieved_context: List[str],
        resume_data: dict,
        previous_questions=None,
        num_questions: int = 1
    ) -> List[str]:

        if previous_questions is None:
            previous_questions = []

        try:

            # -------------------------------
            # Fallback if RAG returns nothing
            # -------------------------------
            if not retrieved_context:
                logger.warning(
                    "No retrieved context found. Using fallback questions."
                )

                return self._fallback_question_generation(
                    role,
                    resume_data,
                    previous_questions
                )

            context = "\n".join(retrieved_context[:3])

            skills = ", ".join(
                resume_data.get("skills", [])[:8]
            ) or "General Programming"

            technologies = ", ".join(
                resume_data.get("technologies", [])[:8]
            ) or "General Technologies"

            domains = ", ".join(
                resume_data.get("domain_exposure", [])
            ) or "Software Engineering"

            previous = "\n".join(previous_questions)

            prompt = f"""
You are an experienced Senior Technical Interviewer.

Conduct an interview for a {role} candidate.

Candidate Resume Information

Skills:
{skills}

Technologies:
{technologies}

Domains:
{domains}

Knowledge Base:
{context}

Previous Questions:
{previous if previous else "None"}

Rules:

1. Never repeat any previous question.
2. Never ask the same question in different words.
3. Ask only ONE question.
4. Base the question on the resume.
5. Increase difficulty gradually.
6. Mix concepts, projects, coding, debugging and scenario questions.
7. Ask concise questions.

Return ONLY the question.
"""
            

            logger.debug("Generating interview question using OpenAI")

            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior technical interviewer. "
                            "Never repeat previous questions. "
                            "Always ask one unique technical question."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=200
            )

            content = response.choices[0].message.content.strip()

            questions = [
                q.strip("- ").strip()
                for q in content.split("\n")
                if q.strip()
            ]

            if not questions:
                logger.warning("No questions generated. Using fallback.")

                return self._fallback_question_generation(
                    role,
                    resume_data,
                    previous_questions
                )

            logger.info(f"Generated {len(questions)} question(s)")

            return questions[:num_questions]

        except Exception as e:

            logger.error(
                f"Question generation failed: {str(e)}"
            )

            return self._fallback_question_generation(
                role,
                resume_data,
                previous_questions
            )
        

    def _fallback_question_generation(
        self,
        role: str,
        resume_data: dict,
        previous_questions=None
    ) -> List[str]:
        """
        Generate fallback interview questions when OpenAI is unavailable.
        Ensures previously asked questions are not repeated.
        """

        if previous_questions is None:
            previous_questions = []

        logger.info(f"Using fallback question generation for role: {role}")

        role = role.lower()

        domains = resume_data.get("domain_exposure", [])

        # ---------- ML / Data Scientist ----------
        if (
            "ml" in role
            or "machine learning" in role
            or "data" in role
        ):

            questions = [
                "Describe a machine learning project you've worked on. What was the problem, your approach, and the outcome?",
                f"Explain the difference between supervised and unsupervised learning using an example from {domains[0] if domains else 'your project'}.",
                "How do you perform feature engineering in a real-world project?",
                "How do you detect and prevent overfitting?",
                "How do you evaluate a machine learning model?",
                "Explain precision, recall and F1-score.",
                "When would you choose Random Forest over XGBoost?",
                "Explain the bias-variance tradeoff.",
                "How does cross-validation work?",
                "How would you deploy a machine learning model into production?",
                "Explain Gradient Descent.",
                "How do you handle missing values in a dataset?",
                "What is regularization?",
                "Explain PCA and when you would use it.",
                "Describe an end-to-end ML pipeline."
            ]

        # ---------- Backend ----------
        elif "backend" in role:

            questions = [
                "Design a scalable REST API.",
                "Explain REST vs GraphQL.",
                "Explain JWT authentication.",
                "How do database indexes improve performance?",
                "Difference between SQL and NoSQL?",
                "How do you optimize slow SQL queries?",
                "Explain caching and Redis.",
                "What are microservices?",
                "How do you secure REST APIs?",
                "Explain optimistic and pessimistic locking.",
                "Explain Docker.",
                "How would you deploy a backend service?",
                "Explain load balancing.",
                "What is message queuing?",
                "Describe ACID properties."
            ]

        # ---------- Data Scientist ----------
        elif "scientist" in role:

            questions = [
                "Describe a data science project you've completed.",
                "Explain data preprocessing.",
                "How do you clean noisy data?",
                "Explain hypothesis testing.",
                "Difference between regression and classification.",
                "Explain correlation vs causation.",
                "How do you deal with imbalanced datasets?",
                "Explain A/B Testing.",
                "How do you visualize insights?",
                "Describe your EDA process."
            ]

        # ---------- Generic ----------
        else:

            questions = [
                "Tell me about your biggest technical project.",
                "Describe a difficult bug you solved.",
                "How do you improve code quality?",
                "How do you learn new technologies?",
                "Tell me about a technical challenge you overcame.",
                "Describe a project you're proud of.",
                "How do you debug production issues?",
                "How do you manage deadlines?",
                "How do you work in a team?",
                "What software architecture patterns have you used?"
            ]

        # Remove already asked questions
        available_questions = [
            q
            for q in questions
            if q not in previous_questions
        ]

        # Reset if all questions have been used
        if len(available_questions) == 0:
            available_questions = questions

        question = random.choice(available_questions)

        logger.info(f"Selected question: {question}")

        return [question]