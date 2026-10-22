import json
from pathlib import Path

from semantic_search import search_documents


DATASET_PATH = Path("evaluation_dataset.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_retrieval(test_case):
    # Abstention questions are handled separately.
    if test_case["expected_behavior"] == "abstain":
        return {
            "status": "MANUAL",
            "sources": []
        }

    results = search_documents(
        test_case["question"],
        top_k=6
    )

    retrieved_sources = {
        result["source"]
        for result in results
    }

    expected_sources = set(
        test_case["expected_sources"]
    )

    source_match = expected_sources.issubset(
        retrieved_sources
    )

    return {
        "status": "PASS" if source_match else "REVIEW",
        "sources": sorted(retrieved_sources)
    }


def main():
    dataset = load_dataset()

    passed = 0
    review = 0
    manual = 0

    print("=" * 60)
    print("RAG RETRIEVAL EVALUATION")
    print("=" * 60)

    for test_case in dataset:

        print("\n" + "-" * 60)
        print(f"Test: {test_case['id']}")
        print(f"Question: {test_case['question']}")

        try:
            result = evaluate_retrieval(test_case)

            print(f"Retrieval status: {result['status']}")

            if result["status"] == "PASS":
                passed += 1

            elif result["status"] == "REVIEW":
                review += 1

            else:
                manual += 1

            if result["sources"]:
                print("Retrieved sources:")

                for source in result["sources"]:
                    print(f"  - {source}")

            if result["status"] == "MANUAL":
                print(
                    "Note: Abstention behavior requires "
                    "answer-generation testing."
                )

        except Exception as error:
            review += 1

            print("ERROR while processing this test:")
            print(type(error).__name__, "-", error)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Retrieval PASS:   {passed}")
    print(f"Retrieval REVIEW: {review}")
    print(f"Manual checks:    {manual}")
    print(f"Total tests:      {len(dataset)}")
    print("=" * 60)


if __name__ == "__main__":
    main()