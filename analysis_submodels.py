import os

from analysis import BNAnalysis

gc_model = os.path.join(os.getcwd(), "model_3_gyn-cycle")
gc_submodels_paths = [
    os.path.join(gc_model, "SketchBook", "LH_submodel", "sat_networks_1_colored", "candidate_1.aeon"),
    os.path.join(gc_model, "SketchBook", "FSH_submodel", "sat_networks_1", "candidate_1.aeon"),
    os.path.join(gc_model, "SketchBook", "GnRH_submodel", "sat_networks_1", "candidate_1.aeon"),
    os.path.join(gc_model, "SketchBook", "reduced_submodel", "sat_networks_1", "candidate_1.aeon")]
for model_path in gc_submodels_paths:
    bna = BNAnalysis(model_path)
    bna.print_basic_info()
    results_classes = bna.attractor_analysis()