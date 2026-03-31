"""
Resume and Job Description Parser
Extracts text from PDF/DOCX files and parses key information
"""
import os
from typing import Dict, List, Any, Optional
from pathlib import Path


class ResumeParser:
    """Parse resume files (PDF, DOCX) and extract structured information"""

    def __init__(self):
        self.supported_extensions = {".pdf", ".docx", ".txt"}

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a resume file and return structured data"""
        ext = Path(file_path).suffix.lower()

        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {ext}")

        # Extract raw text
        if ext == ".txt":
            text = self._parse_txt(file_path)
        elif ext == ".pdf":
            text = self._parse_pdf(file_path)
        elif ext == ".docx":
            text = self._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # Parse structured information
        return self._extract_info(text)

    def _parse_txt(self, file_path: str) -> str:
        """Read plain text file"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            raise RuntimeError("pypdf not installed. Install with: pip install pypdf")

    def _parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except ImportError:
            raise RuntimeError("python-docx not installed. Install with: pip install python-docx")

    def _extract_info(self, text: str) -> Dict[str, Any]:
        """Extract structured information from resume text"""
        import re

        # Simple regex-based extraction
        # In production, use LLM for better extraction

        info = {
            "raw_text": text.strip(),
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text),
            "education": self._extract_education(text),
            "languages": self._extract_languages(text)
        }

        return info

    def _extract_name(self, text: str) -> str:
        """Extract candidate name"""
        # Simple heuristic: first non-empty line that's not a contact info
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        for line in lines[:5]:
            # Skip lines that look like email, phone, or address
            if re.match(r'[\w.+-]+@[\w.-]+\.\w+', line):
                continue
            if re.match(r'[\d\s\-\(\)\+]+', line):
                continue
            if len(line) < 50:  # Name is usually short
                return line
        return "Unknown"

    def _extract_email(self, text: str) -> str:
        """Extract email address"""
        match = re.search(r'[\w.+-]+@[\w.-]+\.\w+', text)
        return match.group(0) if match else ""

    def _extract_phone(self, text: str) -> str:
        """Extract phone number"""
        match = re.search(r'[\+\d][\d\s\-\(\)]{8,}\d', text)
        return match.group(0) if match else ""

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume"""
        skills = []

        # Common tech skills pattern
        skill_patterns = [
            r'\b(Python|Java|JavaScript|TypeScript|C\+\+|Go|Rust)\b',
            r'\b(React|Vue|Angular|Svelte|Next\.js)\b',
            r'\b(Node\.js|Express|Django|Flask|FastAPI|Spring)\b',
            r'\b(AWS|Azure|GCP|Cloud)\b',
            r'\b(Docker|Kubernetes|Terraform)\b',
            r'\b(SQL|NoSQL|PostgreSQL|MongoDB|Redis)\b',
            r'\b(Git|CI/CD|DevOps|Agile|Scrum)\b',
        ]

        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.extend(matches)

        return list(set(skills))

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience"""
        experiences = []

        # Look for company names and date ranges
        # This is a simplified extraction - LLM would be better
        lines = text.split("\n")
        current_exp = {}

        for line in lines:
            line = line.strip()
            # Look for date patterns like "2020-2023" or "Jan 2020 - Present"
            date_match = re.search(r'(\d{4}|\w{3}\s+\d{4})\s*[-–]\s*(\d{4}|\w{3}\s+\d{4}|Present)', line)

            if date_match and len(line) < 100:
                # Likely a job title line
                if current_exp:
                    experiences.append(current_exp)
                current_exp = {
                    "title_line": line,
                    "dates": date_match.group(0)
                }

        if current_exp:
            experiences.append(current_exp)

        return experiences

    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        education = []

        # Look for degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|MBBS|B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?)',
            r'(Computer Science|Engineering|Business|Mathematics|Physics)'
        ]

        lines = text.split("\n")
        for line in lines:
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    education.append({"line": line.strip()})
                    break

        return education

    def _extract_languages(self, text: str) -> List[str]:
        """Extract languages mentioned"""
        languages = []

        lang_patterns = [
            r'\b(English|Chinese|Mandarin|Spanish|French|German|Japanese|Korean)\b',
            r'\b( Fluent | Proficient | Intermediate | Basic | Native )'
        ]

        for pattern in lang_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            languages.extend(matches)

        return list(set(languages))


