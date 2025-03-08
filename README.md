# GenFlow: Graph-Based Adaptive Multi-Agent LLM Workflows

GenFlow is a proof-of-concept project that combines the power of graph databases (Neo4j) with serverless computing (AWS Lambda) and workflow orchestration (AWS Step Functions) to create SCALABLE, ROBUST, and ADAPTIVE multi-agent LLM workflows.

## Key Features

### Graph-Based Agent Architecture
- **Dynamic Agent Relationships**: Agents and their relationships are stored in Neo4j, enabling complex, flexible workflows
- **Real-Time Adaptability**: Modify agent behaviors and workflows by updating the graph without changing the underlying infrastructure, with the potential for automating graph changes using large language models
- **Rich Relationship Modeling**: Leverage Neo4j's graph capabilities to model complex agent interactions and dependencies
- **Easy Workflow Visualization**: Naturally visualize agent workflows using Neo4j's built-in visualization tools

### Serverless Scalability
- **AWS Lambda Integration**: Stateless, event-driven agent execution that scales automatically
- **Cost-Effective**: Pay only for actual compute time used during agent interactions
- **High Concurrency**: Handle multiple workflow instances simultaneously without infrastructure management
- **Automatic Resource Management**: AWS manages scaling, availability, and fault tolerance

### Flexible Orchestration
- **AWS Step Functions**: Reliable workflow orchestration with built-in error handling and retries
- **Simplified Workflow Engine**: Step Functions provides a simple, recursive workflow engine applicable to complex workflows (it processes one agent, passes the output to the next agent along the graph, and repeats the process recursively)
![Step Functions Engine](/assets/images/step-functions-engine.png)
- **Parallel Execution**: Support for parallel agent execution using Step Functions' Map state
- **State Management**: Built-in state tracking and execution history
- **Long-Running Workflows**: Handle workflows of any duration with Step Functions' 1-year execution limit

### Adaptive Architecture
- **Dynamic Workflow Updates**: Modify agent behaviors by updating the Neo4j graph without redeploying Step Functions
- **Hot-Swappable Agents**: Add, remove, or modify agents during runtime
- **Flexible Routing**: Change agent interaction patterns by updating graph relationships
- **Version Control**: Track workflow evolution through graph versioning

## Benefits

### Technical Benefits
- **Separation of Concerns**: Clear separation between workflow logic, agent behavior, and infrastructure
- **Easy Maintenance**: Update workflows by modifying the graph, not the code
- **Monitoring & Observability**: Comprehensive logging and tracing through AWS services
- **Security**: Built-in IAM integration and secure secret management
- **Disaster Recovery**: Automatic backups and point-in-time recovery with Neo4j

### Business Benefits
- **Rapid Iteration**: Quickly prototype and modify agent workflows without code changes
- **Cost Optimization**: Pay-as-you-go pricing for both compute and storage
- **Scalability**: Handle varying workloads without infrastructure management
- **Reliability**: Enterprise-grade reliability through AWS managed services
- **Future-Proof**: Easily integrate new LLM providers or agent types

### Development Benefits
- **Simple Testing**: Test new workflows by creating subgraphs in Neo4j
- **Clear Visualization**: Understand complex workflows through graph visualization
- **Version Control**: Track workflow changes through graph snapshots
- **Easy Debugging**: Trace agent interactions through the graph structure
- **Collaborative Development**: Multiple teams can work on different parts of the workflow

## Future Work
- **Enhanced Tool Utilization**: Expanding agent capabilities by integrating with **S3, SNS, SQS, Knowledge Base (RAG)**, and other AWS services for more **dynamic and intelligent workflows**.
- **Context & Memory Optimization**: Implementing **efficient state management** techniques to optimize **context retention** across workflows.
- **Parallel & Hierarchical Processing**: Introducing **multi-level execution strategies** where agents operate in **parallel or hierarchical configurations**, optimizing performance for **large-scale workflows**.
- **Automated Graph Updates**: Further exploration into **LLM-driven workflow optimization**, including **real-time agent orchestration** and **automated relationship modifications**.

## Example: Multi-Agent Medical Accuracy Assessment

Here's an example of a three-agent workflow for medical accuracy assessment:

### Agent Workflow Configuration (neo4j)

```cypher
// Agent creation
CREATE (a1:Agent {
    system_message: "You are a psychiatrist.",
    user_message: "Explain bipolar disorder."
})
CREATE (a2:Agent {
    system_message: "You are an accuracy checker.",
    user_message: "Verify the correctness of the psychiatrist's explanation."
})
CREATE (a3:Agent {
    system_message: "You are an evaluator.",
    user_message: "Assess the accuracy checker's feedback and determine its validity and relevance."
})

// Three-agent workflow configuration
CREATE (a1)-[:NEXT_AGENT]->(a2)
CREATE (a2)-[:NEXT_AGENT]->(a3)
```

### Workflow Visualization

![Three Agent Workflow](/assets/images/three-agent-example.png)

