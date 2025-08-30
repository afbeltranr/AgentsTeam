# run_new_features.py

from run_scholarships import run_scholarships
from run_toefl_jobs import run_toefl_jobs
import time

def run_all_new_features():
    """Run both scholarship search and TOEFL job search"""
    
    print("🚀 Starting comprehensive search for scholarships and TOEFL jobs...")
    print("=" * 80)
    
    # Run scholarship search
    print("\n🎓 PHASE 1: SCHOLARSHIP SEARCH")
    print("-" * 50)
    try:
        run_scholarships()
        print("✅ Scholarship search completed successfully!")
    except Exception as e:
        print(f"❌ Scholarship search failed: {e}")
    
    print("\n" + "=" * 80)
    
    # Wait a bit between searches to be respectful to servers
    print("⏳ Waiting 5 seconds before starting job search...")
    time.sleep(5)
    
    # Run TOEFL job search  
    print("\n💼 PHASE 2: TOEFL JOBS SEARCH")
    print("-" * 50)
    try:
        run_toefl_jobs()
        print("✅ TOEFL job search completed successfully!")
    except Exception as e:
        print(f"❌ TOEFL job search failed: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 ALL SEARCHES COMPLETED!")
    print("📁 Check the 'data/generated_applications/' folder for your reports:")
    print("   - scholarships_YYYY-MM-DD.md")
    print("   - toefl_jobs_YYYY-MM-DD.md")
    print("=" * 80)

if __name__ == "__main__":
    run_all_new_features()
