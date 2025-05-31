Thank you for taking the time to take on the Eightfold engineering challenge! We use this challenge as a way to understand your engineering abilities comprehensively, as well as how you would work within a team here at Eightfold. 
Guidelines
This is an open internet and open book round; feel free to use any resource you find relevant.
You will have 90 minutes to work on this challenge to be used for designing the system and explaining your design choices.
You can use Draw.io for diagrams.
You will be judged based on a mix of approach and design used.
Problem statement
Resume Parsers

These systems are designed with a distributed architecture that allows them to scale easily and handle large volumes of ingestions, processing and viewing.
For this challenge, you must write a code that is capable of Resume Parsing and satisfies these conditions
Multiple known format support
Zero code change for new format addition
Executable code

## Requirements gathering
- We'll get multiple input jsons, can be of different formats... we need to convert them into some structured data which our platform/backend can understand
- Define the entities and their relationships

- config:
    {
        "user": {
            "entity_datatype"
            "name": {
                "key_mapping" : "fullname",
                "data_type": str,
                "data_extraction_formula": "",
                "validations": 
            },
            ""
        },
        "education": {
            "entity_datatype": List[Dict]
            "schools": {
                "name": {
                    "key_mapping": 
                }
                "degree": {
                    "key_mapping": 
                }
            }
        },
        ""
    }
