MODEL_NAME = "meta-llama/Meta-Llama-3-8B"   # base model (decided 2026-03-25)
TORCH_DTYPE = "float32"                    # model weight dtype; bfloat16 halves VRAM vs float32
L_DET = 9              # Set after layer calibration (Stage 1 notebook 1)
L_PRED = 31            # Set after layer calibration (Stage 1 notebook 1)
CONCEPT_CSV = "data/embeddings-concept-openai/concepts.csv"
ONTOLOGY_DISTANCES_CSV = "data/embeddings-concept-openai/ontological_distances.csv"
