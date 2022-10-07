import pandas as pd
def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

print(camelCase("Finger tips Push away"))