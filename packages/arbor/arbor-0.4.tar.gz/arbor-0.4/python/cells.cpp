#include <algorithm>
#include <any>
#include <cstddef>
#include <optional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <arbor/benchmark_cell.hpp>
#include <arbor/cable_cell.hpp>
#include <arbor/lif_cell.hpp>
#include <arbor/morph/label_dict.hpp>
#include <arbor/morph/label_parse.hpp>
#include <arbor/morph/locset.hpp>
#include <arbor/morph/region.hpp>
#include <arbor/morph/segment_tree.hpp>
#include <arbor/schedule.hpp>
#include <arbor/spike_source_cell.hpp>
#include <arbor/util/any_cast.hpp>
#include <arbor/util/unique_any.hpp>

#include "cells.hpp"
#include "conversion.hpp"
#include "error.hpp"
#include "schedule.hpp"
#include "strprintf.hpp"

namespace pyarb {

// Convert a cell description inside a Python object to a cell
// description in a unique_any, as required by the recipe interface.
//
// Warning: requires that the GIL has been acquired before calling,
// if there is a segmentation fault in the cast or isinstance calls,
// check that the caller has the GIL.
arb::util::unique_any convert_cell(pybind11::object o) {
    using pybind11::isinstance;
    using pybind11::cast;

    pybind11::gil_scoped_acquire guard;
    if (isinstance<arb::spike_source_cell>(o)) {
        return arb::util::unique_any(cast<arb::spike_source_cell>(o));
    }
    if (isinstance<arb::benchmark_cell>(o)) {
        return arb::util::unique_any(cast<arb::benchmark_cell>(o));
    }
    if (isinstance<arb::lif_cell>(o)) {
        return arb::util::unique_any(cast<arb::lif_cell>(o));
    }
    if (isinstance<arb::cable_cell>(o)) {
        return arb::util::unique_any(cast<arb::cable_cell>(o));
    }

    throw pyarb_error("recipe.cell_description returned \""
                      + std::string(pybind11::str(o))
                      + "\" which does not describe a known Arbor cell type");
}

//
//  proxies
//

struct label_dict_proxy {
    using str_map = std::unordered_map<std::string, std::string>;
    arb::label_dict dict;
    str_map cache;
    std::vector<std::string> locsets;
    std::vector<std::string> regions;

    label_dict_proxy() = default;

    label_dict_proxy(const str_map& in) {
        for (auto& i: in) {
            set(i.first.c_str(), i.second.c_str());
        }
    }

    std::size_t size() const  {
        return locsets.size() + regions.size();
    }

    void set(const char* name, const char* desc) {
        using namespace std::string_literals;
        // The following code takes an input name and a region or locset
        // description, e.g.:
        //      name='reg', desc='(tag 4)'
        //      name='loc', desc='(terminal)'
        //      name='foo', desc='(join (tag 2) (tag 3))'
        // Then it parses the description, and tests whether the description
        // is a region or locset, and updates the label dictionary appropriately.
        // Errors occur when:
        //  * a region is described with a name that matches an existing locset
        //    (and vice versa.)
        //  * the description is not well formed, e.g. it contains a syntax error.
        //  * the description is well-formed, but describes neither a region or locset.
        try{
            // Evaluate the s-expression to build a region/locset.
            auto result = arb::parse_label_expression(desc);
            if (!result) { // an error parsing / evaluating description.
                throw result.error();
            }
            else if (result->type()==typeid(arb::region)) { // describes a region.
                dict.set(name, std::move(std::any_cast<arb::region&>(*result)));
                auto it = std::lower_bound(regions.begin(), regions.end(), name);
                if (it==regions.end() || *it!=name) regions.insert(it, name);
            }
            else if (result->type()==typeid(arb::locset)) { // describes a locset.
                dict.set(name, std::move(std::any_cast<arb::locset&>(*result)));
                auto it = std::lower_bound(locsets.begin(), locsets.end(), name);
                if (it==locsets.end() || *it!=name) locsets.insert(it, name);
            }
            else {
                // Successfully parsed an expression that is neither region nor locset.
                throw util::pprintf("The defninition of '{} = {}' does not define a valid region or locset.", name, desc);
            }
            // The entry was added succesfully: store it in the cache.
            cache[name] = desc;
        }
        catch (std::string msg) {
            const char* base = "\nError adding the label '{}' = '{}'\n{}\n";

            throw std::runtime_error(util::pprintf(base, name, desc, msg));
        }
        // Exceptions are thrown in parse or eval if an unexpected error occured.
        catch (std::exception& e) {
            const char* msg =
                "\n----- internal error -------------------------------------------"
                "\nError parsing the label: '{}' = '{}'"
                "\n"
                "\n{}"
                "\n"
                "\nPlease file a bug report with this full error message at:"
                "\n    github.com/arbor-sim/arbor/issues"
                "\n----------------------------------------------------------------";
            throw arb::arbor_internal_error(util::pprintf(msg, name, desc, e.what()));
        }
    }

