Objective: Comprehensively extract structured intelligence from provided text documents. Processing Instructions:

Entity Extraction
Identify ALL unique entities with HIGH precision
Entity Categories:
PERSON
ORGANIZATION
LOCATION
DATE/TIME
FINANCIAL (Accounts, Transactions)
COMMUNICATION (Phones, Emails)
IDENTIFIERS (IDs, Registration Numbers)
Relationship Mapping
Detect connections between extracted entities
Relationship Types:
Professional (Works For, Affiliated)
Geographical (Located In)
Financial (Transactional Links)
Hierarchical
Communication Networks
Anomaly Detection
Identify statistically significant deviations
Anomaly Classification:
Contextual Irregularities
Statistical Outliers
Potential Risk Indicators Output Requirements:
Use EXACT JSON structure provided
Include confidence scores (0-1 range)
Prioritize actionable insights
Maintain computational efficiency Critical Constraints:
Maximum 50 entities per document
Minimum confidence threshold: 0.6
Emphasize precision over exhaustive extraction RESPOND WITH STRUCTURED JSON STRICTLY ADHERING TO SPECIFIED FORMAT
[ { "case_id": "", "entities": [ { "id": "", "value": "", "type": "", "context": "", "confidence": 0.0, "source_documents": [] } ], "relations": [ { "relation_id": "", "source": "", "target": "", "type": "", "confidence": 0.0, "evidence": "" } ], "anomalies": [ { "anomaly_id": "", "description": "", "severity": "", "related_entities": [], "potential_impact": "", "confidence": 0.0 } ], "graph_data": { "nodes": [ { "id": "", "label": "", "type": "", "attributes": {} } ], "edges": [ { "source": "", "target": "", "type": "" } ] }, "case_info": { "headline": "", "type": "", "source_documents": [], "processing_timestamp": "" }, "metadata": { "total_entities": 0, "total_relations": 0, "total_anomalies": 0, "processing_model": "", "model_version": "" } } ]
data you need to analyse and give all the responce in the format not leaving anything empty or not recognized:
“Police Bust Multi -State Car Theft Ring After High -Speed Chase A multi -state car theft ring w as uncovered in a joint operation by police forces from New York, New Jersey, and Pennsylvania. The investigation began when a suspicious vehicle, a black BMW X5 with license plate number NY20 Z5678 , was found abandoned near Times Square. Another vehicle, a white Ford F -150 with plate number NJ11 G1234 , was stopped near the George Washington Bridge. Witnesses expressed a mix of shock and relief. Sarah Cooper, a local shop owner, stated, "It's terrifying to think that this could happen right in our neighborh ood. I'm just glad the police caught them in time." Another witness, Thomas Green, remarked, "Honestly, I was afraid to even report what I saw. But now I feel safer knowing they're caught." Further investigations revealed a red Honda Accord with license pl ate PA44 T9999 , registered to a corporate fleet, also stolen and abandoned in Philadelphia. In addition, a yellow Chevrolet Camaro with plate NY33 M1234 was seized during the operation. Authorities have urged citizens to stay vigilant and report any suspic ious activities, emphasizing that community cooperation played a crucial role in solving this case.”