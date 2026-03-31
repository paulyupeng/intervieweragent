-- Database Schema for Interviewer Agent

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users (interviewers/admins)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'interviewer', -- admin, interviewer, viewer
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Candidates
CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    resume_url TEXT,
    resume_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Job Descriptions
CREATE TABLE job_descriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    jd_url TEXT,
    jd_text TEXT NOT NULL,
    requirements JSONB, -- Parsed requirements
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Interview Sessions
CREATE TABLE interview_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID REFERENCES candidates(id),
    job_description_id UUID REFERENCES job_descriptions(id),
    interviewer_id UUID REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'scheduled', -- scheduled, in_progress, completed, cancelled
    language VARCHAR(10) DEFAULT 'en',
    recording_url TEXT,
    transcript TEXT,
    overall_score DECIMAL(5,2),
    hiring_recommendation VARCHAR(50), -- PROCEED, HOLD, REJECT
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Question Banks
CREATE TABLE question_banks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL, -- english_proficiency, industry_understanding, professional_skills, soft_skills
    language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Questions
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_bank_id UUID REFERENCES question_banks(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) DEFAULT 'open', -- open, followup, behavioral, technical
    expected_duration_seconds INTEGER DEFAULT 60,
    weight DECIMAL(3,2) DEFAULT 1.0,
    metadata JSONB, -- Additional metadata like tags, difficulty, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Follow-up Questions
CREATE TABLE followup_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_question_id UUID REFERENCES questions(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    trigger_keywords TEXT[], -- Keywords that trigger this followup
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Interview Questions (questions used in a specific interview)
CREATE TABLE interview_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_session_id UUID REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id),
    question_text TEXT NOT NULL,
    question_order INTEGER NOT NULL,
    is_followup BOOLEAN DEFAULT false,
    parent_question_id UUID REFERENCES interview_questions(id),
    asked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Candidate Responses
CREATE TABLE candidate_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_question_id UUID REFERENCES interview_questions(id) ON DELETE CASCADE,
    transcript TEXT NOT NULL,
    audio_url TEXT,
    duration_seconds INTEGER,
    word_count INTEGER,
    speaking_rate DECIMAL(5,2), -- words per minute
    pause_count INTEGER,
    filler_word_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Scoring Dimensions
CREATE TABLE scoring_dimensions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL, -- fluency, vocabulary, grammar, etc.
    category VARCHAR(100) NOT NULL, -- english_proficiency, industry_understanding, etc.
    weight DECIMAL(3,2) DEFAULT 1.0,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Interview Scores
CREATE TABLE interview_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interview_session_id UUID REFERENCES interview_sessions(id) ON DELETE CASCADE,
    dimension_id UUID REFERENCES scoring_dimensions(id),
    score DECIMAL(5,2) NOT NULL, -- 0-10 scale
    max_score DECIMAL(5,2) DEFAULT 10.0,
    evaluator_type VARCHAR(50) DEFAULT 'automated', -- automated, llm, human
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- JD-Resume Matching
CREATE TABLE jd_resume_matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_id UUID REFERENCES candidates(id),
    job_description_id UUID REFERENCES job_descriptions(id),
    match_score DECIMAL(5,2), -- 0-100
    matching_skills TEXT[], -- Skills that match
    gap_skills TEXT[], -- Skills missing
    analysis TEXT, -- LLM-generated analysis
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Scoring Configuration (customizable weights)
CREATE TABLE scoring_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    config JSONB NOT NULL, -- JSON config for weights and criteria
    is_default BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_interview_sessions_candidate ON interview_sessions(candidate_id);
CREATE INDEX idx_interview_sessions_status ON interview_sessions(status);
CREATE INDEX idx_questions_bank ON questions(question_bank_id);
CREATE INDEX idx_interview_questions_session ON interview_questions(interview_session_id);
CREATE INDEX idx_candidate_responses_question ON candidate_responses(interview_question_id);
CREATE INDEX idx_interview_scores_session ON interview_scores(interview_session_id);
CREATE INDEX idx_jd_resume_matches_candidate ON jd_resume_matches(candidate_id, job_description_id);

-- Insert default scoring dimensions
INSERT INTO scoring_dimensions (name, category, weight, description) VALUES
-- English Proficiency
('fluency', 'english_proficiency', 0.25, 'Speech flow, hesitation, natural pace'),
('vocabulary', 'english_proficiency', 0.20, 'Range and precision of word choice'),
('grammar', 'english_proficiency', 0.20, 'Sentence structure accuracy'),
('comprehension', 'english_proficiency', 0.20, 'Understanding of questions'),
('pronunciation', 'english_proficiency', 0.15, 'Clarity of speech'),
-- Industry Understanding
('market_knowledge', 'industry_understanding', 0.30, 'Awareness of industry trends'),
('competitor_awareness', 'industry_understanding', 0.25, 'Understanding of competitive landscape'),
('regulatory_knowledge', 'industry_understanding', 0.20, 'Awareness of compliance requirements'),
('innovation_awareness', 'industry_understanding', 0.25, 'Knowledge of emerging technologies'),
-- Professional Skills
('technical_competency', 'professional_skills', 0.35, 'Role-specific hard skills'),
('problem_solving', 'professional_skills', 0.30, 'Analytical and solution design abilities'),
('domain_expertise', 'professional_skills', 0.25, 'Depth of field knowledge'),
('tool_proficiency', 'professional_skills', 0.10, 'Familiarity with industry tools'),
-- Soft Skills
('communication', 'soft_skills', 0.25, 'Clarity and articulation'),
('teamwork', 'soft_skills', 0.20, 'Collaboration examples'),
('leadership', 'soft_skills', 0.15, 'Influence and guidance abilities'),
('adaptability', 'soft_skills', 0.20, 'Response to change'),
('emotional_intelligence', 'soft_skills', 0.20, 'Self-awareness and empathy');