### Agent Outputs

#### 1. Psychiatrist's Explanation
```
Bipolar disorder is a complex mental health condition characterized by significant mood swings that include emotional highs (mania or hypomania) and lows (depression). As a psychiatrist, let me break down the key aspects:

Types:
1. Bipolar I Disorder: Characterized by at least one manic episode, which may be preceded or followed by hypomanic or major depressive episodes.
2. Bipolar II Disorder: Characterized by a pattern of depressive episodes and hypomanic episodes, but no full-blown manic episodes.
3. Cyclothymic Disorder: A milder form with chronic fluctuating mood disturbances.

Symptoms:
Manic Episode:
- Increased energy, activity, and agitation
- Euphoria or extreme irritability
- Decreased need for sleep
- Racing thoughts and rapid speech
- Poor judgment and risky behavior
- Inflated self-esteem or grandiosity

Depressive Episode:
- Persistent sadness or hopelessness
- Loss of interest in activities
- Changes in sleep and appetite
- Fatigue and low energy
- Difficulty concentrating
- Thoughts of death or suicide

Causes:
The exact cause isn't fully understood, but several factors contribute:
- Genetic factors (hereditary component)
- Brain structure and functioning
- Environmental triggers
- Stress and trauma
- Substance use

Diagnosis:
Diagnosis requires a comprehensive psychiatric evaluation, including:
- Detailed medical and family history
- Physical examination
- Mental status examination
- Mood charting
- Ruling out other medical conditions

Treatment:
Treatment typically involves a combination approach:
1. Medications:
   - Mood stabilizers (e.g., lithium)
   - Antipsychotics
   - Antidepressants (used cautiously)

2. Psychotherapy:
   - Cognitive Behavioral Therapy (CBT)
   - Interpersonal and Social Rhythm Therapy (IPSRT)
   - Family-focused therapy

3. Lifestyle Management:
   - Regular sleep schedule
   - Stress management
   - Avoiding alcohol and drugs
   - Maintaining routine
   - Exercise and healthy diet

Prognosis:
With proper treatment and management:
- Many people with bipolar disorder lead fulfilling lives
- Early intervention improves outcomes
- Medication adherence is crucial
- Regular monitoring helps prevent relapses
- Support systems play a vital role

Important Notes:
- Bipolar disorder is a lifelong condition requiring ongoing management
- Treatment plans should be individualized
- Regular follow-up with healthcare providers is essential
- Crisis planning is important
- Support from family and friends is valuable

Remember, bipolar disorder is a serious but treatable condition. With proper diagnosis, treatment, and support, individuals can manage their symptoms and maintain stability in their lives.
```

#### 2. Accuracy Checker's Verification
```
I've thoroughly reviewed the psychiatrist's explanation of bipolar disorder, and I can confirm that it is highly accurate and comprehensive. Let me verify each major component:

Verification of Key Components:

1. Types of Bipolar Disorder:
✓ Correctly identified the three main types
✓ Accurate descriptions of Bipolar I, II, and Cyclothymic Disorder
✓ Proper distinction between mania, hypomania, and depression

2. Symptoms:
✓ Accurate description of manic and depressive episodes
✓ Complete list of key symptoms for each phase
✓ Clinically accurate terminology

3. Causes:
✓ Accurate representation of the multifactorial nature
✓ Properly emphasizes that exact cause is not fully understood
✓ Correct inclusion of genetic and environmental factors

4. Diagnosis:
✓ Accurate description of diagnostic process
✓ Proper emphasis on comprehensive evaluation
✓ Correct inclusion of differential diagnosis

5. Treatment:
✓ Accurate representation of multimodal approach
✓ Correct medication categories
✓ Evidence-based psychotherapy options
✓ Appropriate lifestyle management strategies

6. Prognosis:
✓ Accurate representation of outcomes
✓ Proper emphasis on treatment adherence
✓ Correct focus on long-term management

Additional Notes:
1. The explanation appropriately emphasizes the chronic nature of the condition
2. The information about psychotic symptoms in Bipolar I could be expanded
3. The cautious approach to antidepressants is clinically appropriate
4. The emphasis on individualized treatment is consistent with current guidelines

The explanation aligns with:
- Current DSM-5 criteria
- Evidence-based treatment guidelines
- Clinical best practices
- Current research findings

Overall Assessment:
The psychiatrist's explanation is medically accurate, well-structured, and provides a comprehensive overview of bipolar disorder suitable for patient education and understanding.
```

