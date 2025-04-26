import os

from biodivine_aeon import *

msg_ok = ">OK"
msg_nok = ">FAIL"

class BNAnalysis:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = BooleanNetwork.from_file(model_path, repair_graph=True)
        self.stg = None
        self.attractors = None

    def print_basic_info(self):
        print()
        num_star = len(self.model_path)
        print(num_star * "*")
        print(self.model_path)
        print(num_star * "*")

        print("Model implicit params:", self.model.implicit_parameters())

        print("\nModel update functions")
        for v in self.model.variables():
            print(self.model.get_variable_name(v), "=", self.model.get_update_function(v))
        print("\nModel regulations ({})".format(len(self.model.regulations())))
        for regulation in self.model.regulations():
            # print(regulation)
            print("'source:'", self.model.get_variable_name(regulation['source']), end=', ')
            print("'target:'", self.model.get_variable_name(regulation['target']), end=', ')
            print("'essential:'", str(regulation['essential']), end=', ')
            print("'sign:'", str(regulation['sign']))

    def attractor_analysis(self, num_vars=2):
        self.stg = AsynchronousGraph.mk_for_model_checking(self.model, 35)
        self.attractors = Attractors.attractors(self.stg)
        print("\nModel attractors ({})".format(len(self.attractors)))
        attractors_dict = dict()
        results_classes = []
        for attractor in self.attractors:
            classes = Classification.classify_long_term_behavior(self.stg, attractor)
            results_classes.append(classes)
            classes_keys = list(classes.keys())
            if Class(["disorder"]) in classes_keys or Class(["oscillation"]) in classes_keys:
                print(">")
                print("Attractor cardinality:", attractor.cardinality())
                print("Attractor vertices:", attractor.vertices())
                print("class:", classes)
                for class_key in classes_keys:
                    attractors_dict[class_key] = attractors_dict.get(class_key, 0) + 1
            else:
                attractors_dict["stability"] = attractors_dict.get("stability", 0) + 1
        print(attractors_dict)
        return results_classes

    def analyze_periodic_behaviour(self, basic_transitions_ef, path_formula_ef, ovulation_behaviour=None, whole_stg=True):
        print("\nPeriodic behaviour analysis:")
        if whole_stg:
            results_ef_ok = 0
            results_ef_nok = len(basic_transitions_ef)
            result_ef_whole = False
            result_ovul_pattern = False
            print("\nPartial transitions on whole STG")
            for partial_transition in basic_transitions_ef:
                print(partial_transition)
                attractor_mc = ModelChecking.verify(self.stg, partial_transition)
                if attractor_mc.cardinality() > 0:
                    results_ef_ok += 1
                    results_ef_nok -= 1
                    print(msg_ok)
                else:
                    print(msg_nok)
            print("Whole cycle ons whole STG")
            print(path_formula_ef)
            attractors_mc = ModelChecking.verify(self.stg, path_formula_ef)
            if attractors_mc.cardinality() > 0:
                result_ef_whole = True
                print(msg_ok)
            else:
                print(msg_nok)
            if ovulation_behaviour is not None:
                print("Ovul behaviour on whole STG")
                attractors_mc = ModelChecking.verify(self.stg, ovulation_behaviour)
                if attractors_mc.cardinality() > 0:
                    print(msg_ok)
                    result_ovul_pattern = True
                else:
                    print(msg_nok)

        print("Analysis on attractors:")
        results_ef_ok_att = 0
        results_ef_nok_att = len(basic_transitions_ef)
        result_ef_whole_att = False
        result_ovul_att = False
        for attractor in self.attractors:
            stg_att = self.stg.restrict(attractor)
            classes = Classification.classify_long_term_behavior(stg_att, attractor)
            cls_keys = list(classes.keys())
            if Class(["disorder"]) not in cls_keys and Class(["oscillation"]) not in cls_keys:
                continue
            print_at_the_end = False
            print_buffer = "\n"
            print_buffer += "***********\n"
            print_buffer += "class: " + str(classes) + "\n"
            print_buffer += str(attractor.vertices()) + "\n"

            for partial_transition in basic_transitions_ef:
                print_buffer += partial_transition + "\n"
                attractor_mc = ModelChecking.verify(stg_att, partial_transition)
                print_buffer += str(attractor_mc) + "\n"
                if attractor_mc.cardinality() > 0:
                    results_ef_ok_att += 1
                    results_ef_nok_att -= 1
                    print_at_the_end = True
                    print_buffer += msg_ok + "\n"
                else:
                    print_buffer += msg_nok + "\n"

            print_buffer += path_formula_ef + "\n"
            attractors_mc = ModelChecking.verify(stg_att, path_formula_ef)
            print_buffer += str(attractors_mc) + "\n"
            if attractors_mc.cardinality() > 0:
                result_ef_whole_att = True
                print_buffer += msg_ok + "\n"
            else:
                print_buffer += msg_nok + "\n"

            if ovulation_behaviour is not None:
                attractors_mc = ModelChecking.verify(stg_att, ovulation_behaviour)
                print_buffer += str(attractors_mc.colors()) + " " + str(attractors_mc.vertices()) + "\n"
                if attractors_mc.cardinality() > 0:
                    result_ovul_att = True
                    print_at_the_end = True

            if print_at_the_end:
                print(print_buffer)

        if whole_stg:
            whole_stg_res = [str(results_ef_ok) + "/" + str(results_ef_ok + results_ef_nok),
                             result_ef_whole, result_ovul_pattern if ovulation_behaviour is not None else "-"]
        else:
            whole_stg_res = []
        return (whole_stg_res +
                [str(results_ef_ok_att) + "/" + str(results_ef_ok_att + results_ef_nok_att),
                 result_ef_whole_att, result_ovul_att if ovulation_behaviour is not None else "-"])



