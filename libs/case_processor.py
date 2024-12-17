from typing import List, Dict, Any
import re

class CaseProcessor:
    @staticmethod
    def split_into_cases(content: Dict[str,Any]) -> List[Dict[str, Any]]:
        cases = []
        current_case = []
        current_headline = ""
        
        headline_pattern = r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?=\n|$)'
        
        for line in content:
            if not line.strip():
                if current_case:
                    cases.append({
                        'headline': current_headline,
                        'content': '\n'.join(current_case)
                    })
                    current_case = []
                continue
                
            if re.match(headline_pattern, line):
                if current_case:
                    cases.append({
                        'headline': current_headline,
                        'content': '\n'.join(current_case)
                    })
                    current_case = []
                current_headline = line
                
            current_case.append(line)
        
        if current_case:
            cases.append({
                'headline': current_headline,
                'content': '\n'.join(current_case)
            })
        
        return cases

    @staticmethod
    def analyze_case(case: Dict[str, Any]) -> Dict[str, Any]:
        analysis = {
            'headline': case['headline'],
            'type': None,
            'key_entities': [],
            'summary': ""
        }
        
        content = case['content'].lower()
        
        if any(word in content for word in ['theft', 'stolen', 'robbery']):
            analysis['type'] = 'THEFT'
        elif any(word in content for word in ['drug', 'narcotics', 'trafficking']):
            analysis['type'] = 'DRUG_TRAFFICKING'
        elif any(word in content for word in ['fraud', 'scam', 'phishing']):
            analysis['type'] = 'FRAUD'
        elif any(word in content for word in ['gang', 'violence']):
            analysis['type'] = 'GANG_ACTIVITY'
        else:
            analysis['type'] = 'OTHER'
            
        return analysis

    @staticmethod
    def process_document(content: Dict[str,Any]) -> List[Dict[str, Any]]:
        cases = CaseProcessor.split_into_cases(content)
        
        analyzed_cases = []
        for case in cases:
            analysis = CaseProcessor.analyze_case(case)
            analyzed_cases.append({
                'original': case,
                'analysis': analysis
            })
            
        return analyzed_cases