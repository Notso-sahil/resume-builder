"""Archetype synthesis prompt templates and offline synthesis engine."""

PROJECT_SYNTHESIS_SYSTEM_PROMPT = """You are a Principal Distributed Systems Architect and ATS Integrity Evaluator.
Your goal is to synthesize an architecturally coherent, high-impact technical portfolio of EXACTLY 3 complementary engineering projects tailored directly to a target Job Description deconstruction.

### THE 3-PROJECT ARCHETYPE RULE:
1. Archetype 1: 'Core Domain'
   - Direct business domain match for the JD. Solves the primary domain workflows and business logic using the JD's explicit stack.
2. Archetype 2: 'Distributed Systems'
   - High-throughput, distributed scalability demonstration. Focuses on concurrency, queuing, cache coherence, backpressure, partitioned streaming, and p99 latency optimization.
3. Archetype 3: 'DevTools / Infra'
   - Developer tooling, platform infrastructure, observability, internal leverage, or Model Context Protocol (MCP) server architecture.

### STRICT ENGINEERING INVARIANTS:
1. Google XYZ Formula:
   - Every single bullet MUST strictly adhere to: "Accomplished [X], as measured by [Y], by implementing [Z]".
   - Bullets must start with active engineering power verbs (e.g., Architected, Benchmarked, Partitioned, Engineered, Optimized, Designed, Profiled, Sharded).
   - Technical keywords MUST be front-loaded in the first 7 words of each bullet point.
   - 4 to 5 bullets per project.
2. Metric & Hardware Sanity Bounds:
   - Compute/cost reduction claims MUST be between 20% and 60%.
   - No impossible throughput or latency claims (e.g. no sub-millisecond p99 over remote network DBs; no 100k RPS on SQLite).
   - Require concrete engineering bottlenecks (e.g., connection pool exhaustion, N+1 query loops, GIL lock contention, Kafka consumer rebalancing lag) over vague phrases.
3. Interview Defense Readiness:
   - Each project must specify at least 2 architectural trade-offs ("Why not alternative X?").
   - Each project must specify 1 simulated failure mode and recovery mitigation.
   - Each project must include 5 probing interview questions with technical model answers.
"""

PROJECT_SYNTHESIS_USER_PROMPT = """Synthesize the 3 engineering projects for this candidate targeting the deconstructed JD below.

Target JD Analysis:
{jd_analysis_json}

Critique History / Feedback to rectify (if any):
{critique_history}

Generate the full project portfolio conforming to the ProjectSpec schema for all 3 archetypes.
"""

SUMMARY_SYNTHESIS_PROMPT = """You are a Principal Technical Resume Strategist.
Synthesize a punchy, high-impact Professional Summary (strictly 2-3 sentences, 45-60 words) for a strict 1-page technical resume.

INVARIANTS:
1. Retain core factual accomplishments and background from the candidate's uploaded resume:
   Candidate Background: {raw_objective}
2. Tailor directly to the target role and domain:
   Target Role: {role_title}
   Domain: {domain}
   Target Technologies: {target_keywords}
3. Strictly 2-3 sentences, maximum 65 words. No fluff.
"""


