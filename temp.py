def split_dict_string_values(d, chunk_size=100):
    new_dict = {}
    for key, value in d.items():
        if isinstance(value, str) and len(value) > chunk_size:
            for i in range(len(value)//chunk_size +1):
                
                if i!=0:
                    new_dict[key+'_'+str(i)] = value[chunk_size*(i):chunk_size*(i+1)]
                else:
                    new_dict[key] = value[:chunk_size*(i+1)]
        else:
            new_dict[key] = value
    return new_dict

# Example dictionary
test_dict = {
    "short": "short string",
    "long": "a" * 100 + "b"*100 + "c"*50,  # a string of 250 'a's
    "number": 12345
}

split_dict = split_dict_string_values(test_dict)
print(split_dict)