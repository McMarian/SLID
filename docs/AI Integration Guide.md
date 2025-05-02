# AI Integration Guide

## Introduction

SLID integrates powerful AI capabilities to enable users to interact with their data using natural language. This guide explains how the AI features work and provides developers with information on how to extend the AI capabilities.

## Core AI Capabilities

SLID's AI system provides the following core capabilities:

1. **Natural Language Queries**: Users can search and analyze their data across platforms using conversational language
2. **Cross-Platform Data Analysis**: The AI can find patterns and connections across different social media accounts
3. **Context-Aware Responses**: Responses factor in user profile information and connected platforms
4. **Database-Integrated Queries**: AI assistant can run complex SQL queries based on natural language inputs

## Technology Stack

The AI capabilities in SLID are built using:

- **LangChain**: For creating the AI agents and workflow orchestration
- **OpenAI API**: Powers the language model (GPT-3.5/4) for natural language understanding
- **SQLDatabase**: LangChain utility for integrating with the PostgreSQL database
- **Django**: Framework that handles routing AI requests and responses

## How AI Works in SLID

### Architecture Overview

```
User Query → Django View → LangChain Agent → SQL Database → AI Processing → Response
```

When a user submits a natural language query:

1. The query is received by the Django view (`ai` function in `profile_management/views.py`)
2. User context is gathered, including profile data and social media connections
3. The query is enhanced with this context and schema information
4. LangChain's SQL agent processes the query using the OpenAI model
5. The agent translates the natural language into SQL queries when appropriate
6. Results are processed, formatted, and returned to the user

### Code Implementation

The main AI implementation resides in the `ai` function in `profile_management/views.py`:

```python
@login_required
def ai(request):
    """Handle AI-powered user data analysis and queries"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    user_query = request.POST.get('data')
    if not user_query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    try:
        # Get user context including social media data
        user_data = get_user_profile(request.user)
        if not user_data:
            return JsonResponse({'error': 'User profile not found'}, status=404)

        # Initialize AI components
        db = SQLDatabase.from_uri(os.getenv('DATABASE_URL'))
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )

        # Create and execute AI agent
        agent = create_sql_agent(llm, db=db, verbose=True)

        # Include social media context in the query
        enhanced_query = f"""
        Context: User {user_data['profile']['username']} with {len(user_data['social_media'])} connected platforms.
        Query: {user_query}
        Schema: {construct_schema_prompt()}
        """

        answer = agent.run(enhanced_query)
        return JsonResponse({'message': answer})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

## Schema Information

The AI agent understands the database schema through the `construct_schema_prompt()` function:

```python
def construct_schema_prompt():
    """Generate database schema description for AI queries"""
    return """
    Database Schema:
    - UserProfile: User details (fullName, bio, profilePicture, verified status)
    - SocialMediaAccount: Unified social platform data
        * Platform types: instagram, facebook, youtube, linkedin, google, x, tiktok
        * Stores: authentication, platform data, connection status
    - Connection: User relationships and networking
    - Post: Content shared across platforms
    """
```

## Extending the AI Capabilities

### Adding New AI Features

To extend the AI capabilities in SLID, you can:

1. **Add New Tools**: Create custom LangChain tools for specific functionality
2. **Enhance Schema Understanding**: Update the schema prompt with new model fields
3. **Create Specialized Agents**: Develop purpose-built agents for specific tasks

### Example: Creating a Custom Tool

You can extend the AI with custom tools. Here's an example framework:

```python
from langchain.tools import BaseTool

class ContentAnalysisTool(BaseTool):
    name = "content_analysis"
    description = "Analyzes user content for sentiment and topic categorization"
    
    def _run(self, query: str) -> str:
        # Implement content analysis logic here
        return "Analysis results"
        
    def _arun(self, query: str) -> str:
        # Async implementation
        return self._run(query)

# In your ai function:
agent = create_sql_agent(
    llm=llm,
    db=db,
    toolkit=SQLDatabaseToolkit(db=db),
    tools=[ContentAnalysisTool()],
    verbose=True
)
```

### Adding New Models to AI Schema

When you add new models to the database, update the schema prompt:

```python
def construct_schema_prompt():
    return """
    Database Schema:
    - UserProfile: User details (fullName, bio, profilePicture, verified status)
    - SocialMediaAccount: Unified social platform data
    - Connection: User relationships and networking
    - Post: Content shared across platforms
    - NewModel: Description of your new model and its relationships
    """
```

## Best Practices for AI Integration

### 1. Context Is Key

Always provide sufficient context to the AI:

```python
enhanced_query = f"""
Context: 
- User: {user_data['profile']['username']}
- Platforms: {', '.join(user_data['social_media'].keys())}
- Query intent: {detect_intent(user_query)}

Query: {user_query}
Schema: {construct_schema_prompt()}
"""
```

### 2. Error Handling

Implement robust error handling for AI responses:

```python
try:
    answer = agent.run(enhanced_query)
    # Validate answer format
    if not answer or len(answer) > 2000:
        answer = "I couldn't generate a clear response. Please try a more specific question."
    return JsonResponse({'message': answer})
except Exception as e:
    logger.error(f"AI error: {str(e)}")
    return JsonResponse({'error': "I encountered an error processing your request."}, status=500)
```

### 3. Rate Limiting

Add rate limiting for AI queries to manage costs:

```python
from django.core.cache import cache

def ai(request):
    user_id = request.user.id
    rate_key = f"ai_rate_limit_{user_id}"
    
    # Check if user has exceeded rate limit
    request_count = cache.get(rate_key, 0)
    if request_count >= 20:  # 20 requests per hour
        return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
    
    # Increment counter
    cache.set(rate_key, request_count + 1, 3600)  # 1 hour expiry
    
    # Process AI request
    # ...
```

## Integration with Social Media Data

The AI capabilities leverage social media data stored in the `SocialMediaAccount` model. When extending AI features, remember to:

1. **Provide Data Context**: Include platform-specific data in the context
2. **Handle Platform Differences**: Different platforms have different data structures
3. **Keep Data Fresh**: Implement mechanisms to refresh social media data regularly

Example enhancement to provide platform-specific context:

```python
def get_platform_specific_context(user, platform):
    """Get detailed context for specific platform"""
    try:
        account = SocialMediaAccount.objects.get(user=user, platform=platform)
        if platform == 'instagram':
            return {
                'post_count': len(account.data.get('data', [])),
                'recent_topics': extract_topics(account.data),
                'engagement_stats': calculate_engagement(account.data)
            }
        # Add handlers for other platforms
    except SocialMediaAccount.DoesNotExist:
        return {}
```

## Security Considerations

When extending AI capabilities:

1. **Validate User Input**: Prevent injection attacks and malicious queries
2. **Limit Exposed Data**: Ensure AI agents can only access authorized data
3. **Monitor Usage**: Implement logging to track AI usage and detect abuse
4. **Protect API Keys**: Never expose API keys in client-side code

## Conclusion

The AI capabilities in SLID provide a powerful way to navigate and analyze cross-platform social media data. By following this guide, developers can extend these capabilities while maintaining security and performance.

For any questions or support, please contact the development team or open an issue on the project repository. 