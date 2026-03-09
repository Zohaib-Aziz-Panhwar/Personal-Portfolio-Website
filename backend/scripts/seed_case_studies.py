"""
Seed script to populate the database with sample case studies.
Run this script to add sample case studies to the database.
"""

import sys
import os
from datetime import datetime, timezone

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_case_studies_collection

def seed_case_studies():
    """Seed the database with sample case studies."""
    collection = get_case_studies_collection()
    
    if collection is None:
        print("[ERROR] Cannot connect to database. Please check your MongoDB connection.")
        return
    
    # Check if case studies already exist
    existing_count = collection.count_documents({})
    if existing_count > 0:
        print(f"[INFO] Database already contains {existing_count} case study(ies).")
        print("[INFO] Adding sample case studies anyway to ensure we have enough for testing...")
    
    sample_case_studies = [
        {
            "title": "Efficient Attention Mechanisms for Low-Resource NLP",
            "slug": "efficient-attention-mechanisms-low-resource-nlp",
            "short_description": "Proposes a lightweight attention variant reducing memory footprint by 40% while maintaining competitive accuracy on benchmark tasks.",
            "description": "This case study explores the development of efficient attention mechanisms specifically designed for low-resource natural language processing scenarios. Traditional attention mechanisms, while effective, often require significant computational resources and memory, making them impractical for resource-constrained environments.\n\nOur research focused on creating a novel attention variant that maintains the effectiveness of standard attention mechanisms while dramatically reducing memory requirements. Through extensive experimentation and optimization, we developed a technique that reduces memory footprint by approximately 40% without compromising on model accuracy.\n\nThe methodology involved analyzing attention patterns across multiple benchmark datasets, identifying redundant computations, and implementing a sparse attention mechanism that selectively processes the most relevant token interactions. We validated our approach on several standard NLP benchmarks including GLUE, SQuAD, and various low-resource language datasets.\n\nResults demonstrated that our efficient attention mechanism achieves competitive or superior performance compared to baseline models while requiring significantly fewer computational resources. This makes the approach particularly valuable for deployment in edge devices, mobile applications, and scenarios with limited computational budgets.\n\nThe implications of this research extend beyond NLP, as the principles can be applied to other domains requiring efficient attention mechanisms, such as computer vision and multimodal learning.",
            "status": "Published",
            "cover_image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200&h=600&fit=crop",
            "tags": ["NLP", "Machine Learning", "Attention Mechanisms", "Low-Resource Computing", "Deep Learning"],
            "author": "Research Team",
            "publication_date": "2024-03-15",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Graph-Based Approaches to Code Vulnerability Detection",
            "slug": "graph-based-code-vulnerability-detection",
            "short_description": "Explores using graph neural networks to identify security vulnerabilities in source code repositories at scale.",
            "description": "This case study presents a comprehensive investigation into applying graph neural networks (GNNs) for automated code vulnerability detection. Traditional static analysis tools often produce high false positive rates and struggle with complex code patterns, while manual security audits are time-consuming and don't scale to large codebases.\n\nOur approach leverages the inherent graph structure of source code, representing code as abstract syntax trees (ASTs) and control flow graphs (CFGs). By modeling code as graphs, we can capture both syntactic and semantic relationships between code elements, enabling more accurate vulnerability detection.\n\nWe developed a novel GNN architecture specifically designed for code analysis, incorporating attention mechanisms to focus on potentially vulnerable code patterns. The model was trained on a diverse dataset of vulnerable and secure code samples from multiple programming languages, including C/C++, Java, Python, and JavaScript.\n\nThe system demonstrates significant improvements over traditional static analysis tools, achieving higher precision and recall rates while reducing false positives. Our approach successfully identifies various vulnerability types including buffer overflows, SQL injection, cross-site scripting (XSS), and authentication bypass vulnerabilities.\n\nPractical applications include integration into CI/CD pipelines for automated security scanning, IDE plugins for real-time vulnerability detection, and large-scale code repository analysis. The graph-based approach also provides interpretability, allowing developers to understand why certain code patterns are flagged as vulnerable.\n\nFuture work involves extending the approach to detect more complex vulnerability patterns, improving cross-language generalization, and developing techniques for vulnerability fix suggestion.",
            "status": "Ongoing",
            "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&h=600&fit=crop",
            "tags": ["Cybersecurity", "Graph Neural Networks", "Code Analysis", "Vulnerability Detection", "Software Security"],
            "author": "Security Research Lab",
            "publication_date": None,
            "created_at": datetime.now(timezone.utc)
        },
        {
            "title": "Federated Learning for Privacy-Preserving Health Data",
            "slug": "federated-learning-privacy-preserving-health-data",
            "short_description": "Investigating decentralized model training techniques for sensitive medical datasets across institutions.",
            "description": "This case study addresses the critical challenge of training machine learning models on sensitive health data while maintaining patient privacy and complying with healthcare regulations such as HIPAA and GDPR. Traditional centralized approaches require sharing patient data across institutions, which raises significant privacy and legal concerns.\n\nFederated learning offers a promising solution by enabling model training across multiple institutions without sharing raw patient data. Instead, each institution trains models locally on their data and shares only model updates (gradients) with a central server, which aggregates these updates to improve the global model.\n\nOur research focuses on adapting federated learning specifically for healthcare applications, addressing unique challenges such as non-IID data distribution (different institutions may have different patient populations), communication efficiency, and robustness against malicious participants.\n\nWe developed a novel federated learning framework that incorporates differential privacy guarantees, ensuring that individual patient information cannot be inferred from shared model updates. The framework also includes mechanisms for handling heterogeneous data distributions and improving convergence rates in federated settings.\n\nExperimental validation was conducted using real-world health datasets from multiple institutions, demonstrating that our approach achieves model performance comparable to centralized training while maintaining strong privacy guarantees. The system successfully trains models for various healthcare applications including disease prediction, treatment recommendation, and medical image analysis.\n\nKey contributions include privacy-preserving aggregation algorithms, communication-efficient update mechanisms, and techniques for handling statistical heterogeneity in federated healthcare settings. The framework has been deployed in pilot studies with multiple healthcare institutions, demonstrating practical feasibility.\n\nThis research has significant implications for enabling collaborative healthcare AI while respecting patient privacy, potentially accelerating medical research and improving patient outcomes through shared knowledge without compromising data confidentiality.",
            "status": "Ongoing",
            "cover_image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1200&h=600&fit=crop",
            "tags": ["Federated Learning", "Healthcare AI", "Privacy", "Medical Data", "Machine Learning"],
            "author": "Healthcare AI Research Group",
            "publication_date": None,
            "created_at": datetime.now(timezone.utc)
        }
    ]
    
    try:
        result = collection.insert_many(sample_case_studies)
        print(f"[SUCCESS] Successfully inserted {len(result.inserted_ids)} sample case study(ies)!")
        print("\nSample case studies created:")
        for case_study in sample_case_studies:
            print(f"  - {case_study['title']} (slug: {case_study['slug']}, status: {case_study['status']})")
    except Exception as e:
        print(f"[ERROR] Failed to insert sample case studies: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting case study seed script...")
    seed_case_studies()
    print("Seed script completed.")

