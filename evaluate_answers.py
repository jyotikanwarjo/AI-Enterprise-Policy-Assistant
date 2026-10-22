import json
from pathlib import Path

from semantic_search import search_documents
from rag import generate_answer


DATASET_PATH = Path("evaluation_dataset.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def check_keywords(answer, expected_keywords):
    answer = answer.lower()

    matches = 0

    for keyword in expected_keywords:
        if keyword.lower() in answer:
            matches += 1

    if not expected_keywords:
        return True

    return matches / len(expected_keywords) >= 0.5


def main():

    dataset = [
    case for case in load_dataset()
    if case["id"] == "T04"
    ]

    passed = 0
    review = 0

    print("=" * 60)
    print("RAG ANSWER QUALITY EVALUATION")
    print("=" * 60)

    for test_case in dataset:

        if test_case["expected_behavior"] != "answer":
            continue

        print("\n" + "-" * 60)
        print(f"Test: {test_case['id']}")
        print(f"Question: {test_case['question']}")

        try:
            # Retrieve only once
            results = search_documents(
                test_case["question"],
                top_k=6
            )

            # Reuse those retrieved results
            result = generate_answer(
                test_case["question"],
                results=results
            )

            answer = result["answer"]

            answer_pass = check_keywords(
                answer,
                test_case["expected_keywords"]
            )

            if answer_pass:
                passed += 1
                status = "PASS"
            else:
                review += 1
                status = "REVIEW"

            print(f"Answer check: {status}")

            print("\nGenerated answer:")
            print(answer)

            print("\nSources:")
            for source in result.get("sources", []):
                print(
                    f"  - {source['source']}, "
                    f"Page {source['page']}"
                )

        except Exception as error:

            review += 1

            print("ERROR:")
            print(type(error).__name__, "-", error)

    total = passed + review

    print("\n" + "=" * 60)
    print("ANSWER EVALUATION SUMMARY")
    print("=" * 60)

    print(f"Answer PASS:   {passed}")
    print(f"Answer REVIEW: {review}")
    print(f"Total tested:  {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()