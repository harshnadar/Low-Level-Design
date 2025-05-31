import json
from parser import ConfigurableResumeParser
from pathlib import Path

def demo_parse_resume():
    """Demo function to parse resumes using the configurable parser"""
    
    # Initialize parser with config
    config_path = "eightfold_interview/configs/config_schema.json"
    parser = ConfigurableResumeParser(config_path)
    
    # Test with both input JSONs
    input_files = ["eightfold_interview/input_json1.json", "eightfold_interview/input_json2.json", "eightfold_interview/input_json3.json"]
    
    for input_file in input_files:
        print(f"\n{'='*60}")
        print(f"Parsing: {input_file}")
        print('='*60)
        
        try:
            # Load resume data
            with open(input_file, 'r') as f:
                resume_data = json.load(f)
            
            # Parse resume
            parsed_resume = parser.parse(resume_data)
            
            # Display results
            if parsed_resume.personal_info:
                print("\n📋 Personal Information:")
                print(f"   Name: {parsed_resume.personal_info.full_name}")
                print(f"   Email: {parsed_resume.personal_info.email}")
                if parsed_resume.personal_info.phone:
                    print(f"   Phone: {parsed_resume.personal_info.phone}")
                if parsed_resume.personal_info.location:
                    print(f"   Location: {parsed_resume.personal_info.location}")
            
            if parsed_resume.education:
                print("\n🎓 Education:")
                for edu in parsed_resume.education:
                    print(f"   • {edu.degree} from {edu.school_name}")
                    if edu.field_of_study:
                        print(f"     Field: {edu.field_of_study}")
                    if edu.graduation_year:
                        print(f"     Year: {edu.graduation_year}")
            
            if parsed_resume.experience:
                print("\n💼 Experience:")
                for exp in parsed_resume.experience:
                    print(f"   • {exp.title} at {exp.company}")
                    if exp.duration:
                        print(f"     Duration: {exp.duration}")
                    if exp.description:
                        print(f"     {exp.description[:100]}...")
            
            if parsed_resume.skills:
                print("\n🛠️  Skills:")
                skills_list = [skill.skill_name for skill in parsed_resume.skills]
                print(f"   {', '.join(skills_list)}")
            
            # Save parsed output
            output_filename = Path(input_file).name
            output_file = f"parsed_{output_filename}"
            with open(output_file, 'w') as f:
                json.dump(parsed_resume.to_dict(), f, indent=2)
            print(f"\n✅ Parsed output saved to: {output_file}")
            # print(f"\n✅ Parsed output saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error parsing {input_file}: {e}")
            import traceback
            traceback.print_exc()

def test_with_custom_format():
    """Test with a custom format to show flexibility"""
    print("\n" + "="*60)
    print("Testing with Custom Format")
    print("="*60)
    
    # Create a custom format resume
    custom_resume = {
        "candidateName": "John Doe",
        "mail": "john.doe@example.com",
        "mobile": "+1234567890",
        "city": "San Francisco",
        "qualifications": [
            {
                "university": "MIT",
                "course": "Computer Science",
                "major": "AI/ML",
                "graduation_year": 2020
            }
        ],
        "employment": [
            {
                "organization": "Tech Corp",
                "designation": "Senior Engineer",
                "tenure": "2020-2023",
                "responsibilities": "Led team of 5 engineers"
            }
        ],
        "technologies": ["Python", "Machine Learning", "AWS", "Docker"]
    }
    
    # Save and parse
    with open("custom_format.json", "w") as f:
        json.dump(custom_resume, f, indent=2)
    
    parser = ConfigurableResumeParser("configs/config_schema.json")
    parsed = parser.parse(custom_resume)
    
    print(f"\nParsed from custom format:")
    print(f"Name: {parsed.personal_info.full_name if parsed.personal_info else 'Not found'}")
    print(f"Email: {parsed.personal_info.email if parsed.personal_info else 'Not found'}")
    print(f"Education: {len(parsed.education)} entries")
    print(f"Experience: {len(parsed.experience)} entries")
    print(f"Skills: {len(parsed.skills)} entries")

if __name__ == "__main__":
    # Run the demo
    demo_parse_resume()
    
    # # Test with custom format
    # test_with_custom_format()

    # with open("eightfold_interview/configs/config_schema.json", "r") as f:
    #     config = json.load(f)
    # print("Configuration loaded successfully:")