#### 3. Evaluator's Assessment
```
The accuracy checker's feedback is **valid, relevant, and highly accurate**. Below is an assessment of the feedback's strengths and areas where it could be further refined or expanded:

### Strengths of the Feedback

1. **Comprehensive Coverage**:
   - The feedback thoroughly addresses all major aspects of bipolar disorder, including its types, symptoms, causes, diagnosis, treatment, and prognosis. This aligns with the psychiatrist's explanation and ensures no critical details are overlooked.

2. **Accuracy**:
   - The feedback correctly verifies the psychiatrist's explanation, confirming that the information provided is consistent with current diagnostic criteria (e.g., DSM-5) and clinical understanding of bipolar disorder.

3. **Additional Notes**:
   - The inclusion of "Additional Notes" enhances the feedback by providing supplementary information that clarifies or expands on the psychiatrist's points. For example, the note about psychotic symptoms in Bipolar I and the cautious use of antidepressants adds depth to the explanation.

4. **Structure and Clarity**:
   - The feedback is well-organized, with clear headings and subheadings that make it easy to follow. This structure mirrors the psychiatrist's explanation, ensuring a logical flow of information.

5. **Evidence-Based**:
   - The feedback references evidence-based practices, such as the use of specific psychotherapies (CBT, IPSRT) and medications (lithium, antipsychotics), which strengthens its credibility.

6. **Balanced Perspective**:
   - The feedback acknowledges the complexity of bipolar disorder, including the interplay of genetic, biological, and environmental factors, as well as the importance of early intervention and adherence to treatment.

### Areas for Improvement or Expansion

1. **Cultural and Individual Variability**:
   - While the feedback is thorough, it could briefly mention how cultural factors or individual differences might influence the presentation, diagnosis, or treatment of bipolar disorder. For example, stigma in certain cultures may delay seeking help.

2. **Comorbidity**:
   - The feedback could highlight common comorbid conditions (e.g., anxiety disorders, substance use disorders) that often accompany bipolar disorder and how they might complicate diagnosis and treatment.

3. **Emerging Treatments**:
   - While the feedback covers standard treatments, it could briefly mention emerging or alternative therapies (e.g., ketamine for treatment-resistant depression, transcranial magnetic stimulation) to provide a more forward-looking perspective.

4. **Patient-Centered Care**:
   - The feedback could emphasize the importance of tailoring treatment plans to individual needs, preferences, and circumstances, as bipolar disorder manifests differently in each person.

5. **Myths and Misconceptions**:
   - A brief section addressing common myths or misconceptions about bipolar disorder (e.g., "It's just mood swings") could enhance the educational value of the feedback.

### Overall Assessment
The accuracy checker's feedback is **excellent** in terms of validity, relevance, and thoroughness. It effectively verifies the psychiatrist's explanation while adding valuable context and detail. With minor additions (e.g., cultural considerations, comorbidity, emerging treatments), the feedback could become even more comprehensive and informative.

If further refinement is desired, the feedback could incorporate the suggested improvements to address a broader range of perspectives and considerations related to bipolar disorder.
```

## Use Cases

1. **Healthcare and Medical**
   - Multi-specialist diagnosis and consultation
   - Mental health assessment and therapy planning
   - Clinical trial data validation and compliance
   - Drug interaction analysis and verification
   - Medical documentation review and verification

2. **Financial Services**
   - Risk assessment and compliance checking
   - Fraud detection and investigation
   - Investment strategy evaluation
   - Credit application processing
   - Regulatory compliance verification

3. **Legal Document Processing**
   - Contract review and analysis
   - Legal research and case preparation
   - Compliance verification
   - Patent application review
   - Legal document drafting and verification

4. **Content Creation and Publishing**
   - Multi-stage content creation and review
   - Fact-checking and source verification
   - Translation quality assurance
   - SEO optimization and verification
   - Brand voice consistency checking

5. **Customer Service**
   - Complex query resolution
   - Multi-tier support escalation
   - Customer satisfaction verification
   - Response quality assurance
   - Service level compliance monitoring

6. **Research and Analysis**
   - Academic paper review and validation
   - Research methodology verification
   - Data analysis and validation
   - Literature review and synthesis
   - Experimental design review

7. **Software Development**
   - Code review and analysis
   - Security vulnerability assessment
   - Documentation verification
   - Test case generation and validation
   - Architecture review and evaluation

8. **Education and Training**
   - Curriculum development and review
   - Student assessment and feedback
   - Learning material validation
   - Educational content adaptation
   - Performance evaluation## 📈 Future Enhancements

1. **Graph Analytics**
   - Workflow optimization through path analysis
   - Agent performance metrics
   - Bottleneck identification

2. **Advanced Orchestration**
   - Dynamic parallel execution paths
   - Conditional workflow branching
   - A/B testing of agent configurations

3. **Machine Learning Integration**
   - Automated workflow optimization
   - Agent behavior learning
   - Performance prediction

## Getting Started

1. **Prerequisites**
   - AWS Account with appropriate permissions
   - Neo4j instance (local or cloud)
   - Python 3.9+

2. **Installation**
   - Clone the repository
   - Install dependencies: `pip install -r requirements.txt`
   - Configure AWS credentials
   - Set up Neo4j connection details

3. **Configuration**
   - Update environment variables
   - Configure AWS services
   - Initialize Neo4j schema

4. **Running Workflows**
   - Create agents in Neo4j
   - Deploy Lambda functions
   - Start Step Functions execution

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.