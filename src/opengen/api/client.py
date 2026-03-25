"""
OpenGen  - Public API Client
=============================

Client library for querying the OpenGen knowledge graph.
Use this to search verified knowledge, explore connections,
and integrate OpenGen data into your own applications.

Status: Skeleton (Phase 5). The public API is not yet deployed.
"""

from opengen.models.shared import GraphStats, KnowledgeNode, SearchResult


class OpenGenAPI:
    """
    Client for the OpenGen public knowledge API.

    Usage (once the API is deployed):
        api = OpenGenAPI()
        results = api.search("photosynthesis")
        for r in results:
            print(r.node.title, r.node.quality_score)
    """

    def __init__(self, base_url: str = "https://api.opengen.live", api_key: str = ""):
        """
        Initialize the API client.

        Args:
            base_url: The OpenGen API URL.
            api_key: Optional API key for higher rate limits.
                     Public tier (100 requests/hour) requires no key.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def search(self, query: str, domain: str = "", limit: int = 10) -> list[SearchResult]:
        """
        Search the verified knowledge graph.

        Args:
            query: Search text (matched against titles, content, tags).
            domain: Optional domain filter (e.g., "biology", "physics").
            limit: Maximum number of results (1-100).

        Returns:
            A list of SearchResult objects, ranked by relevance.
        """
        # TODO: Implement API call
        # GET /api/v1/knowledge/search?q={query}&domain={domain}&limit={limit}
        raise NotImplementedError("Public API not yet deployed (Phase 5)")

    def get_node(self, node_id: str) -> KnowledgeNode | None:
        """
        Get a specific knowledge node by ID.

        Returns the full node including content, review history,
        version history, and connections.
        """
        # TODO: Implement API call
        # GET /api/v1/knowledge/nodes/{node_id}
        raise NotImplementedError("Public API not yet deployed (Phase 5)")

    def get_connections(self, node_id: str) -> list[dict]:
        """
        Get all connections for a knowledge node.

        Returns a list of connected nodes with edge types and weights.
        """
        # TODO: Implement API call
        # GET /api/v1/knowledge/nodes/{node_id}/connections
        raise NotImplementedError("Public API not yet deployed (Phase 5)")

    def get_suggestions(self, node_id: str) -> list[KnowledgeNode]:
        """
        Get related topics for a knowledge node.

        "You read about photosynthesis  - you might also want to know
        about chlorophyll, oxygen production, or Mars terraforming."
        """
        # TODO: Implement API call
        # GET /api/v1/knowledge/suggestions/{node_id}
        raise NotImplementedError("Public API not yet deployed (Phase 5)")

    def ask(self, question: str) -> dict:
        """
        Ask the Knowledge Guide a question.

        The Guide answers only from verified knowledge  - no hallucination.
        Every claim is linked to its source node.
        """
        # TODO: Implement API call
        # POST /api/v1/guide/ask
        raise NotImplementedError("Public API not yet deployed (Phase 5)")

    def stats(self) -> GraphStats:
        """
        Get public statistics about the knowledge graph.

        Returns node count, edge count, domain distribution,
        active worker count, and more.
        """
        # TODO: Implement API call
        # GET /api/v1/stats
        raise NotImplementedError("Public API not yet deployed (Phase 5)")


if __name__ == "__main__":
    print("=" * 60)
    print("  OpenGen  - Public API Client")
    print("=" * 60)
    print()
    print("  The public API is planned for Phase 5.")
    print("  This client library will allow you to:")
    print()
    print("    api = OpenGenAPI()")
    print("    results = api.search('photosynthesis')")
    print("    node = api.get_node('node-id')")
    print("    related = api.get_suggestions('node-id')")
    print("    answer = api.ask('How does photosynthesis work?')")
    print("    stats = api.stats()")
    print()
    print("  Rate limits:")
    print("    Public:        100 requests/hour (no key)")
    print("    Developer:   1,000 requests/hour (free key)")
    print("    Institutional: 10,000 requests/hour (contact)")
    print()
    print("  Star this repo and watch for updates.")
    print("=" * 60)