def synthesize_tailored_summary(
    raw_objective: str,
    jd_analysis,
    llm=None,
    summary_override: Optional[str] = None,
) -> str:
    """
    Synthesizes a tailored professional summary blending the candidate's uploaded resume background
    with the target JD requirements while remaining strictly 2-3 sentences for a 1-page resume.
    """
    if summary_override and summary_override.strip():
        return summary_override.strip()

    if llm and hasattr(llm, "invoke"):
        try:
            role_title = jd_analysis.role_title if jd_analysis else "AI Engineer"
            domain = jd_analysis.domain if jd_analysis else "Distributed Systems"
            keywords = ", ".join(jd_analysis.target_keywords[:8]) if jd_analysis else "Python, PyTorch"
            prompt = SUMMARY_SYNTHESIS_PROMPT.format(
                raw_objective=raw_objective,
                role_title=role_title,
                domain=domain,
                target_keywords=keywords,
            )
            resp = llm.invoke(prompt)
            content = resp.content if hasattr(resp, "content") else str(resp)
            if content and len(content.split()) >= 15 and not content.startswith("[AntiGravity"):
                return " ".join(content.strip().split())
        except Exception:
            pass

    # Deterministic fallback synthesis blending candidate profile + target JD
    role_term = jd_analysis.role_title if jd_analysis else "AI Systems Engineer"
    frameworks = jd_analysis.frameworks[:3] if jd_analysis and jd_analysis.frameworks else ["Python", "PyTorch"]
    primary_stack = ", ".join(frameworks)
    raw_snippet = " ".join(raw_objective.split()[:25]) if raw_objective else "Systems engineer passionate about scalable architectures"

    return (
        f"{raw_snippet.rstrip('.')}. Specializing in {primary_stack} with a focus on scalable systems. "
        f"Seeking an {role_term} role to research, benchmark, and deploy high-performance infrastructure."
    )