    std::string to_string() const {
        std::string s;
        s += "(label_dict";
        for (auto& x: dict.regions()) {
            s += util::pprintf(" (region  \"{}\" {})", x.first, x.second);
        }
        for (auto& x: dict.locsets()) {
            s += util::pprintf(" (locset \"{}\" {})", x.first, x.second);
        }
        s += ")";
        return s;
    }
};

global_props_shim::global_props_shim():
    cat(arb::global_default_catalogue())
{
    props.catalogue = &cat;
}

// This isn't pretty. Partly because the information in the global parameters
// is all over the place.
std::string to_string(const global_props_shim& G) {
    std::string s = "{arbor.cable_global_properties";

    const auto& P = G.props;
    const auto& D = P.default_parameters;
    const auto& I = D.ion_data;
    // name, valence, int_con, ext_con, rev_pot, rev_pot_method
    s += "\n  ions: {";
    for (auto& ion: P.ion_species) {
        if (!I.count(ion.first)) {
            s += util::pprintf("\n    {name: '{}', valence: {}, int_con: None, ext_con: None, rev_pot: None, rev_pot_method: None}",
                    ion.first, ion.second);
        }
        else {
            auto& props = I.at(ion.first);
            std::string method = D.reversal_potential_method.count(ion.first)?
                "'"+D.reversal_potential_method.at(ion.first).name()+"'": "None";
            s += util::pprintf("\n    {name: '{}', valence: {}, int_con: {}, ext_con: {}, rev_pot: {}, rev_pot_method: {}}",
                    ion.first, ion.second,
                    props.init_int_concentration,
                    props.init_ext_concentration,
                    props.init_reversal_potential,
                    method);
        }
    }
    s += "}\n";
    s += util::pprintf("  parameters: {Vm: {}, cm: {}, rL: {}, tempK: {}}\n",
            D.init_membrane_potential, D.membrane_capacitance,
            D.axial_resistivity, D.temperature_K);
    s += "}";
    return s;
}


//
// string printers
//

std::string lif_str(const arb::lif_cell& c){
    return util::pprintf(
        "<arbor.lif_cell: tau_m {}, V_th {}, C_m {}, E_L {}, V_m {}, t_ref {}, V_reset {}>",
        c.tau_m, c.V_th, c.C_m, c.E_L, c.V_m, c.t_ref, c.V_reset);
}


std::string mechanism_desc_str(const arb::mechanism_desc& md) {
    return util::pprintf("mechanism('{}', {})",
            md.name(), util::dictionary_csv(md.values()));
}

void register_cells(pybind11::module& m) {
    using namespace pybind11::literals;
    using std::optional;

    // arb::spike_source_cell

    pybind11::class_<arb::spike_source_cell> spike_source_cell(m, "spike_source_cell",
        "A spike source cell, that generates a user-defined sequence of spikes that act as inputs for other cells in the network.");

    spike_source_cell
        .def(pybind11::init<>(
            [](const regular_schedule_shim& sched){
                return arb::spike_source_cell{sched.schedule()};}),
            "schedule"_a, "Construct a spike source cell that generates spikes at regular intervals.")
        .def(pybind11::init<>(
            [](const explicit_schedule_shim& sched){
                return arb::spike_source_cell{sched.schedule()};}),
            "schedule"_a, "Construct a spike source cell that generates spikes at a sequence of user-defined times.")
        .def(pybind11::init<>(
            [](const poisson_schedule_shim& sched){
                return arb::spike_source_cell{sched.schedule()};}),
            "schedule"_a, "Construct a spike source cell that generates spikes at times defined by a Poisson sequence.")
        .def("__repr__", [](const arb::spike_source_cell&){return "<arbor.spike_source_cell>";})
        .def("__str__",  [](const arb::spike_source_cell&){return "<arbor.spike_source_cell>";});

    // arb::benchmark_cell

    pybind11::class_<arb::benchmark_cell> benchmark_cell(m, "benchmark_cell",
        "A benchmarking cell, used by Arbor developers to test communication performance.\n"
        "A benchmark cell generates spikes at a user-defined sequence of time points, and\n"
        "the time taken to integrate a cell can be tuned by setting the realtime_ratio,\n"
        "for example if realtime_ratio=2, a cell will take 2 seconds of CPU time to\n"
        "simulate 1 second.\n");

    benchmark_cell
        .def(pybind11::init<>(
            [](const regular_schedule_shim& sched, double ratio){
                return arb::benchmark_cell{sched.schedule(), ratio};}),
            "schedule"_a, "realtime_ratio"_a=1.0,
            "Construct a benchmark cell that generates spikes at regular intervals.")
        .def(pybind11::init<>(
            [](const explicit_schedule_shim& sched, double ratio){
                return arb::benchmark_cell{sched.schedule(), ratio};}),
            "schedule"_a, "realtime_ratio"_a=1.0,
            "Construct a benchmark cell that generates spikes at a sequence of user-defined times.")
        .def(pybind11::init<>(
            [](const poisson_schedule_shim& sched, double ratio){
                return arb::benchmark_cell{sched.schedule(), ratio};}),
            "schedule"_a, "realtime_ratio"_a=1.0,
            "Construct a benchmark cell that generates spikes at times defined by a Poisson sequence.")
        .def("__repr__", [](const arb::benchmark_cell&){return "<arbor.benchmark_cell>";})
        .def("__str__",  [](const arb::benchmark_cell&){return "<arbor.benchmark_cell>";});

    // arb::lif_cell

    pybind11::class_<arb::lif_cell> lif_cell(m, "lif_cell",
        "A benchmarking cell, used by Arbor developers to test communication performance.");

    lif_cell
        .def(pybind11::init<>())
        .def_readwrite("tau_m", &arb::lif_cell::tau_m,
            "Membrane potential decaying constant [ms].")
        .def_readwrite("V_th", &arb::lif_cell::V_th,
            "Firing threshold [mV].")
        .def_readwrite("C_m", &arb::lif_cell::C_m,
            "Membrane capacitance [pF].")
        .def_readwrite("E_L", &arb::lif_cell::E_L,
            "Resting potential [mV].")
        .def_readwrite("V_m", &arb::lif_cell::V_m,
            "Initial value of the Membrane potential [mV].")
        .def_readwrite("t_ref", &arb::lif_cell::t_ref,
            "Refractory period [ms].")
        .def_readwrite("V_reset", &arb::lif_cell::V_reset,
            "Reset potential [mV].")
        .def("__repr__", &lif_str)
        .def("__str__",  &lif_str);

    // arb::label_dict

    pybind11::class_<label_dict_proxy> label_dict(m, "label_dict",
        "A dictionary of labelled region and locset definitions, with a\n"
        "unique label is assigned to each definition.");
    label_dict
        .def(pybind11::init<>(), "Create an empty label dictionary.")
        .def(pybind11::init<const std::unordered_map<std::string, std::string>&>(),
            "Initialize a label dictionary from a dictionary with string labels as keys,"
            " and corresponding definitions as strings.")
        .def("__setitem__",
            [](label_dict_proxy& l, const char* name, const char* desc) {
                l.set(name, desc);})
        .def("__getitem__",
            [](label_dict_proxy& l, const char* name) {
                if (!l.cache.count(name)) {
                    throw std::runtime_error(util::pprintf("\nKeyError: '{}'", name));
                }
                return l.cache.at(name);
            })
        .def("__len__", &label_dict_proxy::size)
        .def("__iter__",
            [](const label_dict_proxy &ld) {
                return pybind11::make_key_iterator(ld.cache.begin(), ld.cache.end());},
            pybind11::keep_alive<0, 1>())
        .def_readonly("regions", &label_dict_proxy::regions,
             "The region definitions.")
        .def_readonly("locsets", &label_dict_proxy::locsets,
             "The locset definitions.")
        .def("__repr__", [](const label_dict_proxy& d){return d.to_string();})
        .def("__str__",  [](const label_dict_proxy& d){return d.to_string();});

    // arb::gap_junction_site

    pybind11::class_<arb::gap_junction_site> gjsite(m, "gap_junction",
            "For marking a location on a cell morphology as a gap junction site.");
    gjsite
        .def(pybind11::init<>())
        .def("__repr__", [](const arb::gap_junction_site&){return "<arbor.gap_junction>";})
        .def("__str__", [](const arb::gap_junction_site&){return "<arbor.gap_junction>";});

    // arb::i_clamp

    pybind11::class_<arb::i_clamp> i_clamp(m, "iclamp",
        "A current clamp, for injecting a single pulse of current with fixed duration and current.");
    i_clamp
        .def(pybind11::init(
                [](double ts, double dur, double cur) {
                    return arb::i_clamp{ts, dur, cur};
                }), "tstart"_a=0, "duration"_a=0, "current"_a=0)
        .def_readonly("tstart", &arb::i_clamp::delay,       "Time at which current starts [ms]")
        .def_readonly("duration", &arb::i_clamp::duration,  "Duration of the current injection [ms]")
        .def_readonly("current", &arb::i_clamp::amplitude,  "Amplitude of the injected current [nA]")
        .def("__repr__", [](const arb::i_clamp& c){
            return util::pprintf("(iclamp {} {} {})", c.delay, c.duration, c.amplitude);})
        .def("__str__", [](const arb::i_clamp& c){
            return util::pprintf("<arbor.iclamp: tstart {} ms, duration {} ms, current {} nA>",
                                 c.delay, c.duration, c.amplitude);});

    // arb::threshold_detector

    pybind11::class_<arb::threshold_detector> detector(m, "spike_detector",
            "A spike detector, generates a spike when voltage crosses a threshold.");
    detector
        .def(pybind11::init(
            [](double thresh) {
                return arb::threshold_detector{thresh};
            }), "threshold"_a)
        .def_readonly("threshold", &arb::threshold_detector::threshold, "Voltage threshold of spike detector [ms]")
        .def("__repr__", [](const arb::threshold_detector& d){
            return util::pprintf("<arbor.threshold_detector: threshold {} mV>", d.threshold);})
        .def("__str__", [](const arb::threshold_detector& d){
            return util::pprintf("(threshold_detector {})", d.threshold);});

    // arb::cable_cell_ion_data

    pybind11::class_<arb::initial_ion_data> ion_data(m, "ion",
        "For setting ion properties (internal and external concentration and reversal potential) on cells and regions.");
    ion_data
        .def(pybind11::init(
                [](const char* name,
                   optional<double> int_con,
                   optional<double> ext_con,
                   optional<double> rev_pot)
                {
                    arb::initial_ion_data x;
                    x.ion = name;
                    if (int_con) x.initial.init_int_concentration = *int_con;
                    if (ext_con) x.initial.init_ext_concentration = *ext_con;
                    if (rev_pot) x.initial.init_reversal_potential = *rev_pot;
                    return x;
                }
            ),
            "ion_name"_a,
            pybind11::arg_v("int_con", pybind11::none(), "Intial internal concentration [mM]"),
            pybind11::arg_v("ext_con", pybind11::none(), "Intial external concentration [mM]"),
            pybind11::arg_v("rev_pot", pybind11::none(), "Intial reversal potential [mV]"),
            "If concentrations or reversal potential are specified as 'None',"
            " cell default or global default value will be used, in that order if set.");

    // arb::cable_cell_global_properties

    pybind11::class_<global_props_shim> gprop(m, "cable_global_properties");
    gprop
        .def(pybind11::init<>())
        .def(pybind11::init<const global_props_shim&>())
        .def("check", [](const global_props_shim& shim) {
                arb::check_global_properties(shim.props);},
                "Test whether all default parameters and ion specids properties have been set.")
        // set cable properties
        .def("set_properties",
            [](global_props_shim& G,
               optional<double> Vm, optional<double> cm,
               optional<double> rL, optional<double> tempK)
            {
                if (Vm) G.props.default_parameters.init_membrane_potential = Vm;
                if (cm) G.props.default_parameters.membrane_capacitance=cm;
                if (rL) G.props.default_parameters.axial_resistivity=rL;
                if (tempK) G.props.default_parameters.temperature_K=tempK;
            },
            "Vm"_a=pybind11::none(), "cm"_a=pybind11::none(), "rL"_a=pybind11::none(), "tempK"_a=pybind11::none(),
            "Set global default values for cable and cell properties.\n"
            " Vm:    initial membrane voltage [mV].\n"
            " cm:    membrane capacitance [F/m²].\n"
            " rL:    axial resistivity [Ω·cm].\n"
            " tempK: temperature [Kelvin].")
        .def("foo", [](global_props_shim& G, double x, pybind11::object method) {
                        std::cout << "foo(" << x << ", " << method << ")\n";},
                    "x"_a, "method"_a=pybind11::none())
        // add/modify ion species
        .def("set_ion",
            [](global_props_shim& G, const char* ion,
               optional<double> int_con, optional<double> ext_con,
               optional<double> rev_pot, pybind11::object method)
            {
                auto& data = G.props.default_parameters.ion_data[ion];
                if (int_con) data.init_int_concentration = *int_con;
                if (ext_con) data.init_ext_concentration = *ext_con;
                if (rev_pot) data.init_reversal_potential = *rev_pot;
                // allow rev_pot_method to be specified with string or mechanism_desc
                if (!method.is_none()) {
                    if (auto m=try_cast<std::string>(method)) {
                        G.props.default_parameters.reversal_potential_method[ion] = *m;
                    }
                    else if (auto m=try_cast<arb::mechanism_desc>(method)) {
                        G.props.default_parameters.reversal_potential_method[ion] = *m;
                    }
                    else {
                        throw std::runtime_error(util::pprintf("invalid rev_pot_method: {}", method));
                    }
                }
            },
            "ion"_a,
            "int_con"_a=pybind11::none(),
            "ext_con"_a=pybind11::none(),
            "rev_pot"_a=pybind11::none(),
            "rev_pot_method"_a=pybind11::none(),
            "Set the global default propoerties of ion species named 'ion'.\n"
            "Species concentrations and reversal potential can be overridden on\n"
            "specific regions using the paint interface, while the method for calculating\n"
            "reversal potential is global for all compartments in the cell, and can't be\n"
            "overriden locally.\n"
            " ion:     name of ion species.\n"
            " int_con: initial internal concentration [mM].\n"
            " ext_con: initial external concentration [mM].\n"
            " rev_pot: initial reversal potential [mV].\n"
            " rev_pot_method:  method for calculating reversal potential.")
        .def_readwrite("catalogue", &global_props_shim::cat, "The mechanism catalogue.")
        .def("__str__", [](const global_props_shim& p){return to_string(p);});

    // arb::cable_cell

    pybind11::class_<arb::cable_cell> cable_cell(m, "cable_cell",
        "Represents morphologically-detailed cell models, with morphology represented as a\n"
        "tree of one-dimensional cable segments.");
    cable_cell
        .def(pybind11::init(
            [](const arb::morphology& m, const label_dict_proxy& labels) {
                return arb::cable_cell(m, labels.dict);
            }), "morphology"_a, "labels"_a)
        .def(pybind11::init(
            [](const arb::segment_tree& t, const label_dict_proxy& labels) {
                return arb::cable_cell(arb::morphology(t), labels.dict);
            }),
            "segment_tree"_a, "labels"_a,
            "Construct with a morphology derived from a segment tree.")
        .def_property_readonly("num_branches",
            [](const arb::cable_cell& c) {return c.morphology().num_branches();},
            "The number of unbranched cable sections in the morphology.")
        // Set cell-wide properties
        .def("set_properties",
            [](arb::cable_cell& c,
               optional<double> Vm, optional<double> cm,
               optional<double> rL, optional<double> tempK)
            {
                if (Vm) c.default_parameters.init_membrane_potential = Vm;
                if (cm) c.default_parameters.membrane_capacitance=cm;
                if (rL) c.default_parameters.axial_resistivity=rL;
                if (tempK) c.default_parameters.temperature_K=tempK;
            },
            "Vm"_a=pybind11::none(), "cm"_a=pybind11::none(), "rL"_a=pybind11::none(), "tempK"_a=pybind11::none(),
            "Set default values for cable and cell properties. These values can be overridden on specific regions using the paint interface.\n"
            " Vm:    initial membrane voltage [mV].\n"
            " cm:    membrane capacitance [F/m²].\n"
            " rL:    axial resistivity [Ω·cm].\n"
            " tempK: temperature [Kelvin].")
        .def("set_ion",
            [](arb::cable_cell& c, const char* ion,
               optional<double> int_con, optional<double> ext_con,
               optional<double> rev_pot, optional<arb::mechanism_desc> method)
            {
                auto& data = c.default_parameters.ion_data[ion];
                if (int_con) data.init_int_concentration = *int_con;
                if (ext_con) data.init_ext_concentration = *ext_con;
                if (rev_pot) data.init_reversal_potential = *rev_pot;
                if (method)  c.default_parameters.reversal_potential_method[ion] = *method;
            },
            "ion"_a,
            "int_con"_a=pybind11::none(),
            "ext_con"_a=pybind11::none(),
            "rev_pot"_a=pybind11::none(),
            "method"_a=pybind11::none(),
            "Set the propoerties of ion species named 'ion' that will be applied\n"
            "by default everywhere on the cell. Species concentrations and reversal\n"
            "potential can be overridden on specific regions using the paint interface, \n"
            "while the method for calculating reversal potential is global for all\n"
            "compartments in the cell, and can't be overriden locally.\n"
            " ion:     name of ion species.\n"
            " int_con: initial internal concentration [mM].\n"
            " ext_con: initial external concentration [mM].\n"
            " rev_pot: reversal potential [mV].\n"
            " method:  method for calculating reversal potential.")
        // Paint mechanisms.
        .def("paint",
            [](arb::cable_cell& c, const char* region, const arb::mechanism_desc& d) {
                c.paint(region, d);
            },
            "region"_a, "mechanism"_a,
            "Associate a mechanism with a region.")
        .def("paint",
            [](arb::cable_cell& c, const char* region, const char* mech_name) {
                c.paint(region, mech_name);
            },
            "region"_a, "mechanism"_a,
            "Associate a mechanism with a region.")
        // Paint membrane/static properties.
        .def("paint",
            [](arb::cable_cell& c,
                const char* region,
               optional<double> Vm, optional<double> cm,
               optional<double> rL, optional<double> tempK)
            {
                if (Vm) c.paint(region, arb::init_membrane_potential{*Vm});
                if (cm) c.paint(region, arb::membrane_capacitance{*cm});
                if (rL) c.paint(region, arb::axial_resistivity{*rL});
                if (tempK) c.paint(region, arb::temperature_K{*tempK});
            },
            "region"_a, "Vm"_a=pybind11::none(), "cm"_a=pybind11::none(), "rL"_a=pybind11::none(), "tempK"_a=pybind11::none(),
            "Set cable properties on a region.\n"
            " Vm:    initial membrane voltage [mV].\n"
            " cm:    membrane capacitance [F/m²].\n"
            " rL:    axial resistivity [Ω·cm].\n"
            " tempK: temperature [Kelvin].")



        // Paint ion species initial conditions on a region.
        .def("paint",
            [](arb::cable_cell& c, const char* region, const char* name,
               optional<double> int_con, optional<double> ext_con, optional<double> rev_pot) {
                if (int_con) c.paint(region, arb::init_int_concentration{name, *int_con});
                if (ext_con) c.paint(region, arb::init_ext_concentration{name, *ext_con});
                if (rev_pot) c.paint(region, arb::init_reversal_potential{name, *rev_pot});
            },
            "region"_a, "ion_name"_a,
             pybind11::arg_v("int_con", pybind11::none(), "Intial internal concentration [mM]"),
             pybind11::arg_v("ext_con", pybind11::none(), "Intial external concentration [mM]"),
             pybind11::arg_v("rev_pot", pybind11::none(), "Intial reversal potential [mV]"),
            "Set ion species properties conditions on a region.")
        // Place synapses
        .def("place",
            [](arb::cable_cell& c, const char* locset, const arb::mechanism_desc& d) {
                c.place(locset, d); },
            "locations"_a, "mechanism"_a,
            "Place one instance of synapse described by 'mechanism' to each location in 'locations'.")
        .def("place",
            [](arb::cable_cell& c, const char* locset, const char* mech_name) {
                c.place(locset, mech_name);
            },
            "locations"_a, "mechanism"_a,
            "Place one instance of synapse described by 'mechanism' to each location in 'locations'.")
        // Place gap junctions.
        .def("place",
            [](arb::cable_cell& c, const char* locset, const arb::gap_junction_site& site) {
                c.place(locset, site);
            },
            "locations"_a, "gapjunction"_a,
            "Place one gap junction site at each location in 'locations'.")
        // Place current clamp stimulus.
        .def("place",
            [](arb::cable_cell& c, const char* locset, const arb::i_clamp& stim) {
                c.place(locset, stim);
            },
            "locations"_a, "iclamp"_a,
            "Add a current stimulus at each location in locations.")
        // Place spike detector.
        .def("place",
            [](arb::cable_cell& c, const char* locset, const arb::threshold_detector& d) {
                c.place(locset, d);
            },
            "locations"_a, "detector"_a,
            "Add a voltage spike detector at each location in locations.")
        // Get locations associated with a locset label.
        .def("locations",
            [](arb::cable_cell& c, const char* label) {return c.concrete_locset(label);},
            "label"_a, "The locations of the cell morphology for a locset label.")
        // Get cables associated with a region label.
        .def("cables",
            [](arb::cable_cell& c, const char* label) {return c.concrete_region(label).cables();},
            "label"_a, "The cable segments of the cell morphology for a region label.")
        // Discretization control.
        .def("compartments_on_segments",
            [](arb::cable_cell& c) {c.default_parameters.discretization = arb::cv_policy_every_segment{};},
            "Decompose each branch into compartments defined by segments.")
        .def("compartments_length",
            [](arb::cable_cell& c, double len) {
                c.default_parameters.discretization = arb::cv_policy_max_extent{len};
            },
            "maxlen"_a, "Decompose each branch into compartments of equal length, not exceeding maxlen.")
        .def("compartments_per_branch",
            [](arb::cable_cell& c, unsigned n) {c.default_parameters.discretization = arb::cv_policy_fixed_per_branch{n};},
            "n"_a, "Decompose each branch into n compartments of equal length.")
        // Stringification
        .def("__repr__", [](const arb::cable_cell&){return "<arbor.cable_cell>";})
        .def("__str__",  [](const arb::cable_cell&){return "<arbor.cable_cell>";});
}

} // namespace pyarb
