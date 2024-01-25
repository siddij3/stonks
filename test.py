import re
def dict_maker(input_string):

    input_string = re.sub(r"[,.;@#?!&$]+\*", "", input_string)
    input_string = input_string.lower()

    # Assume cleaned text
    dict_count = {}

    words = input_string.split(" ")
    
    for i in words:

        if i in ['the', 'and', 'is', 'of', 'for', 'in', 'on']: #And whatever else I missed
            continue
        
        try:
            dict_count[i] += 1
        except:
            dict_count[i] = 1

    return dict_count

print(dict_maker("Hello world, hello to the world!"))




