#! /usr/bin/python3

import xml.etree.ElementTree as ET

tree1 = ET.parse('1.xml')
root1 = tree1.getroot()

tree2 = ET.parse('2.xml')
root2 = tree2.getroot()

tree3 = ET.parse('2.xml')
root3 = tree2.getroot()

def has_module(root, name):
    for result in root1.iter('modules'):
        for module in result:
            if module.attrib["name"] == name:
                return module

    return None

def has_function(root, module_name, function_name):
    module = has_module(root, module_name)

    if module == None:
        return None

    for functions in module.iter('functions'):
        for function in functions.iter('function'):
            if function.attrib['name'] == function_name:
                return function

    return None

def has_range(root, module_name, function_name, range_cmp):
    function = has_function(root, module_name, function_name)

    if function == None:
        return None

    for ranges in function.iter('ranges'):
        for range in ranges.iter('range'):
            if range.attrib['source_id'] == range_cmp.attrib['source_id'] and \
                range.attrib['start_line'] == range_cmp.attrib['start_line'] and \
                range.attrib['start_column'] == range_cmp.attrib['start_column'] and \
                range.attrib['end_line'] == range_cmp.attrib['end_line'] and \
                range.attrib['end_column'] == range_cmp.attrib['end_column']:
                    return range

    return None

root3 = ET.Element('results')

modules3 = ET.SubElement(root3, 'modules')

for result in root1.iter('modules'):
    print(f'processing result {result.tag}')

    for module in result:
        module_name = module.attrib['name']

        print(f'\tprocessing module {module_name}')

        if has_module(tree2, module_name) == None:
            print('\t\tduplicate module', module_name)
            # TODO

        else:
            for functions in module.iter('functions'):
                for function in functions.iter('function'):
                    function_name = function.attrib['name']

                    print(f'\t\t\tprocessing {function_name}')

                    function2 = has_function(tree2, module_name, function_name)

                    if function2 == None:
                        print(f'\t\t\t\tduplicate {function_name}')
                        # TODO

                    else:
                        function3 = has_function(tree3, module_name, function_name)
                        ranges3 = function3.find('ranges')

                        for ranges in function.iter('ranges'):
                            for range in ranges.iter('range'):
                                opp_range = has_range(tree2, module_name, function_name, range)

                                if not (opp_range == None or range.attrib['covered'] == 'no' or (range.attrib['covered'] == 'no' and opp_range.attrib['covered'] == 'yes')):
                                    print(f'\t\t\t\tremove {range.attrib}')

                                    range3 = has_range(tree3, module_name, function_name, opp_range)

                                    print(range3)

                                    ranges3.remove(range3)

tree3.write('3.xml')
