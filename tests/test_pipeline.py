import os
from pathlib import Path
from scripts import pipeline

def test_pipeline():
    # Setup dummy file with one topic
    dummy_topic_file = "tests/sample_data.json"
    os.makedirs("tests", exist_ok=True)
    Path(dummy_topic_file).write_text('[{"topic": "Artificial Intelligence", "category": "AI"}]')

    # Run pipeline
    pipeline.run_pipeline(
        topics_file=dummy_topic_file,
        out_dir="tests/output",
        chunk_out_dir="tests/output/chunks",
        vectorstore_dir="tests/output/vectorstore"
    )

    # Check if vectorstore index was created
    index_path = Path("tests/output/vectorstore/index.faiss")
    assert index_path.exists(), "Vectorstore index not created."

    # Clean up
    import shutil
    shutil.rmtree("tests/output")
    os.remove(dummy_topic_file)
