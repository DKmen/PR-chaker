# Introduction

Welcome to the GitHub Code Review project! This project aims to provide a comprehensive guide and tools for conducting effective code reviews on GitHub. Whether you are a beginner or an experienced developer, this project will help you understand the best practices, techniques, and tools available to improve code quality and collaboration within your team.

## Folder Structure

The project directory structure is organized as follows:

```
github-code-review/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   └── review.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── review.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── review.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── review_service.py
│   └── tasks/
│       ├── __init__.py
│       └── review_tasks.py
├── tests/
│   ├── __init__.py
│   └── test_review.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

This structure helps in maintaining a clean and organized codebase, making it easier to navigate and manage different components of the project.

## Technology Stack

This project utilizes the following technologies:

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Docker**: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing.
- **RabbitMQ**: A message broker that enables applications to communicate with each other and exchange information.
- **PostgreSQL**: A powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance.

These technologies work together to create a robust and scalable environment for developing and deploying applications.

## Running the Project with Docker

To run this project using Docker, follow these steps:

1. **Install Docker**: Make sure you have Docker installed on your machine. You can download and install Docker from [here](https://www.docker.com/products/docker-desktop).

2. **Navigate to the Project Directory**: Open a terminal and navigate to the root directory of the project.

    ```sh
    cd /Users/dhrimilmendapara/Documents/Learning/github-code-review
    ```

3. **Build and Start the Containers**: Use Docker Compose to build and start the containers defined in the `docker-compose.yml` file.

    ```sh
    docker-compose up --build
    ```

4. **Access the Application**: Once the containers are up and running, you can access the application via the following URL:

    ```
    http://localhost:8000
    ```

5. **Run Ollama in Docker**: To run Ollama in Docker and map the local directory to the container, add the following service to your `docker-compose.yml` file:

    ```yaml
    services:
      ollama:
        image: ollama/ollama:latest
        volumes:
          - /path/to/local/ollama:/path/in/container
        ports:
          - "8080:8080"
    ```

    Replace `/path/to/local/ollama` with the path to your local Ollama directory and `/path/in/container` with the desired path inside the container.

6. **Stopping the Containers**: To stop the running containers, use the following command:

    ```sh
    docker-compose down
    ```

By following these steps, you will have the project up and running in a Dockerized environment, making it easy to manage dependencies and ensure consistency across different development setups.

## Future Scope

### GitHub-Based Login

To enhance the functionality of this project, we plan to implement GitHub-based login. This will allow users to authenticate using their GitHub credentials and access personalized features based on their GitHub profile.

### Fetch User Data

Once authenticated, the application will fetch data using the user's GitHub profile. This data can include repositories, pull requests, and other relevant information to provide a more tailored code review experience.

### Implement Test Cases

To ensure the reliability and correctness of the functions within the project, we will implement comprehensive test cases. These test cases will cover various scenarios and edge cases to validate the functionality and performance of the code.

By incorporating these features, the project will offer a more integrated and user-friendly experience, leveraging GitHub's capabilities to streamline the code review process.

## API Overview

### Analyze Pull Request

**POST** `http://localhost:8000/analyze-pr`

**Example Request Body:**
```json
{
    "repo_url": "repo_url",
    "pr_id": 1,
    "github_token": "github_token"
}
```

**Example Response:**
```json
{
    "refrance_branch": "branch_name",
    "repo": "repo_name",
    "id": 167,
    "title": "PR Title",
    "pull_request_id": "1",
    "github_token": "github_token",
    "owner": "owner_name",
    "total_files": 3,
    "status": "PENDING"
}
```

### Check Task Status

**GET** `http://localhost:8000/status/<task_id>`

**Example Response:**
```json
{
    "refrance_branch": "branch",
    "repo": "repo",
    "id": 1,
    "title": "PR Title",
    "pull_request_id": "1",
    "github_token": "github_token",
    "owner": "owner",
    "total_files": 3,
    "status": "PENDING"
}
```

### Get Task Result

**GET** `http://0.0.0.0:8000/result/<task_id>`

**Example Response:**
```json
{
    "task_id": 1,
    "status": "SUCCESS",
    "results": {
        "summary": {
            "total_files": 3,
            "total_issues": 6,
            "total_critical": 2
        },
        "files": [
            {
                "name": "src/server.ts",
                "issues": [
                    {
                        "type": "error",
                        "line": 14,
                        "description": "The function `calculateRelaventScoreBasedOnSegment` is not defined in the scope. It seems like a method from a class or module that has not been imported.",
                        "suggestion": "Check if the function is defined elsewhere in the code and import it correctly."
                    }
                ]
            },
            {
                "name": "src/types/campaignStatus.ts",
                "issues": [
                    {
                        "type": "style",
                        "line": 1,
                        "description": "The code is not properly formatted. It seems like a mix of JavaScript and JSON.",
                        "suggestion": "Consider using a consistent formatting style throughout the code, such as Prettier or ESLint."
                    },
                    {
                        "type": "style",
                        "line": 2,
                        "description": "The variable names are not descriptive. It's hard to understand what each variable represents.",
                        "suggestion": "Consider renaming variables to something more meaningful and descriptive, such as `campaignStatus` instead of `Q1JFQVRFRCA9`."
                    },
                    {
                        "type": "error",
                        "line": 5,
                        "description": "The code is trying to export a variable that is not defined.",
                        "suggestion": "Make sure the variable `CampaignStatus` is properly defined before exporting it."
                    },
                    {
                        "type": "performance",
                        "line": 7,
                        "description": "The console.log statement can be removed as it's not serving any purpose in this code.",
                        "suggestion": "Consider removing unnecessary statements to improve performance and readability."
                    }
                ]
            },
            {
                "name": "src/utils/console.ts",
                "issues": [
                    {
                        "type": "style",
                        "line": 1,
                        "description": "The file has no content, it's empty. It would be better to provide some code for analysis.",
                        "suggestion": "Please add some code to the file and then I can analyze it."
                    }
                ]
            }
        ]
    }
}
```

## Conclusion

By following this guide, you will be able to set up, run, and manage the GitHub Code Review project efficiently. The provided folder structure, technology stack, and Docker instructions ensure a streamlined development process. Additionally, the API endpoints allow for easy interaction with the code review functionalities, enabling you to analyze pull requests, check task statuses, and retrieve task results. This project aims to enhance code quality and collaboration within your team, making code reviews more effective and productive.