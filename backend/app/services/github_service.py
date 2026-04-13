import httpx
from app.config import GITHUB_USERNAME


async def fetch_github_repos() -> list[dict]:
    """Fetch public repos for the configured GitHub user."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
            params={"sort": "updated", "per_page": 30},
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        response.raise_for_status()
        repos = response.json()

    return [
        {
            "name": repo["name"],
            "description": repo.get("description", ""),
            "language": repo.get("language", ""),
            "stars": repo.get("stargazers_count", 0),
            "url": repo["html_url"],
            "topics": repo.get("topics", []),
        }
        for repo in repos
        if not repo.get("fork", False)
    ]


async def fetch_repo_readme(repo_name: str) -> str:
    """Fetch the README content for a specific repo."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/readme",
            headers={"Accept": "application/vnd.github.v3.raw"},
        )
        if response.status_code == 200:
            return response.text
        return ""


async def generate_github_document() -> str:
    """Generate a comprehensive document about all GitHub repos for RAG ingestion."""
    repos = await fetch_github_repos()
    parts = [f"# GitHub Profile: {GITHUB_USERNAME}\n"]

    for repo in repos:
        parts.append(f"\n## Repository: {repo['name']}")
        parts.append(f"URL: {repo['url']}")
        if repo["description"]:
            parts.append(f"Description: {repo['description']}")
        if repo["language"]:
            parts.append(f"Primary Language: {repo['language']}")
        if repo["stars"]:
            parts.append(f"Stars: {repo['stars']}")
        if repo["topics"]:
            parts.append(f"Topics: {', '.join(repo['topics'])}")

        readme = await fetch_repo_readme(repo["name"])
        if readme:
            # Truncate very long READMEs
            if len(readme) > 3000:
                readme = readme[:3000] + "\n... (truncated)"
            parts.append(f"\nREADME:\n{readme}")

        parts.append("")

    return "\n".join(parts)
