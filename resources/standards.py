"""Standards and templates for Azure DevOps work items."""


def get_gold_standard():
    """
    Get the gold standard work item structure based on Work Item ID 89.

    Returns:
        str: Complete gold standard content
    """
    return """
# Gold Standard Work Item Structure

**ORIGINAL WORK ITEM**: ID 89 "Data Import and Validation" from Epic 81 "Automation Semantic Model"

This is the proven, enterprise-grade structure that ensures comprehensive task descriptions. ALL new work items should follow this exact format and quality level.

**Access**: Use resource identifier `ado://standard/gold` to reference this standard in any context.

## Structure Requirements

### Required Sections (5 total):
1. **## Objective** - Clear accomplishment statement
2. **## Technical Requirements** - Specific tools and constraints
3. **## Implementation Steps** - 8-10 numbered steps minimum
4. **## Acceptance Criteria** - 6-8 testable checkboxes
5. **## Business Context** - Enterprise value explanation

### Quality Standards:
- **Minimum 4-5 sentences per section** with proper formatting
- **Comprehensive technical details** with specific tools and technologies
- **Clear business value** that ties to company strategic goals
- **Actionable implementation steps** that a developer can follow
- **Measurable acceptance criteria** that can be tested and validated

## Gold Standard Example

**Work Item ID 89**: "Data Import and Validation"

### ## Objective
Implement comprehensive data import and validation system for the semantic model to ensure data integrity and quality throughout the TOML architecture implementation. This task establishes the data ingestion pipeline that validates, cleanses, and transforms raw data from multiple sources into the structured format required by the semantic model. The system will include automated data quality checks, error handling, and monitoring capabilities to maintain high data standards. This work directly enables reliable analytics and reporting capabilities while supporting Omar's Solutions' commitment to delivering accurate data solutions to clients.

### ## Technical Requirements
- Azure Synapse Analytics for ETL processing and data pipeline orchestration
- Power BI semantic model integration with proper data refresh capabilities
- ADLS Gen2 storage containers configured with appropriate access policies and encryption
- Data validation frameworks including Great Expectations or similar quality assurance tools
- Error logging and monitoring systems integrated with Azure Monitor for operational visibility
- Automated testing infrastructure supporting continuous integration and deployment practices
- Performance optimization tools for handling large-scale data processing workloads

### ## Implementation Steps
1. Analyze and document all identified data sources including schema definitions and data volume characteristics
2. Design comprehensive data validation rules covering data types, ranges, relationships, and business logic constraints
3. Implement automated data ingestion pipelines using Azure Synapse with proper error handling and retry mechanisms
4. Configure data quality monitoring dashboards with real-time alerts for data anomalies and processing failures
5. Establish data cleansing and transformation procedures ensuring consistent formatting and standardization across all sources
6. Create comprehensive testing framework validating both individual data elements and end-to-end pipeline functionality
7. Implement automated data refresh schedules optimized for business requirements and system performance constraints
8. Configure monitoring and alerting systems providing operational visibility into data pipeline health and performance metrics
9. Conduct thorough performance testing with production-scale data volumes ensuring system scalability and reliability
10. Document all procedures including troubleshooting guides and operational runbooks for ongoing maintenance

### ## Acceptance Criteria
- [ ] Data validation rules successfully implemented covering all identified data quality requirements with 100% coverage
- [ ] Automated data ingestion pipeline operational with 99.5% uptime and proper error handling for edge cases
- [ ] Data quality monitoring dashboard deployed providing real-time visibility into pipeline status and data health metrics
- [ ] Error logging and alerting system configured with appropriate escalation procedures and notification mechanisms
- [ ] Performance benchmarks met supporting concurrent users and large-scale data processing requirements
- [ ] Comprehensive testing completed including unit tests, integration tests, and end-to-end validation scenarios
- [ ] Data import pipeline successfully processes all identified source systems with 100% accuracy and validated data integrity
- [ ] Documentation completed including technical specifications, user guides, and operational procedures for ongoing support

### ## Business Context
This data import and validation system ensures the semantic model maintains the highest standards of data quality, directly supporting Omar's Solutions' reputation for delivering reliable data solutions to clients. The automated validation and monitoring capabilities reduce operational overhead while providing confidence in data accuracy for critical business decisions. This system enables scalable data operations that support business growth and provides the foundation for advanced analytics and automation initiatives. The implementation directly contributes to client satisfaction through improved data reliability and supports the company's strategic positioning as a leader in Azure-based data solutions and semantic modeling expertise.

---

**Reference**: Always use this structure for comprehensive work item descriptions that meet enterprise quality standards.
"""


def get_description_template():
    """
    Get a streamlined template for work item descriptions.

    Returns:
        str: Template structure
    """
    return """
## Work Item Description Template

Use this template for creating comprehensive work item descriptions:

```
## Objective
[Clear statement of what will be accomplished - 4-5 sentences minimum]

## Technical Requirements
[Specific tools, technologies, and constraints - bulleted list]

## Implementation Steps
[8-10 numbered steps with specific actions]

## Acceptance Criteria
[6-8 testable checkboxes with measurable outcomes]

## Business Context
[Enterprise value and strategic importance - 4-5 sentences]
```

**Quality Guidelines:**
- Each section should have substantial content (4-5 sentences minimum)
- Use specific technical details and tools
- Include measurable, testable criteria
- Connect to business value and company goals
- Reference Work Item ID 89 as the quality standard

**Delimiter for Multiple Tasks:**
When creating multiple tasks, separate descriptions with `|||`:
```
Task 1 complete description ||| Task 2 complete description ||| Task 3 complete description
```
"""
