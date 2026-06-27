import os
from io import BytesIO
from pypdf import PdfReader
from typing import List
import re
import logging

logger = logging.getLogger(__name__)


class ResumeParser:
    """Service to parse and extract information from resumes"""
    
    # Skill categories for better matching
    PROGRAMMING_LANGUAGES = {
        'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++', 'c#',
        'sql', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab',
        'groovy', 'perl', 'shell', 'bash'
    }
    
    WEB_FRAMEWORKS = {
        'react', 'vue', 'angular', 'next.js', 'svelte', 'ember',
        'django', 'flask', 'fastapi', 'spring', 'express', 'nest.js',
        'rails', 'laravel', 'asp.net', 'asp.net core', 'tornado',
        'pyramid', 'aiohttp'
    }
    
    DATABASES = {
        'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'dynamodb', 'cassandra', 'oracle', 'sql server', 'firebase',
        'datastore', 'cosmos db', 'memcached', 'neo4j', 'influxdb',
        'clickhouse'
    }
    
    CLOUD_PLATFORMS = {
        'aws', 'gcp', 'azure', 'heroku', 'railway', 'vercel', 'netlify',
        'digitalocean', 'linode', 'alibaba cloud', 'oracle cloud'
    }
    
    DEVOPS_TOOLS = {
        'docker', 'kubernetes', 'k8s', 'terraform', 'jenkins', 'github actions',
        'gitlab ci', 'circleci', 'travis ci', 'ansible', 'puppet', 'chef',
        'prometheus', 'grafana', 'elk', 'datadog', 'newrelic'
    }
    
    ML_AI_FRAMEWORKS = {
        'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'xgboost', 'lightgbm',
        'numpy', 'pandas', 'scipy', 'opencv', 'nltk', 'spacy', 'transformers',
        'hugging face', 'mllib', 'spark ml'
    }
    
    ALL_SKILLS = PROGRAMMING_LANGUAGES | WEB_FRAMEWORKS | DATABASES | CLOUD_PLATFORMS | DEVOPS_TOOLS | ML_AI_FRAMEWORKS
    
    @staticmethod
    def extract_from_pdf(pdf_content: bytes) -> str:
        """
        Extract text from PDF content
        
        Args:
            pdf_content: Binary PDF content
            
        Returns:
            Extracted text from PDF
            
        Raises:
            ValueError: If PDF extraction fails
        """
        try:
            pdf_reader = PdfReader(BytesIO(pdf_content))
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text += page.extract_text() + "\n"
                except Exception as e:
                    logger.warning(f"Failed to extract page {page_num}: {str(e)}")
                    continue
            
            if not text.strip():
                raise ValueError("No text could be extracted from PDF")
            
            logger.info(f"Successfully extracted {len(text)} characters from PDF")
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise ValueError(f"Failed to extract PDF: {str(e)}")
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """
        Extract technical skills from resume text
        
        Args:
            text: Resume text content
            
        Returns:
            List of identified skills
        """
        try:
            text_lower = text.lower()
            found_skills = []
            
            for skill in ResumeParser.ALL_SKILLS:
                # Use word boundaries for more accurate matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)
            
            # Remove duplicates and sort
            found_skills = sorted(list(set(found_skills)))
            logger.debug(f"Extracted {len(found_skills)} skills: {found_skills[:5]}...")
            return found_skills
        except Exception as e:
            logger.error(f"Skill extraction error: {str(e)}")
            return []
    
    @staticmethod
    def extract_technologies(text: str) -> List[str]:
        """
        Extract technologies/tools mentioned in resume
        
        Args:
            text: Resume text content
            
        Returns:
            List of identified technologies
        """
        try:
            technologies = [
                'git', 'github', 'gitlab', 'bitbucket', 'jira',
                'docker', 'kubernetes', 'terraform',
                'jenkins', 'github actions', 'gitlab ci',
                'linux', 'unix', 'windows', 'macos',
                'vim', 'vscode', 'intellij', 'pycharm', 'visual studio',
                'postman', 'insomnia', 'swagger',
                'rest api', 'graphql', 'grpc', 'websocket',
                'microservices', 'monolith', 'serverless'
            ]
            
            text_lower = text.lower()
            found_tech = []
            
            for tech in technologies:
                pattern = r'\b' + re.escape(tech) + r'\b'
                if re.search(pattern, text_lower):
                    found_tech.append(tech)
            
            found_tech = sorted(list(set(found_tech)))
            logger.debug(f"Extracted {len(found_tech)} technologies: {found_tech[:5]}...")
            return found_tech
        except Exception as e:
            logger.error(f"Technology extraction error: {str(e)}")
            return []
    
    @staticmethod
    def extract_domain_exposure(text: str) -> List[str]:
        """
        Extract domain exposure (e.g., finance, healthcare, etc.)
        
        Args:
            text: Resume text content
            
        Returns:
            List of identified domain exposures
        """
        try:
            domains = [
                'finance', 'fintech', 'banking', 'payment',
                'healthcare', 'medical', 'telemedicine', 'pharma',
                'e-commerce', 'retail', 'marketplace',
                'social media', 'social network', 'streaming', 'media',
                'saas', 'enterprise', 'b2b', 'b2c',
                'startup', 'scale-up', 'unicorn',
                'machine learning', 'ai', 'data science',
                'iot', 'embedded', 'mobile', 'web',
                'gaming', 'nft', 'blockchain', 'crypto',
                'logistics', 'supply chain', 'manufacturing',
                'education', 'edtech', 'learning'
            ]
            
            text_lower = text.lower()
            found_domains = []
            
            for domain in domains:
                pattern = r'\b' + re.escape(domain) + r'\b'
                if re.search(pattern, text_lower):
                    found_domains.append(domain)
            
            found_domains = sorted(list(set(found_domains)))
            logger.debug(f"Extracted {len(found_domains)} domains: {found_domains[:5]}...")
            return found_domains
        except Exception as e:
            logger.error(f"Domain extraction error: {str(e)}")
            return []
    
    @staticmethod
    def parse_resume(resume_text: str) -> dict:
        """
        Parse resume and extract structured information
        
        Args:
            resume_text: Raw resume text content
            
        Returns:
            Dictionary with extracted resume components
        """
        try:
            if not resume_text or not resume_text.strip():
                raise ValueError("Resume text is empty")
            
            result = {
                "skills": ResumeParser.extract_skills(resume_text),
                "technologies": ResumeParser.extract_technologies(resume_text),
                "domain_exposure": ResumeParser.extract_domain_exposure(resume_text),
                "raw_text": resume_text
            }
            
            logger.info(f"Resume parsed successfully: {len(result['skills'])} skills, "
                       f"{len(result['technologies'])} tech, {len(result['domain_exposure'])} domains")
            return result
        except Exception as e:
            logger.error(f"Resume parsing error: {str(e)}")
            raise
