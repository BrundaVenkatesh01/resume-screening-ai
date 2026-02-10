from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the model once when the app starts (not every time we match)
# This model converts text into numbers (vectors) that capture meaning
# "all-MiniLM-L6-v2" is small, fast, and great for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_match_score(resume_text, job_description):
    """
    Compares a resume to a job description and returns a match score.
    
    How it works:
    1. Convert both texts into vectors (lists of numbers)
       - Similar meaning = vectors pointing in same direction
    2. Calculate cosine similarity between the two vectors
       - Score of 1.0 = identical meaning
       - Score of 0.0 = completely unrelated
    3. Convert to a percentage for easy reading
    
    This is SEMANTIC matching - not just keyword counting!
    So "machine learning engineer" and "ML developer" will score high
    even though the words are different.
    """
    # Turn text into vectors
    resume_vector = model.encode([resume_text])
    job_vector = model.encode([job_description])
    
    # Calculate similarity (returns value between -1 and 1)
    similarity = cosine_similarity(resume_vector, job_vector)[0][0]
    
    # Convert to percentage (0-100)
    score = round(float(similarity) * 100, 2)
    
    return score


def extract_keywords(text, top_n=15):
    """
    Extracts the most important keywords from a text.
    
    Why we need this:
    - Shows recruiter WHICH skills are/aren't matching
    - Gives candidate actionable feedback
    
    Simple approach: filter out common words (stop words)
    and return the most frequent meaningful words.
    """
    import re
    from collections import Counter
    
    # Common words to ignore (stop words)
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'shall', 'can',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we',
        'they', 'it', 'its', 'our', 'your', 'their', 'my', 'his', 'her',
        'as', 'if', 'then', 'than', 'so', 'yet', 'both', 'each', 'more',
        'also', 'not', 'no', 'nor', 'up', 'out', 'about', 'into', 'through'
    }
    
    # Clean and split text into words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    # Remove stop words
    meaningful_words = [w for w in words if w not in stop_words]
    
    # Count and return top N most frequent
    word_counts = Counter(meaningful_words)
    top_keywords = [word for word, count in word_counts.most_common(top_n)]
    
    return top_keywords


def find_matching_skills(resume_text, job_description):
    """
    Finds which skills from the job description appear in the resume.
    
    Returns:
    - matched: skills that ARE in the resume
    - missing: skills that are NOT in the resume (improvement areas!)
    """
    job_keywords = set(extract_keywords(job_description, top_n=20))
    resume_keywords = set(extract_keywords(resume_text, top_n=30))
    
    matched = job_keywords.intersection(resume_keywords)
    missing = job_keywords.difference(resume_keywords)
    
    return list(matched), list(missing)


def rank_resumes(resumes_dict, job_description):
    """
    Takes multiple resumes and ranks them by match score.
    
    Args:
        resumes_dict: {"filename": "resume text", ...}
        job_description: the job posting text
    
    Returns:
        List of dicts sorted by score (highest first)
    """
    results = []
    
    for filename, resume_text in resumes_dict.items():
        score = get_match_score(resume_text, job_description)
        matched, missing = find_matching_skills(resume_text, job_description)
        
        results.append({
            "filename": filename,
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })
    
    # Sort by score, highest first
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results