class JobDescriptionParser:
    """Parse job description text and extract requirements"""

    def __init__(self):
        pass

    def parse(self, jd_text: str) -> Dict[str, Any]:
        """Parse job description and extract structured information"""
        return {
            "raw_text": jd_text.strip(),
            "title": self._extract_title(jd_text),
            "company": self._extract_company(jd_text),
            "required_skills": self._extract_required_skills(jd_text),
            "preferred_skills": self._extract_preferred_skills(jd_text),
            "experience_level": self._extract_experience_level(jd_text),
            "responsibilities": self._extract_responsibilities(jd_text),
            "qualifications": self._extract_qualifications(jd_text)
        }

    def _extract_title(self, text: str) -> str:
        """Extract job title"""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return lines[0] if lines else "Unknown Position"

    def _extract_company(self, text: str) -> str:
        """Extract company name"""
        match = re.search(r'(?:at|for)\s+([A-Z][a-zA-Z\s]+)', text)
        return match.group(1).strip() if match else ""

    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills"""
        # Look for "must have", "required", etc.
        skills = []

        # Find the "Requirements" section
        req_section = re.search(
            r'(?:Requirements?|Qualifications?|Must have)(.*?)'
            r'(?:(?:Responsibilities?|Benefits?|About))',
            text, re.IGNORECASE | re.DOTALL
        )

        if req_section:
            section_text = req_section.group(1)
            # Extract bullet points
            bullets = re.findall(r'[•\-\*]\s*(.+?)(?:\n|$)', section_text)
            skills.extend([b.strip() for b in bullets])

        return skills

    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred/nice-to-have skills"""
        skills = []

        # Look for "preferred", "nice to have", "bonus"
        pref_section = re.search(
            r'(?:Preferred|Nice to have|Bonus|Plus)',
            text, re.IGNORECASE
        )

        if pref_section:
            # Extract surrounding text
            start = pref_section.start()
            section_text = text[start:start+500]  # Next 500 chars
            bullets = re.findall(r'[•\-\*]\s*(.+?)(?:\n|$)', section_text)
            skills.extend([b.strip() for b in bullets])

        return skills

    def _extract_experience_level(self, text: str) -> str:
        """Extract experience level requirement"""
        patterns = [
            (r'(\d+)[-–]?\s*(\d+)?\s*(?:years?|yrs?|y\.?o\.?)', "years"),
            (r'(?:entry[- ]?level|junior|associate)', "junior"),
            (r'(?:mid[- ]?level|mid)', "mid"),
            (r'(?:senior|sr\.?|lead|principal)', "senior"),
            (r'(?:staff|distinguished|fellow)', "staff")
        ]

        for pattern, level in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return level

        return "Not specified"

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []

        resp_section = re.search(
            r'(?:Responsibilities?|What you\'ll do|Key duties)(.*?)'
            r'(?:(?:Requirements?|Qualifications?|Benefits?))',
            text, re.IGNORECASE | re.DOTALL
        )

        if resp_section:
            section_text = resp_section.group(1)
            bullets = re.findall(r'[•\-\*]\s*(.+?)(?:\n|$)', section_text)
            responsibilities = [b.strip() for b in bullets]

        return responsibilities

    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract qualifications"""
        qualifications = []

        qual_section = re.search(
            r'(?:Qualifications?|Requirements?|You should have)(.*?)'
            r'(?:(?:Responsibilities?|Benefits?|About))',
            text, re.IGNORECASE | re.DOTALL
        )

        if qual_section:
            section_text = qual_section.group(1)
            bullets = re.findall(r'[•\-\*]\s*(.+?)(?:\n|$)', section_text)
            qualifications = [b.strip() for b in bullets]

        return qualifications


# Import re for the functions
import re

# Create singleton instances
resume_parser = ResumeParser()
jd_parser = JobDescriptionParser()
