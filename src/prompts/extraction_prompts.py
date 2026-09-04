"""JD deconstruction prompt templates."""

JD_EXTRACTION_PROMPT = """You are a Principal Distributed Systems Architect and ATS Integrity Evaluator.
Analyze the following technical Job Description (JD) and perform a deep deconstruction into structured engineering attributes.

Deconstruct the JD into:
1. company_name: The hiring company name (e.g., 'Naïve', 'Stripe', 'Google', 'OpenAI', or 'company' if not mentioned).
2. role_title: The official or normalized job title (e.g., 'Senior AI Platform Engineer', 'Backend Distributed Systems Engineer').
3. seniority_level: Identified seniority (e.g., 'Junior', 'Mid-Level', 'Senior', 'Staff / Principal').
4. domain: The business domain and systems context (e.g., 'Agentic AI / LLM Orchestration', 'Fintech Real-Time Payments', 'AdTech Real-Time Bidding').
5. primary_languages: Programming languages explicitly required or preferred (e.g., Python, Go, TypeScript, Rust, C++).
6. frameworks: Core backend/AI frameworks (e.g., FastAPI, LangChain, LangGraph, PyTorch, Ray, Spring Boot).
7. databases_and_storage: Storage layers (e.g., PostgreSQL, Redis, Kafka, Pinecone, ClickHouse, Cassandra, Qdrant).
8. infrastructure_and_cloud: Cloud, containers, deployment, orchestrators (e.g., Docker, Kubernetes, AWS EKS, GCP Cloud Run, Terraform, Helm).
9. core_engineering_challenges: 3-5 concrete architectural bottlenecks and hard problems emphasized in the JD (e.g., p99 latency guarantees, agentic loop state durability, vector indexing throughput, streaming backpressure).
10. target_keywords: 20-30 high-priority ATS technical keywords, tools, protocols, and concepts found in the JD that must be covered in resume bullets.

Target Job Description:
{raw_jd}
"""
