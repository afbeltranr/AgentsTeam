# demo_scholarships.py

from agents.job_application.markdown_generator_agent import MarkdownGeneratorAgent
from utils.extract_keywords_from_pdf import extract_keywords_from_pdf
from pathlib import Path

def create_demo_scholarships():
    """Create demo scholarship data to show functionality"""
    
    # Extract actual CV keywords
    cv_keywords = extract_keywords_from_pdf("documents/resumes/CV.pdf")
    
    # Sample scholarship data (realistic examples)
    sample_scholarships = [
        {
            "title": "Fulbright Science & Technology Fellowship",
            "description": "This fellowship supports international students pursuing advanced research in chemistry, data science, and educational technology. Candidates should demonstrate strong analytical skills, programming abilities (Python preferred), and interest in science education. The program includes mentorship, research funding, and professional development opportunities.",
            "url": "https://www.fulbright.org/science-technology-fellowship",
            "deadline": "March 15, 2026",
            "amount": "$50,000",
            "source": "Fulbright Foundation",
            "search_term": "chemistry",
            "contact_email": "fellowships@fulbright.org",
            "cv_matches": ["data", "python", "analysis", "learning", "visualization"],
            "fit_score": 8
        },
        {
            "title": "NSF Graduate Research Fellowship in Chemistry Education",
            "description": "The National Science Foundation supports graduate students in chemistry education research. This fellowship particularly values candidates with computational skills, data analysis experience, and interest in improving STEM education through technology. Machine learning applications in education are encouraged.",
            "url": "https://www.nsf.gov/funding/pgm_summ.jsp?pims_id=6201",
            "deadline": "October 25, 2025",
            "amount": "$34,000/year + tuition",
            "source": "National Science Foundation",
            "search_term": "science education",
            "contact_email": "grfp@nsf.gov",
            "cv_matches": ["data", "analysis", "machine", "learning", "python"],
            "fit_score": 7
        },
        {
            "title": "DAAD STEM Education Research Scholarship",
            "description": "German Academic Exchange Service fellowship for international students in STEM education. Focus on innovative teaching methods, educational data analytics, and technology integration in science classrooms. Particularly interested in candidates from Latin America with computational background.",
            "url": "https://www.daad.org/stem-education-fellowship",
            "deadline": "November 30, 2025",
            "amount": "€1,200/month",
            "source": "DAAD",
            "search_term": "educational sciences",
            "contact_email": "fellowships@daad.de",
            "cv_matches": ["data", "colombia", "analysis", "using"],
            "fit_score": 6
        },
        {
            "title": "Chevron STEM Education Fellowship",
            "description": "Supporting future educators in chemistry and environmental sciences. This fellowship values candidates with strong analytical backgrounds, especially those with experience in data visualization and statistical analysis. Focus on sustainable chemistry education.",
            "url": "https://www.chevron.com/sustainability/education",
            "deadline": "January 15, 2026",
            "amount": "$25,000",
            "source": "Chevron Corporation",
            "search_term": "chemistry",
            "contact_email": "education@chevron.com",
            "cv_matches": ["analysis", "visualization", "data"],
            "fit_score": 5
        },
        {
            "title": "ACS Scholars Program for Underrepresented Groups",
            "description": "American Chemical Society scholarship for underrepresented students in chemistry. Values international students with strong academic backgrounds, particularly those with data science and computational chemistry interests.",
            "url": "https://www.acs.org/content/acs/en/funding/scholarships.html",
            "deadline": "March 1, 2026",
            "amount": "$5,000",
            "source": "American Chemical Society",
            "search_term": "chemistry",
            "contact_email": "scholars@acs.org",
            "cv_matches": ["data", "python", "analysis"],
            "fit_score": 5
        },
        {
            "title": "Gates Cambridge Scholarship - Science Education",
            "description": "Full scholarship for international students at Cambridge University. Particularly seeks candidates interested in improving science education through technology and data-driven approaches. Strong preference for candidates with programming skills.",
            "url": "https://www.gatescambridge.org/",
            "deadline": "December 3, 2025",
            "amount": "Full tuition + living expenses",
            "source": "Gates Cambridge Trust",
            "search_term": "science education",
            "contact_email": "info@gatescambridge.org",
            "cv_matches": ["data", "python", "analysis", "learning"],
            "fit_score": 7
        },
        {
            "title": "UNESCO Science Education Innovation Fellowship",
            "description": "International fellowship for innovative approaches to science education. Seeks candidates with strong analytical skills, experience with educational technology, and interest in data-driven educational research.",
            "url": "https://en.unesco.org/themes/education/fellowships",
            "deadline": "September 15, 2025",
            "amount": "$30,000",
            "source": "UNESCO",
            "search_term": "science education",
            "contact_email": "fellowships@unesco.org",
            "cv_matches": ["data", "analysis", "learning"],
            "fit_score": 4
        }
    ]
    
    return sample_scholarships, cv_keywords

def run_demo_scholarships():
    print("🎓 Running demo scholarship search to show functionality...\n")
    
    # Get demo data
    scholarships, cv_keywords = create_demo_scholarships()
    
    print(f"📊 Demo found {len(scholarships)} scholarships")
    print(f"🎯 CV Keywords: {', '.join(cv_keywords)}")
    
    # Generate markdown report
    print("📝 Generating demo markdown report...")
    markdown_generator = MarkdownGeneratorAgent(name="MarkdownGenerator")
    generator_result = markdown_generator.receive_message({
        "type": "scholarships",
        "scholarships": scholarships,
        "cv_keywords": cv_keywords
    })
    
    if generator_result.get("type") == "response":
        print(f"✅ Demo scholarship report generated: {generator_result['filename']}")
        
        # Show summary
        print("\n" + "="*80)
        print("🏆 DEMO TOP SCHOLARSHIP MATCHES")
        print("="*80)
        
        for i, scholarship in enumerate(scholarships[:3], 1):
            title = scholarship.get("title", "Unknown")
            amount = scholarship.get("amount", "Not specified")
            deadline = scholarship.get("deadline", "Not specified")
            fit_score = scholarship.get("fit_score", 0)
            matches = scholarship.get("cv_matches", [])
            
            print(f"\n{i}. {title}")
            print(f"   💰 Amount: {amount}")
            print(f"   📅 Deadline: {deadline}")
            print(f"   ⭐ Fit Score: {fit_score}/10")
            print(f"   🎯 Matched Keywords: {', '.join(matches)}")
            print(f"   🔗 URL: {scholarship.get('url', 'N/A')}")
        
        print(f"\n📄 Full demo report available in: {generator_result['filename']}")
        
    else:
        print("❌ Demo report generation failed")

if __name__ == "__main__":
    run_demo_scholarships()
