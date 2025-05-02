# SLID

![Coverage](coverage.svg)

SLID is a platform that integrates most social media and online accounts into one clean, user-friendly interface. It features AI-powered data navigation to streamline the user's digital experience and serves as a digital ID by centralizing and integrating a user's digital presence.

[If you want to read the full technical documentation, you can find it here.](https://mcmarian.github.io/SLID/)

# Documentation
SLID provides comprehensive documentation through a dedicated MkDocs website. The documentation includes user guides, developer guides, API references, deployment instructions, and detailed technical documentation.

## Accessing the Documentation
You can access the documentation in several ways:

1. **Online Documentation**: Visit our [GitHub Pages documentation site](https://mcmarian.github.io/SLID/).

2. **Local Access**: Run the documentation server locally using Docker:
   ```bash
   docker-compose -f docker-compose-docs.yml up
   ```
   Then visit `http://localhost:8080` in your browser.

3. **GitHub Repository**: Browse through the documentation files in the `docs/` directory of the repository.

## Documentation Structure
- **User Guides**: End-user manuals and guides
- **Developer Guides**: Installation, architecture, and development instructions
- **API Reference**: Detailed API documentation and integration guides
- **Deployment**: Deployment guides and cloud architecture
- **Technical Documentation**: Procedural instructions and diagrams

# Features
> **Unified Social Media Experience:** Consolidate multiple social media platforms into one place for seamless interaction.

> **AI-powered Navigation:** Our AI allows you to smoothly navigate through your data and connections' data across platforms using natural language.

> **Digital Identity:** Use SLID as your digital ID, integrating your entire digital presence across platforms.

> **Cross-platform Integration:** Connect and manage accounts from a variety of social media platforms with ease.

# AI Capabilities
SLID features advanced AI-driven search and navigation, allowing users to interact with their data using simple commands. Whether you're looking for specific interactions, posts, or even cross-platform connections, the AI makes it simple and intuitive.

# Tech Stack
- **Frontend**: Django templates for rendering HTML and managing the user interface.
- **Backend**: Django (Python) for handling server-side logic and application framework.
- **Database**: PostgreSQL for storing user data, posts, and relationships.
- **Containerization**: Docker for creating, deploying, and managing application containers.
- **AI**: LangChain agents and tools for NLP-based search and navigation.
- **Version Control**: Git for tracking changes and collaboration.
- **Testing Framework**: pytest for testing the application and ensuring code quality.
- **Deployment**: Docker Compose for managing multi-container Docker applications.


# How to Run
1. ### Clone the repository:
   ```bash
   git clone https://github.com/McMarian/SLID.git
2. ### Navigate to the project directory:
   ```bash
   cd SLID
3. ### Build and Run the Project Using Docker

   **Don't have Docker? Install it first:**
   
   - **For Windows:** Download and install Docker Desktop from the [Docker website](https://www.docker.com/products/docker-desktop).
   - **For macOS:** Download and install Docker Desktop from the [Docker website](https://www.docker.com/products/docker-desktop).
   - **For Linux:** Follow the instructions for your specific distribution in the [Docker installation guide](https://docs.docker.com/engine/install/).

   **Once Docker is installed, run the following command in your terminal:**
   
   ```bash
   docker-compose up
4. ### Access the application locally at:
   ```bash
   http://localhost:8080

# References and Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [LangChain Documentation](https://docs.langchain.com/)

# Contributing to Documentation

We welcome contributions to the SLID documentation! Here's how you can help improve our docs:

## Documentation Development Workflow

1. **Setup the Documentation Environment:**
   ```bash
   docker-compose -f docker-compose-docs.yml up
   ```
   This will start the documentation server at `http://localhost:8080`.

2. **Make Changes:**
   - All documentation files are in the `docs/` directory
   - The documentation structure is defined in `mkdocs.yml`
   - Files are written in Markdown format

3. **Preview Your Changes:**
   - The documentation server has live reload enabled
   - As you save your changes, the preview will update automatically

4. **Submit Your Contributions:**
   - Commit and push your changes to a new branch
   - Create a pull request for review
   - Once approved, the GitHub Actions workflow will deploy the updated documentation

## Documentation Guidelines

- Use clear, concise language
- Include code examples where applicable
- Add screenshots or diagrams to illustrate complex concepts
- Organize content logically with appropriate headings
- Link to related documentation sections when relevant