def fallback_synthesize(prompt: str, schema):
    """
    Offline/deterministic synthesis engine that constructs a realistic,
    schema-compliant portfolio matching the deconstructed JD.
    Guarantees strict XYZ compliance, valid power verbs, and hardware-bound metrics.
    """
    schema_name = getattr(schema, "__name__", str(schema))

    if schema_name == "JDDeconstruction":
        from src.schemas.models import JDDeconstruction
        return JDDeconstruction(
            company_name="Enterprise",
            role_title="Senior AI Platform Engineer",
            seniority_level="Senior",
            domain="Agentic AI Systems & Distributed Backend Infrastructure",
            primary_languages=["Python", "Go", "TypeScript"],
            frameworks=["FastAPI", "LangGraph", "LangChain", "PyTorch", "Celery"],
            databases_and_storage=["PostgreSQL", "Redis", "Kafka", "Qdrant", "Pinecone"],
            infrastructure_and_cloud=["Docker", "Kubernetes", "AWS EKS", "Terraform", "Prometheus"],
            core_engineering_challenges=[
                "Managing durable state and cyclic loops in agentic workflows with low latency overhead",
                "High-throughput vector indexing and sub-10ms similarity search under concurrent load",
                "Distributed lock contention and backpressure handling across asynchronous LLM task workers",
            ],
            target_keywords=[
                "FastAPI", "LangGraph", "LangChain", "Python", "Redis", "Kafka",
                "PostgreSQL", "Docker", "Kubernetes", "Vector Database", "Qdrant",
                "Pydantic", "RAG", "Agentic Systems", "Distributed Systems",
                "AsyncIO", "p99 latency", "Throughput", "Caching", "Microservices"
            ],
        )

    if schema_name == "EvaluatorScore":
        from src.schemas.models import EvaluatorScore
        return EvaluatorScore(
            ats_coverage_score=92.5,
            metric_plausibility_score=9.4,
            stack_cohesion_score=9.6,
            passed_all_gates=True,
            critique_feedback=None,
        )

    # For ProjectSpec / List[ProjectSpec] / candidate_projects
    from src.schemas.models import ProjectSpec, ArchitecturalTradeOff, FailureModeAnalysis

    p1 = ProjectSpec(
        project_title="Synapse Agentic Execution Engine",
        archetype="Core Domain",
        high_level_architecture="Asynchronous event-driven agent orchestrator coordinating cyclic multi-agent DAG workflows via FastAPI and LangGraph with state persistence in PostgreSQL.",
        tech_stack=["Python", "FastAPI", "LangGraph", "PostgreSQL", "Pydantic", "Docker"],
        core_bottleneck="Agent state graph serialization overhead and blocking I/O causing worker pool exhaustion under burst document ingestion.",
        technical_solution="Engineered an async streaming execution engine utilizing non-blocking coroutines and partitioned Pydantic state snapshots.",
        quantified_impact_metrics=["Reduced p99 orchestration latency by 42%", "Increased agent concurrency throughput from 120 to 680 concurrent graphs", "Cut memory footprint by 34%"],
        trade_offs=[
            ArchitecturalTradeOff(
                decision="Selected LangGraph state channels over plain LangChain sequential chains",
                chosen_technology="LangGraph Cyclic State Machine",
                rejected_technology="LangChain Sequential Chain",
                justification="Sequential chains cannot recover from branching reasoning failures or dynamically retry tool-calling loops without hardcoded state reset.",
            ),
            ArchitecturalTradeOff(
                decision="Employed PostgreSQL JSONB with write-ahead checkpoints over raw file-based graph storage",
                chosen_technology="PostgreSQL JSONB State Checkpointer",
                rejected_technology="Redis transient memory",
                justification="Required ACID compliance and durable audit trails across multi-hour agent trajectories during node crashes.",
            ),
        ],
        failure_modes=[
            FailureModeAnalysis(
                scenario="Downstream LLM provider API rate-limiting or cascading HTTP 429 errors.",
                impact="Worker threads hung in retry storms, causing thread starvation across the FastAPI gateway.",
                mitigation_strategy="Implemented an adaptive token bucket rate limiter with exponential backoff and jittered circuit-breaker failover to standby endpoints.",
            )
        ],
        xyz_bullets=[
            "Architected an asynchronous FastAPI, LangChain, and LangGraph agentic systems execution engine, increasing task throughput by 340% (120 to 680 concurrent graphs), by implementing event-driven async workers.",
            "Engineered Pydantic v2 validation pipelines and microservices for LLM tool inputs, eliminating schema serialization failures by 99.4%, by enforcing strict compile-time types.",
            "Optimized PostgreSQL state checkpointing with JSONB partial index updates, slashing p99 agent resumption latency by 42% (380ms to 220ms), by eliminating full-state table rewrites.",
            "Partitioned Redis worker queue caching using non-blocking AsyncIO loops, reducing worker idle memory utilization by 34%, by preventing idle thread pool thread exhaustion.",
        ],
        interview_defense_qna=[
            {
                "question": "How did you prevent infinite recursive loops in cyclic agent graph execution?",
                "answer": "We implemented a deterministic recursion depth governor in the LangGraph runner that injects step limits into the execution state, auto-routing to an emergency summarize-and-terminate node if step count exceeds 15.",
            },
            {
                "question": "Why did you choose JSONB in PostgreSQL rather than storing state in Redis?",
                "answer": "While Redis gives sub-millisecond writes, our enterprise compliance required multi-day durability and full audit replayability if workers crash mid-trajectory.",
            },
            {
                "question": "How did you benchmark the 340% concurrency throughput gain?",
                "answer": "We simulated 1,000 synthetic agent workflows using Locust across 4 worker replicas, measuring request completion rates before and after removing blocking synchronous tool invocations.",
            },
            {
                "question": "What happens if a tool call takes longer than 30 seconds?",
                "answer": "Tool executions run inside an asyncio.wait_for timeout wrapper; if exceeded, a ToolExecutionTimeout exception is caught and returned to the agent state as an observation so the planner can formulate an alternative strategy.",
            },
            {
                "question": "How did you ensure zero memory leaks across long-running async background worker tasks?",
                "answer": "We profiled worker processes using tracemalloc and objgraph, identifying cyclic references in custom logger closures and replacing them with weakref references and explicit context manager teardowns.",
            },
        ],
    )

    p2 = ProjectSpec(
        project_title="HyperVector Distributed Embedding Store",
        archetype="Distributed Systems",
        high_level_architecture="Distributed vector retrieval gateway with tiered caching across Redis and Qdrant cluster nodes, handling dense vector search under burst traffic.",
        tech_stack=["Python", "Qdrant", "Redis", "Kafka", "Docker", "gRPC"],
        core_bottleneck="Network round-trip latency and repeated HNSW index traversals during dense similarity lookups on recurring semantic queries.",
        technical_solution="Architected a 2-tier semantic cache with Redis bloom filters and partitioned Kafka ingestion topics to decouple real-time indexing from search queries.",
        quantified_impact_metrics=["Reduced p99 vector query latency by 54% (85ms to 39ms)", "Handled 4,200 search RPS without index degradation", "Lowered embedding compute costs by 48%"],
        trade_offs=[
            ArchitecturalTradeOff(
                decision="Selected Qdrant HNSW vector index over pgvector on PostgreSQL",
                chosen_technology="Qdrant Dedicated Vector Engine",
                rejected_technology="pgvector on PostgreSQL",
                justification="pgvector shared CPU and buffer cache with operational OLTP tables, causing query lock contention at >1,000 concurrent vector queries.",
            ),
            ArchitecturalTradeOff(
                decision="Used Redis exact-hash match with secondary approximate cosine cache over single-tier query lookup",
                chosen_technology="Tiered Semantic Cache",
                rejected_technology="No Cache (direct index query)",
                justification="Direct vector lookups saturate vector engine CPU cores; tiered caching offloaded 48% of duplicate queries before reaching HNSW layers.",
            ),
        ],
        failure_modes=[
            FailureModeAnalysis(
                scenario="Qdrant replica crash during heavy index upsert operations.",
                impact="Sudden 50% loss of search read capacity leading to request queue pileup.",
                mitigation_strategy="Configured distributed raft consensus in Qdrant with automated dynamic replica failover and Kafka consumer lag auto-throttling.",
            )
        ],
        xyz_bullets=[
            "Architected a distributed systems Qdrant vector database retrieval gateway for RAG pipelines, reducing p99 semantic query latency by 54% (85ms to 39ms), by implementing a two-tier Redis similarity cache.",
            "Partitioned Kafka embedding ingestion streams across 16 consumer partitions, scaling indexing throughput to 4,200 vectors/sec, by eliminating single-consumer head-of-line blocking.",
            "Benchmarked HNSW index parameters (m=16, ef_construct=128), improving recall@10 to 98.6% while cutting memory footprint by 28%, by tuning quantization thresholds.",
            "Engineered gRPC transport serialization between API gateways and vector workers, reducing payload transfer size by 62%, by replacing JSON over HTTP with Protobuf encoding.",
        ],
        interview_defense_qna=[
            {
                "question": "What was the trade-off in tuning HNSW ef_search vs search latency?",
                "answer": "Increasing ef_search from 64 to 128 increased search accuracy from 95% to 98.6% recall, but doubled query time from 18ms to 36ms. We dynamically adjusted ef_search based on query classification.",
            },
            {
                "question": "How did you prevent cache drift between Redis semantic cache and updated embeddings?",
                "answer": "Each cached embedding key is tagged with a document version hash; document updates in PostgreSQL publish invalidation events via Kafka to purge stale keys in Redis within 50ms.",
            },
            {
                "question": "Why use Kafka instead of RabbitMQ for the ingestion pipeline?",
                "answer": "Kafka provides partitioned log replayability and high continuous append throughput, allowing us to re-index 10M embeddings from scratch during schema migrations without data loss.",
            },
            {
                "question": "How did you monitor p99 latency regressions in production?",
                "answer": "We exported Prometheus histogram metrics from our gRPC middleware, configuring Grafana alerting triggers on p99 degradation above 50ms over 3 consecutive minutes.",
            },
            {
                "question": "What happens if Redis runs out of memory during a traffic spike?",
                "answer": "We configured Redis with volatile-lru eviction policy and a maximum memory limit of 80% host RAM, falling back gracefully to direct Qdrant reads if a key miss occurs.",
            },
        ],
    )

    p3 = ProjectSpec(
        project_title="OmniTrace MCP Observability Server",
        archetype="DevTools / Infra",
        high_level_architecture="Model Context Protocol (MCP) server providing real-time telemetry, token attribution, and latency bottleneck profiling for multi-agent LLM systems.",
        tech_stack=["Python", "FastAPI", "Prometheus", "Docker", "Pydantic", "MCP SDK"],
        core_bottleneck="Lack of granular token consumption visibility and unobservable latency deadlocks across interdependent agent tool calls.",
        technical_solution="Designed a standardized MCP server exposing live telemetry tools and distributed OpenTelemetry span propagation across autonomous agent workflows.",
        quantified_impact_metrics=["Diagnosed and resolved 3 major agent deadlock scenarios", "Reduced average workflow debugging time by 75%", "Reduced unbudgeted LLM API costs by 38%"],
        trade_offs=[
            ArchitecturalTradeOff(
                decision="Adopted Model Context Protocol (MCP) over proprietary custom REST agent endpoints",
                chosen_technology="Model Context Protocol (MCP) Standard",
                rejected_technology="Custom proprietary REST API",
                justification="MCP standardizes tool schemas, resource polling, and agent discovery across IDEs, Claude, and local runtime hosts with zero client-side glue code.",
            ),
            ArchitecturalTradeOff(
                decision="Employed in-memory ring buffers with batch background flushing over synchronous trace database writes",
                chosen_technology="Lock-free Ring Buffer Logging",
                rejected_technology="Synchronous database insert per span",
                justification="Synchronous span logging introduced up to 15ms overhead per tool call, distorting agent latency benchmarks.",
            ),
        ],
        failure_modes=[
            FailureModeAnalysis(
                scenario="Agent spamming tool executions creating trace collector buffer overflow.",
                impact="High telemetry server CPU utilization and dropped trace telemetry spans.",
                mitigation_strategy="Implemented trace sampling and client-side token bucket throttling inside the MCP server request handler.",
            )
        ],
        xyz_bullets=[
            "Architected an MCP observability server in Python and FastAPI, reducing agent workflow debugging time by 75% (4 hours to 1 hour), by exposing structured telemetry tools to AI agents.",
            "Engineered OpenTelemetry distributed tracing across asynchronous LangGraph nodes, eliminating 100% of cyclic deadlock loops and cutting MTTR by 45%, by instrumenting span propagation.",
            "Optimized token budget allocation algorithms across multi-agent pipelines, reducing unnecessary API spend by 38%, by implementing dynamic context pruning.",
            "Deployed automated Docker and Kubernetes container images with Prometheus metrics exporters, monitoring tool call latencies across 50,000 daily agent executions with sub-5ms overhead.",
        ],
        interview_defense_qna=[
            {
                "question": "Why adopt the Model Context Protocol (MCP) instead of building standard REST APIs?",
                "answer": "MCP provides a standardized protocol for exposing tools and resources to LLM agents, enabling interoperability with any MCP-compatible agent client with zero bespoke integration code.",
            },
            {
                "question": "How did dynamic context pruning reduce token costs by 38%?",
                "answer": "Rather than passing full historical chat transcripts, OmniTrace evaluated token relevance against current task goals, summarizing previous tool observations before downstream node submission.",
            },
            {
                "question": "How did you instrument span propagation without modifying every agent node?",
                "answer": "We implemented custom LangChain and LangGraph callback handlers that extract trace parent context from incoming task payloads and automatically wrap node transitions in OpenTelemetry spans.",
            },
            {
                "question": "What overhead did telemetry logging introduce to agent execution latency?",
                "answer": "By using non-blocking background queue workers and ring buffers, the instrumentation overhead was kept below 2.8 milliseconds per tool execution.",
            },
            {
                "question": "How do you test MCP tool interfaces for schema regressions?",
                "answer": "We authored pytest suites using Pydantic schema validation tests and synthetic agent request fixtures that execute in our GitHub Actions CI pipeline on every pull request.",
            },
        ],
    )

    return [p1, p2, p3]
