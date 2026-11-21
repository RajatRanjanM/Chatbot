import os
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from dotenv import load_dotenv

load_dotenv()

def search(
    project_id: str,
    location: str,
    data_store_id: str,
    search_query: str,
) -> str:
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)

    serving_config = (
        f"projects/{project_id}/locations/{location}/collections/default_collection"
        f"/dataStores/{data_store_id}/servingConfigs/default_config"
    )

    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=5,
        content_search_spec=content_search_spec,
    )

    page_result = client.search(request)

    results = []
    for response in page_result:
        doc = response.document
        derived = doc.derived_struct_data
        title = derived.get("title", "Untitled")
        snippets = [s.get("snippet", "") for s in derived.get("snippets", [])]
        text = " ".join(snippets)
        if text:
            results.append(f"[{title}]: {text}")

    return "\n\n".join(results) if results else "No relevant documents found."


def search_betty_docs(query: str) -> str:
    """Search Betty's Bird Boutique internal documents (history, hours, staff)."""
    return search(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "lab18572440-1795209679"),
        location="global",
        data_store_id=os.getenv("DATASTORE_ID", "betty-datastore"),
        search_query=query,
    )
