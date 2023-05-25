#! /usr/bin/python3

from lxml import etree
import sys

tree1 = etree.parse(sys.argv[1])
root1 = tree1.getroot()

tree2 = etree.parse(sys.argv[2])
root2 = tree2.getroot()

def has_module(root, name):
    for result in root.iter('modules'):
        for module in result:
            if module.attrib["name"] == name:
                return module

    return None

def has_function(root, module_name, function_name):
    module = has_module(root, module_name)

    if module == None:
        return None

    for functions in module.iterchildren('functions'):
        for function in functions.iterchildren('function'):
            if function.attrib['name'] == function_name:
                return function

    return None

def has_range(root, module_name, function_name, range_cmp):
    function = has_function(root, module_name, function_name)

    if function == None:
        return None

    for ranges in function.iterchildren('ranges'):
        for range in ranges.iterchildren('range'):
            if range.attrib['source_id'] == range_cmp.attrib['source_id'] and \
                range.attrib['start_line'] == range_cmp.attrib['start_line'] and \
                range.attrib['start_column'] == range_cmp.attrib['start_column'] and \
                range.attrib['end_line'] == range_cmp.attrib['end_line'] and \
                range.attrib['end_column'] == range_cmp.attrib['end_column']:
                    return (ranges, range)

    return None

for result in root1.iterchildren('modules'):
    print(f'processing result {result.tag}')

    for module in result:
        module_name = module.attrib['name']

        print(f'\tprocessing module {module_name}')

        if has_module(tree2, module_name) == None:
            print('\t\tduplicate module', module_name)
            # TODO

        else:
            for functions in module.iterchildren('functions'):
                for function in functions.iterchildren('function'):
                    function_name = function.attrib['name']

                    print(f'\t\t\tprocessing {function_name}')

                    function2 = has_function(tree2, module_name, function_name)

                    if function2 == None:
                        print(f'\t\t\t\tduplicate {function_name}')
                        # TODO

                    else:
                        for ranges in function.iterchildren('ranges'):
                            for range in ranges.iterchildren('range'):
                                opp_range = has_range(tree2, module_name, function_name, range)

                                if range.attrib['covered'] == 'yes' and not opp_range is None:
                                    print(f'\t\t\t\tremove {range.attrib} from {function2}')

                                    opp_range[0].remove(opp_range[1])

tree2.write(sys.argv[3])
